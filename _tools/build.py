# 使い方: python3 _tools/build.py  （posts.py の記事からブログページ・一覧・sitemapを作り直す）
import os,sys,json,datetime
sys.path.insert(0,os.path.dirname(__file__))
from posts import POSTS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOLD='#C9A54C'; SITE='https://horyuji.bng.co.jp'
OPEN=dict(slug='opening',date='2026-11-18',cat='お知らせ',img='/img/store-front.webp',title='斑鳩町・法隆寺の買取店「買取大吉 法隆寺店」のご案内')
def page(title,desc,canon,body,ld='',ogtype='article'):
    return f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="{ogtype}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/img/store-front.jpg">
<link rel="icon" href="/logo.png">
{ld}
<style>
body{{margin:0;background:#F5F6FA;font-family:'Noto Sans JP',-apple-system,'Hiragino Sans',sans-serif;color:#1A1A1A;line-height:1.9;font-size:17px}}
a{{color:#232C7A}} img{{max-width:100%;height:auto}}
.wrap{{max-width:760px;margin:0 auto;padding:32px 20px 120px}}
.head{{background:#fff;border-bottom:1px solid #DDE0EA}}
.head .in{{max-width:760px;margin:0 auto;padding:12px 20px;display:flex;align-items:center;justify-content:space-between;gap:12px}}
.btn{{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 18px;border-radius:8px;font-weight:700;text-decoration:none}}
.card{{background:#fff;border:1px solid #DDE0EA;border-radius:12px;padding:24px}}
h1{{font-size:26px;line-height:1.5;margin:0 0 8px}} h2{{font-size:21px;margin:32px 0 8px;border-left:5px solid {GOLD};padding-left:12px;line-height:1.5}}
ul{{padding-left:1.4em}} li{{margin:4px 0}}
.meta{{font-size:14px;color:#5E6272}}
.cta{{position:fixed;left:0;right:0;bottom:0;display:flex;gap:8px;padding:8px;background:rgba(255,255,255,.96);border-top:1px solid #DDE0EA}}
.cta a{{flex:1;min-height:48px;display:flex;align-items:center;justify-content:center;border-radius:8px;font-weight:700;text-decoration:none}}
</style>
</head>
<body>
<header class="head"><div class="in">
<a href="/" style="display:flex;align-items:center;gap:10px;text-decoration:none"><img src="/logo.png" alt="買取大吉" style="height:44px;width:auto"><span style="font-weight:700;color:#232C7A">法隆寺店</span></a>
<span style="display:flex;gap:14px;font-weight:700;font-size:15px"><a href="/#coupon">クーポン</a><a href="/price/">参考価格</a><a href="/blog/">実績・ブログ</a></span>
</div></header>
<main class="wrap">
{body}
</main>
<footer style="background:#12163F;color:#CDD1E6;padding:28px 20px 100px;font-size:14px"><div style="max-width:760px;margin:0 auto">
<strong style="color:#fff">買取大吉 法隆寺店</strong><br>奈良県生駒郡斑鳩町興留5-1-35サンメゾン法隆寺<br>TEL 06-7777-6590 ／ 10:00〜19:00 ／ 年中無休<br>
古物商許可番号 第62106R070875号（大阪府公安委員会）</div></footer>
<nav class="cta" aria-label="お問い合わせ">
<a href="tel:0677776590" style="background:{GOLD};color:#1A1A1A">電話で相談</a>
<a href="https://line.me/ti/p/CZCmVd4SQf" style="background:#06C755;color:#0B2A16">LINEで査定</a>
<a href="https://www.google.com/maps/dir/?api=1&amp;destination=%E8%B2%B7%E5%8F%96%E5%A4%A7%E5%90%89%20%E6%B3%95%E9%9A%86%E5%AF%BA%E5%BA%97" style="flex:0 0 72px;background:#232C7A;color:#fff">道順</a>
</nav>
</body>
</html>
'''
STORECARD='''<div class="card" style="margin-top:32px">
<p style="margin:0 0 4px;font-weight:700;font-size:18px">買取大吉 法隆寺店</p>
<p style="margin:0 0 16px;font-size:15px">奈良県生駒郡斑鳩町興留5-1-35サンメゾン法隆寺<br>TEL 06-7777-6590 ／ 10:00〜19:00 ／ 年中無休 ／ 無料駐車場あり<br>査定無料・予約不要・ご相談だけでも大丈夫です。</p>
<div style="display:flex;flex-wrap:wrap;gap:10px">
<a class="btn" href="/#coupon" style="background:#C8102E;color:#fff">WEBクーポンを見る</a>
<a class="btn" href="/" style="background:#232C7A;color:#fff">お店のページへ</a>
</div></div>'''

from cats import CATS as _C
_REV={}
for _c in _C:
    for _s in _c['results']+_c['cols']: _REV.setdefault(_s,_c)
def catlink(p):
    c=_REV.get(p['slug'])
    return f'<p style="margin:24px 0 0"><a class="btn" href="/{c["slug"]}/" style="background:#232C7A;color:#fff">斑鳩町の{c["name"]}の買取について見る →</a></p>' if c else ''
today=datetime.date.today().isoformat()
for p in POSTS:
    p.setdefault('date',today)
    d=p['date']
    body=f'''<article>
<p class="meta">{d.replace('-','.')}　{p['cat']}</p>
<h1>{p['title']}</h1>
<img src="{p['img']}" alt="{p['alt']}" width="1400" height="1050" style="border-radius:10px;margin:16px 0">
{p['body']}
{catlink(p)}
</article>
{STORECARD}'''
    ld=json.dumps({"@context":"https://schema.org","@type":"BlogPosting","headline":p['title'],"description":p['desc'],"datePublished":d,"dateModified":d,"image":SITE+p['img'].replace('.webp','.jpg'),"author":{"@type":"Person","name":"吉原 涼"},"publisher":{"@type":"Organization","name":"買取大吉 法隆寺店","logo":{"@type":"ImageObject","url":SITE+"/logo.png"}},"mainEntityOfPage":f"{SITE}/blog/{p['slug']}/"},ensure_ascii=False)
    os.makedirs(f"{ROOT}/blog/{p['slug']}",exist_ok=True)
    open(f"{ROOT}/blog/{p['slug']}/index.html",'w',encoding='utf-8').write(page(p['title']+'｜買取大吉 法隆寺店',p['desc'],f"{SITE}/blog/{p['slug']}/",body,f'<script type="application/ld+json">{ld}</script>'))
allp=POSTS+[OPEN]
items=''.join(f'''<a href="/blog/{q['slug']}/" data-k="{'results' if q['cat']=='お買取り実績' else 'column'}" class="card" style="display:flex;align-items:center;gap:14px;text-decoration:none;color:#1A1A1A;padding:10px;margin-bottom:10px">
<img src="{q['img']}" alt="" width="1400" height="1050" loading="lazy" style="flex:0 0 112px;width:112px;height:84px;object-fit:cover;border-radius:6px">
<div style="min-width:0"><p class="meta" style="margin:0;line-height:1.5">{q['cat']}</p><p style="margin:2px 0 0;font-weight:700;font-size:16px;line-height:1.55">{q['title'].split('｜')[0]}</p></div></a>''' for q in allp)
nres=sum(1 for q in allp if q['cat']=='お買取り実績')
lb=f'''<h1>お買取り実績・店長ブログ</h1><p class="meta" style="margin-bottom:16px">斑鳩町・法隆寺の買取大吉 法隆寺店から、お買取り実績やお役立ち情報をお届けします。</p>
<style>.tb{{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 20px}}.tb a{{min-height:44px;padding:0 16px;border-radius:999px;border:1px solid #232C7A;color:#232C7A;font-weight:700;text-decoration:none;display:inline-flex;align-items:center;background:#fff}}.tb a.on{{background:#232C7A;color:#fff}}</style>
<nav class="tb" aria-label="記事の種類"><a href="#all" data-f="all">すべて（{len(allp)}）</a><a href="#results" data-f="results">お買取り実績（{nres}）</a><a href="#column" data-f="column">店長ブログ（{len(allp)-nres}）</a></nav>
<div id="list">{items}</div>
<script>
function f(){{var k=(location.hash||'#all').slice(1);if(['all','results','column'].indexOf(k)<0)k='all';document.querySelectorAll('.tb a').forEach(function(a){{a.classList.toggle('on',a.dataset.f===k)}});document.querySelectorAll('#list [data-k]').forEach(function(c){{c.style.display=(k==='all'||c.dataset.k===k)?'flex':'none'}})}}
window.addEventListener('hashchange',f);f();
</script>'''
open(f'{ROOT}/blog/index.html','w',encoding='utf-8').write(page('お買取り実績・店長ブログ｜買取大吉 法隆寺店（斑鳩町）','買取大吉 法隆寺店（奈良県斑鳩町）の店長ブログ。金・ブランド品・時計の買取のコツやお知らせを更新しています。',f'{SITE}/blog/',lb,ogtype='website'))

# ===== 買取参考価格ページ（_tools/price_raw.tsv：カテゴリ / 品名 / 価格 / 本部画像パス）=====
from urllib.parse import quote
PRICE_DATE='2026年11月18日'
CDN='https://cdn.speedsize.com/238b2c9c-0e0b-44a9-9a48-93e2951b75dc/www.kaitori-daikichi.jp/cms/wp-content/uploads/'
rows=[l.rstrip('\n').split('\t') for l in open(os.path.join(os.path.dirname(__file__),'price_raw.tsv'),encoding='utf-8') if l.strip()]
CATS=['金・貴金属','ジュエリー','時計','バッグ','財布・小物','お酒','切手','古銭・記念硬貨','服','カメラ']
rows.sort(key=lambda r:CATS.index(r[0]) if r[0] in CATS else 99)
cards=''.join(f'<div class="pc" data-cat="{c}"><img src="{CDN}{quote(i)}" alt="{n}" width="335" height="230" loading="lazy" referrerpolicy="no-referrer"><div class="pb"><span class="tag">{c}</span><span class="nm">{n}</span><span class="lb">買取参考価格</span><span class="pr">{p}<small>円</small></span></div></div>' for c,n,p,i in rows)
present=[c for c in CATS if any(r[0]==c for r in rows)]
btns='<button class="fb on" data-f="all">すべて（'+str(len(rows))+'）</button>'+''.join(f'<button class="fb" data-f="{c}">{c}（{sum(1 for r in rows if r[0]==c)}）</button>' for c in present)
pb=f"""<style>
.wrap{{max-width:1120px!important}}
.fbs{{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 20px}}
.fb{{font:inherit;font-size:15px;font-weight:700;min-height:44px;padding:0 14px;border-radius:999px;border:1px solid #232C7A;background:#fff;color:#232C7A;cursor:pointer}}
.fb.on{{background:#232C7A;color:#fff}}
.pg{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px}} @media (max-width:600px){{.pg{{grid-template-columns:1fr 1fr;gap:10px}} .pr{{font-size:20px}} .nm{{font-size:14px}} .fb{{min-height:40px;font-size:14px;padding:0 12px}}}}
.pc{{background:#fff;border:1px solid #DDE0EA;border-radius:10px;overflow:hidden;display:flex;flex-direction:column}}
.pc img{{width:100%;height:auto;aspect-ratio:335/230;object-fit:contain;background:#fff;display:block;border-bottom:1px solid #EEF0F7}}
.pb{{padding:12px 14px 14px;display:flex;flex-direction:column;gap:4px;flex:1}}
.tag{{align-self:flex-start;background:#EEF0F7;color:#232C7A;font-size:12px;font-weight:700;padding:1px 9px;border-radius:999px}}
.nm{{font-size:15px;font-weight:700;line-height:1.5;flex:1}}
.lb{{font-size:12px;color:#5E6272}}
.pr{{font-size:24px;font-weight:700;color:#C8102E;line-height:1.2}} .pr small{{font-size:14px;margin-left:2px}}
</style>
<h1>買取参考価格</h1>
<p class="meta" style="margin:0 0 6px">全国の買取大吉でのお買取り例 {len(rows)}点（{PRICE_DATE}時点）</p>
<p style="margin:0 0 20px;font-size:16px">金・ジュエリー・時計・バッグなど、買取大吉の公式サイトに載っている買取参考価格です。同じお品物でも、状態や付属品、その日の相場で金額は変わります。<strong>「うちのはいくら？」は、法隆寺店で無料査定</strong>してください。</p>
<div class="fbs" role="group" aria-label="カテゴリで絞り込む">{btns}</div>
<div class="pg" id="pg">{cards}</div>
<p class="meta" style="margin-top:20px">※出典：買取大吉 公式サイト掲載の買取参考価格・写真（{PRICE_DATE}時点）。買取金額を保証するものではありません。<br>※お品物の状態・付属品の有無・その日の相場によって金額は変わります。金・プラチナは毎日の相場で価格が変わります。</p>
<script>
document.querySelectorAll('.fb').forEach(b=>b.addEventListener('click',()=>{{document.querySelectorAll('.fb').forEach(x=>x.classList.toggle('on',x===b));const f=b.dataset.f;document.querySelectorAll('.pc').forEach(c=>c.style.display=(f==='all'||c.dataset.cat===f)?'':'none');}}));
</script>
{{STORECARD}}"""
pb=pb.replace('{STORECARD}',STORECARD)
os.makedirs(f'{ROOT}/price',exist_ok=True)
open(f'{ROOT}/price/index.html','w',encoding='utf-8').write(page('買取参考価格 100点｜買取大吉 法隆寺店（斑鳩町）','金・ジュエリー・時計・バッグ・切手など、買取大吉の買取参考価格を写真付きで紹介。斑鳩町・法隆寺の買取大吉 法隆寺店では査定無料・予約不要です。',f'{SITE}/price/',pb,ogtype='website'))

# ===== LPの「お買取り実績・店長ブログ」欄（index.html の AUTO:LATEST の間を書き換え）=====
import re as _re
def short(t):
    t=t.split('｜')[0]
    return _re.sub(r'をお買取りしました$','',t)
def row(q,label):
    return f'<a href="/blog/{q["slug"]}/" class="lt-row"><img src="{q["img"]}" alt="" width="1400" height="1050" loading="lazy"><span class="lt-tx"><span class="lt-cat">{label}</span><span class="lt-ti">{q["_t"]}</span></span></a>'
res=[dict(q,_t=short(q['title'])) for q in POSTS if q['cat']=='お買取り実績']
col=[dict(q,_t=q['title']) for q in POSTS if q['cat']!='お買取り実績']
L=f"""<!-- AUTO:LATEST -->
<section id="results" style="background: #F5F6FA; padding: 72px 24px">
<style>
#results .lt-grid{{display:flex;flex-wrap:wrap;gap:24px}}
#results .lt-col{{flex:1 1 420px;min-width:0;background:#fff;border:1px solid #DDE0EA;border-radius:12px;padding:20px 20px 16px;display:flex;flex-direction:column}}
#results .lt-h{{margin:0 0 4px;font-size:21px;line-height:1.5;border-left:5px solid #C9A54C;padding-left:12px}}
#results .lt-row{{display:flex;gap:14px;align-items:center;padding:12px 0;border-bottom:1px solid #EEF0F7;text-decoration:none;color:#1A1A1A}}
#results .lt-row img{{flex:0 0 96px;width:96px;height:72px;object-fit:cover;border-radius:6px;display:block}}
#results .lt-tx{{display:flex;flex-direction:column;gap:2px;min-width:0}}
#results .lt-cat{{font-size:13px;color:#5E6272}}
#results .lt-ti{{font-size:16px;font-weight:700;line-height:1.5}}
#results .lt-more{{align-self:center;margin-top:14px;background:#232C7A;color:#fff;text-decoration:none;font-weight:700;padding:12px 24px;border-radius:8px;min-height:48px;box-sizing:border-box;display:inline-flex;align-items:center}}
</style>
<div style="max-width: 1120px; margin: 0 auto; display: flex; flex-direction: column; gap: 24px">
<div style="display: flex; flex-direction: column; gap: 8px; text-align: center">
<p style="margin: 0; font-size: 14px; color: #232C7A; font-weight: 700; letter-spacing: 0.16em">RESULTS &amp; BLOG</p>
<h2 style="margin: 0; font-size: 30px; line-height: 1.5">お買取り実績・店長ブログ</h2>
<p style="margin: 0; font-size: 15px; color: #3D4150">法隆寺店で実際にお買取りした品物と、売る前に知っておきたいことを書いています。</p>
</div>
<div class="lt-grid">
<div class="lt-col"><h3 class="lt-h">法隆寺店のお買取り実績</h3>{''.join(row(q,'お買取り実績') for q in res[:6])}<a class="lt-more" href="/blog/#results">実績をもっと見る（全{len(res)}件）</a></div>
<div id="blog" class="lt-col"><h3 class="lt-h">店長ブログ</h3>{''.join(row(q,q['cat']) for q in col[:6])}<a class="lt-more" href="/blog/#column">ブログをもっと見る（全{len(col)+1}件）</a></div>
</div>
<p style="margin: 0; font-size: 13px; color: #5E6272; text-align: center">※実績の写真は背景や明るさを調整しています。</p>
</div>
</section>
<!-- /AUTO:LATEST -->"""
ip=f'{ROOT}/index.html'; h=open(ip,encoding='utf-8').read()
h=_re.sub(r'<!-- AUTO:LATEST -->.*?<!-- /AUTO:LATEST -->',lambda m:L,h,flags=_re.S)
open(ip,'w',encoding='utf-8').write(h)

# ===== 品目別ページ（_tools/cats.py）=====
from cats import CATS
BYSLUG={q['slug']:q for q in POSTS}
DIRURL='https://www.google.com/maps/dir/?api=1&amp;destination=%E8%B2%B7%E5%8F%96%E5%A4%A7%E5%90%89%20%E6%B3%95%E9%9A%86%E5%AF%BA%E5%BA%97'
CATCSS="""<style>
.wrap{max-width:960px!important}
.lead{font-size:18px;line-height:1.9;margin:0 0 20px}
.cta2{display:flex;flex-wrap:wrap;gap:10px;margin:20px 0}
.cta2 a{flex:1 1 200px;min-height:56px;display:flex;flex-direction:column;align-items:center;justify-content:center;border-radius:10px;font-weight:700;text-decoration:none;font-size:17px;line-height:1.35;text-align:center;padding:6px 10px}
.cta2 a small{font-size:13px;font-weight:500}
.lst{margin:0;padding:0;list-style:none;display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:8px}
.lst li{background:#fff;border:1px solid #DDE0EA;border-radius:8px;padding:10px 14px 10px 36px;position:relative;font-size:16px}
.lst li:before{content:'✓';position:absolute;left:14px;color:#C9A54C;font-weight:700}
.pts{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px}
.pts div{background:#fff;border:1px solid #DDE0EA;border-radius:10px;padding:16px}
.pts b{display:block;color:#232C7A;font-size:17px;margin-bottom:4px}
.rs{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px}
.rs a{background:#fff;border:1px solid #DDE0EA;border-radius:10px;overflow:hidden;text-decoration:none;color:#1A1A1A;display:flex;flex-direction:column}
.rs img{width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;display:block}
.rs span{padding:8px 10px;font-size:14px;font-weight:700;line-height:1.5}
.pg2{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px}
.pg2 div{background:#fff;border:1px solid #DDE0EA;border-radius:10px;overflow:hidden}
.pg2 img{width:100%;height:auto;aspect-ratio:335/230;object-fit:contain;background:#fff;display:block}
.pg2 p{margin:0;padding:8px 10px;font-size:14px;line-height:1.5}
.pg2 b{display:block;color:#C8102E;font-size:19px}
details.fq{background:#fff;border:1px solid #DDE0EA;border-radius:10px;padding:14px 16px;margin-bottom:8px}
details.fq summary{font-weight:700;cursor:pointer;font-size:17px}
.oc{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}.oc a{background:#fff;border:1px solid #232C7A;border-radius:999px;padding:8px 14px;text-decoration:none;font-weight:700;font-size:15px}
@media (max-width:600px){.rs,.pg2{grid-template-columns:1fr 1fr}.lead{font-size:17px}}
</style>"""
def cta2(c30=True):
    sub='時計・アクセサリー30%UP（11/30まで）' if c30 else '対象や条件はお電話で確認できます'
    return f'<div class="cta2"><a href="/#coupon" style="background:#C8102E;color:#fff">WEBクーポンを見る<small>{sub}</small></a><a href="tel:0677776590" style="background:{GOLD};color:#1A1A1A">電話で相談する<small>06-7777-6590・10〜19時</small></a><a href="https://line.me/ti/p/CZCmVd4SQf" style="background:#06C755;color:#0B2A16">LINEで写真査定<small>撮って送るだけ・無料</small></a></div>'
for c in CATS:
    rs=[BYSLUG[s] for s in c['results'] if s in BYSLUG]
    rhtml=''.join(f'<a href="/blog/{q["slug"]}/"><img src="{q["img"]}" alt="{q.get("alt","")}" width="1400" height="1050" loading="lazy"><span>{q["title"].split("｜")[0].replace("をお買取りしました","")}</span></a>' for q in rs)
    prs=[r for r in rows if r[0] in c['price']]
    prs=sorted(prs,key=lambda r:0 if any(k in r[1] for k in c.get('pricefirst',[])) else 1)[:8]
    phtml=''.join(f'<div><img src="{CDN}{quote(i)}" alt="{n}" width="335" height="230" loading="lazy" referrerpolicy="no-referrer"><p>{n}<b>{pz}円</b></p></div>' for ca,n,pz,i in prs)
    cols=[BYSLUG[s] for s in c['cols'] if s in BYSLUG]
    colhtml=('<h2>あわせて読みたい</h2><ul>'+''.join(f'<li><a href="/blog/{q["slug"]}/">{q["title"]}</a></li>' for q in cols)+'</ul>') if cols else ''
    others=''.join(f'<a href="/{o["slug"]}/">{o["name"]}</a>' for o in CATS if o['slug']!=c['slug'])
    b=f"""{CATCSS}
<nav class="meta" aria-label="パンくず"><a href="/">買取大吉 法隆寺店</a> ＞ {c.get('crumb',c['name']+'の買取')}</nav>
<h1>{c['h1']}</h1>
<p class="lead">{c['lead']}</p>
<p style="margin:-6px 0 14px;font-weight:700;color:#232C7A">査定だけでも大歓迎です。金額を聞いてから、売るかどうかお決めいただけます。</p>
<p class="meta" style="margin:-8px 0 0">査定無料・予約不要・半個室・無料駐車場10台以上・年中無休 10:00〜19:00（最終受付19:00）</p>
{cta2(c['c30'])}
<h2>こんな品物をお買取りしています</h2>
<ul class="lst">{''.join(f'<li>{x}</li>' for x in c['items'])}</ul>
<h2>{c['more'][0]}</h2>
<p>{c['more'][1]}</p>
<h2>査定で見るところ</h2>
<div class="pts">{''.join(f'<div><b>{t}</b>{d}</div>' for t,d in c['points'])}</div>
{f'<h2>法隆寺店のお買取り実績</h2><p class="meta" style="margin:0 0 10px">当店で実際にお買取りした品物です（写真は背景や明るさを調整しています）。</p><div class="rs">{rhtml}</div>' if rs else ''}
{f'<h2>買取参考価格（全国の買取大吉の例）</h2><p class="meta" style="margin:0 0 10px">買取大吉 公式サイト掲載の参考価格・写真（{PRICE_DATE}時点）。法隆寺店の買取金額を保証するものではありません。状態・付属品・その日の相場で変わります。</p><div class="pg2">{phtml}</div><p style="margin:10px 0 0"><a href="/price/">参考価格をもっと見る（100点）→</a></p>' if prs else ''}
<h2>よくあるご質問</h2>
{''.join(f'<details class="fq"><summary>Q. {q}</summary><p style="margin:10px 0 0">A. {a}</p></details>' for q,a in c['faq'])}
<details class="fq"><summary>Q. 何を持って行けばいいですか？</summary><p style="margin:10px 0 0">A. お品物と、運転免許証やマイナンバーカードなどの本人確認書類をお持ちください。</p></details>
{colhtml}
<h2>お店の場所</h2>
<p style="margin:0">奈良県生駒郡斑鳩町興留5-1-35サンメゾン法隆寺。法隆寺駅から徒歩7分、万代 法隆寺店の向かい、chocoZAPの隣です。無料駐車場は建物の裏にあります（10台以上・他の施設と共用）。</p>
<p style="margin:8px 0 0"><a href="{DIRURL}">今いる場所からの道順を見る</a> ／ <a href="/#access">道順の図を見る</a></p>
<p class="meta" style="margin:8px 0 0">斑鳩町のほか、王寺町・安堵町・三郷町・平群町・河合町・大和郡山市からも、お車で来やすい場所です。</p>
{cta2(c['c30'])}
<h2>ほかの品物の買取</h2>
<div class="oc">{others}<a href="/price/">参考価格100点</a></div>
{STORECARD}"""
    faqld={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in c['faq']]}
    bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"買取大吉 法隆寺店","item":SITE+"/"},{"@type":"ListItem","position":2,"name":c.get('crumb',c['name']+"の買取"),"item":f"{SITE}/{c['slug']}/"}]}
    ld='<script type="application/ld+json">'+json.dumps(faqld,ensure_ascii=False)+'</script><script type="application/ld+json">'+json.dumps(bc,ensure_ascii=False)+'</script>'
    os.makedirs(f"{ROOT}/{c['slug']}",exist_ok=True)
    open(f"{ROOT}/{c['slug']}/index.html",'w',encoding='utf-8').write(page(c['title'],c['desc'],f"{SITE}/{c['slug']}/",b,ld,ogtype='website'))
urls=[('/',today),('/price/',today)]+[(f"/{c['slug']}/",today) for c in CATS]+[('/blog/',today)]+[(f"/blog/{q['slug']}/",q['date']) for q in allp]
open(f'{ROOT}/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{SITE}{u}</loc><lastmod>{d}</lastmod></url>\n' for u,d in urls)+'</urlset>\n')
print('built',len(POSTS),'posts')
