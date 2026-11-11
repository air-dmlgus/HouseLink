"""HouseLink sample website. Run with: python app.py"""
from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

from recommender import FEATURES, PROFILES, cluster_areas, load_areas, recommend

PAGE = r"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>HouseLink | 주거지 추천 데모</title>
<style>
:root{font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#172b3c;background:#f3f7fa}
*{box-sizing:border-box}body{margin:0}header{background:linear-gradient(120deg,#102f4e,#087e8b);color:white;padding:55px max(24px,calc((100vw - 1000px)/2))}
header .eyebrow{font-size:12px;font-weight:800;letter-spacing:.2em;color:#a8e5e6}
h1{font-size:clamp(34px,6vw,56px);margin:14px 0 12px}header p{line-height:1.8;max-width:610px;color:#ddf0f4}
main{max-width:1000px;margin:30px auto;padding:0 20px 50px}.notice{background:#fff8e7;border:1px solid #f1dba1;color:#66521b;border-radius:12px;padding:14px 18px;line-height:1.6;font-size:14px}
.panel{background:#fff;border:1px solid #dfe8ef;border-radius:18px;padding:24px;margin-top:20px;box-shadow:0 5px 20px #183c5710}
h2{font-size:22px;margin:0 0 8px}.muted{color:#6a7d8b;font-size:14px}.options{display:flex;gap:10px;flex-wrap:wrap;margin:22px 0}
button{border:1px solid #ccdae3;background:#f8fbfd;border-radius:99px;padding:11px 18px;cursor:pointer;font-size:14px;font-weight:700;color:#204359}
button.active{background:#106d7e;color:white;border-color:#106d7e}button:hover{border-color:#106d7e}
.results{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:14px;margin-top:22px}
.place{border:1px solid #e0e9ef;border-radius:14px;padding:20px;background:#fff}
.place:first-child{border-color:#42a5a0;background:#f4fdfb}
.rank{color:#188f95;font-size:12px;font-weight:800}.place h3{margin:8px 0 5px;font-size:20px}
.score{font-weight:800;color:#10546c;font-size:24px;margin:0 0 14px}
.metric{display:grid;grid-template-columns:52px 1fr 38px;gap:8px;align-items:center;margin:9px 0;font-size:13px;color:#567}
.track{background:#e7eff3;height:8px;border-radius:99px;overflow:hidden}
.fill{background:#25a5a4;height:100%;border-radius:99px}.cluster{margin-top:15px;font-size:12px;color:#6a7d8b}
footer{color:#71828c;text-align:center;padding:20px;font-size:13px}
</style>
</head>
<body>
<header><div class="eyebrow">MICROSOFT AI SCHOOL · PORTFOLIO RECONSTRUCTION</div>
<h1>HouseLink</h1>
<p>어떤 동네가 나에게 맞을까? 치안·교육·의료 지표를 선호도에 맞게 반영해 지역별 비교 결과를 보여주는 주거지 추천 데모입니다.</p>
</header>
<main>
<section class="notice"><strong>시연용 가상 데이터</strong> — 아래 지역명과 점수는 임의로 만든 예시입니다. 실제 서울 지역의 치안·교육·의료 수준을 나타내지 않으며 거주지 결정에 사용하면 안 됩니다.</section>
<section class="panel">
<h2>무엇을 더 중요하게 생각하나요?</h2>
<div class="muted">선호도에 따라 분야별 가중치를 달리해 추천 순위를 계산합니다.</div>
<div class="options" id="options">
<button data-profile="balanced" class="active">균형 있게</button>
<button data-profile="safety">치안 중심</button>
<button data-profile="education">교육 중심</button>
<button data-profile="medical">의료 중심</button>
</div>
<div id="status" class="muted" role="status">데이터를 불러오는 중입니다.</div>
<div id="results" class="results"></div>
</section>
<section class="panel">
<h2>추천 방식</h2>
<p class="muted">가중합 점수로 지역을 정렬하고, K-Means 방식으로 지표가 비슷한 지역을 3개 군집으로 묶습니다. 군집 번호는 우열을 뜻하지 않습니다.</p>
</section>
</main>
<footer>HouseLink · 학습용 재구현 데모 · 원본 팀 프로젝트와 별개</footer>
<script>
const captions={safety:"치안",education:"교육",medical:"의료"};
const results=document.getElementById("results");
const status=document.getElementById("status");
function el(tag,className,text){const node=document.createElement(tag);if(className)node.className=className;if(text!==undefined)node.textContent=text;return node;}
async function load(profile){
 document.querySelectorAll("button[data-profile]").forEach(btn=>btn.classList.toggle("active",btn.dataset.profile===profile));
 status.textContent="추천 결과를 계산하는 중입니다.";
 try{
  const response=await fetch("/api/recommend?profile="+encodeURIComponent(profile));
  const data=await response.json();
  if(!response.ok)throw new Error(data.error||"서버 오류");
  results.replaceChildren();
  data.results.forEach((item,index)=>{
   const card=el("article","place");
   card.append(el("div","rank","TOP "+(index+1)),el("h3","",item.district),el("p","score",item.score.toFixed(1)+"점"));
   ["safety","education","medical"].forEach(key=>{
    const metric=el("div","metric");
    const track=el("div","track");const fill=el("div","fill");
    fill.style.width=item[key]+"%";track.append(fill);
    metric.append(el("span","",captions[key]),track,el("strong","",String(item[key])));
    card.append(metric);
   });
   card.append(el("div","cluster","유사 특성 군집 "+item.cluster+" · 예시 데이터"));
   results.append(card);
  });
  status.textContent=data.results.length+"개 가상 지역의 비교 결과";
 }catch(error){results.replaceChildren();status.textContent="오류: "+error.message;}
}
document.querySelectorAll("button[data-profile]").forEach(btn=>btn.addEventListener("click",()=>load(btn.dataset.profile)));
load("balanced");
</script>
</body></html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        route = urlsplit(self.path)
        if route.path == "/":
            payload = PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
        elif route.path == "/api/recommend":
            profile = parse_qs(route.query).get("profile", ["balanced"])[0]
            try:
                areas = load_areas()
                labels = cluster_areas(areas, min(3, len(areas)))
                label_map = {area["district"]: labels[i] + 1 for i, area in enumerate(areas)}
                rows = recommend(areas, profile)
                for row in rows:
                    row["cluster"] = label_map[row["district"]]
                payload = json.dumps({"profile": profile, "results": rows}, ensure_ascii=False).encode("utf-8")
                self.send_response(200)
            except (ValueError, KeyError) as error:
                payload = json.dumps({"error": str(error)}, ensure_ascii=False).encode("utf-8")
                self.send_response(400)
            self.send_header("Content-Type", "application/json; charset=utf-8")
        else:
            payload = b"Not found"
            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    with ThreadingHTTPServer(("127.0.0.1", port), Handler) as server:
        print(f"HouseLink demo: http://127.0.0.1:{port}")
        server.serve_forever()
