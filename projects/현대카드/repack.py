import os, zipfile

base = 'C:/Users/Admin/Downloads/ai-education-proposal/projects/현대카드'
unpacked_dir = os.path.join(base, 'unpacked_draft')
output_path = os.path.join(base, '현대카드_커머셜_2026_팀세미나_제안서_2차_Codex워크샵.docx')

with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
    for root, dirs, files in os.walk(unpacked_dir):
        for file in files:
            if file.endswith('_pretty.xml'):
                continue
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, unpacked_dir)
            zout.write(file_path, arcname)

print('Created:', output_path)
print('Size:', os.path.getsize(output_path))
