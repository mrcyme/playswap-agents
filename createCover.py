from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import random
import math

def add_rectangle_and_text(image_url, output_image, font_path, text):
    # Fetch the image from the URL
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    
    # Define the dimensions and position of the rectangle
    rect_width = img.width
    rect_height = img.height
    rect_x = 0
    rect_y = 0

    # Create a new image for the rectangle
    rect_img = Image.new('RGBA', (rect_width, rect_height), (0, 0, 0, 255))
    draw_rect = ImageDraw.Draw(rect_img)

    # Define the font for the text
    font = ImageFont.truetype(font_path, 40)

    # Get text width and height
    text_width, text_height = draw_rect.textsize(text, font=font)
    
    # Calculate the x, y coordinates of the text
    text_x = (rect_width - text_width) // 2
    text_y = (rect_height - text_height) // 2
    
    # Place the text on the rectangle image
    draw_rect.text((text_x, text_y), text, fill="white", font=font)
    
    # Randomly tilt the rectangle image
    tilt_angle = - random.randint(3, 10)

    rotated_rect = rect_img.rotate(tilt_angle, expand=1, center=(rect_width//2, rect_height//2))
    new_rect_x = 0
    new_rect_y = 300
    
    # Paste the rotated rectangle onto the original image
    img.paste(rotated_rect, (new_rect_x, new_rect_y), rotated_rect)
    
    # Paste the rotated rectangle onto the original image
    img.paste(rotated_rect, (rect_x, rect_y), rotated_rect)
    
    # Save the resulting image
    img.save(output_image)


if __name__ == "__main__":
    input_image_path = "https://i1.sndcdn.com/artworks-pIXpVdIKMRx0cicf-4PzCpA-t500x500.jpg"
    output_image_path = "./image.jpg"
    font_path = "C:\WINDOWS\FONTS\AGENCYR.TTF" # Change this to the path of your font
    text_to_add = "Your Text Here"

    add_rectangle_and_text(input_image_path, output_image_path, font_path, text_to_add)
