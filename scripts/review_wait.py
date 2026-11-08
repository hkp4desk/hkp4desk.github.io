#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""阻塞等待下一条未处理批注。用法: python3 scripts/review_wait.py <slug> [max_seconds]
有新批注则打印其 JSON 并退出 0；超时退出 3。"""
import json, os, sys, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
slug = sys.argv[1]
mx = float(sys.argv[2]) if len(sys.argv) > 2 else 900
nf = os.path.join(ROOT, 'docs', 'review', slug + '.jsonl')
t0 = time.time()
while True:
    if os.path.exists(nf):
        rows = [json.loads(l) for l in open(nf, encoding='utf-8') if l.strip()]
        op = [r for r in rows if r.get('status') != 'fixed']
        if op:
            print(json.dumps(op[0], ensure_ascii=False)); sys.exit(0)
    if time.time() - t0 > mx:
        print('TIMEOUT'); sys.exit(3)
    time.sleep(2)
