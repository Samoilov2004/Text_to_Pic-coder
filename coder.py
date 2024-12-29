import matplotlib.pyplot as plt
import numpy as np
import random
from PIL import Image
import argparse


class Coder:
    def __init__(self, message):
        self.message = message

    def colors(self):
        byte_array = bytearray(self.message, "utf-8")
        hex_values = [format(byte, "02x") for byte in byte_array]

        # Add a space sign to avoid frequent repetition of colors
        if len(hex_values) % 3 == 0:
            hex_values.append("20")

        # Addind motif to the end. This motif would be helpful in decoding
        hex_values.append(hex_values[0])
        hex_values.append(hex_values[1])
        hex_values.append(hex_values[2])

        while len(hex_values) % 3 != 0:
            hex_values.append("".join(random.choices("0123456789abcdef", k=2)))

        # Generate colors in RGB format
        hex_colors = [
            "#" + "".join(hex_values[i : i + 3]) for i in range(0, len(hex_values), 3)
        ]

        return hex_colors

    def make_paint(self, filename):
        hex_colors = self.colors()
        num_colors = len(hex_colors)
        side_length = int(num_colors**0.5) + 1

        # Adding random hex numbers to square picture
        while len(hex_colors) < side_length**2:
            hex_colors.append("#" + "".join(random.choices("0123456789abcdef", k=6)))

        hex_colors = np.array(hex_colors).reshape(side_length, side_length)
        # Convert to RGB format
        rgb_colors = np.array(
            [
                [int(color[i : i + 2], 16) for i in (1, 3, 5)]
                for color in hex_colors.flatten()
            ]
        )
        rgb_colors = rgb_colors.reshape(side_length, side_length, 3) / 255.0

        plt.imshow(rgb_colors)
        plt.axis("off")
        plt.savefig(filename, format="png")
        # plt.show()  # You can turn on this option


def decode(image_path):
    # Loading picture
    image = Image.open(image_path)
    image = image.convert("RGB")
    image_array = np.array(image)

    hex_colors = []
    unique_colors = set()

    for row in image_array:
        for pixel in row:
            hex_color = "{:02x}{:02x}{:02x}".format(pixel[0], pixel[1], pixel[2])
            if hex_color not in unique_colors:
                unique_colors.add(hex_color)
                hex_colors.append(hex_color)

    # find our stop_motif
    hex_string = "".join(hex_colors)[6:]
    terminator = hex_string.index(hex_string[0:6], 3)
    final_hex = hex_string[0:terminator]

    byte_array = bytearray.fromhex("".join(final_hex))
    message = byte_array.decode("utf-8", errors="ignore")

    return message


def main():
    parser = argparse.ArgumentParser(
        description="Encode or decode an image to/from text."
    )
    parser.add_argument(
        "action",
        type=str,
        choices=["encode", "decode"],
        help="Action to perform: encode or decode",
    )
    parser.add_argument("--message", type=str, help="Message to encode")
    parser.add_argument("--path", type=str, help="Path to save/read the image")
    args = parser.parse_args()

    if args.action == "encode":
        if not args.message:
            parser.error("The --message argument is required for encoding.")
        print(f"Encoding message: {args.message}")
        if not args.path:
            parser.error("The --output_path argument is required for encoding.")
        coder = Coder(args.message)
        coder.make_paint(args.path)
        print(f"Encoded message saved to {args.path}")
    elif args.action == "decode":
        if not args.path:
            parser.error("The --image_path argument is required for decoding.")
        decoded_message = decode(args.path)
        print("Decoded message:", decoded_message)


if __name__ == "__main__":
    main()