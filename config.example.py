"""
配置文件示例
将本文件复制为 config.py 并填写实际配置
注意：不要将真实凭证提交到Git仓库
"""

# Uptime Kuma 配置
UPTIME_KUMA_CONFIG = {
    "base_url": "https://kuma.runnable.run",
    "username": "your_username",  # 替换为实际用户名
    "password": "your_password"   # 替换为实际密码
}

# Cloudflare R2 配置
R2_CONFIG = {
    "bucket_name": "your-bucket-name",
    "endpoint_url": "https://your-endpoint.r2.cloudflarestorage.com",
    "access_key_id": "your-access-key-id",
    "secret_access_key": "your-secret-access-key",
    "region": "auto",
    "public_domain": "your-public-domain.example.com"
}

# Selenium 配置
SELENIUM_CONFIG = {
    "selenium_url": "http://localhost:4444/wd/hub",
    "headless": True,
    "window_size": "1920,1080"
}

# 通用配置
GENERAL_CONFIG = {
    "timeout": 30,
    "retry_attempts": 3,
    "log_level": "INFO"
}
