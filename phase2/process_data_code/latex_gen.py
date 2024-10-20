import json

# Đọc file JSON
with open('ontology\intent_entities.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Tạo mã LaTeX cho bảng
latex_code = r"""
\begin{table}[htbp]
    \centering
    \begin{tabular}{|l|l|}
        \hline
        \textbf{Ý định} & \textbf{Các thực thể liên quan}  \\
        \hline
"""

# Thêm các phần tử vào bảng LaTeX
for section, details in data.items():
    entities = ', '.join(details['entities'])
    latex_code += f"        {section} & {entities} \\\\\n        \\hline\n"

# Kết thúc bảng LaTeX
latex_code += r"""
    \end{tabular}
\end{table}
"""

# Ghi mã LaTeX vào file
with open('table.tex', 'w', encoding='utf-8') as file:
    file.write(latex_code)

print("Mã LaTeX đã được tạo thành công và lưu vào file table.tex")
