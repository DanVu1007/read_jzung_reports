import pytesseract
import re
from PIL import Image

def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang='vie')  # Trích xuất văn bản từ ảnh
        return text
    except Exception as e:
        print("Error:", e)
        return None

image_path = "anhlong.png"
extracted_text = extract_text_from_image(image_path)

if extracted_text:
    # print("Extracted text:", extracted_text)
    start_index = extracted_text.find("Đơn giá SL T.tiền")
    end_index = extracted_text.find("Tạm tính ")
    if start_index != -1:
        relevant_text = extracted_text[start_index:end_index]

    print(relevant_text)
    text = relevant_text

    item_pattern = r"\d+\.\s+(.*?)\s+-\s+(.*?)\s+-\s+(.*?)\s+([\d.,]+)\sx(\d+)\s+([\d.,]+)"
    items = re.findall(item_pattern, text, re.DOTALL)

    result = []

    for item in items:
        name = item[0]
        weight = item[1]
        variant = item[2]
        price = item[3]
        qty = int(item[4].replace(',', ''))  # Chuyển đổi số lượng thành số nguyên
        price_per_item = item[5]

        result.append({
            'name': name.replace('\n', ' ') if '\n' in name else name,
            'weight': weight,
            'variant': variant.replace('\n', ' ') if '\n' in variant else variant,
            'price': price,
            'qty': qty
        })

    print(result)
