import os
import requests

def send(message):
    """发送飞书机器人通知"""
    webhook = os.environ.get('FEISHU_WEBHOOK')
    if not webhook:
        print("未配置 FEISHU_WEBHOOK，跳过飞书推送")
        return
    
    # 限制消息长度
    if len(message) > 4000:
        message = message[:4000] + "\n...（内容过长已截断）"
    
    data = {
        "msg_type": "text",
        "content": {
            "text": message
        }
    }
    
    try:
        response = requests.post(webhook, json=data, timeout=10)
        if response.status_code == 200:
            print("✅ 飞书通知发送成功")
        else:
            print(f"❌ 飞书通知发送失败: {response.text}")
    except Exception as e:
        print(f"❌ 飞书通知发送异常: {e}")
