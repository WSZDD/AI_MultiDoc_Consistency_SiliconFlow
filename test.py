import os, requests
from dotenv import load_dotenv
load_dotenv()  # 自动读取当前目录的 .env 文件

api_key = os.getenv("SILICONFLOW_API_KEY")
url = "https://api.siliconflow.cn/v1/chat/completions"

payload = {
    "model": "deepseek-ai/DeepSeek-V2.5",
    "messages": [
        {"role": "system", "content": "你是一个助手"},
        {"role": "user", "content": "你好，请简单回答：1+1=？"}
    ]
}

headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

resp = requests.post(url, headers=headers, json=payload)
print(resp.status_code)
print(resp.text)
