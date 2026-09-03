import openpyxl
import os

file_path = r"c:\Users\Admin\Downloads\ai-education-proposal\projects\전주대학교_AI부트캠프사업\견적\[비즈팀] 전주대_AI 부트캠프_예산산출.xlsx"
out_path = r"c:\Users\Admin\Downloads\ai-education-proposal\projects\전주대학교_AI부트캠프사업\견적\[비즈팀] 전주대_AI 부트캠프_예산산출_업데이트.xlsx"

try:
    wb = openpyxl.load_workbook(file_path)
    sheets_to_update = ['ND1', 'ND2', 'ND5']

    for sheet_name in sheets_to_update:
        if sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
            # Find the start of '재료비' rows (around row 15-22 logic from earlier extraction)
            
            # Let's search for the cells
            for row in ws.iter_rows(min_row=1, max_row=50):
                # Update "AI 툴 사용료" (e.g. ChatGPT, Claude API / 1인당 40,000원 * 30명)
                if row[2].value == 'AI 툴 사용료':
                    ws.cell(row=row[0].row, column=4).value = 40000 # 단가
                    ws.cell(row=row[0].row, column=5).value = 30 # 수량(명)
                    ws.cell(row=row[0].row, column=7).value = 1 # 단위
                    ws.cell(row=row[0].row, column=9).value = 1 # 단위
                    # Calculate total
                    # row[11] is K (합계)
                    # For formula, we can just write the formula or value
                    ws.cell(row=row[0].row, column=11).value = "=D{}*E{}*G{}*I{}".format(row[0].row, row[0].row, row[0].row, row[0].row)
                    ws.cell(row=row[0].row, column=12).value = "OpenAI, Claude 등 API 활용 크레딧 (인당 4만원)"
                
                # Update "클라우드 사용료"
                if row[2].value == '클라우드 사용료':
                    # GPU instances, DevOps environment, Web-IDE etc.
                    ws.cell(row=row[0].row, column=4).value = 2500 # 단가 (시간당)
                    ws.cell(row=row[0].row, column=5).value = 30 # 인원
                    ws.cell(row=row[0].row, column=6).value = "명" 
                    ws.cell(row=row[0].row, column=7).value = 60 # 60시간(4모듈)
                    ws.cell(row=row[0].row, column=8).value = "시간"
                    ws.cell(row=row[0].row, column=9).value = 1 
                    ws.cell(row=row[0].row, column=11).value = "=D{}*E{}*G{}*I{}".format(row[0].row, row[0].row, row[0].row, row[0].row)
                    ws.cell(row=row[0].row, column=12).value = "카카오 클라우드 고성능 GPU 및 보조 클러스터 (시간당 단가 환산치)"

                # We can also add specifically if we want, but 'AI 툴 사용료' and '클라우드 사용료' covers the main infra.
                # Let's also update '기타 재료비' if we want to add "Web-IDE 개발환경(공통)"
                if row[2].value == '기타 구독료':
                    ws.cell(row=row[0].row, column=4).value = 30000 # 단가
                    ws.cell(row=row[0].row, column=5).value = 30 # 명
                    ws.cell(row=row[0].row, column=7).value = 2 # 2개월
                    ws.cell(row=row[0].row, column=9).value = 1 
                    ws.cell(row=row[0].row, column=11).value = "=D{}*E{}*G{}*I{}".format(row[0].row, row[0].row, row[0].row, row[0].row)
                    ws.cell(row=row[0].row, column=12).value = "AI Augmented Coding (자동채점 등) 구독료"

    wb.save(out_path)
    print("Success")
except Exception as e:
    print("Error:", e)
