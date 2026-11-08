#!/usr/bin/env python3
# HKP4 文风门禁：交稿前必跑。用法: python3 scripts/check_style.py src/content/articles/zh/xxx.md [en/xxx.md ...]
# 硬伤=fail(非零退出)；腔调疑点=warn(列出但不拦，交主编裁)
import re, sys

HARD_JARGON = ['交付','落地','抓手','閉環','賦能','對齊','顆粒','打法','拉通','心智','驗過','對賬','過數','分筆清還','記一筆','記賬','記帳','當賬收','照單全收','照單記入','筆筆']
HARD_Fierce = ['子彈','釘死','清算','血債','擋箭牌','獻祭式']
HARD_LABEL  = ['陣營','營內','營外','社運人物','意見領袖','泛民','建制派']   # 归类即立场，编者不贴
HARD_LEDGER = ['账','帳']           # 当事人讲「账」时人工放行，默认禁（賬戶/賬號作「账户」解时不在此列）
WARN_TONE   = [('擱置|擱住|擱下','内地公文腔「擱」，港报多写「擺」「放」——复核'),
               ('放低','「放低」配情绪可、配事情冷处理不可——复核'),
               ('對面|那一邊','对立框架词嫌疑——复核'),
               ('上心|走向|向好','北腔嫌疑——复核'),
               ('止損','港式财经写「止蝕」——复核')]
# 演/沉/置为正字简繁同形，非简体误写，不在疑点列
SUS_SIMP = '个们关问答这为动劳级产户门与写读谢让语员运远违连类术样极权发变给网络习乡书买众会举构档检风飞驶马当灯东车长责线恶里团练签虽并帐说叶两両带来后于义乐农冲决钟错闻闲断适迁征确复难样'
KNOWN_OK = {'答','准','台','肃','遣','面','里','了','才','布','托','干','秘','克','咸'}
# 立规前发表的历史篇：词汇类照拦，结构类（段数/括号/列表/反问数/em dash）降为 warn
LEGACY = ('joshua-wong-sentence', 'one-country-two-systems')

