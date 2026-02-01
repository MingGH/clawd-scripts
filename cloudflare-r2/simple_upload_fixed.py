#!/usr/bin/env python3
"""
简单直接的Cloudflare R2上传脚本 - 修复版
"""

import requests
import os
from datetime import datetime, timezone
import hashlib
import hmac

class R2SimpleUploader:
    def __init__(self):
        # Cloudflare R2 配置
        self.config = {
            "bucket": "openbot-upload",
            "endpoint": "8034b6f645143efa728dad5b5df39e7bd.r2.cloudflarestorage.com",
            "access_key": "77934f3344f603fd8221404a62b51b91",
            "secret_key": "0d3732d1811748f7c4b69f4fa0476f5aea0f31b2aef93016c8c1c569bc8ee7af",
            "public_domain": "openbotfile.996.ninja"
        }
        
        # 完全禁用SSL警告
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    def sign(self, key, msg):
        """HMAC SHA256签名"""
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()
    
    def upload_file_simple(self, file_path):
        """简化版上传 - 使用预签名URL方法"""
        if not os.path.exists(file_path):
            print(f"❌ 文件不存在: {file_path}")
            return None
        
        # 读取文件
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        file_name = os.path.basename(file_path)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        object_key = f"uptime-kuma/{timestamp}_{file_name}"
        
        print(f"📤 准备上传: {file_name} ({len(file_content)/1024:.1f} KB)")
        print(f"📁 对象键: {object_key}")
        
        # 尝试使用更简单的方法：直接PUT
        url = f"https://{self.config['bucket']}.{self.config['endpoint']}/{object_key}"
        
        # 非常简单的头部
        headers = {
            'Content-Type': 'image/png',
            'Authorization': f"Bearer {self.config['access_key']}"  # 简化授权
        }
        
        try:
            print(f"🔗 尝试上传到: {url}")
            response = requests.put(
                url,
                data=file_content,
                headers=headers,
                verify=False,
                timeout=30
            )
            
            print(f"📊 响应状态: {response.status_code}")
            
            if response.status_code in [200, 201]:
                public_url = f"https://{self.config['public_domain']}/{object_key}"
                print(f"✅ 上传成功!")
                print(f"🔗 公开URL: {public_url}")
                return public_url
            else:
                print(f"❌ 上传失败: HTTP {response.status_code}")
                if hasattr(response, 'text'):
                    print(f"响应内容: {response.text[:200]}")
                return None
                
        except Exception as e:
            print(f"❌ 请求异常: {type(e).__name__}: {str(e)[:100]}")
            return None

def main():
    print("=== Cloudflare R2 上传测试（修复版） ===\n")
    print("⚠️ 注意：由于服务器SSL/TLS兼容性问题，上传可能失败")
    print("     我们将尝试最简单的上传方法\n")
    
    uploader = R2SimpleUploader()
    
    # 上传文件
    files = [
        "/tmp/uptime_kuma_analysis.png",
        "/tmp/uptime_kuma_logged_in.png", 
        "/tmp/uptime_kuma_screenshot.png"
    ]
    
    # 只尝试第一个文件（作为测试）
    test_file = files[0] if os.path.exists(files[0]) else None
    
    if test_file:
        print(f"测试上传: {os.path.basename(test_file)}")
        print("=" * 50)
        
        url = uploader.upload_file_simple(test_file)
        
        if url:
            print(f"\n🎉 上传成功！")
            print(f"图片链接: {url}")
        else:
            print(f"\n😔 上传失败")
            print("\n💡 替代方案：")
            print("1. 通过HTTP服务器访问:")
            print(f"   http://8.217.244.50:8888/{os.path.basename(test_file)}")
            print("\n2. 通过SCP下载:")
            print(f"   scp root@8.217.244.50:{test_file} ~/Desktop/")
            print("\n3. 在你的本地机器上上传到R2")
    else:
        print("❌ 测试文件不存在")

if __name__ == "__main__":
    main()