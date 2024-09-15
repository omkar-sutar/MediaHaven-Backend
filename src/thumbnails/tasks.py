from PIL import Image, ImageOps
from moviepy.editor import VideoFileClip
import os
from src import env
from utils import get_logger

THUMBNAIL_SIZE=200,200
TMP_DIR="tmp"

image_extensions = [".jpg", ".png",".dng"]
video_extensions = [".mp4",".mkv"]

logger = get_logger()

def transform_filename(filename:str):
    return filename+".jpg"

def generate_image_thumbnail(image_path:str,thumbnails_dir:str):
    filename = os.path.basename(image_path)
    with Image.open(image_path) as img:
        # Sometimes image rotation info is stored at exif
        # Transform the image appropriately, by default pillow doesn't do it
        img = ImageOps.exif_transpose(img)
        img.thumbnail(THUMBNAIL_SIZE)
        new_filename=transform_filename(filename)
        img.save(os.path.join(thumbnails_dir,new_filename),format="jpeg")

def compress_image(image_path:str,quality)->str:
    filename = os.path.basename(image_path)
    parent_dir=os.path.dirname(image_path)
    is_image=filename.endswith(tuple(image_extensions))
    new_path = os.path.join(parent_dir,TMP_DIR,f"{quality}-{filename}")     # Quality-filename, for caching according to quality
    if os.path.exists(new_path):
        logger.debug("Compressed image already exists")
        return new_path

    if not is_image:
        raise ValueError("Invalid image")
    with Image.open(image_path) as img:
        # Sometimes image rotation info is stored at exif
        # Transform the image appropriately, by default pillow doesn't do it
        img = ImageOps.exif_transpose(img)
        img.save(new_path,quality=quality,optimize=True)
    return new_path

def generate_video_thumbnail(video_path:str,thumbnails_dir:str):
    filename = os.path.basename(video_path)
    with VideoFileClip(video_path) as video:
        imgarr = video.get_frame(0.0)
        img = Image.fromarray(imgarr)

        # Weird behavior of moviepy, for some reason it expands portrait videos
        # to make it appear like landscape
        # i.e. its resolution is interchanged (w,h->h,w)
        # Portrait videos have .rotation=90 or 270
        # resize image for such thumbnails
        # See https://github.com/Zulko/moviepy/pull/529
        # https://stackoverflow.com/questions/41200027/how-can-i-find-video-rotation-and-rotate-the-clip-accordingly-using-moviepy#comment87514785_41588571
        
        if video.rotation==90 or video.rotation==270:
            img = img.resize((img.size[1],img.size[0]))

        img.thumbnail(THUMBNAIL_SIZE)
        new_filename=transform_filename(filename)
        img.save(os.path.join(thumbnails_dir,new_filename),format="jpeg")

def generate_thumbnail(media_path:str)->bool:
    """
    Generates thumbnail of given media.
    Raise exception if media type is not supported.
    """
    parent_dir=os.path.dirname(media_path)
    thumbnails_dir=os.path.join(parent_dir,os.getenv(env.THUMBNAIL_DIR))

    for suffix in image_extensions:
        if media_path.endswith(suffix):
            return generate_image_thumbnail(media_path,thumbnails_dir)
    for suffix in video_extensions:
        if media_path.endswith(suffix):
            return generate_video_thumbnail(media_path,thumbnails_dir)
    #raise Exception("Invalid media type")
        
def generate_thumbnails_bulk(media_dir:str,override=False):
    """
    Generates thumbnails for medias at given path.
    If override=True, regenerates thumbnails.
    """
    files = os.listdir(media_dir)
    for file in files:
        if os.path.isdir(os.path.join(media_dir,file)):
            continue
        if not os.path.isfile(os.path.join(media_dir,os.getenv(env.THUMBNAIL_DIR),os.path.basename(transform_filename(file)))) or override:
            generate_thumbnail(os.path.join(media_dir,file))
