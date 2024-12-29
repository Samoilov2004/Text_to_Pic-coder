 # Image Encoder/Decoder

This script allows you to encode text messages into images and decode them back. The program uses hexadecimal color codes to store information in the image.

## Description

The program consists of two main functions:
1. **Encoding**: Converts a text message into an image where each pixel represents part of the message.
2. **Decoding**: Extracts the text message from the image.

## Installation

To use the program, you need Python 3.x and a few libraries. Install the required libraries using `pip`:

```sh
pip install numpy pillow matplotlib
```

## Usage

### Encoding a Message

To encode a message into an image, use the encode command and pass the message and the path to save the image (optional):

```sh
python image_decoder.py encode --message "Your message here" --output_path "/path/to/save/image.png"
```

### Decoding 

To decode an image back into a text message, use the decode command and pass the path to the image:

```sh 
python image_decoder.py decode --image_path "/path/to/your/image.png"
```

### Encoding 'Hello World' message
<div align="center"> <img src="Text_to_Pic-coder/coder.py" alt="HelloWorld Image" width="400"/> </div>