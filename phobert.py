from infer import tokenize_function, data_collator, extract_answer
from model.mrc_model import MRCQuestionAnswering
from transformers import AutoTokenizer

model_checkpoint = "C:\\Users\\Dell\\.cache\\huggingface\\hub\\phobert"

tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
model = MRCQuestionAnswering.from_pretrained(model_checkpoint)

QA_input = {
  'question': "rút môn học với học kỳ nào?",
  'context': "Em muốn rút môn học Tư tưởng HCM ở học kỳ này (231)"
}

inputs = [tokenize_function(QA_input, tokenizer)]
inputs_ids = data_collator(inputs, tokenizer)
outputs = model(**inputs_ids)
answer = extract_answer(inputs, outputs, tokenizer)

print(answer['answer'])