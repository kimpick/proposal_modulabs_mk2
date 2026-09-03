import pandas as pd
import json

files = [
    'B2B 제안용 과정 VOD 리스트 & 표준 견적서_[한국도로교통공사].xlsx',
    '[모두의연구소] 유사 과정 기업 맞춤형 VOD 제작 커리큘럼.xlsx'
]

for f in files:
    print(f"\n# File: {f}")
    try:
        xls = pd.ExcelFile(f)
        for sheet in xls.sheet_names:
            print(f"\n## Sheet: {sheet}")
            df = pd.read_excel(f, sheet_name=sheet)
            print(df.head(20).to_markdown(index=False))
    except Exception as e:
        print(f"Error reading {f}: {e}")
