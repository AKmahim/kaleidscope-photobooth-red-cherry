# ==========================================================================================
# ================== this is for ivcam ===============================================
# ==========================================================================================

import os
import io
from flask import Flask, request, jsonify
from PIL import Image
from rembg import remove
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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


# def remove_bg(input_path):
#     with open(input_path, "rb") as inp_file:
#         img = remove(inp_file.read())
#         print('remove bg okay')
#         return img

def remove_background(input_image_path: str, output_image_path: str = "uploads/without_bg.png"):
    with open(input_image_path, "rb") as input_file:
        input_data = input_file.read()
        output_data = remove(input_data)
    
    with open(output_image_path, "wb") as output_file:
        output_file.write(output_data)


def overlay_img(overlay_image, background_image_path, position, size):
    background_image = Image.open(background_image_path)
    overlay_image = Image.open(io.BytesIO(overlay_image))
    overlay_image = overlay_image.resize(size)
    background_image.paste(overlay_image, position, overlay_image)
    return background_image

@app.route('/', methods=['GET'])
def index():
    return jsonify({'status': 'okay'})

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return "No file part", 400

    file = request.files['image']

    if file.filename == '':
        return "No selected file", 400

    if file:
        inputFileName = 'input_img.jpg'
        filename = os.path.join(app.config['UPLOAD_FOLDER'], inputFileName)
        file.save(filename)

        # position = (-300, 400)
        # scale = 100
        # height = 960 + scale
        # width = 1280 + scale
        # height = 720 + scale
        # width = 1280 + scale
        # size = (width, height)

        # img_without_bg = remove_bg(filename)
        remove_background("uploads/input_img.jpg")


        # result_image = overlay_img(img_without_bg, 'bg2.jpg', position, size)

        # result_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'result.jpg')

        #added backgrouund 
        add_watermark('bg3.jpg', 'uploads/without_bg.png', 'uploads/result.jpg')

        
        # Save the image with compression
        # result_image.save(result_filename, 'JPEG', quality=100)  # Adjust the quality as needed (0-100)

        # applying overlay
        add_watermark('uploads/result.jpg', 'watermark.png', 'uploads/result.jpg')

        # Convert the result image to base64
        with open('uploads/result.jpg', "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

        return jsonify({'image': base64_image})

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
