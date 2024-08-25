from rembg import remove
from PIL import Image

def remove_background(input_image_path: str, output_image_path: str = "uploads/without_bg.png"):
    with open(input_image_path, "rb") as input_file:
        input_data = input_file.read()
        output_data = remove(input_data)
    
    with open(output_image_path, "wb") as output_file:
        output_file.write(output_data)

# Example usage
remove_background("demo.jpg")