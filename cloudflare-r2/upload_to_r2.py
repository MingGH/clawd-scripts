#!/usr/bin/env python3
import boto3
from botocore.config import Config
import os
from datetime import datetime

# Cloudflare R2 配置
R2_CONFIG = {
    "bucket_name": "openbot-upload",
    "endpoint_url": "https://8034b6f645143efa728dad5b5df39e7bd.r2.cloudflarestorage.com",
    "access_key_id": "77934f3344f603fd8221404a62b51b91",
    "secret_access_key": "0d3732d1811748f7c4b69f4fa0476f5aea0f31b2aef93016c8c1c569bc8ee7af",
    "region": "auto",  # Cloudflare R2 使用 auto 区域
    "public_domain": "openbotfile.996.ninja"
}

# 要上传的文件
FILES_TO_UPLOAD = [
    "/tmp/uptime_kuma_analysis.png",
    "/tmp/uptime_kuma_logged_in.png",
    "/tmp/uptime_kuma_screenshot.png"
]

def create_r2_client():
    """创建R2 S3客户端"""
    try:
        # 配置S3客户端
        s3_config = Config(
            region_name=R2_CONFIG["region"],
            s3={'addressing_style': 'virtual'},
            signature_version='s3v4'
        )
        
        # 创建客户端
        s3_client = boto3.client(
            's3',
            endpoint_url=R2_CONFIG["endpoint_url"],
            aws_access_key_id=R2_CONFIG["access_key_id"],
            aws_secret_access_key=R2_CONFIG["secret_access_key"],
            config=s3_config
        )
        
        print("✅ R2 S3客户端创建成功")
        return s3_client
    except Exception as e:
        print(f"❌ 创建R2客户端失败: {e}")
        return None

def check_bucket_exists(s3_client):
    """检查存储桶是否存在"""
    try:
        s3_client.head_bucket(Bucket=R2_CONFIG["bucket_name"])
        print(f"✅ 存储桶 '{R2_CONFIG['bucket_name']}' 存在")
        return True
    except Exception as e:
        print(f"❌ 存储桶检查失败: {e}")
        return False

def upload_file(s3_client, file_path):
    """上传单个文件到R2"""
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return None
    
    # 生成对象键（使用日期时间戳避免冲突）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = os.path.basename(file_path)
    object_key = f"uptime-kuma/{timestamp}_{file_name}"
    
    try:
        # 获取文件信息
        file_size = os.path.getsize(file_path)
        file_size_mb = file_size / (1024 * 1024)
        
        print(f"\n📤 上传文件: {file_name}")
        print(f"   大小: {file_size_mb:.2f} MB")
        print(f"   对象键: {object_key}")
        
        # 上传文件
        with open(file_path, 'rb') as file_data:
            s3_client.put_object(
                Bucket=R2_CONFIG["bucket_name"],
                Key=object_key,
                Body=file_data,
                ContentType='image/png' if file_name.endswith('.png') else 'application/octet-stream'
            )
        
        # 生成公开访问URL
        public_url = f"https://{R2_CONFIG['public_domain']}/{object_key}"
        
        print(f"✅ 上传成功!")
        print(f"🔗 公开URL: {public_url}")
        
        return {
            "object_key": object_key,
            "public_url": public_url,
            "file_name": file_name,
            "file_size": file_size
        }
        
    except Exception as e:
        print(f"❌ 上传失败: {e}")
        return None

def list_bucket_contents(s3_client):
    """列出存储桶内容"""
    try:
        print(f"\n📂 存储桶 '{R2_CONFIG['bucket_name']}' 内容:")
        
        response = s3_client.list_objects_v2(Bucket=R2_CONFIG["bucket_name"])
        
        if 'Contents' in response:
            for obj in response['Contents']:
                size_kb = obj['Size'] / 1024
                last_modified = obj['LastModified'].strftime("%Y-%m-%d %H:%M:%S")
                print(f"  • {obj['Key']} ({size_kb:.1f} KB, {last_modified})")
        else:
            print("  (空存储桶)")
            
    except Exception as e:
        print(f"❌ 列出内容失败: {e}")

def main():
    print("=== Cloudflare R2 文件上传工具 ===\n")
    
    # 创建R2客户端
    s3_client = create_r2_client()
    if not s3_client:
        return
    
    # 检查存储桶
    if not check_bucket_exists(s3_client):
        print("尝试创建存储桶...")
        try:
            s3_client.create_bucket(Bucket=R2_CONFIG["bucket_name"])
            print("✅ 存储桶创建成功")
        except Exception as e:
            print(f"❌ 创建存储桶失败: {e}")
            return
    
    # 上传文件
    uploaded_files = []
    for file_path in FILES_TO_UPLOAD:
        if os.path.exists(file_path):
            result = upload_file(s3_client, file_path)
            if result:
                uploaded_files.append(result)
        else:
            print(f"⚠️ 跳过不存在的文件: {file_path}")
    
    # 列出存储桶内容
    list_bucket_contents(s3_client)
    
    # 输出总结
    print(f"\n=== 上传总结 ===")
    print(f"总共尝试上传: {len(FILES_TO_UPLOAD)} 个文件")
    print(f"成功上传: {len(uploaded_files)} 个文件")
    
    if uploaded_files:
        print("\n📎 上传的文件链接:")
        for file_info in uploaded_files:
            print(f"  • {file_info['file_name']}: {file_info['public_url']}")
    
    print(f"\n🌐 公开域名: https://{R2_CONFIG['public_domain']}/")
    print("💡 提示: 你可以通过公开域名直接访问上传的文件")

if __name__ == "__main__":
    main()