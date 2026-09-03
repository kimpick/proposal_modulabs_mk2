import pandas as pd
import json

excel_path = r'C:\Users\Admin\Downloads\ai-education-proposal\projects\삼성전자MX_추가교육제안\[모두의연구소] AI 기업교육 커리큘럼_초안 (3).xlsx'
xl = pd.ExcelFile(excel_path)
df_summary = pd.read_excel(xl, sheet_name='전체 커리큘럼').head(50)
df_summary = df_summary[df_summary['코드'].notna()]

results = []

for _, row in df_summary.iterrows():
    sheet_name = row['세부 코드']
    course_name = row['과정 명']
    target = row['권장 대상']
    duration = row['소요 시간']
    
    if pd.isna(sheet_name) or str(sheet_name).strip() not in xl.sheet_names:
        continue
        
    df_course = pd.read_excel(xl, sheet_name=str(sheet_name).strip())
    
    # We will just append the raw df_course content or try to parse
    # Let's extract everything from df_course into a simpler text format to find '주요 도구', '목표', '핵심 내용'
    sheet_data = df_course.to_dict(orient='records')
    results.append({
        '세부 코드': sheet_name,
        '과정 명': course_name,
        '권장 대상': target,
        '소요 시간': duration,
        'sheet_data': sheet_data[:15] # top 15 rows usually enough
    })

with open('courses_data.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
