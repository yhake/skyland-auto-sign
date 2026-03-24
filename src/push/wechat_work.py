import os
import requests
import logging

def push_wechat_work(all_logs):
    """发送企业微信机器人通知"""
    webhook = os.environ.get('WECHAT_WEBHOOK')
    if not webhook:
        logging.info("未配置 WECHAT_WEBHOOK，跳过企业微信推送")
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
                logging.info("✅ 企业微信通知发送成功")
            else:
                logging.error(f"❌ 企业微信通知发送失败: {result}")
        else:
            logging.error(f"❌ 企业微信通知发送失败: {response.text}")
    except Exception as e:
        logging.error(f"❌ 企业微信通知发送异常: {e}")
