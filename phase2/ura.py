import requests

def get_gemma(input_sentence):
    # Tạo prompt
    prompt = prompt = f"""
    Hãy cho biết ý định của câu sau: '{input_sentence}'    
    """



    # Gửi yêu cầu đến API
    x = requests.post(
        'https://ws.gvlab.org/fablab/ura/llama/api/generate',
        headers={
            'Content-Type': 'application/json'
        },
        json={
            "inputs": f"<start_of_turn>user\n{prompt}<end_of_turn>\n<start_of_turn>model\n",
        }
    )

    # Nhận kết quả sinh ra từ mô hình
    generated_text = x.json()['generated_text']

    # In kết quả ra màn hình
    print(generated_text)

input_sentence = "Tôi muốn đăng ký môn học nhập môn lập trình vào học kỳ tới."
get_gemma(input_sentence)
