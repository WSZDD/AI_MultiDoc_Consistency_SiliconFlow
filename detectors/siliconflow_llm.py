import os, json, requests, re

SF_BASE = os.environ.get('SILICONFLOW_API_BASE', 'https://api.siliconflow.cn/v1/chat/completions')
SF_KEY_ENV = 'SILICONFLOW_API_KEY'

def call_siliconflow(prompt, api_key=None, model='deepseek-ai/DeepSeek-V2.5', timeout=90):
    if not api_key:
        raise ValueError('Missing SILICONFLOW_API_KEY')
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    body = {
        'model': model,
        'messages': [
            {'role': 'user', 'content': prompt}
        ],
        'max_tokens': 512,
        'temperature': 0.0
    }
    resp = requests.post(SF_BASE, headers=headers, json=body, timeout=timeout)
    resp.raise_for_status()
    return resp.text

def parse_json_from_text(text):
    m = re.search(r'\{.*\}', text, re.S)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            return None
    return None

def silicon_check_consistency(docstring: str, code: str, external: str = '', api_key: str = None):
    prompt = f"""请比较下面的函数文档（docstring）、外部文档与实现代码的一致性。
以JSON格式返回：{{"score":0-100,"issues":"...","suggestion":"...","explanation":"..."}}。
函数文档：\n{docstring}\n\n外部文档：\n{external}\n\n实现代码：\n{code}\n\n请集中指出主要不一致点并给出改进建议。使用中文回答。"""
    try:
        raw = call_siliconflow(prompt, api_key=api_key)
    except Exception as e:
        # propagate to caller to handle fallback
        raise
    data = parse_json_from_text(raw)
    if data and isinstance(data, dict):
        return data
    else:
        return {'score': 75, 'issues': 'No structured JSON returned', 'suggestion': '请检查模型返回', 'explanation': raw[:2000]}
