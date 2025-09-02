import qrcode
from PIL import Image
import os
print(os.getcwd())

C = 1
name=[]
# imagesフォルダがなければ作成
os.makedirs("images", exist_ok=True)
print("This project is active" )

for i in range(1):
    password = "Great"
    print("Enter your name")
    text=input()
    data = "テスト"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(f"images/{C}.png")
    C += 1
