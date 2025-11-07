import os, json, traceback
from detectors.rule_based import extract_docstrings_from_file, extract_all_external_docs, similarity, basic_rule_checks
from detectors.siliconflow_llm import silicon_check_consistency
import pandas as pd, matplotlib.pyplot as plt
from dotenv import load_dotenv
load_dotenv()

ROOT = os.path.dirname(__file__)
SAMPLE_FILE = os.path.join(ROOT, 'sample_project', 'math_ops.py')
EXTERNAL_DIR = os.path.join(ROOT, 'docs')
REPORTS = os.path.join(ROOT, 'reports')
os.makedirs(REPORTS, exist_ok=True)

AI_LOG = os.path.join(REPORTS, 'ai_log.txt')
OUTPUT_JSON = os.path.join(REPORTS, 'output.json')

def analyze(api_key=None):
    internal = extract_docstrings_from_file(SAMPLE_FILE)
    external = extract_all_external_docs(EXTERNAL_DIR)
    results = []
    ai_logs = []
    for func, doc in internal.items():
        ext = external.get(func, '')
        with open(SAMPLE_FILE, 'r', encoding='utf-8') as f:
            src = f.read()
        start = src.find(f'def {func}(')
        code_block = ''
        if start != -1:
            end = src.find('\ndef ', start+1)
            code_block = src[start:] if end == -1 else src[start:end]
        rule_sim = round(similarity(doc, ext), 3)
        issues = basic_rule_checks(func, doc, code_block, ext)
        semantic = {'score': None, 'issues': '', 'suggestion': '', 'explanation': ''}
        if api_key:
            try:

                api_response = silicon_check_consistency(doc, code_block, external=ext, api_key=api_key)
    
                # 第一步：提取choices中的content（包含JSON的字符串）
                content = api_response['choices'][0]['message']['content']
                
                # 第二步：移除代码块标记（```json和```），提取纯JSON字符串
                json_str = content.strip().strip('```json').strip('```').strip()
                
                # 第三步：解析JSON字符串为字典
                sem = json.loads(json_str)
                semantic.update(sem)
                ai_logs.append({'function': func, 'model_output': sem})
            except Exception as e:
                ai_logs.append({'function': func, 'error': str(e), 'trace': traceback.format_exc()})
        results.append({
            'function': func,
            'docstring': doc,
            'external_doc': ext,
            'rule_similarity': rule_sim,
            'rule_issues': '; '.join(issues) if issues else '',
            'semantic_score': semantic.get('score'),
            'semantic_issues': semantic.get('issues'),
            'semantic_suggestion': semantic.get('suggestion'),
            'semantic_explanation': semantic.get('explanation')
        })
    df = pd.DataFrame(results)
    csv_path = os.path.join(REPORTS, 'consistency_report.csv')
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    with open(AI_LOG, 'w', encoding='utf-8') as f:
        f.write(json.dumps(ai_logs, ensure_ascii=False, indent=2))
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        f.write(df.to_json(orient='records', force_ascii=False, indent=2))
    plt.figure(figsize=(8, max(3, 0.6*len(df))))
    indices = range(len(df))
    rule_vals = df['rule_similarity'].astype(float).tolist()
    sem_vals = []
    for v in df['semantic_score'].tolist():
        try:
            sem_vals.append((float(v)/100.0) if v is not None else 0.0)
        except:
            sem_vals.append(0.0)
    import numpy as np
    bar_w = 0.35
    plt.barh([i+bar_w for i in indices], rule_vals, height=bar_w, label='Rule similarity (0-1)')
    plt.barh(indices, sem_vals, height=bar_w, label='Semantic score (0-1)')
    plt.yticks([i+bar_w/2 for i in indices], df['function'].tolist())
    plt.legend()
    plt.xlabel('Score')
    plt.title('Doc Consistency: Rule vs Semantic (normalized)')
    plot_path = os.path.join(REPORTS, 'consistency_plot.png')
    plt.tight_layout()
    plt.savefig(plot_path)
    print('Saved report to', csv_path)
    print('Saved ai log to', AI_LOG)
    print('Saved output json to', OUTPUT_JSON)
    print('Saved plot to', plot_path)
    return csv_path, plot_path, AI_LOG, OUTPUT_JSON

if __name__ == '__main__':
    key = os.environ.get('SILICONFLOW_API_KEY')
    analyze(api_key=key)
