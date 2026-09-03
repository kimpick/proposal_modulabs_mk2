import pandas as pd
import json

excel_path = '[모두의연구소] AI 기업교육 커리큘럼_초안 (3).xlsx'
xl = pd.ExcelFile(excel_path)
df_summary = pd.read_excel(xl, sheet_name='전체 커리큘럼').head(40)
df_summary = df_summary[df_summary['코드'].notna()]

results = {}
for _, row in df_summary.iterrows():
    sheet_name = str(row['세부 코드']).strip()
    course_name = str(row['과정 명']).strip()
    if sheet_name in xl.sheet_names:
        df_course = pd.read_excel(xl, sheet_name=sheet_name)
        
        # Collect all texts in the sheet to find '목표' and '핵심 내용' manually
        text_data = []
        for _, c_row in df_course.iterrows():
            text_data.append([str(x) for x in c_row.values if not pd.isna(x)])
            
        results[sheet_name] = {'course': course_name, 'data': text_data[:10]} # top 10 rows

with open('debug2.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
