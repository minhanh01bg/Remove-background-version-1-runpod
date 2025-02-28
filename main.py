import os
import runpod
from runpod.serverless.utils.rp_validator import validate
from background_removal import extract_object, birefnet
from utils_birefnet import random_string, remove_file
import base64
import io
from PIL import Image
from utils_birefnet import prepare_image_input  
from rp_schemas import INPUT_SCHEMA
from PIL import ImageOps

def main(job):
    job_input = job["input"]
    # validated_input = validate(job_input, INPUT_SCHEMA)

    # if 'errors' in validated_input:
    #     return {"error": validated_input['errors']}
    # job_input = validated_input['validated_input']
    print(job_input.get('input_type'))
    image_data = prepare_image_input(job_input)   
    if image_data is None:
        return {
            "image":'',
            "result_base64":'',
            "mask_base64":'',
            'message':'error input job',
        }
    
    # Processing image
    result, mask = extract_object(birefnet, io.BytesIO(image_data))
    buffered_image = io.BytesIO()
    buffered_mask = io.BytesIO()
    # Save the image and mask into BytesIO objects
    # result.save(buffered_image, format="PNG")
    if "exif" in result.info:
        exif = result.info.get("exif")
        result = ImageOps.exif_transpose(result)
    result.save(buffered_image, format="WebP", lossless=True)
    mask.convert("RGB").save(buffered_mask, format="PNG")
    
    # Encode
    image_base64 = base64.b64encode(buffered_image.getvalue()).decode('utf-8')
    mask_base64 = base64.b64encode(buffered_mask.getvalue()).decode('utf-8')

    # test
    base64_length = len(image_base64) 
    original_size_bytes = base64_length * 3 / 4  # Tính ngược lại kích thước gốc

    # Chuyển đổi sang MB
    original_size_mb = original_size_bytes / (1024 * 1024)

    print(f"Image size: {original_size_mb:.2f} MB")

    return {
        # "mask": base64.b64encode(mask).decode('utf-8'),
        "result_base64":image_base64,
        "mask_base64":mask_base64,
        "message":"Image processed successfully"
    }

runpod.serverless.start({'handler':main})

