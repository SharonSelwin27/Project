from PIL import Image

def encode_image(image_path, secret_message):
    try:
        image = Image.open(image_path)
        binary_message = ''.join(format(ord(i), '08b') for i in secret_message) + '1111111111111110'
        pixels = image.load()
        width, height = image.size
        data_index = 0

        for y in range(height):
            for x in range(width):
                pixel = list(pixels[x, y])
                for i in range(3):
                    if data_index < len(binary_message):
                        pixel[i] = pixel[i] & 254 | int(binary_message[data_index])
                        data_index += 1
                pixels[x, y] = tuple(pixel)

        output_path = 'encoded_image.png'
        image.save(output_path)
        return output_path
    except Exception as e:
        raise Exception(f"Error encoding image: {e}")

def decode_image(image_path):
    try:
        image = Image.open(image_path)
        binary_message = ""
        pixels = image.load()
        width, height = image.size

        for y in range(height):
            for x in range(width):
                pixel = list(pixels[x, y])
                for i in range(3):
                    binary_message += str(pixel[i] & 1)

        binary_message = binary_message.split('1111111111111110')[0]
        secret_message = ''.join(chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8))

        return secret_message
    except Exception as e:
        raise Exception(f"Error decoding image: {e}")
