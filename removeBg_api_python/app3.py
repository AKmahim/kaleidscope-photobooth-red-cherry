# ==========================
# add glow effect on the image and for dslr camera

import os
import io
from flask import Flask, request, jsonify
from PIL import Image, ImageFilter
from rembg import remove
from flask_cors import CORS
import base64
from capture import func_TakeNikonPicture

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#overlay watermark
def add_watermark(input_image_path, watermark_image_path, output_image_path):
    # Open the original image
    base_image = Image.open(input_image_path)
    base_width, base_height = base_image.size

    # Open the watermark image
    watermark = Image.open(watermark_image_path)
    watermark_width, watermark_height = watermark.size

    # Calculate position for the watermark: bottom center
    position = ((base_width - watermark_width) // 2, base_height - watermark_height-200)

    # Create a transparent layer the size of the base image
    transparent = Image.new('RGBA', (base_width, base_height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, position, mask=watermark)

    # Convert to RGB mode and save the result
    result = transparent.convert('RGB')
    result.save(output_image_path)


def remove_bg(input_path):
    with open(input_path, "rb") as inp_file:
        img = remove(inp_file.read())
        print('remove bg okay')
        return img

def add_glow_effect(image_data):
    image = Image.open(io.BytesIO(image_data))
    glow = image.filter(ImageFilter.GaussianBlur(radius=100))  # Adjust the radius for the glow effect
    # Composite the original image with the glow effect
    glow = Image.composite(image, glow, image)
    return glow

def overlay_img(overlay_image, background_image_path, position, size):
    background_image = Image.open(background_image_path)
    # watermark_image = Image.open('output2.png')
    overlay_image = overlay_image.resize(size)
    background_image.paste(overlay_image, position, overlay_image)
    # background_image.paste(watermark_image, position, overlay_image)
    return background_image

# def overlay_img(main_image, background_image_path, main_position, main_size, watermark_image_path, watermark_position):
#     background_image = Image.open(background_image_path)
#     main_image = main_image.resize(main_size)
#     background_image.paste(main_image, main_position, main_image)
    
#     # Open the watermark image
#     watermark_image = Image.open(watermark_image_path)
#     # Resize the watermark image if necessary
#     watermark_image = watermark_image.resize((int(main_size[0] * 0.1), int(main_size[1] * 0.1)))  # Example resizing, adjust as needed
    
#     # Calculate the position for the watermark to be at the bottom
#     watermark_x_position = main_position[0]
#     watermark_y_position = main_position[1] + main_size[1]  # Position below the main image
    
#     # Paste the watermark image onto the background
#     background_image.paste(watermark_image, (watermark_x_position, watermark_y_position), watermark_image)
    
#     return background_image

@app.route('/', methods=['GET'])
def index():
    return jsonify({'status': 'okay'})

@app.route('/process_image', methods=['GET'])
def process_image():
    # if 'image' not in request.files:
    #     return "No file part", 400

    # file = request.files['image']

    # if file.filename == '':
    #     return "No selected file", 400

    # if file:
    # inputFileName = 'input_img.jpg'
    # filename = os.path.join(app.config['UPLOAD_FOLDER'], inputFileName)
    # file.save(filename)

    position = (-500, 900) # (x,y) 
    size = (1920, 1080)

    filename = func_TakeNikonPicture()

    img_without_bg = remove_bg(filename)

    # Add glow effect
    img_with_glow = add_glow_effect(img_without_bg)

    # Overlay the processed image on a background
    result_image = overlay_img(img_with_glow, 'bg.jpg', position, size)
    # result_image = overlay_img(img_with_glow, 'output1.jpg', position, size, 'output2.png', (position[0], position[1] + size[1]))

    result_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'result.jpg')
    
    # Save the image with compression
    result_image.save(result_filename, 'JPEG', quality=100)  # Adjust the quality as needed (0-100)

    # applying overlay
    add_watermark('uploads/result.jpg', 'watermark.png', 'uploads/result.jpg')
    # Convert the result image to base64
    with open(result_filename, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    return jsonify({'image': base64_image})

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
