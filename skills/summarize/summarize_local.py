#!/usr/bin/env python3
import argparse
import json
import os
import pathlib
import re
import subprocess
import sys
import urllib.request
from html import unescape

MAX_CHARS = 12000
DEFAULT_MODEL = os.environ.get('YMOS_SUMMARIZE_MODEL', 'qwen2.5-coder:7b')


def fetch_url(url: str) -> str:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=20) as resp:
        raw = resp.read().decode('utf-8', errors='ignore')
    text = re.sub(r'(?is)<(script|style).*?>.*?</\1>', ' ', raw)
    text = re.sub(r'(?s)<[^>]+>', ' ', text)
    text = unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def read_file(path: str) -> str:
    p = pathlib.Path(path)
    suffix = p.suffix.lower()
    if suffix in {'.txt', '.md', '.markdown', '.csv', '.json', '.py', '.js', '.ts', '.html', '.htm'}:
        return p.read_text(encoding='utf-8', errors='ignore')
    raise SystemExit(f'暂不支持直接摘要该文件类型: {suffix}；建议先转 txt/md/html 再摘要。')


def load_content(target: str) -> str:
    if re.match(r'^https?://', target, re.I):
        return fetch_url(target)
    return read_file(target)


def build_prompt(content: str, style: str, target: str) -> str:
    clipped = content[:MAX_CHARS]
    return f'''你是一个专业中文摘要助手。请基于给定内容，生成高信息密度、少废话的中文摘要。\n\n目标对象: {target}\n输出风格: {style}\n\n严格按下面结构输出：\n1. 一句话结论\n2. 核心要点（3-7条）\n3. 风险点 / 争议点\n4. 对当前任务的可用价值\n\n要求：\n- 不要编造未出现的信息\n- 如果原文证据不足，要明确标注“原文未充分说明”\n- 尽量保留数字、时间、结论性表述\n- 语言专业、简洁、可执行\n\n原始内容如下：\n{clipped}\n'''


def run_ollama(model: str, prompt: str) -> str:
    result = subprocess.run(
        ['ollama', 'run', model],
        input=prompt,
        text=True,
        capture_output=True,
        encoding='utf-8',
        errors='ignore'
    )
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or f'ollama 调用失败，退出码 {result.returncode}')
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description='本地 summarize 替代实现：读取 URL/文本文件并调用 Ollama 生成中文摘要。')
    parser.add_argument('target', help='URL 或本地文本文件路径')
    parser.add_argument('--model', default=DEFAULT_MODEL, help='Ollama 模型名，默认读取 YMOS_SUMMARIZE_MODEL 或 qwen2.5-coder:7b')
    parser.add_argument('--style', default='财经研究 / 自媒体提炼', help='摘要风格提示')
    parser.add_argument('--json', action='store_true', help='输出 JSON 包装结果')
    args = parser.parse_args()

    content = load_content(args.target)
    if not content:
        raise SystemExit('未提取到可摘要内容。')
    prompt = build_prompt(content, args.style, args.target)
    summary = run_ollama(args.model, prompt)
    if args.json:
        print(json.dumps({'target': args.target, 'model': args.model, 'summary': summary}, ensure_ascii=False, indent=2))
    else:
        print(summary)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
