# -*- coding: utf-8 -*-
import openai
import httpx
import time
import sys
import os
os.environ["OPENAI_BASE_URL"] = "https://api.deepseek.com/v1"  # 替换为 DeepSeek API 的实际 URL
os.environ["OPENAI_API_KEY"] = "sk-sk-adc69ce5a86b47d39f118eb64053fc9e"  # 替换为您的密钥
os.environ["OPENAI_MODEL"] = 'deepseek-reasoner'
# 然后继续原有代码...``
print("=== 强制配置 ===")
print(f"OPENAI_BASE_URL: {os.environ['OPENAI_BASE_URL']}")
print(f"OPENAI_MODEL: {os.environ['OPENAI_MODEL']}")
def test_deepseek_api(api_key, model="deepseek-chat", max_retries=3):
    """测试 DeepSeek API 连接性和密钥有效性"""
    # 创建安全的客户端配置
    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )
    
    # 准备测试结果
    test_result = {
        "status": "失败",
        "message": "",
        "response": None,
        "error_details": None
    }
    
    # 重试机制
    for attempt in range(max_retries):
        try:
            # 发送纯ASCII内容的测试请求
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Reply 'Test Successful'"}],
                timeout=10
            )
            
            # 处理响应内容（安全处理非ASCII字符）
            try:
                response_content = response.choices[0].message.content.encode('utf-8').decode('utf-8')
            except:
                response_content = response.choices[0].message.content
            
            # 更新测试结果
            test_result["status"] = "成功"
            test_result["message"] = f"API 响应成功 (尝试 {attempt+1}/{max_retries})"
            test_result["response"] = response_content
            return test_result
        
        except openai.AuthenticationError as e:
            test_result["status"] = "认证失败"
            test_result["message"] = f"API 密钥无效 (尝试 {attempt+1}/{max_retries})"
            test_result["error_details"] = str(e)
            
        except openai.APITimeoutError as e:
            test_result["status"] = "超时"
            test_result["message"] = f"请求超时 (尝试 {attempt+1}/{max_retries})"
            test_result["error_details"] = str(e)
            
        except openai.RateLimitError as e:
            test_result["status"] = "限流"
            test_result["message"] = f"请求频率过高 (尝试 {attempt+1}/{max_retries})"
            test_result["error_details"] = str(e)
            time.sleep(2)  # 遇到限流时等待2秒
            
        except Exception as e:
            # 获取更详细的错误信息
            error_class = e.__class__.__name__
            error_details = str(e)
            test_result["status"] = "错误"
            test_result["message"] = f"{error_class} 错误 (尝试 {attempt+1}/{max_retries})"
            test_result["error_details"] = error_details
        
        # 如果不是最后一次尝试，则等待后重试
        if attempt < max_retries - 1:
            wait_time = 1 + attempt  # 退避策略：1秒, 2秒, 3秒...
            time.sleep(wait_time)
    
    return test_result

def run_tests(api_key):
    """运行多个测试并提供详细诊断信息"""
    print("="*50)
    print(f"测试 DeepSeek API 连接性")
    print("="*50)
    
    # 测试 1: 基本连接测试
    print("\n[测试 1: 基本连接]")
    result = test_deepseek_api(api_key)
    
    # 输出测试结果（确保使用安全编码）
    safe_print(f"状态: {result['status']}")
    safe_print(f"消息: {result['message']}")
    
    if result["status"] == "成功":
        safe_print(f"响应内容: {result['response']}")
    else:
        safe_print(f"错误详情: {result['error_details']}")
    
    # 测试 2: 网络连接测试
    print("\n[测试 2: 网络连接诊断]")
    test_network_connection()
    
    # 测试 3: API 服务状态检查
    print("\n[测试 3: API 服务状态]")
    test_api_status()
    
    print("\n" + "="*50)
    print("测试完成")
    if result["status"] == "成功":
        print("✅ API 密钥有效且连接正常")
    else:
        print("❌ 存在问题:", result["message"])
        print("建议解决方案:")
        if "认证" in result["message"]:
            print("1. 访问 https://platform.deepseek.com/ 获取新密钥")
            print("2. 确保密钥格式以 'sk-' 开头")
            print("3. 检查账户状态和额度")
        elif "网络" in result["message"]:
            print("1. 检查您的网络连接")
            print("2. 尝试禁用 VPN 或防火墙")
            print("3. 验证是否能够访问 api.deepseek.com")
        elif "限流" in result["message"]:
            print("1. 稍等几分钟后重试")
            print("2. 减少 API 请求频率")
        else:
            print("1. 尝试使用不同的网络环境")
            print("2. 更新 Python 和 openai 库")
            print("3. 联系 DeepSeek 技术支持")

def safe_print(text):
    """安全打印函数，处理编码问题"""
    try:
        print(text)
    except UnicodeEncodeError:
        # 如果遇到编码问题，使用替代方案
        try:
            print(text.encode('utf-8').decode('utf-8'))
        except:
            print(text.encode('ascii', 'replace').decode('ascii', 'replace'))

def test_network_connection():
    """测试网络连接情况"""
    try:
        safe_print("测试基本网络连接...")
        response = httpx.get("https://api.deepseek.com", timeout=5)
        safe_print(f"状态码: {response.status_code} - 网络连接正常")
    except Exception as e:
        safe_print(f"网络连接失败: {str(e)}")
        safe_print("请检查您的互联网连接或网络设置")

def test_api_status():
    """测试 API 服务器状态"""
    try:
        safe_print("获取 API 服务状态...")
        # Ping API
        ping_response = httpx.get("https://api.deepseek.com", timeout=5)
        safe_print(f"API Ping 返回状态码: {ping_response.status_code}")
        
        if ping_response.status_code == 200:
            safe_print("API 服务正常运行")
        else:
            safe_print("API 服务可能存在问题")
            safe_print(f"完整响应: {ping_response.text[:100]}...")
    except Exception as e:
        safe_print(f"服务状态检查失败: {str(e)}")

if __name__ == "__main__":
    # 设置默认编码为 UTF-8
    sys.stdout.reconfigure(encoding='utf-8')
    
    # 在这里输入您的 API 密钥
    API_KEY = "sk-adc69ce5a86b47d39f118eb64053fc9e"  # 替换为您的实际密钥
    
    # 或者从命令行参数获取密钥
    if len(sys.argv) > 1:
        API_KEY = sys.argv[1]
    
    run_tests(API_KEY)