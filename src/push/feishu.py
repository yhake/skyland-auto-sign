import os
import requests
import logging

def push_feishu(all_logs):
    """发送飞书机器人通知"""
    webhook = os.environ.get('FEISHU_WEBHOOK')
    if not webhook:
        logging.info("未配置 FEISHU_WEBHOOK，跳过飞书推送")
        return
    
    # 格式化日志内容
    if isinstance(all_logs, list):
        content = "\n".join(all_logs)
    else:
        content = str(all_logs)
    
    # 添加时间戳
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"【森空岛签到】{timestamp}\n\n{content}"
    
    # 限制消息长度（飞书限制）
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
            logging.info("✅ 飞书通知发送成功")
        else:
            logging.error(f"❌ 飞书通知发送失败: {response.text}")
    except Exception as e:
        logging.error(f"❌ 飞书通知发送异常: {e}")
