#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import sys

def test_uptime_kuma():
    """使用Selenium测试Uptime Kuma登录"""
    
    print("=== 启动Selenium浏览器测试 ===")
    
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
        
        # 访问Uptime Kuma
        url = "https://kuma.runnable.run/dashboard"
        print(f"访问: {url}")
        driver.get(url)
        
        # 等待页面加载
        time.sleep(3)
        
        # 获取页面信息
        print(f"页面标题: {driver.title}")
        print(f"当前URL: {driver.current_url}")
        
        # 查看页面内容
        page_source = driver.page_source
        print(f"页面大小: {len(page_source)} 字符")
        
        # 查找登录相关元素
        login_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Login') or contains(text(), 'Sign In') or contains(text(), '登录')]")
        print(f"找到 {len(login_elements)} 个登录相关元素")
        
        # 查找输入框
        input_elements = driver.find_elements(By.TAG_NAME, "input")
        print(f"找到 {len(input_elements)} 个输入框")
        
        for i, inp in enumerate(input_elements[:5]):  # 只显示前5个
            input_type = inp.get_attribute("type") or "unknown"
            input_name = inp.get_attribute("name") or inp.get_attribute("id") or f"input_{i}"
            print(f"  输入框[{i}]: type={input_type}, name/id={input_name}")
        
        # 查找按钮
        button_elements = driver.find_elements(By.TAG_NAME, "button")
        print(f"找到 {len(button_elements)} 个按钮")
        
        # 截屏保存
        screenshot_path = "/tmp/uptime_kuma_screenshot.png"
        driver.save_screenshot(screenshot_path)
        print(f"✓ 截图已保存: {screenshot_path}")
        
        # 尝试查找登录表单
        forms = driver.find_elements(By.TAG_NAME, "form")
        print(f"找到 {len(forms)} 个表单")
        
        if forms:
            for i, form in enumerate(forms):
                form_id = form.get_attribute("id") or f"form_{i}"
                print(f"  表单[{i}]: id={form_id}")
        
        print("\n=== 分析结果 ===")
        if len(input_elements) >= 2:
            print("✓ 页面有输入框，可能需要登录")
            print("建议：通过浏览器手动登录查看具体表单结构")
        else:
            print("✗ 页面可能已经登录或不需要登录")
        
        # 关闭浏览器
        driver.quit()
        print("✓ 浏览器已关闭")
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    test_uptime_kuma()