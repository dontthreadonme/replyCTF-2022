from PIL import Image
from pyzbar.pyzbar import decode


for i in [1, 2, 3]:
    qr_val = decode(Image.open(f"{i}.png"))[0][0].decode("utf-8")
    print(qr_val)
    print("last 40:", "0x"+qr_val[-40:])
    # crypto adr??
