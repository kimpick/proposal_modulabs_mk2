import pandas as pd
import json
import os

excel_path = next(f for f in os.listdir('.') if os.path.isfile(f) and os.path.getsize(f) == 2362770)

xl = pd.ExcelFile(excel_path)
df_summary = pd.read_excel(xl, sheet_name='전체 커리큘럼').head(50)
df_summary = df_summary[df_summary['코드'].notna()]

results = {}
for _, row in df_summary.iterrows():
    sheet_name = str(row['세부 코드']).strip()
    course_name = str(row['과정 명']).strip()
    if sheet_name in xl.sheet_names:
        df_course = pd.read_excel(xl, sheet_name=sheet_name)
        text_data = []
        for _, c_row in df_course.iterrows():
            vals = [str(x) for x in c_row.values if not pd.isna(x) and str(x) != 'nan']
            if vals:
                text_data.append(vals)
        
        # If the sheet is already in results, just append the course name to show mapping issue
        if sheet_name in results:
            results[sheet_name]['mapped_courses'].append(course_name)
        else:
            results[sheet_name] = {
                'mapped_courses': [course_name], 
                'data': text_data[:15]
            }

with open('debug3.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
