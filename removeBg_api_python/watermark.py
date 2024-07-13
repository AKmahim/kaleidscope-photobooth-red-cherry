from PIL import Image

def add_watermark(input_image_path, watermark_image_path, output_image_path):
    # Open the original image
    base_image = Image.open(input_image_path)
    base_width, base_height = base_image.size

    # Open the watermark image
    watermark = Image.open(watermark_image_path)
    watermark_width, watermark_height = watermark.size

    # Calculate position for the watermark: bottom center
    position = ((base_width - watermark_width) // 2, base_height - watermark_height)

    # Create a transparent layer the size of the base image
    transparent = Image.new('RGBA', (base_width, base_height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, position, mask=watermark)

    # Convert to RGB mode and save the result
    result = transparent.convert('RGB')
    result.save(output_image_path)

# Example usage:
input_image = 'result.jpg'  # Replace with your input image file name
watermark_image = 'watermark.png'  # Replace with your watermark image file name
output_image = 'new-image.jpg'

add_watermark(input_image, watermark_image, output_image)

