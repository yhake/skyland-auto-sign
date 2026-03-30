import os
import requests
import logging
from datetime import datetime

def push_feishu(all_logs):
    """发送飞书交互式卡片通知"""
    webhook = os.environ.get('FEISHU_WEBHOOK')
    if not webhook:
        logging.info("未配置 FEISHU_WEBHOOK，跳过飞书推送")
        return
    
    # 格式化日志内容
    if isinstance(all_logs, list):
        content = "\n".join(all_logs)
    else:
        content = str(all_logs)
    
    if len(content) > 1500:
        content = content[:1500] + "\n...（内容过长已截断）"
    
    from datetime import timezone, timedelta

    # 东八区 UTC+8
    beijing_tz = timezone(timedelta(hours=8))
    timestamp = datetime.now(beijing_tz).strftime("%Y-%m-%d %H:%M:%S")
    
    # 判断状态
    if "成功" in content or "签到完成" in content:
        status = "success"
        status_text = "✅ 签到成功"
        color = "green"
    elif "失败" in content or "错误" in content:
        status = "error"
        status_text = "❌ 签到失败"
        color = "red"
    else:
        status = "info"
        status_text = "📋 签到完成"
        color = "blue"
    
    # 飞书交互式卡片（符合 Open Message 格式）
    data = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True,
                "enable_forward": True
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"【森空岛签到】{status_text}"
                },
                "template": color
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**📅 时间**：{timestamp}\n\n**📊 状态**：{status_text}\n\n**📝 详情**：\n{content}"
                    }
                },
                {
                    "tag": "hr"
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": "🔔 此消息由 GitHub Actions 自动发送"
                    }
                },
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {
                                "tag": "plain_text",
                                "content": "查看仓库"
                            },
                            "type": "primary",
                            "url": "https://github.com/yhake/skyland-auto-sign"
                        },
                        {
                            "tag": "button",
                            "text": {
                                "tag": "plain_text",
                                "content": "手动签到"
                            },
                            "type": "default",
                            "url": "https://github.com/yhake/skyland-auto-sign/actions"
                        }
                    ]
                }
            ]
        }
    }
    
    try:
        response = requests.post(webhook, json=data, timeout=10)
        if response.status_code == 200:
            logging.info("✅ 飞书交互卡片发送成功")
        else:
            logging.error(f"❌ 飞书交互卡片发送失败: {response.text}")
    except Exception as e:
        logging.error(f"❌ 飞书交互卡片发送异常: {e}")
