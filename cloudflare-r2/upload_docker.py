#!/usr/bin/env python3
"""Docker版R2上传脚本"""
import boto3
from botocore.config import Config
import os
import glob

R2_CONFIG = {
    "bucket": "openbot-upload",
    "endpoint": "https://8034b6f645143efa728dad5b5df39e7bd.r2.cloudflarestorage.com",
    "access_key": "77934f3344f603fd8221404a62b51b91",
    "secret_key": "0d3732d1811748f7c4b69f4fa0476f5aea0f31b2aef93016c8c1c569bc8ee7af",
    "public_domain": "openbotfile.996.ninja"
}

def upload_to_r2(file_path):
    s3 = boto3.client(
        's3',
        endpoint_url=R2_CONFIG['endpoint'],
        aws_access_key_id=R2_CONFIG['access_key'],
        aws_secret_access_key=R2_CONFIG['secret_key'],
        config=Config(signature_version='s3v4'),
        region_name='auto'
    )
    
    file_name = os.path.basename(file_path)
    object_key = f"uptime-kuma/{file_name}"
    
    print(f"📤 上传: {file_name}")
    s3.upload_file(file_path, R2_CONFIG['bucket'], object_key)
    public_url = f"https://{R2_CONFIG['public_domain']}/{object_key}"
    print(f"✅ 成功: {public_url}")
    return public_url

def main():
    print("=== Docker R2 上传 ===\n")
    
    # 查找/data目录下的PNG文件
    files = glob.glob("/data/*.png")
    
    if not files:
        print("❌ /data目录下没有PNG文件")
        return
    
    urls = []
    for f in files:
        try:
            url = upload_to_r2(f)
            urls.append(url)
        except Exception as e:
            print(f"❌ 上传失败 {f}: {e}")
    
    print(f"\n=== 完成: {len(urls)}/{len(files)} ===")
    for url in urls:
        print(f"  {url}")

if __name__ == "__main__":
    main()