# ── EN 分支词表：移植自 conorbronsdon/avoid-ai-writing（MIT）Tier 1，2026-11-12 取自 detector/patterns.js
# 1A＝AI 高频标记词（其检测器权重5，视为成文来源证据）→ fail；1B＝ clarity 冗词（其权重与 Tier 2 同级，非 AI 证据）→ warn
EN_T1A = [  # (regex, 展示名)；含词形变化与连字符变体
    (r'\bdelv(?:e|es|ed|ing)\b', 'delve'),
    (r'\btapestr(?:y|ies)\b', 'tapestry'),
    (r'\bparadigm\b', 'paradigm'),
    (r'\bbeacons?\b', 'beacon'),
    (r'\brobust(ness)?\b', 'robust'),
    (r'\bcomprehensive(ly)?\b', 'comprehensive'),
    (r'\bcutting[\s-]edge\b', 'cutting-edge'),
    (r'\bpivotal(ly)?\b', 'pivotal'),
    (r'\bmeticulous(ly)?\b', 'meticulous'),
    (r'\bseamless(ly)?\b', 'seamless'),
    (r'\bgame[\s-]chang(?:er|ing)\b', 'game-changer'),
    (r'\bnestled\b', 'nestled'),
    (r'\bvibrant\b', 'vibrant'),
    (r'\bthriving\b', 'thriving'),
    (r'\bbustling\b', 'bustling'),
    (r'\bintricac(?:y|ies|e(ly)?)\b', 'intricate'),
    (r'\bever[\s-]evolving\b', 'ever-evolving'),
    (r'\benduring\b', 'enduring'),
    (r'\bdaunting\b', 'daunting'),
    (r'\bholistic(ally)?\b', 'holistic'),
    (r'\bactionable\b', 'actionable'),
    (r'\bimpactful\b', 'impactful'),
    (r'\blearnings\b', 'learnings'),
    (r'\bsynerg(?:y|ies)\b', 'synergy'),
    (r'\binterplay\b', 'interplay'),
    (r'\bsymphon(?:y|ies)\b', 'symphony'),
    (r'\bembrac(?:e|es|ed|ing)\b', 'embrace'),
    (r'\bleverag(?:e|es|ing|ed)\b', 'leverage'),
    (r'\btestament\s+to\b', 'testament to'),
    (r'\bwatershed\s+moment\b', 'watershed moment'),
    (r'\bmarking\s+a\s+pivotal\s+moment\b', 'marking a pivotal moment'),
    (r'\bthe\s+future\s+looks\s+bright\b', 'the future looks bright'),
    (r'\bonly\s+time\s+will\s+tell\b', 'only time will tell'),
    (r'\bdespite\s+challenges\b[^.]{0,80}\bcontinues?\s+to\s+thrive\b', 'despite challenges…thrives'),
    (r'\bdeep\s+dive\b', 'deep dive'),
    (r'\bdive\s+into\b', 'dive into'),
    (r'\bunpack(?:s|ing|ed)?\b', 'unpack'),
    (r'\bcomplexities\b', 'complexities'),
    (r'\bthought\s+leader(?:ship)?\b', 'thought leader'),
    (r'\bbest\s+practices\b', 'best practices'),
    (r'\bat\s+its\s+core\b', 'at its core'),
    (r'\blandscapes?\b', 'landscape'),
    (r'\brealms?\b', 'realm'),
    (r'\bshowcas(?:e|es|ing|ed)\b', 'showcase'),
    (r'\bembark(?:s|ing|ed)?\b', 'embark'),
    (r'\bunderscor(?:es|ing|ed)\b', 'underscore'),
]
EN_T1B = [
    (r'\bin\s+order\s+to\b', 'in order to'),
    (r'\bdue\s+to\s+the\s+fact\s+that\b', 'due to the fact that'),
    (r'\bserv(?:e|es|ing|ed)\s+as\b', 'serve as'),
    (r'\bboasts?\b', 'boast'),
    (r'\butiliz(?:e|es|ing|ed)\b', 'utilize'),
    (r'\bcommenc(?:e|es|ing|ed)\b', 'commence'),
    (r'\bascertain(?:s|ing|ed)?\b', 'ascertain'),
    (r'\bendeavou?r(?:s|ing|ed)?\b', 'endeavour'),
]
EN_T2 = [  # Tier 2 原为段内 2+ 成簇才报，此处按篇计、一律 warn 交主编
    (r'\bharness(?:es|ing|ed)?\b', 'harness'),
    (r'\bnavigat(?:e|es|ing|ed)\b', 'navigate'),
    (r'\bfoster(?:s|ing|ed)?\b', 'foster'),
    (r'\belevat(?:e|es|ing|ed)\b', 'elevate'),
    (r'\bstreamlin(?:e|es|ing|ed)\b', 'streamline'),
    (r'\bempower(?:s|ing|ed)?\b', 'empower'),
    (r'\bunleash(?:es|ing|ed)?\b', 'unleash'),
]
# 结构规则（其目录 #16 #18 #23 #39 等）：句式壳与注水腔，命中即 fail 的均为硬伤，存疑交人的一律 warn
EN_STRUCT_FAIL = [
    (r"\b(?:it|this|that)['’]?s\s+not\s+(?:just\s+|merely\s+|simply\s+)?[^.!?]{1,80}?,\s*(?:it|this|that)['’]?s\b", "it's not X, it's Y 对比壳"),
    (r"\bnot\s+(?:just|merely)\s+[^.!?]{1,60}[—–]{1,2}\s*(?:it|this|that)['’]?s\b", "not just X — it's Y 对比壳"),
    (r'\b(?:could|may|might)\s+(?:potentially|eventually|ultimately)\b', '对冲叠加'),
    (r"\bin\s+today['’]?s\s", "In today's 开场"),
]
EN_STRUCT_WARN = [
    (r'(?m)^(?:Moreover|Furthermore|Additionally)[,.]', 'Moreover 系过渡词'),
    (r'\b(?:experts?\s+believe|studies\s+show|research\s+suggests)\b', '模糊引源'),
    (r'\bit\s+is\s+worth\s+noting|\bworth\s+noting\b', 'worth noting'),
    (r'\bplays?\s+a\s+(crucial|vital|pivotal|key)\s+role\b', 'plays a role 套话'),
]

# 断行（排版上的法槌）：≤50字/180字符的独立短段＝断语，不占 6–10 段数，全篇≤3处、至多两句（SOP 第十一节）
SINGLE_MAX_ZH, SINGLE_MAX_EN = 50, 180

def body_of(t):
    return t.split('---\n', 2)[2].split('\n---\n')[0]

def strip_quotes(b):
    return re.sub(r'「[^」]*」', '', b)

def en_strip_quotes(b):
    return re.sub(r'“[^”]*”|"[^"]*"', '', b)

def en_hits(rules, text):
    out = []
    for pat, name in rules:
        n = len(re.findall(pat, text, re.I))
        if n: out.append(name if n == 1 else f'{name}×{n}')
    return out

