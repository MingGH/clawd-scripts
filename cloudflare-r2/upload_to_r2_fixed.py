#!/usr/bin/env python3
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
import os
from datetime import datetime
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Cloudflare R2 配置
R2_CONFIG = {
    "bucket_name": "openbot-upload",
    "endpoint_url": "https://8034b6f645143efa728dad5b5df39e7bd.r2.cloudflarestorage.com",
    "access_key_id": "77934f3344f603fd8221404a62b51b91",
    "secret_access_key": "0d3732d1811748f7c4b69f4fa0476f5aea0f31b2aef93016c8c1c569bc8ee7af",
    "region": "auto",
    "public_domain": "openbotfile.996.ninja"
}

# 要上传的文件
FILES_TO_UPLOAD = [
    "/tmp/uptime_kuma_analysis.png",
    "/tmp/uptime_kuma_logged_in.png",
    "/tmp/uptime_kuma_screenshot.png"
]

def create_r2_client():
    """创建R2 S3客户端（禁用SSL验证）"""
    try:
        # 配置S3客户端
        s3_config = Config(
            region_name=R2_CONFIG["region"],
            s3={'addressing_style': 'virtual'},
            signature_version='s3v4',
            connect_timeout=10,
            retries={'max_attempts': 3}
        )
        
        # 创建客户端，禁用SSL验证
        s3_client = boto3.client(
            's3',
            endpoint_url=R2_CONFIG["endpoint_url"],
            aws_access_key_id=R2_CONFIG["access_key_id"],
            aws_secret_access_key=R2_CONFIG["secret_access_key"],
            config=s3_config,
            verify=False  # 禁用SSL验证
        )
        
        print("✅ R2 S3客户端创建成功")
        return s3_client
    except Exception as e:
        print(f"❌ 创建R2客户端失败: {e}")
        return None

def upload_file_simple(s3_client, file_path):
    """简化版文件上传"""
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return None
    
    # 生成对象键
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = os.path.basename(file_path)
    object_key = f"uptime-kuma/{timestamp}_{file_name}"
    
    try:
        file_size = os.path.getsize(file_path)
        print(f"\n📤 上传: {file_name} ({file_size/1024:.1f} KB)")
        
        # 上传文件
        with open(file_path, 'rb') as file_data:
            s3_client.put_object(
                Bucket=R2_CONFIG["bucket_name"],
                Key=object_key,
                Body=file_data,
                ContentType='image/png'
            )
        
        public_url = f"https://{R2_CONFIG['public_domain']}/{object_key}"
        print(f"✅ 上传成功!")
        print(f"🔗 {public_url}")
        
        return public_url
        
    except Exception as e:
        print(f"❌ 上传失败: {e}")
        return None

def test_connection(s3_client):
    """测试连接"""
    try:
        # 尝试列出存储桶（最简单的操作）
        response = s3_client.list_buckets()
        print("✅ 连接测试成功")
        print(f"可用存储桶: {[b['Name'] for b in response.get('Buckets', [])]}")
        return True
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'AccessDenied':
            print("⚠️ 访问被拒绝，但连接正常")
            return True
        else:
            print(f"❌ 连接测试失败: {error_code}")
            return False
    except Exception as e:
        print(f"❌ 连接测试异常: {e}")
        return False

def main():
    print("=== Cloudflare R2 文件上传 ===\n")
    
    # 创建客户端
    s3_client = create_r2_client()
    if not s3_client:
        print("尝试使用requests直接上传...")
        return fallback_upload()
    
    # 测试连接
    if not test_connection(s3_client):
        print("尝试直接上传...")
    
    # 上传文件
    print(f"\n准备上传 {len(FILES_TO_UPLOAD)} 个文件...")
    uploaded_urls = []
    
    for file_path in FILES_TO_UPLOAD:
        if os.path.exists(file_path):
            url = upload_file_simple(s3_client, file_path)
            if url:
                uploaded_urls.append(url)
        else:
            print(f"⚠️ 跳过: {file_path} 不存在")
    
    # 输出结果
    print(f"\n=== 完成 ===")
    print(f"成功上传: {len(uploaded_urls)}/{len(FILES_TO_UPLOAD)} 个文件")
    
    if uploaded_urls:
        print("\n📎 图片链接:")
        for url in uploaded_urls:
            print(f"  • {url}")
        
        # 主要截图
        main_screenshot = uploaded_urls[0] if uploaded_urls else None
        if main_screenshot:
            print(f"\n🎯 主要截图: {main_screenshot}")
    
    print(f"\n🌐 公开域名: https://{R2_CONFIG['public_domain']}/")

def fallback_upload():
    """备选方案：使用requests直接上传"""
    print("使用备选方案上传...")
    
    # 这里可以实现直接HTTP上传
    # 但需要知道R2的具体API端点
    
    print("备选方案需要更多配置信息")
    return False

if __name__ == "__main__":
    main()