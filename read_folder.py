import re
import os
from PIL import Image
import pytesseract

from handledata import Handle

folder_path = "reports"
valid_image_extensions = [".jpg", ".jpeg", ".png", ".gif"]

# Lặp qua các tệp trong thư mục
image_files = [file for file in os.listdir(folder_path) if os.path.splitext(file)[-1].lower() in valid_image_extensions]

result_array = [] #================================================RESULT#================================================
for image_file in image_files:
    image_path = os.path.join(folder_path, image_file)
    print('Bắt đầu đọc ảnh: ' + image_path)
    extracted_text = Handle.extract_text_from_image(image_path)
    imageData = Handle.get_data_of_image(extracted_text)
    result_array.extend(imageData)

resultArray = Handle.show_the_result(result_array)
print (Handle.str_result(resultArray))
