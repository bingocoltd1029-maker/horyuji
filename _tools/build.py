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
<a href="/blog/" style="font-weight:700;font-size:15px">ブログ一覧</a>
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
<a href="https://maps.app.goo.gl/qmBYRcdpAQeCupgSA" style="flex:0 0 72px;background:#232C7A;color:#fff">地図</a>
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
today=datetime.date.today().isoformat()
for p in POSTS:
    p.setdefault('date',today)
    d=p['date']
    body=f'''<article>
<p class="meta">{d.replace('-','.')}　{p['cat']}</p>
<h1>{p['title']}</h1>
<img src="{p['img']}" alt="{p['alt']}" width="1400" height="1050" style="border-radius:10px;margin:16px 0">
{p['body']}
</article>
{STORECARD}'''
    ld=json.dumps({"@context":"https://schema.org","@type":"BlogPosting","headline":p['title'],"description":p['desc'],"datePublished":d,"dateModified":d,"image":SITE+p['img'].replace('.webp','.jpg'),"author":{"@type":"Person","name":"吉原 涼"},"publisher":{"@type":"Organization","name":"買取大吉 法隆寺店","logo":{"@type":"ImageObject","url":SITE+"/logo.png"}},"mainEntityOfPage":f"{SITE}/blog/{p['slug']}/"},ensure_ascii=False)
    os.makedirs(f"{ROOT}/blog/{p['slug']}",exist_ok=True)
    open(f"{ROOT}/blog/{p['slug']}/index.html",'w',encoding='utf-8').write(page(p['title']+'｜買取大吉 法隆寺店',p['desc'],f"{SITE}/blog/{p['slug']}/",body,f'<script type="application/ld+json">{ld}</script>'))
allp=POSTS+[OPEN]
items=''.join(f'''<a href="/blog/{q['slug']}/" class="card" style="display:flex;flex-wrap:wrap;gap:16px;text-decoration:none;color:#1A1A1A;padding:0;overflow:hidden;margin-bottom:16px">
<img src="{q['img']}" alt="" width="1400" height="1050" loading="lazy" style="flex:1 1 220px;min-width:0;height:160px;object-fit:cover">
<div style="flex:999 1 280px;padding:16px 20px"><p class="meta" style="margin:0">{q['date'].replace('-','.')}　{q['cat']}</p><p style="margin:4px 0 0;font-weight:700;font-size:18px;line-height:1.6">{q['title']}</p></div></a>''' for q in allp)
lb=f'<h1>店長ブログ</h1><p class="meta" style="margin-bottom:24px">斑鳩町・法隆寺の買取大吉 法隆寺店から、お買取り実績やお役立ち情報をお届けします。</p>{items}'
open(f'{ROOT}/blog/index.html','w',encoding='utf-8').write(page('店長ブログ｜買取大吉 法隆寺店（斑鳩町）','買取大吉 法隆寺店（奈良県斑鳩町）の店長ブログ。金・ブランド品・時計の買取のコツやお知らせを更新しています。',f'{SITE}/blog/',lb,ogtype='website'))

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
.pg{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px}}
.pc{{background:#fff;border:1px solid #DDE0EA;border-radius:10px;overflow:hidden;display:flex;flex-direction:column}}
.pc img{{width:100%;aspect-ratio:335/230;object-fit:contain;background:#fff;display:block;border-bottom:1px solid #EEF0F7}}
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
urls=[('/',today),('/price/',today),('/blog/',today)]+[(f"/blog/{q['slug']}/",q['date']) for q in allp]
open(f'{ROOT}/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{SITE}{u}</loc><lastmod>{d}</lastmod></url>\n' for u,d in urls)+'</urlset>\n')
print('built',len(POSTS),'posts')
