#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HKP4 稿件批注页：在文章上选字 → 浮出批注框 → 写意见 → 点按钮，意见写入 docs/review/<slug>.jsonl
用法：python3 scripts/review_server.py <slug> [--port 4322] [--lang zh]
  打开 http://localhost:4322/        （中文稿）
  打开 http://localhost:4322/?lang=en （英文稿）
页面每 5 秒检查稿件/批注文件是否有更新，有则自动刷新，并恢复到原来的滚动位置。
"""
import html, json, os, re, sys, threading, time, urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else 'wang-fuk-fund-accounts'
PORT = 4322
if '--port' in sys.argv:
    PORT = int(sys.argv[sys.argv.index('--port') + 1])
NOTE_DIR = os.path.join(ROOT, 'docs', 'review')
os.makedirs(NOTE_DIR, exist_ok=True)
NOTE_FILE = os.path.join(NOTE_DIR, SLUG + '.jsonl')

def article_path(lang):
    return os.path.join(ROOT, 'src', 'content', 'articles', 'zh' if lang == 'zh' else 'en', SLUG + '.md')

def read_article(lang):
    p = article_path(lang)
    t = open(p, encoding='utf-8').read()
    parts = t.split('\n---\n', 2)   # parts[0]=frontmatter 正文, parts[1]=正文, parts[2]=附件
    body = parts[1] if len(parts) >= 2 else t
    sources = parts[2] if len(parts) >= 3 else ''
    paras = [x.strip() for x in body.strip().split('\n\n') if x.strip()]
    fm = parts[0] if len(parts) >= 2 else ''
    def field(k):
        m = re.search(r'(?m)^' + k + r':\s*(.*)$', fm)
        if not m: return ''
        v = m.group(1).strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in '"\'': v = v[1:-1]
        return v
    return paras, sources.strip(), os.path.getmtime(p), field('title'), field('description')

def read_notes():
    if not os.path.exists(NOTE_FILE):
        return []
    out = []
    for line in open(NOTE_FILE, encoding='utf-8'):
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out

def version():
    notes = read_notes()
    try:
        m1 = os.path.getmtime(article_path('zh')); m2 = os.path.getmtime(article_path('en'))
    except OSError:
        m1 = m2 = 0
    return f'{max(m1, m2):.0f}-{len(notes)}-{sum(len(n.get("fix", "")) for n in notes)}'

class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, code, ctype, body):
        b = body.encode('utf-8') if isinstance(body, str) else body
        self.send_response(code); self.send_header('Content-Type', ctype); self.send_header('Content-Length', str(len(b)))
        self.send_header('Cache-Control', 'no-store'); self.end_headers(); self.wfile.write(b)

    def do_GET(self):
        u = urllib.parse.urlparse(self.path); q = urllib.parse.parse_qs(u.query)
        lang = (q.get('lang', ['zh'])[0])
        if u.path == '/version':
            return self.send(200, 'text/plain', version())
        if u.path == '/notes.json':
            return self.send(200, 'application/json', json.dumps(read_notes(), ensure_ascii=False))
        if u.path == '/article.json':
            paras, sources, _, title, desc = read_article(lang)
            return self.send(200, 'application/json', json.dumps({'lang': lang, 'paras': paras, 'sources': sources, 'title': title, 'description': desc}, ensure_ascii=False))
        return self.send(200, 'text/html; charset=utf-8', PAGE)

    def do_POST(self):
        if self.path != '/note':
            return self.send(404, 'text/plain', 'not found')
        n = int(self.headers.get('Content-Length', '0'))
        d = json.loads(self.rfile.read(n).decode('utf-8'))
        notes = read_notes()
        d.setdefault('comment', '') 
        if not d.get('comment'):
            d['comment'] = '我覺得這個地方別扭，需要修改'
        d['id'] = (max([x['id'] for x in notes]) + 1) if notes else 1
        d['ts'] = time.strftime('%Y-%m-%d %H:%M:%S'); d['status'] = 'open'; d['fix'] = ''
        with open(NOTE_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(d, ensure_ascii=False) + '\n')
        self.send(200, 'application/json', json.dumps(d, ensure_ascii=False))

PAGE = r"""<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><title>HKP4 批注 · __SLUG__</title>
<style>
:root{--ink:#1b2a4a;--paper:#f7f3ea;--mark:#ffd9a0;--fixed:#bfe8c4}
body{margin:0;background:var(--paper);color:var(--ink);font:18px/1.9 "Songti SC","Noto Serif CJK SC","PingFang SC",serif}
#bar{position:sticky;top:0;background:#fff8e8;border-bottom:1px solid #d8cfbf;padding:8px 16px;font:14px/1.6 -apple-system,sans-serif;display:flex;gap:14px;align-items:center;flex-wrap:wrap}
#bar a{color:#355;text-decoration:none}#bar b{font-weight:600}
#wrap{max-width:760px;margin:32px auto 120px;padding:0 20px}
#article p{text-indent:2em;margin:0 0 1.4em}
#article p.title{text-indent:0;font-size:28px;font-weight:700;line-height:1.4;margin:0 0 .6em}
#article p.desc{text-indent:0;font-size:15px;line-height:1.7;color:#444;margin:0 0 2em;padding:10px 12px;background:#efe9dc;border-left:4px solid #c9b}
#article p.short{text-indent:0;font-weight:600;margin:2em 0}
#sources{border-top:1px solid #c9bfae;padding-top:16px;font:14px/1.7 -apple-system,sans-serif;color:#444;white-space:pre-wrap}
mark{background:var(--mark);color:inherit;padding:2px 0;cursor:help;border-bottom:2px solid #c96}
mark.fixed{background:var(--fixed);border-bottom-color:#5a5}
mark.open{box-shadow:0 0 0 1px #c96 inset}
#callout{position:absolute;z-index:9;display:none;background:#fff;border:1px solid #b9a;margin:0;padding:10px;width:340px;box-shadow:0 6px 24px rgba(0,0,0,.18);font:15px/1.5 -apple-system,sans-serif}
#callout textarea{width:100%;height:70px;box-sizing:border-box;font:15px/1.5 inherit;padding:6px;border:1px solid #bbb}
#callout .sel{max-height:80px;overflow:auto;background:#f3eee3;padding:4px 6px;font-size:13px;margin-bottom:6px;color:#333}
#callout button{padding:6px 14px;margin-top:6px;margin-right:8px;border:1px solid #8a7;border-radius:4px;background:#2f6b3a;color:#fff;font-size:14px;cursor:pointer}
#callout button.cancel{background:#999;border-color:#999}
#callout .hint{color:#888;font-size:12px}
#list{margin-top:40px;font:15px/1.6 -apple-system,sans-serif}
#list .n{border-left:4px solid #c96;background:#fff8e8;padding:8px 12px;margin:10px 0}
#list .n.fixed{border-left-color:#5a5;background:#eef8ef}
#list .n .sel{color:#555}
#list .n .fix{color:#2f6b3a;margin-top:4px}
kbd{background:#eee;border:1px solid #ccc;border-radius:3px;padding:0 4px;font:12px monospace}
</style></head><body>
<div id="bar"><b>HKP4 批注</b> <span id="title"></span><span>·</span><a id="langlink">切換 中文/English</a><span>·</span>
<span>選取文字後在彈出框寫意見（不寫＝「這裏別扭，需要修改」），點「記下」。<kbd>n</kbd> 下一條 <kbd>p</kbd> 上一條</span>
<span id="count"></span></div>
<div id="wrap"><div id="article"></div><div id="sources"></div><div id="list"></div></div>
<div id="callout"><div class="sel"></div><textarea placeholder="怎麼改？（留空＝這裏別扭，需要修改）"></textarea><br>
<button class="ok">記下</button><button class="cancel">取消</button><div class="hint">記下後頁面立即標記；你改完一批，跟 Tango 說一聲「批注好了」。</div></div>
<script>
const SLUG='__SLUG__';const Q=new URLSearchParams(location.search);const LANG=Q.get('lang')||'zh';
const art=document.getElementById('article'),callout=document.getElementById('callout'),ta=callout.querySelector('textarea'),selBox=callout.querySelector('.sel');
const KEY='rv:'+SLUG+':'+LANG;let notes=[],paras=[];
function load(){return fetch('/article.json?lang='+LANG).then(r=>r.json()).then(d=>{paras=d.paras;render(d);return fetch('/notes.json').then(r=>r.json()).then(n=>{notes=n;applyMarks();renderList();});});}
function render(d){document.getElementById('title').textContent=d.title;document.getElementById('langlink').href='?lang='+(LANG==='zh'?'en':'zh');
 art.innerHTML='';
 const h=document.createElement('p');h.className='title';h.dataset.i=0;h.textContent=d.title;art.appendChild(h);
 const de=document.createElement('p');de.className='desc';de.dataset.i=1;de.textContent=d.description;art.appendChild(de);
 paras.forEach((p,i)=>{const e=document.createElement('p');if(p.length<=50)e.className='short';e.dataset.i=i+2;e.textContent=p;art.appendChild(e);});
 document.getElementById('sources').textContent=d.sources;}
function esc(s){const d=document.createElement('div');d.textContent=s;return d.innerHTML}
function applyMarks(){document.querySelectorAll('mark[data-id]').forEach(m=>{const p=m.parentNode;p.replaceChild(document.createTextNode(m.textContent),m);p.normalize();});
 const open=notes.filter(n=>n.lang===LANG),artPs=[...art.querySelectorAll('p')];
 for(const n of open){const p=artPs[n.para];if(!p)continue;const idx=p.textContent.indexOf(n.text);if(idx<0)continue;const r=textRange(p,idx,idx+n.text.length);if(!r)continue;const m=document.createElement('mark');m.dataset.id=n.id;m.className=n.status==='fixed'?'fixed':'open';m.title='#'+n.id+' '+(n.comment||'')+(n.fix?'\n已改：'+n.fix:'');try{r.surroundContents(m);}catch(e){}}}
function textRange(root,start,end){const w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);let n,off=0;let rs=null,re=null;while(n=w.nextNode()){const L=n.data.length;if(rs===null&&off+L>=start){rs=[n,start-off];}if(off+L>=end){re=[n,end-off];break;}off+=L;}if(!rs||!re)return null;const r=document.createRange();r.setStart(rs[0],rs[1]);r.setEnd(re[0],re[1]);return r;}
function renderList(){const el=document.getElementById('list');const mine=notes.filter(n=>n.lang===LANG);document.getElementById('count').textContent=mine.length?('批注 '+mine.length+' 條，未改 '+mine.filter(n=>n.status!=='fixed').length+' 條'):'';
 el.innerHTML=mine.length?'<div style="font-weight:600;margin-bottom:6px">批注清單</div>':'';mine.forEach(n=>{const d=document.createElement('div');d.className='n '+n.status;d.innerHTML='<div>#'+n.id+' <span class="sel">'+esc(n.text)+'</span></div><div>意見：'+esc(n.comment||'')+'</div>'+(n.fix?'<div class="fix">已改：'+esc(n.fix)+'</div>':'');const a=document.createElement('a');a.href='#';a.textContent='→ 到此';a.style.marginLeft='8px';a.onclick=(e)=>{e.preventDefault();jumpTo(n.id);};d.firstChild.appendChild(a);el.appendChild(d);});}
function marks(){return [...document.querySelectorAll('mark[data-id]')]}
function jumpTo(id){const m=marks().find(x=>x.dataset.id==String(id));if(m){m.scrollIntoView({block:'center'});m.style.outline='3px solid #e8a';setTimeout(()=>m.style.outline='',1500);}}
let cur=-1;function step(d){const ms=marks();if(!ms.length)return;cur=(cur+d+ms.length)%ms.length;ms[cur].scrollIntoView({block:'center'});ms[cur].style.outline='3px solid #e8a';setTimeout(()=>ms[cur].style.outline='',1500);}
document.addEventListener('keydown',e=>{if(e.target.tagName==='TEXTAREA')return;if(e.key==='n'){step(1);}if(e.key==='p'){step(-1);}});
let pending=null;
document.addEventListener('mouseup',e=>{if(callout.contains(e.target))return;setTimeout(()=>{const s=window.getSelection();if(!s||s.isCollapsed||!art.contains(s.anchorNode)){return;}const text=s.toString().trim();if(!text)return;let para=0;let node=s.anchorNode;if(node.nodeType===3)node=node.parentNode;const p=node.closest('p');if(p)para=+p.dataset.i;pending={lang:LANG,para,text};selBox.textContent=text;ta.value='';callout.style.display='block';const x=Math.min(e.pageX,window.scrollX+window.innerWidth-360),y=e.pageY+14;callout.style.left=x+'px';callout.style.top=y+'px';ta.focus();},10);});
callout.querySelector('.ok').onclick=()=>{if(!pending)return;pending.comment=ta.value.trim();fetch('/note',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(pending)}).then(r=>r.json()).then(n=>{notes.push(n);applyMarks();renderList();callout.style.display='none';pending=null;window.getSelection().removeAllRanges();save();});};
callout.querySelector('.cancel').onclick=()=>{callout.style.display='none';pending=null;};
function save(){try{localStorage.setItem(KEY,String(window.scrollY));}catch(e){}}
let t=null;window.addEventListener('scroll',()=>{clearTimeout(t);t=setTimeout(save,150);});
function restore(){let y=0;try{y=+localStorage.getItem(KEY)||0;}catch(e){}window.scrollTo(0,y);}
let v=null;function poll(){fetch('/version').then(r=>r.text()).then(x=>{if(v===null){v=x;return;}if(x!==v){save();location.reload();}}).catch(()=>{});}
load().then(()=>{restore();setInterval(poll,5000);});
</script></body></html>"""

if __name__ == '__main__':
    print(f'review server: http://localhost:{PORT}/  slug={SLUG}  notes={NOTE_FILE}')
    ThreadingHTTPServer(('127.0.0.1', PORT), H).serve_forever()
