import pandas as pd

file1 = pd.read_excel('arm_eval/4/eval0.8.xlsx')
file2 = pd.read_excel('arm_label/label0.4.xlsx')

data1 = file1.iloc[1:, [0, 1]]  
data2 = file2.iloc[1:, [0, 1]]  

data1.columns = ['Column1', 'Column2']
data2.columns = ['Column1', 'Column2']


matching_pairs = pd.merge(data1, data2, how='inner', on=['Column1', 'Column2'])

if len(matching_pairs) == 0:
    print("nothing")

print(f"Số lượng cặp (cột 1, cột 2) giống nhau giữa hai file: {len(matching_pairs)}")
