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
        end_index = extracted_text.find("Tổng cộng ")
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
        # Tạo biến để lưu trữ tổng giá trị
        total_value = 0

        # Tạo từ điển để lưu trữ phân loại sản phẩm và số lượng
        product_categories = {}

        # Tạo từ điển để lưu trữ số lượng của từng variant cụ thể
        variant_quantities = {variant: 0 for variant in ['Nhân lava trứng muôi', 'Nhân lava socola', 'Nhân tiramisu', 'Nhân trà xanh phomai']}

        # Tạo từ điển để lưu trữ tổng số lượng của các trọng lượng (weight) khác nhau
        weight_total_quantities = {}

        # Lặp qua từng sản phẩm và phân loại chúng
        for product in input_data:
            weight = product['weight']
            name = product['name']
            variant = product['variant']
            qty = product['qty']
            price = float(product['price'])
            
            # Cập nhật tổng giá trị
            total_value += qty * price
            
            # Cập nhật số lượng của từng variant cụ thể
            if variant in variant_quantities:
                variant_quantities[variant] += qty
            
            # Cập nhật tổng số lượng của các trọng lượng khác nhau
            if weight not in weight_total_quantities:
                weight_total_quantities[weight] = 0
            weight_total_quantities[weight] += qty
            
            # Tạo cấu trúc dữ liệu nếu chưa tồn tại
            if weight not in product_categories:
                product_categories[weight] = {}
            if name not in product_categories[weight]:
                product_categories[weight][name] = {}
            if variant not in product_categories[weight][name]:
                product_categories[weight][name][variant] = 0
            
            # Tăng số lượng sản phẩm
            product_categories[weight][name][variant] += qty

        # In kết quả theo yêu cầu
        for weight, weight_data in product_categories.items():
            print(weight + ":")
            for name, name_data in weight_data.items():
                print("--" + name + ":")
                for variant, qty in name_data.items():
                    print("----", variant + ":", qty)

        # In số lượng của từng variant cụ thể
        print("Số lượng của từng variant cụ thể:")
        for variant, qty in variant_quantities.items():
            print(f"-- {variant}: {qty}")

        # In tổng số lượng của các trọng lượng khác nhau
        print("Tổng số lượng của các trọng lượng khác nhau:")
        for weight, qty in weight_total_quantities.items():
            print(f"-- {weight}: {qty}")

        # In tổng giá trị của tất cả sản phẩm
        print("Tổng giá trị của tất cả sản phẩm:", total_value)