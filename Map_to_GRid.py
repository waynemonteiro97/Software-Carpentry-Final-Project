'''
Final Software Carpentry Project
Contributors - Prabhjot K. Luthra, Wayne D. Monteiro
Convert the given Google Map Image into Grid
with just the roads
'''
from PIL import Image
from Grid_Solver_2 import Grid
import copy

TET = 0
ROAD = 1
PATH_FOllOWED = 2
STARTPOINT = 3
ENDPOINT = 4

COLORS = {
    TET: (0, 0, 0),
    ROAD: (255, 255, 255),
    STARTPOINT: (255, 0, 0),
    ENDPOINT: (0, 0, 255),
    PATH_FOllOWED: (0, 255, 0)

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


def save_as_grid(maze, basename, blockSize=90):
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
    img = Image.new("RGB", SIZE, color=COLORS[TET])

    for y, row in enumerate(maze):
        for x, block_ID in enumerate(row):
            set_color(img, x, y, blockSize, COLORS[block_ID])

    img.save("%s_recreated_grid.png"
             % (basename.strip(".png")))


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
    new_arr = [[0 for i in range(0, width, 2)] for j in range(0, height, 2)]
    avg_sum_store = []
    newy = 0
    for y in range(0, height, 2):
        newx = 0
        for x in range(0, width, 2):
            sum_val = 0
            if x != width - 1 and y != height - 1:
                for b in range(2):
                    for a in range(2):
                        val = IMG.getpixel((x + a, y + b))
                        sum_val = sum_val + val[0] + val[1] + val[2]
                avg_sum = sum_val / (4 * 3)
                avg_sum_store.append(avg_sum)
                if avg_sum < 42.5:
                    new_arr[newy][newx] = 0
                else:
                    new_arr[newy][newx] = 1
            newx = newx + 1
        newy = newy + 1
    filename = filename.strip(".png")
    save_as_grid(new_arr, filename, blockSize=5)
    fptr_2 = filename + "_black&white.png"
    IMG.save(fptr_2)
    return(new_arr)


def locate_map(location, zoom):

    api_key = "...."
    url = "http://maps.googleapis.com/maps/api/staticmap?"
    center = location
    r = requests.get("https://maps.googleapis.com/maps/api/staticmap?key="+api_key+"&center="+location+"&zoom="+str(zoom)+"&format=png&maptype=roadmap&style=element:labels%7Cvisibility:off&style=feature:administrative.land_parcel%7Cvisibility:off&style=feature:administrative.neighborhood%7Cvisibility:off&size=1230x1230")
    s = requests.get("https://maps.googleapis.com/maps/api/staticmap?key="+api_key+"&center="+location+"&zoom="+str(zoom)+"&format=png&maptype=roadmap&size=1230x1230")
    f = open(location + "_image_without_label.png", "wb")
    f.write(r.content)
    f.close()
    g = open(location + "_image_with_label.png", "wb")
    g.write(s.content)
    g.close()
    return (location + "_image_without_label.png")


if __name__ == "__main__":
    basename = "trial_image.png"
    # basename = locate_map('Udupi', 15)
    grid_from_img = img_to_grid(basename)
    print("Grid Generated")
    '''
    grid_from_img[313][82] = 3 # Charm City Cakes
    grid_from_img[320][115] = 3 # PaperMoon Dinner
    grid_from_img[224][197] = 3 # Chipotle
    grid_from_img[190][147] = 3 # BLC
    grid_from_img[193][163] = 3 # East Gate
    grid_from_img[205][324] = 3 # Giant Food
    grid_from_img[150][194] = 3 # Marylander
    grid_from_img[251][144] = 3 # BMA
    grid_from_img[99][140] = 3 # North Gate
    save_as_grid(grid_from_img, "modified_trial", blockSize=10)
    '''
    start_end_choices = {'1': "North Gate", '2': "BLC", '3': "East Gate",
                         '4': "Marylander", '5': "Chipotle", '6': "Giant Food",
                         '7': "BMA", '8': "PaperMoon Diner", '9': "Charm City Cakes"}
    start_end_coord = {'1': (99, 140), '2': (190, 147), '3': (193, 163),
                       '4': (150, 194), '5': (224, 197), '6': (205, 324),
                       '7': (251, 144), '8': (320, 115), '9': (313, 882)}
    print("Choices for start and end Points are : ")
    print(start_end_choices)
    start_choice = input("Enter choice for start point")
    start_pt = start_end_coord[start_choice]
    end_pt = []
    n = int(input("Number of end points"))
    print("Enter choice for end points")
    choice = None
    for i in range(n):
        choice = input()
        end_pt.append(start_end_coord[choice])
    print("Start and End points Recorded")
    start_pt_list = copy.deepcopy(start_pt)
    end_pt_list = copy.deepcopy(end_pt)
    path_followed = []
    MAXITER = len(end_pt) + 1
    ITER = 0
    while len(end_pt) != 0:
        grid = Grid(grid_from_img, start_pt, end_pt)
        new_origin, path_followed_new = grid.shortest_path()
        path_followed += list(reversed(path_followed_new))
        start_pt = new_origin
        ITER += 1
    images = []
    basename = "trial_image_with_labels.png"
    if ITER <= MAXITER:
        print("Congo")
        # font = ImageFont.truetype("arial.pil", 8)
        for ele in path_followed:
            if ele in end_pt_list:
                x = round(2 * ele[1])
                y = round(2 * ele[0])
                f_img = Image.open(basename).convert("RGB")
                f_img.putpixel((x, y), (255, 0, 0))
                # draw = ImageDraw.Draw(f_img)
                # draw.point((x, y), (255, 0, 0))
                # draw.text((x - 1, y - 1), ele, (255, 255, 255), font=font)
                f_img.save(basename)
                images.append(f_img)
            elif ele == start_pt_list:
                x = round(2 * ele[1])
                y = round(2 * ele[0])
                f_img = Image.open(basename).convert("RGB")
                f_img.putpixel((x, y), (0, 255, 0))
                # draw = ImageDraw.Draw(f_img)
                # draw.point((x, y), (0, 255, 0))
                f_img.save(basename)
                images.append(f_img)
            else:
                x = round(2 * ele[1])
                y = round(2 * ele[0])
                f_img = Image.open(basename).convert("RGB")
                f_img.putpixel((x, y), (0, 0, 0))
                f_img.save(basename)
                images.append(f_img)
        images[0].save(basename.strip(".png") + "_solution.gif", save_all=True, append_images=images[1:], optimize=False, duration=60, loop=0)
        print("Image saved")
    else:
        print("Fail")