# 予約記事をまとめて、11/27から1日1本ずつ日付をつける（build.py が今日までの分だけ公開する）
import datetime
from queue1 import Q as Q1
from queue2 import Q as Q2
from queue3 import Q as Q3
from queue4 import Q as Q4
_all=Q1+Q2+Q3+Q4
# 年末年始の記事は12/22ごろに出す
_n=[q for q in _all if q['slug']=='nenmatsu-nenshi'][0]; _all.remove(_n); _all.insert(25,_n)
START=datetime.date(2026,11,27)
POSTS=[]
for i,q in enumerate(_all):
    q=dict(q); q['date']=(START+datetime.timedelta(days=i)).isoformat(); POSTS.append(q)
