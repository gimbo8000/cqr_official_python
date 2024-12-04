from math import ceil, sqrt
from PIL import Image, ImageDraw

# NULL_BLOCK ASCII value
NULL_BLOCK = chr(26)

def get_color_chunk(url, index):
    chunk = url[index:index + 3]
    chunk += NULL_BLOCK * (3 - len(chunk))  # Pad with NULL_BLOCK if needed
    r = ord(chunk[0]) % 256
    g = ord(chunk[1]) % 256
    b = ord(chunk[2]) % 256
    return (r, g, b)

def create_snaking_qr_grid(url):
    url_length = len(url)
    required_cells = ceil(url_length / 3) + 3  # Add 3 for reserved corner cells
    grid_size = ceil(sqrt(required_cells))  # Ensure grid is large enough
    cell_size = 50
    img_size = grid_size * cell_size

    img = Image.new("RGB", (img_size, img_size), "white")
    draw = ImageDraw.Draw(img)

    # Corner markers
    corners = {
        (0, 0): (0, 255, 0),
        (0, grid_size - 1): (255, 0, 0),
        (grid_size - 1, 0): (255, 255, 0),
    }

    # Generate snaking coordinates
    coordinates = []
    for row in range(grid_size - 1, -1, -1):
        if (grid_size - 1 - row) % 2 == 0:
            coordinates.extend([(row, col) for col in range(grid_size - 1, -1, -1)])
        else:
            coordinates.extend([(row, col) for col in range(grid_size)])

    # Fill the grid
    index = 0
    for coord in coordinates:
        row, col = coord
        if (row, col) in corners:
            color = corners[(row, col)]
        else:
            if index < len(url):
                color = get_color_chunk(url, index)
                index += 3
            else:
                color = (ord(NULL_BLOCK), ord(NULL_BLOCK), ord(NULL_BLOCK))  # Fill remaining with NULL_BLOCK

        x0 = col * cell_size
        y0 = row * cell_size
        x1 = x0 + cell_size
        y1 = y0 + cell_size
        draw.rectangle([x0, y0, x1, y1], fill=color)

    return img

def main():
    url = input("Enter a URL: ")
    grid_image = create_snaking_qr_grid(url)
    grid_image.show()
    grid_image.save("null_block_qr_grid.png")

if __name__ == "__main__":
    main()