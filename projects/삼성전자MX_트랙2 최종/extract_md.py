import pandas as pd

excel_path = r'C:\Users\Admin\Downloads\ai-education-proposal\projects\삼성전자MX_추가교육제안\[모두의연구소] AI 기업교육 커리큘럼_초안 (3).xlsx'
xl = pd.ExcelFile(excel_path)
df_summary = pd.read_excel(xl, sheet_name='전체 커리큘럼').head(40) # Only process first 40 rows or so
df_summary = df_summary[df_summary['코드'].notna()]

md_content = "# AI 기업교육 커리큘럼 소개\n\n"
md_content += "| 교육명 | 대상 | 주요 도구 | 목표 | 핵심 내용 | 소요 시간 |\n"
md_content += "|---|---|---|---|---|---|\n"

for _, row in df_summary.iterrows():
    sheet_name = row['세부 코드']
    course_name = row['과정 명']
    target = row['권장 대상']
    duration = row['소요 시간']
    
    if pd.isna(sheet_name) or str(sheet_name).strip() not in xl.sheet_names:
        continue
        
    df_course = pd.read_excel(xl, sheet_name=str(sheet_name).strip())
    
    # We will search the first two columns for keywords
    tools = ""
    goal = ""
    core_content = ""
    
    for _, c_row in df_course.iterrows():
        col1 = str(c_row.iloc[0]) if len(c_row) > 0 else ""
        col2 = str(c_row.iloc[1]) if len(c_row) > 1 else ""
        text_to_search = col1 + col2
        
        val = str(c_row.iloc[2]) if len(c_row) > 2 else ""
        if pd.isna(val) or val == 'nan':
            val = str(c_row.iloc[1]) if len(c_row) > 1 and pd.notna(c_row.iloc[1]) else ""
            
        if '목표' in text_to_search:
            goal = str(c_row.iloc[2]) if len(c_row) > 2 and not pd.isna(c_row.iloc[2]) else str(c_row.iloc[1])
        if '핵심 스택' in text_to_search or '도구' in text_to_search or '기술' in text_to_search:
            tools = str(c_row.iloc[2]) if len(c_row) > 2 and not pd.isna(c_row.iloc[2]) else str(c_row.iloc[1])
        if '소개' in text_to_search or '특징' in text_to_search or '결과물' in text_to_search:
            if not core_content:
                core_content = str(c_row.iloc[2]) if len(c_row) > 2 and not pd.isna(c_row.iloc[2]) else str(c_row.iloc[1])
                
    # clean up newlines for markdown table
    def clean(t):
        if pd.isna(t) or t == 'nan': return ""
        # Make core content bullet points internally or concise
        cleaned = str(t).replace('\n', '<br>').replace('|', ',')
        # If it's too long, we truncate or format
        if len(cleaned) > 200:
            cleaned = cleaned[:197] + "..."
        return cleaned

    md_content += f"| {clean(course_name)} | {clean(target)} | {clean(tools)} | {clean(goal)} | {clean(core_content)} | {clean(duration)}시간 |\n"

with open('customer_sheet.md', 'w', encoding='utf-8') as f:
    f.write(md_content)
