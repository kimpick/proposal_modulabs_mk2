import json

with open(r'C:\Users\Admin\Downloads\ai-education-proposal\projects\인천대학교\populate_sheets.gs', 'r', encoding='utf-8') as f:
    content = f.read()

# Use JSON encoding for safe JS string
js_content = json.dumps(content)

js_code = f"monaco.editor.getModels()[0].setValue({js_content});"

with open(r'C:\Users\Admin\Downloads\ai-education-proposal\projects\인천대학교\set_editor.js', 'w', encoding='utf-8') as f:
    f.write(js_code)

print('JS file written successfully, length:', len(js_code))
