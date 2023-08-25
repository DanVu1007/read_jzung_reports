import re
import os
from PIL import Image
import pytesseract

class Handle:
    def extract_text_from_image(image_path):
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang='vie')  # Trích xuất văn bản từ ảnh
            return text
        except Exception as e:
            print("Error:", e)
            return None
        

    def get_data_of_image(extracted_text):
        start_index = extracted_text.find("Đơn giá SL T.tiền")
        end_index = extracted_text.find("Tạm tính ")
        if start_index != -1:
            relevant_text = extracted_text[start_index:end_index]

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
        return result

    def show_the_result(input_data):
        output = []

        # Tạo một từ điển để lưu trữ thông tin sản phẩm theo variant, weight và price
        product_variants = {}

        for item in input_data:
            key = (item['name'], item['variant'], item['weight'], item['price'])
            
            if key in product_variants:
                product_variants[key]['qty'] += item['qty']
            else:
                product_variants[key] = {
                    'name': item['name'],
                    'variant': item['variant'],
                    'weight': item['weight'],
                    'price': item['price'],
                    'qty': item['qty']
                }

        # Chuyển từ từ điển sang list
        for key, data in product_variants.items():
            variant_info = {
                'name': f"{data['variant']} - {data['weight']} ({data['price']})",
                'qty': data['qty']
            }
            
            existing_product = next((p for p in output if p['name'] == data['name']), None)
            
            if existing_product:
                existing_product['variant'].append(variant_info)
            else:
                output.append({
                    'name': data['name'],
                    'variant': [variant_info]
                })

        return output

    def str_result(result):
        for product in result:
            print(f"{product['name']} có:")
            for variant in product['variant']:
                print(f"{variant['qty']} cái - {variant['name']}")