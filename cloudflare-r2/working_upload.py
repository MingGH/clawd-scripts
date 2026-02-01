#!/usr/bin/env python3.8
"""
Cloudflare R2 上传脚本 - 使用代理绕过TLS问题
由于阿里云服务器与Cloudflare R2的S3 API存在TLS握手问题，
此脚本提供多种替代方案。

问题诊断结果：
- 服务器IP: 8.217.244.50 (阿里云香港)
- R2 S3 API endpoint的TLS握手失败
- 可能是区域性网络限制或Cloudflare的安全策略

解决方案：
1. 使用HTTP服务器本地托管文件
2. 通过SCP下载到本地后上传
3. 使用Cloudflare Workers作为上传代理
"""

import os
import json
import http.server
import socketserver
import threading
from datetime import datetime

# R2配置
R2_CONFIG = {
    "bucket": "openbot-upload",
    "endpoint": "8034b6f645143efa728dad5b5df39e7bd.r2.cloudflarestorage.com",
    "access_key": "77934f3344f603fd8221404a62b51b91",
    "secret_key": "0d3732d1811748f7c4b69f4fa0476f5aea0f31b2aef93016c8c1c569bc8ee7af",
    "public_domain": "openbotfile.996.ninja"
}

def start_file_server(directory="/tmp", port=8888):
    """启动简单的HTTP文件服务器"""
    os.chdir(directory)
    handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"📂 文件服务器启动在 http://0.0.0.0:{port}")
        print(f"   目录: {directory}")
        httpd.serve_forever()

def list_png_files(directory="/tmp"):
    """列出目录中的PNG文件"""
    files = []
    for f in os.listdir(directory):
        if f.endswith('.png'):
            path = os.path.join(directory, f)
            size = os.path.getsize(path)
            files.append({
                "name": f,
                "path": path,
                "size": f"{size/1024:.1f} KB",
                "url": f"http://8.217.244.50:8888/{f}"
            })
    return files

def generate_scp_commands(files):
    """生成SCP下载命令"""
    commands = []
    for f in files:
        cmd = f"scp root@8.217.244.50:{f['path']} ~/Desktop/"
        commands.append(cmd)
    return commands

def generate_upload_script(files):
    """生成本地上传脚本（在有正常网络的机器上运行）"""
    script = '''#!/usr/bin/env python3
"""
在本地机器上运行此脚本上传文件到Cloudflare R2
需要先用SCP下载文件到本地
"""
import boto3
from botocore.config import Config
import os

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
    
    s3.upload_file(file_path, R2_CONFIG['bucket'], object_key)
    public_url = f"https://{R2_CONFIG['public_domain']}/{object_key}"
    print(f"✅ 上传成功: {public_url}")
    return public_url

# 上传文件
files = [
'''
    for f in files:
        script += f'    "{f["name"]}",\n'
    
    script += ''']

for f in files:
    local_path = os.path.expanduser(f"~/Desktop/{f}")
    if os.path.exists(local_path):
        upload_to_r2(local_path)
    else:
        print(f"❌ 文件不存在: {local_path}")
'''
    return script

def main():
    print("=" * 60)
    print("🔧 Cloudflare R2 上传问题诊断与解决方案")
    print("=" * 60)
    
    print("\n📋 问题说明:")
    print("   此服务器(阿里云香港)无法直接连接Cloudflare R2的S3 API")
    print("   原因: TLS握手失败，可能是区域性网络限制")
    
    # 列出文件
    files = list_png_files("/tmp")
    
    print(f"\n📁 找到 {len(files)} 个PNG文件:")
    for f in files:
        print(f"   • {f['name']} ({f['size']})")
    
    print("\n" + "=" * 60)
    print("💡 解决方案")
    print("=" * 60)
    
    # 方案1: HTTP服务器
    print("\n【方案1】通过HTTP直接访问文件")
    print("-" * 40)
    for f in files:
        print(f"   {f['url']}")
    
    # 方案2: SCP下载
    print("\n【方案2】使用SCP下载到本地")
    print("-" * 40)
    print("   在你的本地机器上运行:")
    for cmd in generate_scp_commands(files):
        print(f"   {cmd}")
    
    # 方案3: 生成本地上传脚本
    print("\n【方案3】在本地机器上传到R2")
    print("-" * 40)
    print("   1. 先用方案2下载文件到本地")
    print("   2. 安装boto3: pip install boto3")
    print("   3. 运行生成的脚本: local_upload.py")
    
    # 保存本地上传脚本
    script = generate_upload_script(files)
    script_path = "/home/admin/clawd-scripts/cloudflare-r2/local_upload.py"
    with open(script_path, 'w') as f:
        f.write(script)
    print(f"\n   本地上传脚本已保存到: {script_path}")
    
    # 询问是否启动HTTP服务器
    print("\n" + "=" * 60)
    print("🚀 启动HTTP文件服务器?")
    print("   这将在端口8888启动一个简单的HTTP服务器")
    print("   你可以通过浏览器直接下载文件")
    print("=" * 60)
    
    try:
        choice = input("\n按Enter启动服务器，或输入'n'退出: ")
        if choice.lower() != 'n':
            start_file_server("/tmp", 8888)
    except KeyboardInterrupt:
        print("\n\n👋 再见!")

if __name__ == "__main__":
    main()
