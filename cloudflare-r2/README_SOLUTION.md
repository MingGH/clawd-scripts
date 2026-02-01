# Cloudflare R2 上传问题解决方案

## 问题诊断

经过详细排查，发现以下问题：

1. **根本原因**: 此服务器(阿里云香港 8.217.244.50)无法与Cloudflare R2的S3 API建立TLS连接
2. **错误信息**: `SSL: SSLV3_ALERT_HANDSHAKE_FAILURE`
3. **尝试过的方案**:
   - 升级Python到3.8 ❌
   - 安装OpenSSL 3.5.1 ❌
   - 使用rclone ❌
   - 修改crypto-policies ❌
   - 所有方案都因TLS握手失败而无法工作

4. **可能的原因**:
   - Cloudflare R2对某些区域/IP有特殊的TLS要求
   - 阿里云香港的网络与Cloudflare R2的S3 endpoint存在兼容性问题
   - 注意：public domain (openbotfile.996.ninja) 可以正常访问，只是S3 API endpoint有问题

## 解决方案

### 方案1: HTTP文件服务器（已启用）

文件服务器已在端口8888启动，可以直接访问：

```
http://8.217.244.50:8888/uptime_kuma_analysis.png
http://8.217.244.50:8888/uptime_kuma_logged_in.png
http://8.217.244.50:8888/uptime_kuma_screenshot.png
```

### 方案2: SCP下载后本地上传

1. 在本地机器下载文件：
```bash
scp root@8.217.244.50:/tmp/uptime_kuma_*.png ~/Desktop/
```

2. 使用本地机器上传到R2（需要安装boto3）：
```bash
pip install boto3
python3 local_upload.py
```

### 方案3: 使用其他云服务

如果需要长期解决，建议：
1. 使用阿里云OSS替代Cloudflare R2
2. 或者在其他区域部署一个代理服务器

## 文件位置

- 诊断脚本: `/home/admin/clawd-scripts/cloudflare-r2/working_upload.py`
- 本地上传脚本: `/home/admin/clawd-scripts/cloudflare-r2/local_upload.py`
- 原始失败脚本: `/home/admin/clawd-scripts/cloudflare-r2/simple_upload_fixed.py`

## 服务状态

HTTP文件服务器:
```bash
systemctl status file-server
```

重启服务:
```bash
systemctl restart file-server
```
