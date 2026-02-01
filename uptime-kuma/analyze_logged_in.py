#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def analyze_logged_in_page():
    """分析登录后的Uptime Kuma页面"""
    
    print("=== 分析Uptime Kuma登录后页面 ===")
    
    # 配置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    try:
        # 连接到Selenium容器（需要重新启动）
        driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            options=chrome_options
        )
        
        print("✓ 浏览器连接成功")
        
        # 直接访问dashboard（假设登录状态通过session保持）
        url = "https://kuma.runnable.run/dashboard"
        print(f"访问: {url}")
        driver.get(url)
        
        # 等待页面加载
        time.sleep(5)
        
        print(f"\n页面标题: {driver.title}")
        print(f"当前URL: {driver.current_url}")
        
        # 检查页面主要内容
        print("\n=== 页面内容分析 ===")
        
        # 查找监控相关的元素
        monitor_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Monitor') or contains(text(), '监控')]")
        print(f"找到 {len(monitor_elements)} 个监控相关元素")
        
        # 查找状态相关的元素
        status_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Status') or contains(text(), '状态') or contains(text(), 'UP') or contains(text(), 'DOWN')]")
        print(f"找到 {len(status_elements)} 个状态相关元素")
        
        # 查找表格或列表
        tables = driver.find_elements(By.TAG_NAME, "table")
        print(f"找到 {len(tables)} 个表格")
        
        lists = driver.find_elements(By.TAG_NAME, "ul") + driver.find_elements(By.TAG_NAME, "ol")
        print(f"找到 {len(lists)} 个列表")
        
        # 查找卡片或面板
        card_elements = driver.find_elements(By.XPATH, "//*[contains(@class, 'card') or contains(@class, 'panel') or contains(@class, 'dashboard')]")
        print(f"找到 {len(card_elements)} 个卡片/面板元素")
        
        # 获取页面文本内容（前1000字符）
        page_text = driver.find_element(By.TAG_NAME, "body").text
        print(f"\n页面文本内容（前500字符）:")
        print(page_text[:500] + "..." if len(page_text) > 500 else page_text)
        
        # 查找具体的监控项目
        print("\n=== 查找监控项目 ===")
        
        # 尝试查找监控项列表
        monitor_items = driver.find_elements(By.XPATH, "//*[contains(@class, 'monitor') or contains(@class, 'item') or contains(@class, 'service')]")
        print(f"找到 {len(monitor_items)} 个可能的监控项目")
        
        for i, item in enumerate(monitor_items[:10]):  # 只显示前10个
            item_text = item.text.strip()
            if item_text and len(item_text) < 200:  # 过滤过长文本
                print(f"  项目[{i}]: {item_text[:100]}...")
        
        # 查找导航菜单
        print("\n=== 导航菜单 ===")
        nav_elements = driver.find_elements(By.XPATH, "//nav//* | //*[contains(@class, 'nav')]//* | //*[contains(@class, 'menu')]//*")
        nav_texts = []
        for elem in nav_elements:
            text = elem.text.strip()
            if text and text not in nav_texts and len(text) < 50:
                nav_texts.append(text)
        
        print(f"找到 {len(nav_texts)} 个导航项:")
        for text in nav_texts[:10]:  # 只显示前10个
            print(f"  - {text}")
        
        # 截屏保存当前页面
        screenshot_path = "/tmp/uptime_kuma_dashboard_details.png"
        driver.save_screenshot(screenshot_path)
        print(f"\n✓ 详细截图已保存: {screenshot_path}")
        
        # 获取页面HTML结构信息
        print("\n=== 页面结构 ===")
        page_source = driver.page_source
        print(f"页面HTML大小: {len(page_source)} 字符")
        
        # 检查是否有特定的监控数据
        if "heartbeat" in page_source.lower() or "uptime" in page_source.lower():
            print("✓ 页面包含心跳/正常运行时间数据")
        
        if "chart" in page_source.lower() or "graph" in page_source.lower():
            print("✓ 页面包含图表数据")
        
        # 关闭浏览器
        driver.quit()
        print("✓ 浏览器已关闭")
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        
        # 尝试读取之前保存的截图信息
        print("\n=== 从保存的截图分析 ===")
        print("登录后截图文件: /tmp/uptime_kuma_logged_in.png")
        print("文件大小: 211KB")
        print("建议：可以下载截图文件查看具体内容")

if __name__ == "__main__":
    # 需要先启动Selenium容器
    print("注意：需要Selenium容器正在运行")
    analyze_logged_in_page()