from wand.image import Image

def apply_filter_to_image(image, filter):
    with Image(blob=image) as img:
        # Resize the image by 50%
        img.resize(int(img.width * 0.5), int(img.height * 0.5))
        
        # Rotate the image by 90 degrees
        img.rotate(90)
        
        # Apply a sepia tone with an 80% threshold
        img.sepia_tone(threshold=0.8)
        
        # Return the modified image data as a byte stream
        return img.make_blob()