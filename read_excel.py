import pandas as pd
import sys

try:
    file_path = r"c:\Users\Admin\Downloads\ai-education-proposal\projects\KCH\AI_리터러시_교육과정\[KCH} AI 리터러시 진단 테스트 결과 (1).xlsx"
    xls = pd.ExcelFile(file_path)
    print('Sheet names:', xls.sheet_names)
    for sheet_name in xls.sheet_names:
        print(f"\n--- Sheet: {sheet_name} ---")
        df = pd.read_excel(xls, sheet_name)
        print("Columns:", df.columns.tolist())
        print(df.head())
except Exception as e:
    print("Error:", e)
