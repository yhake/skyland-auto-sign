import os
import requests
import logging
from datetime import datetime, timezone, timedelta

def push_wechat_work(all_logs):
    """发送企业微信 Markdown 通知"""
    webhook = os.environ.get('WECHAT_WEBHOOK')
    if not webhook:
        logging.info("未配置 WECHAT_WEBHOOK，跳过企业微信推送")
        return
    
    # 格式化日志内容
    if isinstance(all_logs, list):
        content = "\n".join(all_logs)
    else:
        content = str(all_logs)
    
    # 限制长度
    if len(content) > 1500:
        content = content[:1500] + "\n...（内容过长已截断）"
    
    # 东八区 UTC+8
    beijing_tz = timezone(timedelta(hours=8))
    timestamp = datetime.now(beijing_tz).strftime("%Y-%m-%d %H:%M:%S")
    
    # 判断签到状态
    if "成功" in content or "签到完成" in content:
        status_text = "✅ **签到成功**"
        status_color = "info"
    elif "失败" in content or "错误" in content:
        status_text = "❌ **签到失败**"
        status_color = "warning"
    else:
        status_text = "📋 **签到完成**"
    
    # 构建 Markdown 内容
    markdown_content = (
        f"# 【森空岛签到】{status_text}\n\n"
        f"**📅 时间**：{timestamp}\n\n"
        f"**📊 状态**：{status_text}\n\n"
        f"---\n\n"
        f"**📝 签到详情：**\n"
        f"{content}\n\n"
        f"---\n\n"
        f"🔔 此消息由 [GitHub Actions](https://github.com/yhake/skyland-auto-sign/actions) 自动发送"
    )
    
    data = {
        "msgtype": "markdown",
        "markdown": {
            "content": markdown_content
        }
    }
    
    try:
        response = requests.post(webhook, json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get('errcode') == 0:
                logging.info("✅ 企业微信 Markdown 通知发送成功")
            else:
                logging.error(f"❌ 企业微信 Markdown 通知发送失败: {result}")
        else:
            logging.error(f"❌ 企业微信 Markdown 通知发送失败: {response.text}")
    except Exception as e:
        logging.error(f"❌ 企业微信 Markdown 通知发送异常: {e}")
