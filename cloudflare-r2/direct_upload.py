#!/usr/bin/env python3
import hashlib
import hmac
import requests
from datetime import datetime
import os

# Cloudflare R2 配置
R2_CONFIG = {
    "bucket": "openbot-upload",
    "endpoint": "8034b6f645143efa728dad5b5df39e7bd.r2.cloudflarestorage.com",
    "access_key": "77934f3344f603fd8221404a62b51b91",
    "secret_key": "0d3732d1811748f7c4b69f4fa0476f5aea0f31b2aef93016c8c1c569bc8ee7af",
    "public_domain": "openbotfile.996.ninja"
}

def sign(key, msg):
    """生成HMAC SHA256签名"""
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def get_signature_key(key, date_stamp, region_name, service_name):
    """生成签名密钥"""
    k_date = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    k_region = sign(k_date, region_name)
    k_service = sign(k_region, service_name)
    k_signing = sign(k_service, 'aws4_request')
    return k_signing

def upload_file_direct(file_path):
    """直接使用S3 API上传文件"""
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return None
    
    # 读取文件
    with open(file_path, 'rb') as f:
        file_content = f.read()
    
    file_name = os.path.basename(file_path)
    object_key = f"uptime-kuma/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file_name}"
    
    # S3参数
    method = 'PUT'
    service = 's3'
    host = f"{R2_CONFIG['bucket']}.{R2_CONFIG['endpoint']}"
    region = 'auto'
    endpoint = f"https://{host}/{object_key}"
    
    # 当前时间
    t = datetime.utcnow()
    amz_date = t.strftime('%Y%m%dT%H%M%SZ')
    date_stamp = t.strftime('%Y%m%d')
    
    # 规范请求
    canonical_uri = f'/{object_key}'
    canonical_querystring = ''
    canonical_headers = f'host:{host}\nx-amz-date:{amz_date}\n'
    signed_headers = 'host;x-amz-date'
    
    payload_hash = hashlib.sha256(file_content).hexdigest()
    
    canonical_request = f'{method}\n{canonical_uri}\n{canonical_querystring}\n{canonical_headers}\n{signed_headers}\n{payload_hash}'
    
    # 生成签名
    algorithm = 'AWS4-HMAC-SHA256'
    credential_scope = f'{date_stamp}/{region}/{service}/aws4_request'
    
    string_to_sign = f'{algorithm}\n{amz_date}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode()).hexdigest()}'
    
    signing_key = get_signature_key(R2_CONFIG['secret_key'], date_stamp, region, service)
    signature = hmac.new(signing_key, string_to_sign.encode(), hashlib.sha256).hexdigest()
    
    # 授权头
    authorization_header = f'{algorithm} Credential={R2_CONFIG["access_key"]}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}'
    
    # 请求头
    headers = {
        'Host': host,
        'x-amz-date': amz_date,
        'Authorization': authorization_header,
        'Content-Type': 'image/png',
        'Content-Length': str(len(file_content))
    }
    
    print(f"上传: {file_name} -> {object_key}")
    
    try:
        # 发送请求（禁用SSL验证）
        response = requests.put(
            endpoint,
            data=file_content,
            headers=headers,
            verify=False  # 禁用SSL验证
        )
        
        if response.status_code in [200, 201]:
            public_url = f"https://{R2_CONFIG['public_domain']}/{object_key}"
            print(f"✅ 上传成功: {public_url}")
            return public_url
        else:
            print(f"❌ 上传失败: HTTP {response.status_code}")
            print(f"响应: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return None

def main():
    print("=== 直接S3 API上传 ===\n")
    
    files = [
        "/tmp/uptime_kuma_analysis.png",
        "/tmp/uptime_kuma_logged_in.png",
        "/tmp/uptime_kuma_screenshot.png"
    ]
    
    uploaded_urls = []
    
    for file_path in files:
        if os.path.exists(file_path):
            url = upload_file_direct(file_path)
            if url:
                uploaded_urls.append(url)
        else:
            print(f"跳过: {file_path} 不存在")
    
    print(f"\n=== 完成 ===")
    print(f"成功上传: {len(uploaded_urls)}/{len(files)} 个文件")
    
    if uploaded_urls:
        print("\n📎 图片链接:")
        for url in uploaded_urls:
            print(f"  • {url}")

if __name__ == "__main__":
    main()