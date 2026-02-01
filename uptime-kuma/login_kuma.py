#!/usr/bin/env python3
import requests
import json
import sys
from urllib.parse import urljoin

# Uptime Kuma 配置
BASE_URL = "https://kuma.runnable.run"
LOGIN_URL = urljoin(BASE_URL, "/api/login")
DASHBOARD_URL = urljoin(BASE_URL, "/dashboard")

# 登录凭据
USERNAME = "asher"
PASSWORD = "9l@i08E!9wl!"

def test_endpoints():
    """测试API端点"""
    endpoints = [
        "/api/login",
        "/api/auth/login", 
        "/api/user/login",
        "/api/verify-token",
        "/api/me",
        "/dashboard"
    ]
    
    for endpoint in endpoints:
        url = urljoin(BASE_URL, endpoint)
        try:
            response = requests.get(url, timeout=10)
            print(f"{endpoint}: HTTP {response.status_code} - Content-Type: {response.headers.get('content-type', 'unknown')}")
            
            # 检查是否是HTML页面
            if 'text/html' in response.headers.get('content-type', ''):
                print(f"  -> Returns HTML page (likely frontend SPA)")
            elif response.text.strip().startswith('{'):
                print(f"  -> Returns JSON (likely API)")
                print(f"  -> Sample: {response.text[:100]}...")
        except Exception as e:
            print(f"{endpoint}: Error - {e}")

def attempt_login():
    """尝试登录"""
    print("\n=== 尝试登录 ===")
    
    # 首先获取CSRF token或session
    session = requests.Session()
    
    # 获取登录页面
    try:
        response = session.get(DASHBOARD_URL, timeout=10)
        print(f"获取登录页面: HTTP {response.status_code}")
        
        # 检查页面内容
        if response.status_code == 200:
            # 查找可能的登录表单
            if 'login' in response.text.lower() or 'sign in' in response.text.lower():
                print("找到登录页面")
            else:
                print("页面内容中没有明显的登录表单")
                print(f"页面标题: {response.text[:500]}...")
        else:
            print(f"无法访问登录页面: {response.status_code}")
            
    except Exception as e:
        print(f"登录尝试失败: {e}")
        return False
    
    # 尝试POST登录（如果知道正确的端点）
    # 注意：Uptime Kuma的API可能需要特定的端点
    
    return False

def main():
    print("=== Uptime Kuma 登录测试 ===\n")
    
    # 测试端点
    test_endpoints()
    
    # 尝试登录
    # attempt_login()
    
    print("\n=== 建议 ===")
    print("1. Uptime Kuma 是单页面应用(SPA)，通常通过Web界面登录")
    print("2. 直接API登录可能需要特定的端点格式")
    print("3. 考虑通过浏览器手动登录，然后使用API token进行后续操作")
    print("4. 安全提醒：不要在日志或代码中硬编码密码")

if __name__ == "__main__":
    main()