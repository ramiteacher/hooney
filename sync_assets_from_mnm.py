from pathlib import Path
import shutil, zipfile

src = Path(r"C:\Users\jinhy\Desktop\ㅁㄴㅁ")
work = Path(r"C:\Users\jinhy\.openclaw\workspace\hooney\_build_src")
assets = Path(r"C:\Users\jinhy\.openclaw\workspace\hooney\assets")

if work.exists():
    shutil.rmtree(work)
work.mkdir(parents=True, exist_ok=True)
assets.mkdir(parents=True, exist_ok=True)

# copy source folder snapshot
for p in src.rglob('*'):
    rel = p.relative_to(src)
    dst = work / rel
    if p.is_dir():
        dst.mkdir(parents=True, exist_ok=True)
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dst)

# extract zips recursively
for _ in range(3):
    for z in list(work.rglob('*.zip')):
        out = z.with_suffix('')
        out.mkdir(parents=True, exist_ok=True)
        try:
            with zipfile.ZipFile(z) as f:
                f.extractall(out)
        except Exception:
            pass

# clear public assets
for p in assets.glob('*'):
    if p.is_file():
        p.unlink()

pdfs = list(work.rglob('*.pdf'))
imgs = [p for p in work.rglob('*') if p.suffix.lower() in {'.jpg','.jpeg','.png','.webp'}]

cert_keyword = ['자격증', '자격', 'certificate', 'cert']
award_keyword = ['상장', '매출']

certs = []
awards = []
reviews = []

for p in imgs:
    s = str(p)
    if any(k in s for k in cert_keyword):
        certs.append(p)
    elif any(k in s for k in award_keyword):
        awards.append(p)
    else:
        reviews.append(p)

copied = {'resume':[], 'cert':[], 'award':[], 'review':[]}

for i,p in enumerate(sorted(pdfs),1):
    n=f'resume_{i}.pdf'; shutil.copy2(p, assets/n); copied['resume'].append(n)
for i,p in enumerate(sorted(certs),1):
    n=f'cert_{i:02d}{p.suffix.lower()}'; shutil.copy2(p, assets/n); copied['cert'].append(n)
for i,p in enumerate(sorted(awards),1):
    n=f'award_{i:02d}{p.suffix.lower()}'; shutil.copy2(p, assets/n); copied['award'].append(n)
for i,p in enumerate(sorted(reviews),1):
    n=f'review_{i:02d}{p.suffix.lower()}'; shutil.copy2(p, assets/n); copied['review'].append(n)

print(copied)
