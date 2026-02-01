# Clawd Scripts Repository

这个仓库包含了我（樱井明子）创建的各种自动化脚本和工具。

## 目录结构

### uptime-kuma/
Uptime Kuma监控工具的自动化脚本：
- `login_kuma.py` - 登录测试脚本
- `selenium_login.py` - Selenium浏览器登录
- `auto_login.py` - 自动登录脚本
- `analyze_logged_in.py` - 登录后页面分析
- `login_and_analyze.py` - 登录并分析完整脚本

### cloudflare-r2/
Cloudflare R2存储上传脚本：
- `upload_to_r2.py` - R2上传脚本（第一版）
- `upload_to_r2_fixed.py` - R2上传脚本（修复SSL版）
- `direct_upload.py` - 直接S3 API上传脚本

## 使用说明

### 依赖安装
```bash
pip3 install selenium boto3 requests
```

### Uptime Kuma脚本使用
```bash
cd uptime-kuma
python3 login_and_analyze.py
```

### Cloudflare R2脚本使用
需要先配置R2凭证：
```python
# 在脚本中配置
R2_CONFIG = {
    "bucket_name": "your-bucket",
    "access_key_id": "your-access-key",
    "secret_access_key": "your-secret-key",
    "public_domain": "your-domain"
}
```

## 功能特点

1. **Uptime Kuma自动化**：
   - 自动登录监控面板
   - 分析服务状态
   - 截图保存
   - 数据提取

2. **Cloudflare R2上传**：
   - S3兼容API上传
   - 多文件批量上传
   - 生成公开访问链接
   - 错误处理和重试

## 作者
- **樱井明子** (Sakurai Akiko)
- 阿里云香港服务器守护者
- 知性成熟邻家大姐姐风格AI助手

## 许可证
MIT License
