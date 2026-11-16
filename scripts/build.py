#!/usr/bin/env python3
"""Build an offline handbook from the publication's Markdown and JSONL sources."""
from pathlib import Path
from html import escape as esc
import json
import os
import re
from urllib.parse import urlsplit, unquote
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'content'
SITE = ROOT / 'site'
SOURCE = CONTENT / 'survey'
MD = MarkdownIt('commonmark', {'html': False}).enable('table')
REPO = 'https://github.com/SwanChann/ppo-manipulation-handbook'
CHAPTERS = [
    ('00_executive_summary', '结论与优先级', 'SO101、StackCube 与 Factory 分别值得借鉴什么'),
    ('01_ecosystem', '项目生态', '任务套件、仿真平台与 PPO 算法库的角色'),
    ('02_task_taxonomy', '任务索引', '按物理环节寻找控制接口、成功和终止条件'),
    ('03_reward_patterns', '奖励设计', '分段覆盖、事件进度、高水位与势函数'),
    ('04_training_configs', '训练配置', '实际入口、参数覆盖与并行预算'),
    ('05_recommendations', 'OrcaGym 复用方案', '候选干预的证据条件与证伪方式'),
    ('06_gaps', '覆盖与缺口', '静态源码调查的边界和配置冲突'),
]
NAV = [('takeaways', '01', '结论与阅读路线'), ('stages', '02', '阶段策略示意'), ('tasks', '03', '源码任务索引'), ('rewards', '04', '奖励设计机制'), ('configs', '05', '训练配置对照'), ('reading', '06', '完整技术附录')]
FAMILY = {'press-switch': '按钮 / 按键', 'grasp-place': '抓取 / 堆叠', 'insertion-assembly': '插入 / 装配', 'articulated': '抽屉 / 关节物体', 'bimanual': '双臂 / 双手', 'mobile-manipulation': '移动操作'}

# The summaries are editorial routes into the cited source cards, not new measurements.
CARDS = {
 'PickCube-v1': ('maniskill', '抓取与抬升的基本条件门控。', '目标位置和机器人静止；不要求松手。'),
 'StackCube-v1': ('maniskill', '抓住、放置、松手与静止奖励按条件覆盖。', '无机器人返回初态要求。'),
 'PegInsertionSide-v1': ('maniskill', '销头与销中心双点对齐后才激活插入项。', '插入成功不要求释放或撤回。'),
 'TwoRobotStackCube-v1': ('maniskill', '单个联合 Actor；奖励中包含右臂让位项。', '让位没有全部进入 success 条件。'),
 'OpenCabinetDrawer-v1': ('maniskill', '接近把手、抓取和开启奖励。', '开足后奖励与静止验收存在语义差异。'),
 'TurnFaucet-v1': ('maniskill', '保留关节物体任务的环境与成功条件。', '所查版本未核实可用密集 PPO 配置。'),
 'AssemblingKits-v1': ('maniskill', '装配环境可用作任务定义参考。', '所查版本为稀疏奖励，无已核验任务 PPO 配置。'),
 'isaaclab_lift': ('isaac', '高度条件门控目标追踪奖励。', '无独立完整成功布尔量；有掉落与超时终止。'),
 'isaaclab_cabinet': ('isaac', '连续几何塑形与开启奖励。', '开启即终止，不包含返回和停稳。'),
 'isaaclab_factory': ('isaac', '多尺度关键点、特权 Critic 与循环 PPO。', '初态已抓住销，只训练孔口附近的插入。'),
 'isaacgym_stack': ('isaac', '几何条件组合，成功奖励替换密集奖励。', '旧项目；释放检查是几何代理，无连续停稳。'),
 'so101_typing': ('isaac', '事件 FSM、Actor/Critic one-hot、当前阶段进度。', '注册 P0 与公开视觉教程的配置和验收需分开。'),
 'isaaclab_stack_negative': ('isaac', '反例：任务目录存在不等于已提供 PPO 基线。', '所查注册以模仿学习为主，rewards=None。'),
 'playground__PandaPickCubeCartesian': ('breadth', '只奖励历史最高分的新进展；区分状态与视觉变体。', '视觉成功只检查高度差；Brax 部分默认值未知。'),
 'playground__PandaOpenCabinet': ('breadth', '接近事件锁存与开启几何奖励。', '没有明确成功验收；不能由回报推断成功。'),
 'metaworld__button-press-v3': ('breadth', '靠近后激活按压奖励，可参考局部几何塑形。', '无保持、释放、撤回和重复按压验收。'),
 'robosuite__Stack': ('breadth', 'max 组合塑形；接触与松手共同参与堆叠成功。', '无连续保持；无已核验任务专属 PPO 配置。'),
 'bidexhands__ShadowHandOver': ('breadth', '双手联合控制与目标事件锁存。', '成功不检查接收手抓稳、原手释放或停稳。'),
}

def load(name):
    return [json.loads(line) for line in (SOURCE / 'data' / f'{name}.jsonl').read_text().splitlines() if line.strip()]