def check(p):
    fails, warns = [], []
    t = open(p).read(); b = body_of(t); nb = strip_quotes(b)
    legacy = any(k in p for k in LEGACY)
    def bad(msg):
        (warns if legacy else fails).append(('LEGACY warn: ' if legacy else 'FAIL: ') + msg)
    is_en = '/en/' in p
    if is_en:
        if len(re.findall(r'[\u4e00-\u9fff]', t)): fails.append('EN: 正文含中文')
        if b.count('—') > 4: bad(f'EN: em dash {b.count("—")} 处 >4')
        ne = en_strip_quotes(b)
        h = en_hits(EN_T1A, ne)
        if h: bad('EN AI词1A: ' + ', '.join(h))
        h = en_hits(EN_T1B, ne)
        if h: warns.append('EN 冗词1B: ' + ', '.join(h))
        h = en_hits(EN_T2, ne)
        if h: warns.append('EN Tier2: ' + ', '.join(h))
        for pat, why in EN_STRUCT_FAIL:
            m = re.search(pat, ne, re.I)
            if m: bad(f'EN 结构「{m.group(0)[:48]}」— {why}')
        for pat, why in EN_STRUCT_WARN:
            m = re.search(pat, ne)
            if m: warns.append(f'EN 腔调「{m.group(0)[:48]}」— {why}')
        if ne.count('?') > 2: bad(f'EN 作者反问 {ne.count("?")} 处 >2')
        if '!' in ne: bad('EN 引语外出现感叹号')
        if re.search(r'["“][^"”]*[!?]', nb) and 'back-translated' not in b:
            warns.append('EN: 有引语但全文无 back-translated 标注')
        paras = [x for x in b.split('\n\n') if x.strip()]
        singles = [x.strip() for x in paras if len(x.strip()) <= SINGLE_MAX_EN]
        if len(singles) > 3: bad(f'EN 断行 {len(singles)} 处 >3')
        for s in singles:
            if len(re.findall(r'[.!?]', s.rstrip('.!?…'))) + 1 > 2: bad(f'EN 断行超两句:「{s[:40]}…」')
    else:
        for w in HARD_JARGON:  fails.append('黑话: '+w) if w in b else None
        for w in HARD_Fierce:  fails.append('狠话: '+w) if w in b else None
        for w in HARD_LABEL:   fails.append('归类标签: '+w) if w in b else None
        for w in HARD_LEDGER:  fails.append(f'账房字: {w}（当事人讲过「账」才可人工放行）') if w in b else None
        for pat, why in WARN_TONE:
            m = re.search(pat, b)
            if m: warns.append(f'腔调「{m.group(0)}」— {why}')
        simp = sorted({c for c in t if c in SUS_SIMP and c not in KNOWN_OK})
        if simp: fails.append('简体嫌疑: ' + ' '.join(simp) + '（码点复核后入白名单）')
        bad_cp = {hex(ord(c)) for c in t if 0x2E80 <= ord(c) <= 0x2FDF or ord(c) == 0xFFFD}  # 0x6A01=樁 为正字，勿再入黑名单
        if bad_cp: fails.append('死码/部首区码点: ' + ' '.join(sorted(bad_cp)))
        if nb.count('？') > 2: bad(f'作者反问 {nb.count("？")} 处 >2')
        if nb.count('！'): bad('引语外出现感叹号')
        if '（' in b or '(' in re.sub(r'https?://\S+|HK\$?\d[\d,.]*|\(\d{4}', '', b): bad('正文出现括号脚注')
        if re.search(r'^[-*>#] ', b, re.M): bad('正文出现列表/标题行')
        paras = [x for x in b.split('\n\n') if x.strip()]
        singles = [x.strip() for x in paras if len(x.strip()) <= SINGLE_MAX_ZH and '—— HKP4' not in x]
        bodyp = [x for x in paras if x.strip() not in singles]
        if not 6 <= len(bodyp) <= 10: bad(f'段数 {len(bodyp)} 不在 6–10（断行不占段）')
        if len(singles) > 3: bad(f'断行 {len(singles)} 处 >3')
        for s in singles:
            if len(re.findall(r'[。！？]', s.rstrip('。！？…'))) + 1 > 2: bad(f'断行超两句:「{s[:20]}…」')
        short = [i+1 for i, x in enumerate(bodyp) if len(x) < 60]
        if short: warns.append(f'第 {short} 段短于60字')
    return fails, warns

ok = True
for p in sys.argv[1:]:
    f, w = check(p)
    print(('❌ ' if f else '✅ ') + p)
    for x in f: ok = False; print('   FAIL:', x)
    for x in w: print('   warn:', x)
sys.exit(0 if ok else 1)
