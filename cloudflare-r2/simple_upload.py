#!/usr/bin/env python3
"""
简单直接的Cloudflare R2上传脚本
完全禁用SSL验证，专为解决SSL握手问题设计
"""

import requests
import os
from datetime import datetime
import hashlib
import hmac
from urllib.parse import quote

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
    
    def get_amz_headers(self, headers):
        """生成Amazon格式的头部字符串"""
        amz_headers = []
        for key in sorted(headers.keys()):
            if key.startswith('x-amz-'):
                amz_headers.append(f"{key}:{headers[key]}")
        return '\n'.join(amz_headers) + ('\n' if amz_headers else '')
    
    def upload_file(self, file_path):
        """上传文件到R2"""
        if not os.path.exists(file_path):
            print(f"❌ 文件不存在: {file_path}")
            return None
        
        # 读取文件
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        file_name = os.path.basename(file_path)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        object_key = f"uptime-kuma/{timestamp}_{file_name}"
        
        # 生成URL
        url = f"https://{self.config['bucket']}.{self.config['endpoint']}/{object_key}"
        
        # 当前时间
        from datetime import datetime, timezone
        t = datetime.now(timezone.utc)
        amz_date = t.strftime('%Y%m%dT%H%M%SZ')
        date_stamp = t.strftime('%Y%m%d')
        
        # 准备请求
        method = 'PUT'
        content_type = 'image/png'
        
        # 计算签名（简化版）
        # 注意：这是一个简化的签名方法，可能不适用于所有情况
        string_to_sign = f"{method}\n\n{content_type}\n{amz_date}\n/{self.config['bucket']}/{object_key}"
        
        # 生成签名
        signing_key = self.sign(
            self.sign(
                self.sign(
                    self.sign(
                        f"AWS4{self.config['secret_key']}".encode(),
                        date_stamp
                    ),
                    'auto'
                ),
                's3'
            ),
            'aws4_request'
        )
        
        signature = hmac.new(signing_key, string_to_sign.encode(), hashlib.sha256).hexdigest()
        
        # 构建授权头
        authorization = f"AWS4-HMAC-SHA256 Credential={self.config['access_key']}/{date_stamp}/auto/s3/aws4_request,SignedHeaders=host;x-amz-content-sha256;x-amz-date,Signature={signature}"
        
        # 请求头
        headers = {
            'Host': f"{self.config['bucket']}.{self.config['endpoint']}",
            'x-amz-date': amz_date,
            'x-amz-content-sha256': hashlib.sha256(file_content).hexdigest(),
            'Authorization': authorization,
            'Content-Type': content_type
        }
        
        print(f"📤 上传: {file_name} ({len(file_content)/1024:.1f} KB)")
        print(f"🔗 目标: {url}")
        
        try:
            # 发送请求，完全禁用SSL验证
            response = requests.put(
                url,
                data=file_content,
                headers=headers,
                verify=False,  # 完全禁用SSL验证
                timeout=30
            )
            
            print(f"📊 响应状态: {response.status_code}")
            
            if response.status_code in [200, 201]:
                public_url = f"https://{self.config['public_domain']}/{object_key}"
                print(f"✅ 上传成功!")
                print(f"🔗 公开URL: {public_url}")
                return public_url
            else:
                print(f"❌ 上传失败")
                print(f"响应头: {dict(response.headers)}")
                print(f"响应体: {response.text[:200]}")
                return None
                
        except Exception as e:
            print(f"❌ 请求异常: {type(e).__name__}: {e}")
            return None
    
    def test_connection(self):
        """测试连接"""
        print("测试R2连接...")
        try:
            # 尝试简单的HEAD请求
            url = f"https://{self.config['endpoint']}"
            response = requests.head(url, verify=False, timeout=10)
            print(f"端点响应: HTTP {response.status_code}")
            return True
        except Exception as e:
            print(f"连接测试失败: {e}")
            return False

def main():
    print("=== Cloudflare R2 简单上传工具 ===\n")
    
    uploader = R2SimpleUploader()
    
    # 测试连接
    if not uploader.test_connection():
        print("⚠️ 连接测试失败，但仍尝试上传...")
    
    # 上传文件
    files = [
        "/tmp/uptime_kuma_analysis.png",
        "/tmp/uptime_kuma_logged_in.png",
        "/tmp/uptime_kuma_screenshot.png"
    ]
    
    uploaded_urls = []
    
    for file_path in files:
        if os.path.exists(file_path):
            print(f"\n{'='*50}")
            url = uploader.upload_file(file_path)
            if url:
                uploaded_urls.append(url)
        else:
            print(f"⚠️ 跳过: {file_path} 不存在")
    
    # 结果总结
    print(f"\n{'='*50}")
    print(f"📋 上传总结:")
    print(f"   尝试上传: {len(files)} 个文件")
    print(f"   成功上传: {len(uploaded_urls)} 个文件")
    
    if uploaded_urls:
        print(f"\n🔗 成功上传的链接:")
        for url in uploaded_urls:
            print(f"   • {url}")
    
    print(f"\n💡 提示: 如果仍然失败，可能是服务器与Cloudflare R2的TLS兼容性问题")
    print("     建议使用替代方案：")
    print("     1. HTTP服务器: http://8.217.244.50:8888/")
    print("     2. SCP下载: scp root@8.217.244.50:/tmp/filename.png ~/Desktop/")

if __name__ == "__main__":
    main()