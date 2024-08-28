from pydantic import BaseModel, Field, validator
from enum import Enum
from PIL import Image
from azure.functions import InputStream

class FilterType(str, Enum):
    SEPIA = "sepia"
    GRAYSCALE = "grayscale"
    # Add more filter types as needed

class FilterRequest(BaseModel):
    filter: FilterType
    image_data: InputStream

    #Prevents consumers from having to call with {"filter": "FilterType.SEPIA"}
    #Instead they can just do {"filter": "sepia"}
    class Config:
        use_enum_values = True 
        arbitrary_types_allowed = True

    @validator('image_data')
    def validate_image(cls, v: InputStream):
        if not v:
            raise ValueError('No image data provided')
        
        try:
            # Open the image using PIL
            image = Image.open(v)
            image_format = image.format.lower()
            if image_format not in {'jpeg', 'jpg', 'png'}:
                raise ValueError('Invalid file type. Only JPG and PNG are allowed.')
        except Exception as e:
            raise ValueError(f"Invalid image file. Error: {e}")
        finally:
            # Reset the stream position
            v.seek(0)
        
        return v

# TODO Add these models later for consistency, documentation, an serialization
# class FilterResponse(BaseModel):
#     status: str
#     filtered_image_url: InputStream

# class ErrorResponse(BaseModel):
#     error: str
