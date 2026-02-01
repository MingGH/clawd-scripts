#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def login_and_analyze():
    """登录并立即分析页面内容"""
    
    print("=== 登录Uptime Kuma并分析页面 ===")
    
    # 登录凭据
    USERNAME = "asher"
    PASSWORD = "9l@i08E!9wl!"
    
    # 配置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    try:
        # 连接到Selenium容器
        driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            options=chrome_options
        )
        
        print("✓ 浏览器连接成功")
        
        # 访问登录页面
        url = "https://kuma.runnable.run/dashboard"
        print(f"访问: {url}")
        driver.get(url)
        time.sleep(3)
        
        print(f"登录前标题: {driver.title}")
        
        # 登录
        print("\n执行登录...")
        driver.find_element(By.ID, "floatingInput").send_keys(USERNAME)
        driver.find_element(By.ID, "floatingPassword").send_keys(PASSWORD)
        
        # 找到并点击登录按钮
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        login_button.click()
        
        # 等待登录完成
        print("等待登录完成...")
        time.sleep(5)
        
        print(f"登录后标题: {driver.title}")
        print(f"登录后URL: {driver.current_url}")
        
        # 获取页面文本内容
        body_text = driver.find_element(By.TAG_NAME, "body").text
        print(f"\n=== 页面文本内容 ===")
        print(f"总字符数: {len(body_text)}")
        
        # 显示前1000个字符
        preview = body_text[:1000]
        print("\n内容预览:")
        print("-" * 50)
        print(preview)
        if len(body_text) > 1000:
            print(f"... (还有 {len(body_text) - 1000} 字符)")
        print("-" * 50)
        
        # 分析页面结构
        print("\n=== 页面结构分析 ===")
        
        # 查找所有可见文本元素
        all_elements = driver.find_elements(By.XPATH, "//*[text() and string-length(text()) > 0]")
        print(f"找到 {len(all_elements)} 个有文本内容的元素")
        
        # 提取有意义的文本（过滤太短或太长的）
        meaningful_texts = []
        for elem in all_elements:
            text = elem.text.strip()
            if 5 < len(text) < 200:  # 合理的文本长度
                # 检查是否是可见的（简单的可见性检查）
                if elem.is_displayed():
                    meaningful_texts.append(text)
        
        print(f"提取到 {len(meaningful_texts)} 个有意义的文本片段")
        
        # 显示前20个独特的文本片段
        unique_texts = []
        for text in meaningful_texts:
            if text not in unique_texts and len(unique_texts) < 20:
                unique_texts.append(text)
        
        print("\n有意义的文本内容:")
        for i, text in enumerate(unique_texts):
            print(f"  {i+1}. {text}")
        
        # 查找特定的Uptime Kuma元素
        print("\n=== 查找Uptime Kuma特定元素 ===")
        
        # 监控项
        monitor_keywords = ['http', 'https', 'tcp', 'ping', 'port', 'ssl', 'certificate']
        found_monitors = []
        
        for text in meaningful_texts:
            text_lower = text.lower()
            for keyword in monitor_keywords:
                if keyword in text_lower:
                    found_monitors.append(text)
                    break
        
        if found_monitors:
            print(f"找到 {len(found_monitors)} 个可能的监控项:")
            for monitor in found_monitors[:10]:  # 只显示前10个
                print(f"  - {monitor}")
        else:
            print("未找到明显的监控项")
        
        # 状态指示器
        status_keywords = ['up', 'down', 'pending', 'unknown', 'healthy', 'unhealthy']
        found_status = []
        
        for text in meaningful_texts:
            text_lower = text.lower()
            for keyword in status_keywords:
                if keyword in text_lower and len(text) < 50:
                    found_status.append(text)
                    break
        
        if found_status:
            print(f"\n找到 {len(found_status)} 个状态指示器:")
            for status in found_status[:10]:
                print(f"  - {status}")
        
        # 截屏
        screenshot_path = "/tmp/uptime_kuma_analysis.png"
        driver.save_screenshot(screenshot_path)
        print(f"\n✓ 分析截图已保存: {screenshot_path}")
        
        # 保存页面HTML供进一步分析
        html_path = "/tmp/uptime_kuma_page.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print(f"✓ 页面HTML已保存: {html_path} (大小: {len(driver.page_source)} 字符)")
        
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
    login_and_analyze()