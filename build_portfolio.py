from pathlib import Path
import shutil

src = Path(r"C:\Users\jinhy\.openclaw\workspace\portfolio_src\ㅁㄴㅁ")
out = Path(r"C:\Users\jinhy\.openclaw\workspace\portfolio_web")
assets = out / "assets"
assets.mkdir(parents=True, exist_ok=True)

# collect
pdfs = list(src.rglob("*.pdf"))
all_jpg = list(src.rglob("*.jpg"))

cert_imgs = [p for p in all_jpg if "매출에대한" in str(p)]
review_imgs = [p for p in all_jpg if p not in cert_imgs]

copied = {"pdf": [], "cert": [], "review": []}

for i,p in enumerate(pdfs,1):
    dst = assets / f"resume_{i}.pdf"
    shutil.copy2(p, dst)
    copied["pdf"].append(dst.name)

for i,p in enumerate(sorted(cert_imgs),1):
    dst = assets / f"cert_{i}.jpg"
    shutil.copy2(p, dst)
    copied["cert"].append(dst.name)

for i,p in enumerate(sorted(review_imgs),1):
    dst = assets / f"review_{i:02d}.jpg"
    shutil.copy2(p, dst)
    copied["review"].append(dst.name)

resume_link = copied['pdf'][0] if copied['pdf'] else ''
cert_html = "\n".join([f'<img src="assets/{n}" alt="상장 {idx}">' for idx,n in enumerate(copied['cert'],1)])
review_html = "\n".join([f'<img src="assets/{n}" alt="회원 후기 {idx}">' for idx,n in enumerate(copied['review'],1)])

html = f"""<!doctype html>
<html lang=\"ko\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>신성훈 트레이너 | 포트폴리오</title>
  <style>
    :root {{ --bg:#0b1020; --card:#141a2e; --txt:#eef2ff; --muted:#aab3d6; --acc:#6ea8fe; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Noto Sans KR',sans-serif; background:linear-gradient(180deg,#0b1020,#090d1b); color:var(--txt); }}
    .wrap {{ max-width:1100px; margin:0 auto; padding:24px; }}
    .hero {{ background:var(--card); border-radius:18px; padding:24px; margin-bottom:18px; }}
    h1,h2 {{ margin:0 0 10px; }}
    p {{ color:var(--muted); margin:8px 0; line-height:1.6; }}
    .btn {{ display:inline-block; background:var(--acc); color:#081028; text-decoration:none; font-weight:700; padding:10px 14px; border-radius:12px; margin-top:8px; }}
    .grid {{ display:grid; gap:12px; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); }}
    .card {{ background:var(--card); border-radius:16px; padding:14px; }}
    img {{ width:100%; height:100%; object-fit:cover; border-radius:12px; display:block; }}
    .cert-grid img {{ aspect-ratio: 4/3; }}
    .review-grid img {{ aspect-ratio: 3/4; }}
    footer {{ color:var(--muted); text-align:center; padding:20px 0 10px; font-size:14px; }}
  </style>
</head>
<body>
  <div class=\"wrap\">
    <section class=\"hero\">
      <h1>신성훈 트레이너 포트폴리오</h1>
      <p>회원 바디프로필/리뷰, 매출 관련 상장 자료, 이력서 파일을 기반으로 구성한 반응형 웹페이지입니다.</p>
      <p>모바일/태블릿/PC에서 자동으로 레이아웃이 맞춰집니다.</p>
      {f'<a class="btn" href="assets/{resume_link}" target="_blank" rel="noopener">이력서(PDF) 보기</a>' if resume_link else ''}
    </section>

    <section class=\"card\">
      <h2>자격/성과 자료</h2>
      <p>매출 관련 상장 자료</p>
      <div class=\"grid cert-grid\">{cert_html}</div>
    </section>

    <section class=\"card\" style=\"margin-top:14px;\">
      <h2>회원 후기 · 바디프로필</h2>
      <p>회원 변화 사례 및 후기 이미지</p>
      <div class=\"grid review-grid\">{review_html}</div>
    </section>

    <footer>© 신성훈 트레이너 포트폴리오</footer>
  </div>
</body>
</html>
"""

(out / "index.html").write_text(html, encoding="utf-8")
print("built", out / "index.html")
print("resume", len(copied['pdf']), "cert", len(copied['cert']), "review", len(copied['review']))
