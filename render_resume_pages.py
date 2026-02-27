from pathlib import Path
import pypdfium2 as pdfium

pdf_path = Path(r"C:\Users\jinhy\.openclaw\workspace\hooney\assets\resume_1.pdf")
out_dir = Path(r"C:\Users\jinhy\.openclaw\workspace\hooney\assets")

pdf = pdfium.PdfDocument(str(pdf_path))
for i in range(len(pdf)):
    page = pdf[i]
    bitmap = page.render(scale=2.2)
    img = bitmap.to_pil()
    out = out_dir / f"resume_page_{i+1}.jpg"
    img.save(out, format="JPEG", quality=92)
    print(out)
