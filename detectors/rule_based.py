import os, ast, difflib, re

def extract_docstrings_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        src = f.read()
    tree = ast.parse(src)
    results = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            results[node.name] = ast.get_docstring(node) or ''
    return results

def extract_all_external_docs(dir_path):
    docs = {}
    for fname in os.listdir(dir_path):
        if not fname.lower().endswith(('.md','.txt')):
            continue
        path = os.path.join(dir_path, fname)
        current = None
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('## '):
                    current = line[3:].split('(')[0].strip()
                    docs.setdefault(current, []).append((fname, ''))
                elif current:
                    docs[current][-1] = (docs[current][-1][0], docs[current][-1][1] + line + ' ')
    merged = {}
    for k,v in docs.items():
        parts = []
        for src, text in v:
            parts.append(f"[{src}] " + text.strip())
        merged[k] = "\n".join(parts)
    return merged

def similarity(a, b):
    a = a or ''
    b = b or ''
    return difflib.SequenceMatcher(None, a, b).ratio()

def basic_rule_checks(func_name, docstring, code_text, external_text):
    issues = []
    if not docstring.strip():
        issues.append('Missing docstring')
    if re.search(r'raise|raises', (docstring or ''), re.I) and 'raise' not in (code_text or ''):
        issues.append('Doc mentions raise but code has no raise')
    if external_text and 'return' in (external_text or '').lower() and 'return' not in (code_text or '').lower():
        issues.append('External doc mentions return but implementation may differ')
    return issues
