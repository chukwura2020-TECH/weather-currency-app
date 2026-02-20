# gui/utils/icon_loader.py

from PIL import Image, ImageTk


def load_icon(path, size, color=None):
    """
    Load a PNG icon, optionally recolor it, resize it,
    and return a Tkinter PhotoImage.

    Args:
        path (str): Path to PNG file
        size (int): Target width/height (square)
        color (str|None): Optional hex color like "#ffffff"

    Returns:
        ImageTk.PhotoImage
    """

    # Load image with alpha
    image = Image.open(path).convert("RGBA")

    # Resize using high-quality resampling
    image = image.resize((size, size), Image.LANCZOS)

    # Optional recoloring (for white template icons)
    if color:
        r, g, b = tuple(int(color[i:i + 2], 16) for i in (1, 3, 5))

        pixels = image.load()
        for y in range(image.height):
            for x in range(image.width):
                pr, pg, pb, pa = pixels[x, y]
                if pa > 0:  # preserve transparency
                    pixels[x, y] = (r, g, b, pa)

    return ImageTk.PhotoImage(image)