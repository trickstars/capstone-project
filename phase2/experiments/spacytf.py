import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import json

with open('preprocessed_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# nlp = spacy.load('vi_spacy_model')
nlp = spacy.load('vi_core_news_lg')
# doc = nlp("Chào PĐT, em là sinh viên khoá 17, học kì này em có đăng kí môn học công nghệ phần mềm nhưng vẫn chưa có thời khoá biểu. Mong PĐT xử lý sớm giúp em.")

result = []

for message in data:
    doc = nlp(message)
    component = {}
    noun = []
    if doc:
        for token in doc:
            if token.tag_ == 'N' or token.tag_ == 'NP':
                noun.append(token.text)
        if noun: 
            component['message'] = message
            component['noun'] = noun
            result.append(component)
            
# for token in doc:
#     if token.tag_ == 'N' or token.tag_ == 'NP':
#         print(token.text)

with open('extracted_noun.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)