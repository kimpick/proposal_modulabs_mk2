import pandas as pd
import sys

file_path = r"c:\Users\Admin\Downloads\ai-education-proposal\projects\전주대학교_AI부트캠프사업\견적\[비즈팀] 전주대_AI 부트캠프_예산산출.xlsx"
out_path = r"c:\Users\Admin\Downloads\ai-education-proposal\projects\전주대학교_AI부트캠프사업\excel_out.txt"
try:
    with open(out_path, "w", encoding="utf-8") as f:
        xl = pd.ExcelFile(file_path)
        sheets = ['일정', 'ND1', 'ND2', 'ND5']
        for sheet in sheets:
            f.write(f"--- Sheet: {sheet} ---\n")
            if sheet in xl.sheet_names:
                df = xl.parse(sheet)
                f.write(df.head(50).to_string())
            else:
                f.write(f"Sheet '{sheet}' not found.")
            f.write("\n\n")
except Exception as e:
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"Error: {e}")
