import pandas as pd

with open('커리큘럼_소개_시트.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

table_lines = [line.strip() for line in lines if line.strip().startswith('|')]

header = [col.strip() for col in table_lines[0].split('|') if col.strip()][:]
data = []
for line in table_lines[2:]:
    cols = [col.strip().replace('<br>', '\n') for col in line.split('|')][1:-1]
    if len(cols) > 0:
        cols[0] = cols[0].replace('**', '')
    data.append(cols)

df = pd.DataFrame(data, columns=header)
df.to_excel('고객공유용_커리큘럼_소개_v2.xlsx', index=False, engine='openpyxl')
print("Excel file v2 created successfully")
