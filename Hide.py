import argparse
import cv2


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cover-image", dest="cover_image", help="PNG format image to hide the message")
    parser.add_argument("-m", "--message-file", dest="message_file", help="Plain text file with the message to be hidden")
    parser.add_argument("-o", "--out-file", dest="out_file", help="Name of output image with hidden message")
    arguments = parser.parse_args()
    if not arguments.cover_image:
        parser.error("[-] Please specify a valid PNG format image name.")
    elif not arguments.message_file:
        parser.error("[-] Please specify a plain text file with the message to be hidden.")
    elif not arguments.out_file:
        parser.error("[-] Please specify name of output image.")
    else:
        return arguments


def encode_message(image_data, message_in_bits):
    image_array, rows, columns = image_data
    pointer = 0
    counter = 0
    end_value = len(message_in_bits)
    for i in range(rows):
        for j in range(columns):
            for k in range(3):
                if counter != 8:
                    if message_in_bits[pointer] == "0" and image_array[i, j, k] % 2 != 0:
                        image_array[i, j, k] = image_array[i, j, k] - 1
                    elif message_in_bits[pointer] == "1" and image_array[i, j, k] % 2 != 1:
                        image_array[i, j, k] = image_array[i, j, k] + 1
                    counter += 1
                    pointer += 1
                else:
                    if pointer < end_value:
                        image_array[i, j, k] = image_array[i, j, k] if image_array[i, j, k] % 2 == 0 else image_array[i, j, k] - 1
                        counter = 0
                    else:
                        image_array[i, j, k] = image_array[i, j, k] if image_array[i, j, k] % 2 != 0 else image_array[i, j, k] + 1
                        return image_array


def text_to_binary(content):
    binary_message = ""
    for character in content:
        byte = bin(ord(character))[2:].zfill(8)
        binary_message += byte
    return binary_message


def get_image_data(image):
    image_array = cv2.imread(image)
    rows = len(image_array)
    columns = len(image_array[0])
    return image_array, rows, columns


def get_secret_message(file):
    with open(file, "r") as f:
        message_content = "".join(f.readlines())
    message_in_bits = text_to_binary(message_content)
    return message_in_bits


def hide_message(cover_image, message_file, out_file):
    image_data = get_image_data(cover_image)
    message_in_bits = get_secret_message(message_file)
    message_image_array = encode_message(image_data, message_in_bits)
    if cv2.imwrite(out_file + ".png", message_image_array):
        print(f"[+] Message successfully hidden in {out_file}.png")
    else:
        print("[-] Failed to hide.")


arguments = get_arguments()
cover_image = arguments.cover_image
message_file = arguments.message_file
out_file = arguments.out_file

if cover_image[-4:] == ".png":
    hide_message(cover_image, message_file, out_file)
else:
    print("[!] Specified Cover Image is not of PNG format.")
