import json
import re

with open('faqdata.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


conversation = []
new_data = []

for i in range(len(data) - 1):
    if ("ticket closed" not in data[i]['MESSAGE']) and ("Solved" not in data[i]['MESSAGE']) and ("ticket opened" not in data[i]['MESSAGE']) and  ("category" not in data[i]['MESSAGE']) and ("status" not in data[i]['MESSAGE']) and ("priority" not in data[i]['MESSAGE']) and ("support level" not in data[i]['MESSAGE']):
        string = data[i]['MESSAGE'].replace("&gt", "").replace("&lt", "").replace("li&gt", "").replace("i&gt", "").replace("b&gt", "").strip()
        if string != "":
            new_data.append(string)
    if (data[i]["ticket_tieude"] != data[i + 1]["ticket_tieude"]):
        conversation.append(new_data)
        new_data = []
        
tail = data[len(data)-1]['MESSAGE']
if ("ticket closed" not in tail) and ("Solved" not in tail) and ("ticket opened" not in tail) and  ("category" not in tail) and ("status" not in tail) and ("priority" not in tail) and ("support level" not in data[i]['MESSAGE']):
    tail = tail.replace("&gt", "").replace("&lt", "").replace("li&gt", "").replace("i&gt", "").replace("b&gt", "").strip()
    if tail != "":
        conversation.append(tail) 

# data = []
# for sublist in conversation:
#     joined_string = ''.join(sublist)
#     data.append(joined_string)

# for item in conversation:
#     for i in range(len(item)):
#         item[i] = item[i].replace("&lt", "").replace("li&gt", "").replace("i&gt", "").replace("b&gt", "").strip()

# output = []

# for sublist in conversation:
#     joined_string = "".join(sublist)
#     output.append(joined_string)

# item = [string for string in item if string.strip()]

# string = data[i]['MESSAGE'].replace("&lt;", "").replace("li&gt;", "").replace("i&gt", "").replace("b&gt;", "")


exclude_phrases = [
    "Học vụ .",
    "Tốt nghiệp .",
    "Đăng ký môn học .",
    "Rút môn học HK Hè/2019-2020 (có tính học phí) .",
    "Yêu cầu khác:",
    "i Học phí   Học phí học kỳ chính .   b Nội dung yêu cầu  /b . . [not specified]. . . .",
    "i Học phí   Học phí dự thính .   b Nội dung yêu cầu  /b . . Thay Trang test. . . .",
    "i Đăng ký môn học   Tình trạng không đăng ký được . Hi, test coi có đúng ko.. .",
    "Dịch vụ cho sinh viên   Đăng ký in bảng điểm .",
    "I Học vụ- Đại học - Cao đẳng chính quy   Tạm dừng .",
    "Học vụ - Đại học - Cao đẳng chính quy   Khác ... .",
    "Đã phục hồi môn CI1051 nhóm A02 cho bạn.",
    "Đăng ký môn học - Đại học - Cao đẳng chính quy   Khác ... .",
    "B Đăng ký môn học - Đại học - Cao đẳng chính quy   Khác ... .",
    "Đăng ký môn học - Đại học - Cao đẳng chính quy   Chuyển thời khóa biểu .",
    "Đăng ký môn học - Đại học - Cao đẳng chính quy   Tăng sĩ số lớp môn học .",
    "responsible person: [543] [staff_name] [helpdesk staff]",
    "responsible person: [551] [staff_name] [helpdesk staff]",
    "Chứng chỉ ngoại ngữ - Đại học - Cao đẳng chính quy   Khác ... .",
    "Đăng ký môn học - Đại học - Cao đẳng chính quy   Tình trạng không đăng ký được .",
    "HP 2017",
    "b MSSV/MSGV: 002282  /b \t. . . .   i Dịch vụ cho sinh viên   Đăng ký in bảng điểm . in 2 bang",
    "Đăng ký môn học . Em không nhận được Email đăng ký môn học. . [full_name] cảm ơn. .",
    "i Tốt nghiệp .   b Họ tên sinh viên       b Mã sinh viên    ABC123   b Nội dung yêu cầu    Thưa thầy cô, em muốn biết em có đủ điều kiện tốt nghiệp không?",
    "i Yêu cầu khác .   b Họ tên sinh viên       b Mã sinh viên    XYZ123   b Nội dung yêu cầu    Yêu cầu về việc chứng nhận hoàn thành môn học",
    "i Điểm thi .   b Họ tên sinh viên       b Mã sinh viên    D1234   b Nội dung yêu cầu    Tra lục bảng điểm.",
    "i Điểm thi .   b Họ tên sinh viên       b Mã sinh viên    BK1126   b Nội dung yêu cầu    Chào thầy cô, Em muốn xin chấm phúc khảo lại bài thi \"Tư tưởng \" ạ! Em cảm ơn.",
    "i Học phí   khong chinh quy .   b Họ tên sinh viên    sinh vien A   b Mã sinh viên    0001   b Nội dung yêu cầu    Noi dung yeu cau hoc phi   b cau 1    hoi ve hoc phi",
    "i Điểm thi         b Họ tên sinh viên           b Mã sinh viên     312312abc      b Nội dung yêu cầu     abc   ",
    "i Điểm thi .   b Họ tên sinh viên       b Mã sinh viên    097356   b Nội dung yêu cầu      ",
    "i Đăng ký môn học .   b Họ tên sinh viên    [not specified]   b Mã sinh viên    [not specified]   b Nội dung yêu cầu    [not specified]",
    "i Yêu cầu khác .   b Họ tên sinh viên       b Mã sinh viên    0001   b Nội dung yêu cầu    Test giao diện mới",
    "SP1009",
    "Sp1009    sp1009",
    "Học kỳ 203 ."
]

replace_phrases = [
    "b MSSV/MSGV: [student_id]9  /b",
    "b  [student_id]0  /b",
    "b  [student_id]1  /b",
    "b  [student_id]2  /b",
    "b  [student_id]3  /b",
    "b  [student_id]4  /b",
    "b  [student_id]5  /b",
    "b  [student_id]6  /b",
    "b  [student_id]7  /b",
    "b  [student_id]8  /b",
    "b  [student_id]9  /b",
    "b  V[student_id]  /b",
    "MSSV/MSGV:", "V/MSGV:", "MSSV/MSV", "MSSV/MSGV", "MSSVMSGV:",
    "[full_name]", "E-[fullname]", "[fullname]", "[email]", "[student_id]",
    "Yêu cầu khác",
    "Học vụ - Đại học - Cao đẳng chính quy   Rút môn học",
    "Học vụ - Đại học - Cao đẳng chính quy   Miễn môn học",
    "Học vụ   Khác ..",
    "Học vụ - Đại học - Cao đẳng chính quy",
    "Học vụ   Miễn môn học .",
    "Học vụ .",
    "Tốt nghiệp - Đại học - Cao đẳng chính quy   Khác ..",
    "Tốt nghiệp - Đại học - Cao đẳng chính quy",
    "Điểm thi - Đại học - Cao đẳng chính quy   Điểm môn học",
    "Điểm thi - Đại học - Cao đẳng chính quy",
    "Dịch vụ cho sinh viên - Đại học - Cao đẳng chính quy",
    "Dịch vụ cho sinh viên - Đại học - Cao đẳng chính quy   Giấy xác nhận sinh viên",
    "Dịch vụ cho sinh viên - Đại học - Cao đẳng chính quy   Đăng ký in bảng điểm",
    "Dịch vụ cho sinh viên - Đại học - Cao đẳng chính quy   Thông tin sinh viên",
    "Dịch vụ cho sinh viên - Đại học - Cao đẳng chính quy   Bằng tốt nghiệp THPT",
    "Học phí - Đại học - Cao đẳng chính quy   Học phí dự thính .",
    "Học bổng - Đại học - Cao đẳng chính quy",
    "Học bổng (danh sách, điều kiện,...)",
    "Học phí - Đại học - Cao đẳng chính quy",
    "Học phí   Học phí học kỳ chính",
    "Học phí học kỳ chính .",
    "Xét miễn môn anh văn (chuyển điểm)",
    "Lịch thi - Đại học - Cao đẳng chính quy",
    "Đăng ký môn học - Đại học - Cao đẳng chính quy   Khác",
    "Đăng ký môn học - Đại học - Cao đẳng chính quy   Tăng sĩ số lớp môn học",
    "Đăng ký môn học - Đại học - Cao đẳng chính quy",
    "Đăng ký môn học - Đại học - Cao đẳng chính quy   Tình trạng không đăng ký được",
    "i Đăng ký môn học",
    "Đăng ký môn học .",
    "Chứng chỉ ngoại ngữ - Đại học - Cao đẳng chính quy   Khác",
    "Chứng chỉ ngoại ngữ   Khác ..",
    "Chứng chỉ ngoại ngữ - Đại học - Cao đẳng chính quy",
    "Chứng chỉ ngoại ngữ   Xét miễn môn anh văn (chuyển điểm)",
    "Chương trình đào tạo (thiếu môn tiên quyết, song hành...)",
    "ương trình đào tạo (thiếu môn tiên quyết, song hành...)",
    "Chương trình đào tạo - Đại học - Cao đẳng chính quy",
    "Môn tương đương, tiên quyết, ..",
    "Điểm thi   Điểm môn học",
    "Điểm môn học .",
    "Miễn môn học .",
    "Dành cho SV các hệ (không phải Quốc tế, CLC)",
    "Cập nhật ngày CTXH, điểm",
    "Môn tương đương, tiên quyết",
    "Vừa làm vừa học - ĐTTX   Đăng ký môn học",
    "Vừa làm vừa học - ĐTTX   Học vụ .",
    "Vừa làm vừa học - ĐTTX",
    "Rút môn học (phải thanh toán học phí)",
    "Rút môn học HK Hè/2019-2020 (có tính học phí)",
    "Chuyển thời khóa biểu .",
    "Thẩm tra chứng chỉ (nộp chứng chỉ)",
    "Phúc tra bài thi .",
    "Tình trạng không đăng ký được",
    "Chưa cập nhật điểm .",
    "Thu nhận lại .",
    "Tăng sĩ số lớp môn học",
    "Tạm dừng .",
    "Thi vét .",
    "Rút môn học .",
    "Học kỳ 203 .",
    "Khiếu nại đăng ký môn học .",
    "ng ký rút môn học HK192 (không tính HP)",
    "Hỏi đáp học trực tuyến (BKeL)",
    "/b", "b  V   \t. . . .   i ", "\t. . . .   i ", "\t. . . . ", "\t. .", ". . . .", ". .",
    "b    ", "b  0", "b  1", "b  2", "b  3", "b  4", "b  5", "b  6", "b  7", "b  8", "b  9", "b  G", "b  V",
    "/i", "\t", "/U",
    "B   /B", "B   I   /B   /I   B   U ","/B    B", "B   /B", "/B", "B   I      /I   I   /I      B", "B   I   /I",
    "Khác .."
]

prefixes_to_remove = [
    "Tốt nghiệp",
    "Đăng ký môn học",
    "Yêu cầu khác .",
    "Yêu cầu khác:",
    "Học vụ",
    "Chứng chỉ ngoại ngữ",
    "Giấy xác nhận sinh viên"
]

result = []

# result = [sentence[0] for sentence in conversation if sentence and sentence[0] not in exclude_phrases and sentence[0] not in result]

# for i, sentence in enumerate(result):
#     for phrase in replace_phrase:
#         if phrase in sentence:
#             result[i] = sentence.replace(phrase, "")

for sentence in conversation:
    if len(sentence) > 0 and sentence[0]:
        if sentence[0] not in exclude_phrases:
            # remove characters
            for phrase in replace_phrases:
                if phrase in sentence[0]:
                    sentence[0] = sentence[0].replace(phrase, "")
            sentence[0] = sentence[0].lstrip()
            # remove prefixes
            for prefix in prefixes_to_remove:
                if sentence[0].startswith(prefix):
                    # sentence[0] = sentence[0].replace(prefix, "")
                    sentence[0] = sentence[0][len(prefix):]
            sentence[0] = sentence[0].lstrip()
            sentence[0] = re.sub(r'^[^a-zA-Z]+|^[BbIiU\s]', '', sentence[0])
            sentence[0] = sentence[0].lstrip()
            if sentence[0]:
                result.append(sentence[0])

with open('output2.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
