#!/usr/bin/env python3
import ssl
import socket

def test_tls_versions():
    """测试服务器支持的TLS版本"""
    hostname = "8034b6f645143efa728dad5b5df39e7bd.r2.cloudflarestorage.com"
    port = 443
    
    print(f"测试 {hostname} 的TLS支持\n")
    
    # 测试不同的TLS/SSL版本
    protocols = {
        'TLSv1.2': ssl.PROTOCOL_TLSv1_2,
        'TLSv1.1': ssl.PROTOCOL_TLSv1_1 if hasattr(ssl, 'PROTOCOL_TLSv1_1') else None,
        'TLSv1.0': ssl.PROTOCOL_TLSv1 if hasattr(ssl, 'PROTOCOL_TLSv1') else None,
        'SSLv3': ssl.PROTOCOL_SSLv3 if hasattr(ssl, 'PROTOCOL_SSLv3') else None,
        'SSLv23': ssl.PROTOCOL_SSLv23,
    }
    
    for name, protocol in protocols.items():
        if protocol is None:
            continue
            
        print(f"测试 {name}: ", end='')
        try:
            context = ssl.SSLContext(protocol)
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            with socket.create_connection((hostname, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    print(f"✅ 支持 - 密码: {ssock.cipher()[0]}")
        except Exception as e:
            print(f"❌ 不支持 - {type(e).__name__}")

def check_firewall():
    """检查防火墙和网络连接"""
    print("\n检查网络连接...")
    
    import subprocess
    
    # 测试基本连接
    test_host = "8034b6f645143efa728dad5b5df39e7bd.r2.cloudflarestorage.com"
    
    # 1. 测试DNS解析
    print("1. DNS解析测试: ", end='')
    try:
        import socket
        ip = socket.gethostbyname(test_host)
        print(f"✅ 成功 - IP: {ip}")
    except Exception as e:
        print(f"❌ 失败 - {e}")
        return False
    
    # 2. 测试TCP连接（不使用SSL）
    print("2. TCP端口连接测试: ", end='')
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((ip, 443))
        sock.close()
        
        if result == 0:
            print("✅ 端口443可访问")
        else:
            print(f"❌ 端口不可访问 (错误代码: {result})")
            return False
    except Exception as e:
        print(f"❌ 失败 - {e}")
        return False
    
    return True

def main():
    print("=== 全面SSL/TLS诊断 ===\n")
    
    # 检查网络基础
    network_ok = check_firewall()
    
    if network_ok:
        print("\n网络基础连接正常，开始TLS测试...")
        test_tls_versions()
    else:
        print("\n网络基础连接有问题，请先解决网络问题")
    
    print("\n" + "="*50)
    print("💡 诊断建议:")
    
    if network_ok:
        print("1. 服务器与Cloudflare R2的TLS协商失败")
        print("2. 可能是TLS版本或密码套件不兼容")
        print("3. 尝试完全重启系统: sudo reboot")
        print("4. 或者使用代理服务器上传")
    else:
        print("1. 检查防火墙设置")
        print("2. 检查阿里云安全组规则")
        print("3. 确保443端口对外开放")
        print("4. 检查DNS配置")

if __name__ == "__main__":
    main()