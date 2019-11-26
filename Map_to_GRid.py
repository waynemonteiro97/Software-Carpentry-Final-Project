'''
Final Software Carpentry Project
Contributors - Prabhjot K. Luthra, Wayne D. Monteiro
Convert the given Google Map Image into Grid
with just the roads
'''
from PIL import Image

WALL = 0
PATH = 1
VALID_PATH = 2
INVALID_PATH = 3
ENDPOINT = 4

COLORS = {
    WALL: (0, 0, 0),
    PATH: (255, 255, 255),

}


def set_color(img, x0, y0, dim, color):
    '''
    This function will put a colour to a block of pixels
    **Parameters***
    img:
        Points to the image
    x0 : *int*
        the initial x value of the block
    y0 : *int*
        the initial y value of the block
    dim : *int*
        Dimension of the block
    *** Returns***
    None
    '''

    for x in range(dim):
        for y in range(dim):
            img.putpixel(
                (dim * x0 + x, dim * y0 + y),
                color
            )


def save_as_grid(maze, basename, blockSize=20):
    '''
    This function will save the  maze  as an image file
    **Parameters***
    maze: *list* *int*
        List of lists containing the corresponding value of a path
    blockSize : *int*
        Number of pixels that fit into a block
    basename : *str*
        Name of maze
    *** Returns***
    None
    '''
    w_blocks = len(maze[0])
    h_blocks = len(maze)
    SIZE = (w_blocks * blockSize, h_blocks * blockSize)
    img = Image.new("RGB", SIZE, color=COLORS[WALL])

    for y, row in enumerate(maze):
        for x, block_ID in enumerate(row):
            set_color(img, x, y, blockSize, COLORS[block_ID])

    img.save("%s_recreated_grid.png"
             % (basename))


def img_to_grid(filename):
    IMG = Image.open(filename).convert("RGB")
    img = Image.open(filename).convert("RGB")
    width, height = img.size
    # Creating a Black Image
    for x in range(width):
        for y in range(height):
            IMG.putpixel((x, y), (0, 0, 0))
    for y in range(height):
        for x in range(width):
            pxl = img.getpixel((x, y))
            if pxl == (255, 255, 255):
                IMG.putpixel((x, y), (255, 255, 255))
    # Storing as a Grid
    new_arr = [[0 for i in range(0, width, 2)] for j in range(0, height, 3)]
    avg_sum_store = []
    newy = 0
    for y in range(0, height, 3):
        newx = 0
        for x in range(0, width, 2):
            sum_val = 0
            if x != width - 1 and y != height - 1:
                for b in range(3):
                    for a in range(2):
                        val = IMG.getpixel((x + a, y + b))
                        sum_val = sum_val + val[0] + val[1] + val[2]
                avg_sum = sum_val / (6 * 3)
                avg_sum_store.append(avg_sum)
                if avg_sum < 42.5:
                    new_arr[newy][newx] = 0
                else:
                    new_arr[newy][newx] = 1
            newx = newx + 1
        newy = newy + 1
    save_as_grid(new_arr, filename, blockSize=5)
    fptr_2 = filename + "only_white.png"
    IMG.save(fptr_2)
    for i in range(len(new_arr)):
        print(new_arr[i])


if __name__ == "__main__":
    basename = "trial_image.PNG"
    img_to_grid(basename)