from io import BytesIO
from PIL import Image


def rotate_image(file: bytes) -> BytesIO:
    image = Image.open(BytesIO(file))
    frames = [image for _ in range(9)] + [
        image.rotate(degree)
        for degree in range(0, 360, 10)
    ]
    res_image = BytesIO()
    frames[0].save(
        res_image, format="GIF", append_images=frames, save_all=True, duration=40, loop=0
    )
    res_image.seek(0)  # reset the buffer to start
    return res_image
