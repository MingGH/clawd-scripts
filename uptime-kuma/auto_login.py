#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import sys

def login_uptime_kuma():
    """自动登录Uptime Kuma"""
    
    print("=== Uptime Kuma 自动登录 ===")
    
    # 登录凭据
    USERNAME = "asher"
    PASSWORD = "9l@i08E!9wl!"
    
    # 配置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    try:
        # 连接到Selenium容器
        driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            options=chrome_options
        )
        
        print("✓ 浏览器连接成功")
        
        # 访问Uptime Kuma登录页面
        url = "https://kuma.runnable.run/dashboard"
        print(f"访问: {url}")
        driver.get(url)
        
        # 等待页面加载
        time.sleep(3)
        
        print(f"页面标题: {driver.title}")
        
        # 查找登录表单元素
        print("\n查找登录表单元素...")
        
        # 用户名输入框
        username_input = driver.find_element(By.ID, "floatingInput")
        print("✓ 找到用户名输入框")
        
        # 密码输入框
        password_input = driver.find_element(By.ID, "floatingPassword")
        print("✓ 找到密码输入框")
        
        # 登录按钮（可能是button或input type="submit"）
        login_button = None
        try:
            # 先尝试找button
            login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login') or contains(text(), 'Sign In')]")
        except:
            try:
                # 尝试找input type="submit"
                login_button = driver.find_element(By.XPATH, "//input[@type='submit']")
            except:
                # 尝试找任何button
                buttons = driver.find_elements(By.TAG_NAME, "button")
                if buttons:
                    login_button = buttons[0]
        
        if login_button:
            print(f"✓ 找到登录按钮: {login_button.tag_name} - {login_button.text}")
        else:
            print("✗ 未找到登录按钮")
            driver.quit()
            return False
        
        # 输入用户名和密码
        print("\n输入登录凭据...")
        username_input.clear()
        username_input.send_keys(USERNAME)
        print("✓ 输入用户名")
        
        password_input.clear()
        password_input.send_keys(PASSWORD)
        print("✓ 输入密码")
        
        # 点击登录按钮
        print("点击登录按钮...")
        login_button.click()
        
        # 等待登录完成
        time.sleep(5)
        
        # 检查登录结果
        print(f"\n登录后页面标题: {driver.title}")
        print(f"登录后URL: {driver.current_url}")
        
        # 检查是否有错误消息
        error_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'error') or contains(text(), 'Error') or contains(text(), 'invalid') or contains(text(), 'Invalid')]")
        if error_elements:
            print("⚠️ 发现错误消息:")
            for error in error_elements[:3]:  # 只显示前3个
                print(f"  - {error.text[:100]}")
        
        # 检查是否重定向到dashboard
        if "dashboard" in driver.current_url or "Uptime Kuma" in driver.title:
            print("✓ 可能登录成功")
            
            # 截屏保存登录后的页面
            screenshot_path = "/tmp/uptime_kuma_logged_in.png"
            driver.save_screenshot(screenshot_path)
            print(f"✓ 登录后截图已保存: {screenshot_path}")
            
            # 尝试获取页面内容
            page_source = driver.page_source
            if "monitor" in page_source.lower() or "status" in page_source.lower():
                print("✓ 页面包含监控相关内容")
            else:
                print("⚠️ 页面可能不包含预期的监控内容")
        else:
            print("⚠️ 可能登录失败或需要额外验证")
        
        # 获取cookies（如果有）
        cookies = driver.get_cookies()
        print(f"\n获取到 {len(cookies)} 个cookies")
        
        # 关闭浏览器
        driver.quit()
        print("✓ 浏览器已关闭")
        
        return True
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    login_uptime_kuma()