from PIL import Image
from pyzbar.pyzbar import decode
import qrcode

def generate_qrcode(data, file_name='qrcode.png'):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_name)

def extract_wifi_info(data):
    # Extract SSID and password from the QR code data
    ssid_start = data.find("WIFI:S:") + len("WIFI:S:")
    ssid_end = data.find(";", ssid_start)
    ssid = data[ssid_start:ssid_end]

    password_start = data.find("T:WPA;P:") + len("T:WPA;P:")
    password_end = data.find(";", password_start)
    password = data[password_start:password_end]

    return ssid, password

def decode_qrcode(image_path):
    # Open the image
    image = Image.open(image_path)

    # Decode QR code using zbar
    decoded_objects = decode(image)

    if decoded_objects:
        for obj in decoded_objects:
            data = obj.data.decode('utf-8')
            print(f"Decoded QR Code: {data}")

            if data.startswith("WIFI:S:"):
                ssid, password = extract_wifi_info(data)
                print(f"SSID: {ssid}")
                print(f"Password: {password}")
    else:
        print("No QR Code detected.")

def main():
    print("\nChoose from the options below. \n1) Generate QR Code \n2) Decode a QR Code")
    option = int(input("#: "))

    if option == 1:
        # Generate QR Code
        data_to_encode = input("Input Your data: ")
        generate_qrcode(data_to_encode, file_name='generated_qrcode.png')
        print(f"QR Code generated with data: {data_to_encode}")
    elif option == 2:
        # Decode QR Code from an image
        image_path_to_decode = input('Enter path to qr_code_image: ')
        decode_qrcode(image_path_to_decode)
    else:
        print("Invalid input!")

if __name__ == "__main__":
    main()
