#!/usr/bin/env python3
"""
测试DeepSeek API Key有效性
"""

import requests
import json
from datetime import datetime

def test_deepseek_api(api_key):
    """测试API Key是否有效"""
    
    # DeepSeek API端点
    url = "https://api.deepseek.com/v1/chat/completions"
    
    # 请求头
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 请求数据 - 简单的测试消息
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一个测试助手，请回复'API测试成功！'"},
            {"role": "user", "content": "请说'API Key测试通过！'"}
        ],
        "max_tokens": 50,
        "temperature": 0.7
    }
    
    try:
        print(f"🔍 正在测试API Key...")
        print(f"📅 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 50)
        
        # 发送请求
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        print(f"📡 HTTP状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            # 提取回复内容
            if "choices" in result and len(result["choices"]) > 0:
                message = result["choices"][0]["message"]["content"]
                print(f"✅ API测试成功！")
                print(f"💬 AI回复: {message}")
                
                # 显示使用量信息
                if "usage" in result:
                    usage = result["usage"]
                    print(f"📊 使用统计:")
                    print(f"   提示词token: {usage.get('prompt_tokens', 'N/A')}")
                    print(f"   完成token: {usage.get('completion_tokens', 'N/A')}")
                    print(f"   总token: {usage.get('total_tokens', 'N/A')}")
                
                return True
            else:
                print(f"❌ 响应格式异常: {result}")
                return False
                
        elif response.status_code == 401:
            print(f"❌ API Key无效或已过期")
            print(f"响应内容: {response.text[:200]}")
            return False
            
        elif response.status_code == 429:
            print(f"⚠️  请求频率限制")
            print(f"响应内容: {response.text[:200]}")
            return False
            
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(f"响应内容: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"❌ 请求超时")
        return False
        
    except requests.exceptions.ConnectionError:
        print(f"❌ 连接错误")
        return False
        
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False


def test_multiple_models(api_key):
    """测试不同模型"""
    models_to_test = ["deepseek-chat", "deepseek-coder"]
    
    print("\n" + "=" * 50)
    print("🤖 测试不同AI模型")
    print("=" * 50)
    
    for model in models_to_test:
        print(f"\n测试模型: {model}")
        
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": f"用{model}模型说'模型测试通过！'"}
            ],
            "max_tokens": 30,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=20)
            
            if response.status_code == 200:
                result = response.json()
                if "choices" in result:
                    message = result["choices"][0]["message"]["content"]
                    print(f"  ✅ {model}: {message}")
                else:
                    print(f"  ❌ {model}: 响应格式错误")
            else:
                print(f"  ❌ {model}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ {model}: {e}")


def test_concurrent_capability():
    """测试并发能力（模拟多AI协作）"""
    print("\n" + "=" * 50)
    print("🚀 测试并发处理能力")
    print("=" * 50)
    
    # 模拟多个任务
    tasks = [
        "编写一个Python函数计算斐波那契数列",
        "用JavaScript写一个简单的DOM操作",
        "解释什么是RESTful API",
        "写一个SQL查询语句",
        "创建一个简单的Dockerfile"
    ]
    
    print(f"模拟 {len(tasks)} 个并发任务:")
    for i, task in enumerate(tasks, 1):
        print(f"  {i}. {task}")
    
    print("\n💡 在实际多AI协作中，这些任务会分配给不同的AI同时处理")
    print("   每个AI专注于自己的专业领域，效率大幅提升！")


def main():
    """主函数"""
    print("=" * 60)
    print("🤖 DeepSeek API Key 测试工具")
    print("=" * 60)
    
    # 使用你提供的API Key
    api_key = "sk-ce09c4acdb1a4a8cac48c068a8ee7a17"
    
    # 隐藏部分Key显示
    masked_key = api_key[:10] + "..." + api_key[-10:] if len(api_key) > 20 else "***"
    print(f"🔑 测试的API Key: {masked_key}")
    
    # 测试1: 基础API功能
    success = test_deepseek_api(api_key)
    
    if success:
        # 测试2: 不同模型
        test_multiple_models(api_key)
        
        # 测试3: 并发能力演示
        test_concurrent_capability()
        
        print("\n" + "=" * 60)
        print("🎉 API Key测试完成！")
        print("=" * 60)
        print("✅ 这个API Key完全有效！")
        print("✅ 可以用于多AI协作开发")
        print("✅ 我作为'老大'可以指挥其他AI工作了")
        print("\n💡 下次需要开发时，我会说：")
        print('   "小弟AI们，开工了！" 🚀')
    else:
        print("\n" + "=" * 60)
        print("❌ API Key测试失败")
        print("=" * 60)
        print("请检查API Key是否正确或是否已过期")
    
    print("\n测试完成时间:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == "__main__":
    main()