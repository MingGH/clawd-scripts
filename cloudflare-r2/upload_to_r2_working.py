#!/usr/bin/env python3
"""
Cloudflare R2 上传脚本 - 修复版
问题原因：之前的endpoint URL写错了！多了一个5
"""
import boto3
from botocore.config import Config
import os
import glob
from datetime import datetime

# 正确的R2配置
R2_CONFIG = {
    "bucket": "openbot-upload",
    "endpoint": "https://8034b6f645143efa728dad5bdf39e7bd.r2.cloudflarestorage.com",  # 正确的endpoint！
    "access_key": "e5e657b805e251539f6f93c8681deb35",
    "secret_key": "00b9b547f95fbae20055c27ef61a8b91ac1af488305d837d435bcb241713a612",
    "public_domain": "openbotfile.996.ninja"
}

def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url=R2_CONFIG['endpoint'],
        aws_access_key_id=R2_CONFIG['access_key'],
        aws_secret_access_key=R2_CONFIG['secret_key'],
        config=Config(signature_version='s3v4'),
        region_name='auto'
    )

def upload_file(file_path, prefix="uptime-kuma"):
    """上传单个文件到R2"""
    s3 = get_s3_client()
    file_name = os.path.basename(file_path)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    object_key = f"{prefix}/{timestamp}_{file_name}"
    
    print(f"📤 上传: {file_name}")
    s3.upload_file(file_path, R2_CONFIG['bucket'], object_key)
    public_url = f"https://{R2_CONFIG['public_domain']}/{object_key}"
    print(f"✅ 成功: {public_url}")
    return public_url

def upload_files(file_paths, prefix="uptime-kuma"):
    """批量上传文件"""
    urls = []
    for path in file_paths:
        if os.path.exists(path):
            try:
                url = upload_file(path, prefix)
                urls.append(url)
            except Exception as e:
                print(f"❌ 失败 {path}: {e}")
        else:
            print(f"⚠️ 跳过: {path} 不存在")
    return urls

def main():
    print("=== Cloudflare R2 上传 ===\n")
    
    # 默认上传/tmp下的uptime_kuma截图
    files = glob.glob("/tmp/uptime_kuma*.png")
    
    if not files:
        print("没有找到要上传的文件")
        print("用法: python upload_to_r2_working.py [文件路径...]")
        return
    
    print(f"找到 {len(files)} 个文件\n")
    urls = upload_files(files)
    
    print(f"\n=== 完成: {len(urls)}/{len(files)} ===")
    if urls:
        print("\n📎 图片链接:")
        for url in urls:
            print(f"  {url}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        upload_files(sys.argv[1:])
    else:
        main()
