# read_jzung_reports

### cài đặt thư viện Pillow (nếu bạn chưa cài đặt):
```
pip install Pillow
```

### cài đặt Tesseract và thư viện pytesseract (wrapper cho Tesseract):
```
pip install pytesseract
```
Nếu không thành công cài thêm:
```
sudo apt update
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
```

### Thêm ngôn ngữ tiếng Việt cho Tesseract

- Truy cập trang sau (https://github.com/tesseract-ocr/tessdata) và tải về file `vie.traineddata`
- Cập nhật biến môi trường `TESSDATA_PREFIX` (đường dẫn đến thư mục chứa dữ liệu ngôn ngữ):
```
export TESSDATA_PREFIX=/usr/local/share/
```
Nếu không thành công copy `vie.traineddata` vào thư mục `/usr/share/tesseract-ocr/4.00/tessdata/` bằng lệnh sau:
```
sudo cp vie.traineddata /usr/share/tesseract-ocr/4.00/tessdata/
```
