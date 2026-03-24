import os
import requests

def send(message):
    """发送企业微信机器人通知"""
    webhook = os.environ.get('WECHAT_WEBHOOK')
    if not webhook:
        print("未配置 WECHAT_WEBHOOK，跳过企业微信推送")
        return
    
    # 限制消息长度（企业微信限制 2048）
    if len(message) > 2000:
        message = message[:2000] + "\n...（内容过长已截断）"
    
    data = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    
    try:
        response = requests.post(webhook, json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get('errcode') == 0:
                print("✅ 企业微信通知发送成功")
            else:
                print(f"❌ 企业微信通知发送失败: {result}")
        else:
            print(f"❌ 企业微信通知发送失败: {response.text}")
    except Exception as e:
        print(f"❌ 企业微信通知发送异常: {e}")
