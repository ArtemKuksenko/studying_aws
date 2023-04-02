from io import BytesIO

from PIL import Image


def process_image(file: bytes):
    image = Image.open(BytesIO(file))
    frames = [
        image.rotate(degree)
        for degree in range(0, 360, 10)
    ]
    frame_one = frames[0]
    res_image = BytesIO()
    frame_one.save(
        "my_awesome.gif", format="GIF", append_images=frames, save_all=True, duration=20, loop=0
    )
    frame_one.save(
        res_image, format="GIF", append_images=frames, save_all=True, duration=20, loop=0
    )
    # rotated_image = image.rotate(180)
    # rotated_image.save("geeks.jpg")