def card_key(t):
    tid = t['id']
    if tid.startswith('maniskill__'): return tid.split('__', 1)[1]
    if tid.startswith('so101__'): return 'so101_typing'
    if tid.startswith('isaaclab__'):
        if 'Lift-' in tid: return 'isaaclab_lift'
        if 'Cabinet' in tid: return 'isaaclab_cabinet'
        if 'Factory' in tid: return 'isaaclab_factory'
        return 'isaaclab_stack_negative'
    if tid.startswith('isaacgymenvs__'): return 'isaacgym_stack'
    return tid

def title(t):
    tid = t['id']
    if tid == 'so101__Physical-P0': return 'SO101 按键 · 注册 P0'
    if tid == 'so101__TutorialRandom13': return 'SO101 按键 · 公开视觉教程'
    return t['name'].replace('Isaac-', '').replace(' / single-agent PPO / egg full_state', '').replace(' (negative PPO baseline example)', ' · PPO 负例')

def shell(content, page_title, dest, article=False):
    root = os.path.relpath(SITE, dest.parent).replace(os.sep, '/')
    prefix = '' if root == '.' else root + '/'
    nav = ''.join(f'<a href="{prefix}index.html#{key}"><b>{num}</b>{label}</a>' for key,num,label in NAV)
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><meta name="description" content="机械臂操作 PPO 源码手册：任务、奖励、阶段事件与训练配置。"><title>{esc(page_title)} · 操作 PPO 手册</title><link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}assets/style.css"><script src="{prefix}assets/app.js" defer></script></head>
<body><a class="skip-link" href="#main">跳到正文</a><aside class="sidebar"><a class="brand" href="{prefix}index.html">操作 PPO<br>源码手册<small>MANIPULATION FIELD GUIDE</small></a><nav aria-label="主导航">{nav}</nav><div class="side-footer">源码调查 · 2026-11-16<br>ManiSkill / Isaac / MuJoCo<a href="{REPO}">GitHub 公开仓库 ↗</a><a href="{prefix}reference/06_gaps.html">证据范围与未知值</a></div></aside>
<header class="mobile-header"><a href="{prefix}index.html">操作 PPO 源码手册</a><a href="{prefix}index.html#reading">目录 ↓</a></header><main id="main" class="main {'article-shell' if article else ''}">{content}<footer class="footer"><span>基于固定源码版本的技术调查 · 未执行上游训练</span><a href="{REPO}">SwanChann / ppo-manipulation-handbook ↗</a></footer></main><a class="back-top" href="#main" aria-label="返回顶部">↑</a></body></html>'''

def rewrite_links(rendered, source, dest):
    def replace(m):
        href = m.group(1)
        if urlsplit(href).scheme or href.startswith('#'): return m.group(0)
        target = (source.parent / unquote(href.split('#')[0])).resolve()
        anchor = '#' + href.split('#', 1)[1] if '#' in href else ''
        if not target.is_relative_to(SOURCE):
            raise ValueError(f'Unpublished path survived import: {source}: {href}')
        rel = target.relative_to(SOURCE)
        if target.suffix == '.md': out = SITE / 'reference' / rel.with_suffix('.html')
        elif rel.parts[0] == 'data': out = SITE / rel
        else: out = SITE / 'reference' / rel
        if not target.exists(): raise FileNotFoundError(f'{source}: {href}')
        return f'href="{esc(os.path.relpath(out, dest.parent).replace(os.sep, "/") + anchor)}"'
    return re.sub(r'href="([^"]+)"', replace, rendered)

def render_article(path):
    text = path.read_text()
    # Some source cards contain raw JSON outside fences. Format those blocks for reading.
    lines = text.splitlines(); formatted = []; fenced = False; i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('```'): fenced = not fenced
        if not fenced and line == '{':
            end = i + 1
            while end < len(lines) and lines[end] != '}': end += 1
            candidate = '\n'.join(lines[i:end+1])
            try: json.loads(candidate)
            except (ValueError, json.JSONDecodeError): pass
            else:
                formatted += ['```json', candidate, '```']; i = end + 1; continue
        formatted.append(line); i += 1
    text = '\n'.join(formatted)
    rendered = MD.render(text)
    dest = SITE / 'reference' / path.relative_to(SOURCE).with_suffix('.html')
    rendered = rewrite_links(rendered, path, dest)
    toc = []
    def heading(m):
        index = len(toc) + 1; label = re.sub('<[^>]+>', '', m.group(1)); toc.append((index,label))
        return f'<h2 id="section-{index}">{m.group(1)}</h2>'
    rendered = re.sub(r'<h2>(.*?)</h2>', heading, rendered)
    rendered = re.sub(r'<table>(.*?)</table>', r'<div class="table-wrap"><table>\1</table></div>', rendered, flags=re.S)
    heading_match = re.search(r'^# (.+)$', text, re.M)
    page_title = heading_match.group(1) if heading_match else path.stem
    header = '<div class="article-header"><a href="' + os.path.relpath(SITE/'index.html', dest.parent).replace(os.sep,'/') + '#reading">← 返回阅读目录</a><span>完整技术附录 · 源码调查快照</span></div>'
    table = '<nav class="article-toc" aria-label="本页目录"><ul>' + ''.join(f'<li><a href="#section-{i}">{label}</a></li>' for i,label in toc) + '</ul></nav>' if toc else ''
    rendered = rendered.replace('</h1>', '</h1>' + table, 1)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(shell(header + '<article class="prose">' + rendered + '</article>', page_title, dest, article=True))

def fmt(x):
    return '未知' if x is None else f'{x:,}' if isinstance(x,int) else esc(str(x))

def main():
    tasks = load('tasks'); repos = {r['id']: r for r in load('repositories')}; evidence = {e['id']:e for e in load('evidence')}
    cards = []
    priority = {'so101__Physical-P0':0,'so101__TutorialRandom13':1,'maniskill__StackCube-v1':2,'maniskill__PegInsertionSide-v1':3,'isaaclab__Isaac-Factory-PegInsert-Direct-v0':4}
    for t in sorted(tasks, key=lambda t: priority.get(t['id'], 10)):
        key = card_key(t); part, desc, boundary = CARDS[key]
        label = title(t); project = repos[t['repository_id']]['name']; family = FAMILY.get(t['family'], t['family'])
        href = f'reference/parts/{part}/task_cards/{key}.html'
        search = ' '.join([label, t['name'], project, family, desc, boundary]).lower()
        status = '源码已核验' if t['status'] == 'verified' else '部分核验'
        cards.append(f'<article class="card task-card" data-family="{t["family"]}" data-search="{esc(search)}"><div class="task-project">{esc(project)} · {esc(family)}</div><span class="tag">{status}</span><h3>{esc(label)}</h3><p>{esc(desc)}</p><p class="boundary"><strong>验收边界：</strong>{esc(boundary)}</p><a href="{href}">公式、接口与配置 →</a></article>')
    rows = []
    taskmap = {t['id']: t for t in tasks}
    for i,c in enumerate(load('configs')):
        h = c['hyperparameters']; t = taskmap[c['task_id']]
        variant = c.get('task_variant') or c['id']
        rid = 'config-detail-' + str(i)
        cells = [h.get('num_envs'), h.get('rollout_steps', h.get('num_steps', h.get('unroll_length'))), h.get('total_timesteps',h.get('num_timesteps')),h.get('learning_rate'),h.get('gamma',h.get('discounting'))]
        label = title(t); search = ' '.join([label,variant,c['id'],c['trainer']]).lower()
        rows.append(f'<tr class="config-row" data-detail="{rid}" data-search="{esc(search)}"><td>{esc(label)}<small>{esc(variant)}</small></td>' + ''.join(f'<td>{fmt(x)}</td>' for x in cells) + f'<td><button type="button" class="config-toggle" aria-expanded="false" aria-controls="{rid}">展开</button></td></tr>')
        links = ''.join(f'<a href="{esc(evidence[e]["url"])}">源码证据 {j+1} ↗</a>' for j,e in enumerate(c['config_evidence_ids']))
        detail = {'trainer':c['trainer'],'entrypoint_unexecuted':c['entrypoint'],'config_chain':c.get('config_chain'),'source_revision':c.get('source_revision'),'status':c['status'],'hyperparameters':h,'notes':c.get('notes')}
        rows.append(f'<tr class="config-detail" id="{rid}" hidden><td colspan="7"><strong>入口与完整参数</strong><pre><code>{esc(json.dumps(detail,ensure_ascii=False,indent=2))}</code></pre><div class="evidence-links">{links}</div></td></tr>')
    chapters = ''.join(f'<a class="chapter-link" href="reference/{name}.html"><strong>{i+1:02} · {title}</strong><span>{desc}</span></a>' for i,(name,title,desc) in enumerate(CHAPTERS))
    references = []
    for p in sorted(SOURCE.rglob('*.md')):
        rel = p.relative_to(SOURCE)
        if 'parts' in rel.parts:
            heading = next((s[2:] for s in p.read_text().splitlines() if s.startswith('# ')), p.stem)
            references.append(f'<a href="reference/{rel.with_suffix(".html").as_posix()}">{esc(heading)} <span class="muted">({esc(str(rel.parent))})</span></a>')
        render_article(p)
    homepage = (CONTENT/'start.html').read_text().replace('{{TASK_CARDS}}',''.join(cards)).replace('{{CONFIG_ROWS}}',''.join(rows)).replace('{{CHAPTER_LINKS}}',chapters).replace('{{REFERENCE_LINKS}}',''.join(references))
    (SITE/'index.html').write_text(shell(homepage, '机械臂多阶段强化学习', SITE/'index.html'))
    import shutil
    shutil.copytree(SOURCE/'data', SITE/'data', dirs_exist_ok=True)
    for path in SOURCE.glob('*.json'):
        shutil.copy2(path, SITE/'reference'/path.name)
    for path in SOURCE.glob('*.txt'):
        shutil.copy2(path, SITE/'reference'/path.name)
    print(json.dumps({'html_pages':len(list(SITE.rglob('*.html'))),'tasks':len(tasks),'configs':len(load('configs'))},ensure_ascii=False))

if __name__ == '__main__': main()
