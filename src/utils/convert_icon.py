from PIL import Image
import os

def convert_to_ico(input_path, output_path):
    # Open the image
    img = Image.open(input_path)
    
    # Convert to RGBA if not already
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Create icon sizes
    sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
    img.save(output_path, format='ICO', sizes=sizes)

# Convert the image
convert_to_ico('corgi-helper.jpg', 'corgi-helper.ico')
print("Icon conversion complete!") 