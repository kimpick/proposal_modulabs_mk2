import os
import sys
import subprocess

def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        if hasattr(pip, 'main'):
            pip.main(['install', package])
        else:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
    finally:
        globals()[package] = importlib.import_module(package)

install_and_import('markdown')
import markdown

ROOT = r"C:\Users\Admin\Downloads\ai-education-proposal"
PROJECT = os.path.join(ROOT, "projects", "기웅정보통신")

# 1. run build.py to generate proposal_render.html
subprocess.run([sys.executable, os.path.join(ROOT, 'build.py'), '기웅정보통신/컨설팅_제안서'], check=True)

BASE_HTML_PATH = os.path.join(PROJECT, "컨설팅_제안서", "proposal_render.html")
with open(BASE_HTML_PATH, "r", encoding="utf-8") as f:
    base_html = f.read()

MD_PATH = os.path.join(PROJECT, "상세_운영안.md")
with open(MD_PATH, "r", encoding="utf-8") as f:
    text = f.read()
    
# Convert markdown
html_md = markdown.markdown(text, extensions=['tables'])

md_style = """
<style>
.md-content { margin-top: 30px; }
.md-content h1 { color: #1a1a1a; border-bottom: 2px solid #ea5a39; padding-bottom: 10px; margin-bottom: 30px; font-size:28px; }
.md-content h2 { color: #ea5a39; margin-top: 40px; font-size:20px; }
.md-content h3 { color: #333; margin-top: 25px; border-left: 4px solid #ea5a39; padding-left: 10px; font-size:16px;}
.md-content table { width: 100%; border-collapse: collapse; margin-top: 20px; font-size:13px; }
.md-content th, .md-content td { border: 1px solid #ddd; padding: 12px; text-align: left; }
.md-content th { background-color: #f7f9fc; color: #333; font-weight:600; text-align:center; }
.md-content td { color: #555; }
.md-content ul { padding-left: 20px; }
.md-content li { margin-bottom: 5px; color:#444; line-height:1.6;font-size:14px;}
.footer { margin-top: 15px !important; padding-top: 15px !important; }
</style>
<div class="page-break"></div>
<div class="md-content">
""" + html_md + "</div>"

# Inject the md_content BEFORE the footer
footer_tag = '<div class="footer">'
if footer_tag in base_html:
    combined_html = base_html.replace(footer_tag, md_style + "\n" + footer_tag)
else:
    combined_html = base_html.replace('</body>', md_style + "\n</body>")

COMBINED_HTML_PATH = os.path.join(PROJECT, "컨설팅_제안서", "combined_render.html")
FINAL_PDF = os.path.join(PROJECT, "컨설팅_제안서", "[모두의연구소]기웅정보통신 컨설팅_제안서_최종.pdf")

with open(COMBINED_HTML_PATH, "w", encoding="utf-8") as f:
    f.write(combined_html)

# Convert to PDF
edge_candidates = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "msedge",
]
cmd_edge = None
for candidate in edge_candidates:
    if candidate == "msedge" or os.path.exists(candidate):
        cmd_edge = candidate
        break

cmd = [
    cmd_edge,
    "--headless",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    "--no-pdf-header-footer",
    f"--print-to-pdf={os.path.abspath(FINAL_PDF)}",
    f"file:///{os.path.abspath(COMBINED_HTML_PATH)}",
]

subprocess.run(cmd, check=True)
print(f"🎉 PDF 렌더링 완료! 푸터가 마지막 페이지로 이동되었습니다: {FINAL_PDF}")
