import pandas as pd
import sys

file_path = r"c:\Users\Admin\Downloads\ai-education-proposal\projects\전주대학교_AI부트캠프사업\견적\[비즈팀] 전주대_AI 부트캠프_예산산출.xlsx"
try:
    xl = pd.ExcelFile(file_path)
    sheets = ['일정', 'ND1', 'ND2', 'ND5']
    for sheet in sheets:
        print(f"--- Sheet: {sheet} ---")
        if sheet in xl.sheet_names:
            df = xl.parse(sheet)
            print(df.head(30).to_string())
        else:
            print(f"Sheet '{sheet}' not found.")
        print("\n")
except Exception as e:
    print(f"Error: {e}")
