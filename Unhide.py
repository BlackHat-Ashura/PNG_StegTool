import argparse
import cv2


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--extract", dest="encoded_image", help="PNG format image with hidden message")
    parser.add_argument("-o", "--out-file", dest="out_file", help="File name to write the hidden message")
    arguments = parser.parse_args()
    if not arguments.encoded_image:
        parser.error("[-] Please specify a valid PNG format image name.")
    elif not arguments.out_file:
        parser.error("[-] Please specify a file name to write the hidden message.")
    else:
        return arguments


def binary_to_text(message_in_bits, out_file):
    length = len(message_in_bits)
    with open(out_file, "w") as f:
        for i in range(0, length, 8):
            byte = message_in_bits[i:i+8]
            character = chr(int(byte, 2))
            f.write(character)


def decode_message(image_data):
    image_array, rows, columns = image_data
    counter = 0
    message_in_bits = ""
    for i in range(rows):
        for j in range(columns):
            for k in range(3):
                if counter != 8:
                    if image_array[i, j, k] % 2 == 0:
                        message_in_bits += "0"
                    else:
                        message_in_bits += "1"
                    counter += 1
                else:
                    if image_array[i, j, k] % 2 == 1:
                        return message_in_bits
                    counter = 0


def get_image_data(encoded_image):
    image_array = cv2.imread(encoded_image)
    rows = len(image_array)
    columns = len(image_array[0])
    return image_array, rows, columns


def unhide_message(encoded_image, out_file):
    image_data = get_image_data(encoded_image)
    message_in_bits = decode_message(image_data)
    if binary_to_text(message_in_bits, out_file):
        print(f"[+] Hidden message extracted to {out_file}")
    else:
        print("[-] Failed to extract hidden message.")


arguments = get_arguments()
encoded_image = arguments.encoded_image
out_file = arguments.out_file


if encoded_image[-4:] == ".png":
    unhide_message(encoded_image, out_file)
else:
    print("[!] Specified Message Encoded Image is not of PNG format.")
