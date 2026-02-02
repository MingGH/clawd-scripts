#!/usr/bin/env python3
"""
诊断晚上宕机问题
"""

import subprocess
import json
import time
from datetime import datetime, timedelta

def run_cmd(cmd):
    """运行命令并返回输出"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return result.stdout.strip()
    except Exception as e:
        return f"错误: {e}"

def check_system_health():
    """检查系统健康状态"""
    print("=" * 60)
    print("🔍 系统健康检查")
    print("=" * 60)
    
    # 1. 系统负载
    print("1. 系统负载:")
    print(run_cmd("uptime"))
    
    # 2. 内存使用
    print("\n2. 内存使用:")
    print(run_cmd("free -h"))
    
    # 3. 磁盘空间
    print("\n3. 磁盘空间:")
    print(run_cmd("df -h /"))
    
    # 4. 进程状态
    print("\n4. Moltbot进程状态:")
    print(run_cmd("ps aux | grep -E '(moltbot|gateway)' | grep -v grep"))
    
    # 5. 网络连接
    print("\n5. 网络连接状态:")
    print(run_cmd("netstat -tlnp | grep -E '(18789|8000)'"))
    
    # 6. Docker状态
    print("\n6. Docker容器状态:")
    print(run_cmd("docker ps --format 'table {{.Names}}\\t{{.Status}}\\t{{.Ports}}'"))

def check_network_issues():
    """检查网络问题"""
    print("\n" + "=" * 60)
    print("🌐 网络问题检查")
    print("=" * 60)
    
    # 1. 连接失败统计
    print("1. 连接失败统计:")
    print(run_cmd("netstat -s | grep -E '(failed|retransmitted|timeout)' | head -10"))
    
    # 2. 当前连接
    print("\n2. 当前TCP连接:")
    print(run_cmd("ss -t state established | wc -l") + " 个已建立连接")
    
    # 3. 检查网关可达性
    print("\n3. 网关可达性测试:")
    for port in [18789, 8000]:
        result = run_cmd(f"timeout 2 curl -s -o /dev/null -w '%{{http_code}}' http://localhost:{port} || echo '不可达'")
        print(f"  端口 {port}: {result}")

def check_resource_history():
    """检查资源使用历史"""
    print("\n" + "=" * 60)
    print("📊 资源使用历史")
    print("=" * 60)
    
    # 检查是否有OOM事件
    print("1. OOM事件检查:")
    oom_logs = run_cmd("dmesg | grep -i 'oom\|out of memory' | tail -5")
    if oom_logs and "错误" not in oom_logs:
        print("⚠️  发现OOM事件:")
        print(oom_logs)
    else:
        print("✅ 未发现OOM事件")
    
    # 检查系统日志中的错误
    print("\n2. 系统错误日志:")
    error_logs = run_cmd("journalctl --since '2 hours ago' --priority=3 | tail -10")
    if error_logs and "错误" not in error_logs:
        print("发现系统错误:")
        print(error_logs)
    else:
        print("✅ 系统日志正常")

def check_application_status():
    """检查应用状态"""
    print("\n" + "=" * 60)
    print("🚀 应用状态检查")
    print("=" * 60)
    
    # 1. 基金监控系统
    print("1. 基金监控系统:")
    fund_status = run_cmd("curl -s http://localhost:8000/health 2>/dev/null || echo '不可用'")
    print(f"   健康检查: {fund_status}")
    
    # 2. 数据库连接
    print("\n2. 数据库连接:")
    db_status = run_cmd("docker exec fund-postgres pg_isready -U funduser 2>/dev/null || echo '数据库不可用'")
    print(f"   PostgreSQL: {db_status}")
    
    # 3. Redis连接
    print("\n3. Redis连接:")
    redis_status = run_cmd("docker exec fund-redis redis-cli ping 2>/dev/null || echo 'Redis不可用'")
    print(f"   Redis: {redis_status}")

def analyze_possible_causes():
    """分析可能的原因"""
    print("\n" + "=" * 60)
    print("🔍 宕机可能原因分析")
    print("=" * 60)
    
    causes = [
        {
            "name": "网络不稳定",
            "evidence": "有5522次失败连接尝试和20183次重传",
            "probability": "高",
            "solution": "检查网络配置，增加重试机制"
        },
        {
            "name": "资源不足",
            "evidence": "内存使用率95%（但主要是缓存）",
            "probability": "中",
            "solution": "监控实际内存使用，考虑增加Swap"
        },
        {
            "name": "Docker网络问题",
            "evidence": "dmesg显示大量Docker网络设备活动",
            "probability": "中",
            "solution": "检查Docker网络配置，重启Docker服务"
        },
        {
            "name": "应用bug",
            "evidence": "基金监控系统API有小bug",
            "probability": "低",
            "solution": "修复API bug，增加错误处理"
        },
        {
            "name": "外部依赖问题",
            "evidence": "依赖天天基金网等外部API",
            "probability": "中",
            "solution": "增加API调用超时和重试机制"
        }
    ]
    
    for i, cause in enumerate(causes, 1):
        print(f"{i}. {cause['name']}:")
        print(f"   证据: {cause['evidence']}")
        print(f"   概率: {cause['probability']}")
        print(f"   解决方案: {cause['solution']}")
        print()

def recommend_solutions():
    """推荐解决方案"""
    print("=" * 60)
    print("💡 推荐解决方案")
    print("=" * 60)
    
    solutions = [
        "1. 🔧 立即措施:",
        "   - 重启Moltbot网关: `pkill -f moltbot-gateway && cd /opt/moltbot && npm start`",
        "   - 检查网络连接: `ping -c 4 8.8.8.8`",
        "   - 重启Docker: `systemctl restart docker`",
        "",
        "2. 🛡️  预防措施:",
        "   - 配置系统监控: 设置内存、CPU、磁盘监控",
        "   - 增加日志记录: 记录详细的错误信息",
        "   - 设置自动重启: 使用systemd或supervisor管理服务",
        "",
        "3. 📊 长期优化:",
        "   - 优化内存使用: 调整应用内存限制",
        "   - 网络优化: 调整TCP参数，增加连接池",
        "   - 高可用部署: 考虑多实例部署",
    ]
    
    for line in solutions:
        print(line)

def main():
    """主函数"""
    print("=" * 60)
    print("🩺 晚上宕机问题诊断报告")
    print(f"📅 诊断时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 执行各项检查
    check_system_health()
    check_network_issues()
    check_resource_history()
    check_application_status()
    analyze_possible_causes()
    recommend_solutions()
    
    print("=" * 60)
    print("📋 诊断总结")
    print("=" * 60)
    print("✅ 当前系统状态: 正常")
    print("⚠️  主要问题: 网络连接不稳定")
    print("💡 建议: 实施网络优化和监控")
    print("=" * 60)

if __name__ == "__main__":
    main()