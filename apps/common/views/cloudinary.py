from settings import CLOUDINARY_URL
import cloudinary

cloudinary.config(
    cloud_name=CLOUDINARY_URL.split('@')[1],
    api_key=CLOUDINARY_URL.split(':')[1].strip('//'),
    api_secret=CLOUDINARY_URL.split(':')[2]
)
