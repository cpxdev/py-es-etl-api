import pandas as pd

df = pd.read_excel('../data/Earth Finance Employee Details.xlsx')
print(df)
print(df.to_json())