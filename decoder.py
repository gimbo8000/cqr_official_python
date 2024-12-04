from PIL import Image

# NULL_BLOCK ASCII value
NULL_BLOCK = chr(26)

def get_chunk_from_color(color, tolerance=10):
    r, g, b = color
    # Adjust the color channels within a certain tolerance
    # Create a function to map the color back to a character chunk
    chunk = chr(max(0, min(255, r))) + chr(max(0, min(255, g))) + chr(max(0, min(255, b)))
    return chunk

def decode_snaking_qr_grid(image_path):
    img = Image.open(image_path)
    pixels = img.load()
    img_size = img.size[0]
    cell_size = 50
    grid_size = img_size // cell_size

    # Generate snaking coordinates
    coordinates = []
    for row in range(grid_size - 1, -1, -1):
        if (grid_size - 1 - row) % 2 == 0:
            coordinates.extend([(row, col) for col in range(grid_size - 1, -1, -1)])
        else:
            coordinates.extend([(row, col) for col in range(grid_size)])

    # Corner positions to skip
    corners = {(0, 0), (0, grid_size - 1), (grid_size - 1, 0)}
    decoded_url = ""

    for row, col in coordinates:
        if (row, col) not in corners:
            x = col * cell_size + cell_size // 2
            y = row * cell_size + cell_size // 2
            color = pixels[x, y]
            chunk = get_chunk_from_color(color)

            # Stop processing if NULL_BLOCK is encountered
            for char in chunk:
                if char == NULL_BLOCK:
                    return decoded_url
                decoded_url += char

    return decoded_url

def main():
    image_path = 'null_block_qr_grid.png'
    decoded_url = decode_snaking_qr_grid(image_path)
    print("Decoded URL:", decoded_url)

if __name__ == "__main__":
    main()