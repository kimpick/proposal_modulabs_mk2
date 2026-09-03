import pandas as pd
import json

excel_path = r'C:\Users\Admin\Downloads\ai-education-proposal\projects\삼성전자MX_추가교육제안\[모두의연구소] AI 기업교육 커리큘럼_초안 (3).xlsx'
xl = pd.ExcelFile(excel_path)
df_summary = pd.read_excel(xl, sheet_name='전체 커리큘럼').head(40)
df_summary = df_summary[df_summary['코드'].notna()]

results = {}
for _, row in df_summary.iterrows():
    sheet_name = str(row['세부 코드']).strip()
    course_name = str(row['과정 명']).strip()
    if sheet_name in xl.sheet_names:
        df_course = pd.read_excel(xl, sheet_name=sheet_name)
        # Find intro row
        intro = ""
        for _, c_row in df_course.iterrows():
            row_str = " ".join([str(x) for x in c_row.values])
            if '연구 목적에 특화된 RAG' in row_str or '선형 회귀' in row_str or 'Streamlit' in row_str or 'AI 기반 연구 데이터 자동화' in row_str:
                intro += row_str + "\n"
        results[course_name] = {'sheet': sheet_name, 'matched': intro[:200]}

with open('debug_mismatch.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
