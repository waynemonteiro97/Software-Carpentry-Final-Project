'''
Final Software Carpentry Project
Contributors - Prabhjot K. Luthra, Wayne D. Monteiro
***** Welcome to the Shortest-Path-Finder/Optimzer *****
Here we ask the user to give us the location or the place where
he or she is and the zoom level on google maps
This code then first gets the image through the Google API.
Then this image is converted to a grid or more specifically
a maze, where in only the white roads and yellow highways are the
valid paths. Once we get the grid, we ask the user to enter the
start and all the end points through clicking on the image at those
points (the image window pops up and can be closed by pressing the
Esc Key). Once the start and all the end points are recorded, then
the shortest path is calculated using the breadth for search alogorithm,
which is written as Gri_Solver_2.py and imported as a class Grid.
The function shortest_path() of this Grid Class returns the shortest
distance between the two points and returns the endpoint it reached first
from the list of endpoints and the path ir took to reach there. We carry
this out till the end point list is empty i.e all the end points are
reached. We then save this path so followed as a GIF! Additionally, we
then ask the user if he wants to find a shorter path i.e which point
should we remove so that the reduction is most. And if the user wants
he can use this as his final solution or keep his original one!

Further we this has the potential to be a back end code for
websites and apps that utilize this function. Apps like
Uber Pool or even JHU Night Ride Shuttle can use this to go
through the smallest distance and drop everyone! (Saving fuel!)
'''
from PIL import Image, ImageDraw
from Grid_Solver_2 import Grid
from Comparison_EndPts import Compare
from Cost_Analysis import Cost_Analysis
import copy
import shutil
import matplotlib.pyplot as plt
import mpldatacursor
import requests
import warnings
import cv2
import time

TET = 0
# TET is Terrestial Land (No Roads)
ROAD = 1
PATH_FOllOWED = 2
STARTPOINT = 3
ENDPOINT = 4
point_list = []

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


def save_as_grid(grid, basename, blockSize=90):
    '''
    This function will save the grid as an image file
    ** Parameters**
    grid : List- *int*
        List of lists containing the corresponding value of a path
    blockSize : *int*
        Number of pixels that fit into a block
    basename : *str*
        Name of grid
    ** Returns **
    Nothing!
    '''
    w_blocks = len(grid[0])
    h_blocks = len(grid)
    SIZE = (w_blocks * blockSize, h_blocks * blockSize)
    img = Image.new("RGB", SIZE, color=COLORS[TET])

    for y, row in enumerate(grid):
        for x, block_ID in enumerate(row):
            set_color(img, x, y, blockSize, COLORS[block_ID])

    img.save("%s_recreated_grid.png"
             % (basename.strip(".png")))


def img_to_grid(filename):
    '''
    This function will convert the image to a Grid
    so that we use that for the shortest path calculator
    ** Parameters **
    filename : *str*
                Name of the image file
    ** Returns **
    new_arr : List of Lists - *int*
            This is the grid so formed
    '''
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
            if (253 <= pxl[0] <= 257 and 253 <= pxl[1] <= 257 and 253 <= pxl[2] <= 257 ) or (245 <= pxl[0] <= 255 and 220 <= pxl[1] <= 245 and 100 <= pxl[2] <= 180 ):
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
                if avg_sum == 0:
                    new_arr[newy][newx] = 0
                else:
                    new_arr[newy][newx] = 1
            newx = newx + 1
        newy = newy + 1

    filename = filename.strip(".png")
    save_as_grid(new_arr, filename, blockSize=5)
    fptr_2 = filename + "_black&white.png"
    IMG.save(fptr_2)

    img.close()
    IMG.close()

    return(new_arr)


def locate_map(location, zoom):
    '''
    This function get the Google Maps Image
    from the location and zoom level entered by the user
    ** Parameter **
    location : *str*
             Name of the location
    zoom : *int*
        Zoom level
    ** Returns **
    Name of the image file
    as location + "_image_without_label.png"
    '''
    api_key = "AIzaSyAJhA7-eaS4nEkNwJ9dktMnpnbZ4sFaaoA"
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


def open_img(location):
    '''
    This function is to pop up the image in a window
    and save the start and end points so clicked by the user
    on the image as a list. Once the user presses the Esc key
    they image window is closed.
    https://stackoverflow.com/questions/28327020/opencv-detect-mouse-position-clicking-over-a-picture
    ** Parameters **
    location : *str*
             location so chosen by the user
    ** Returns **
    Nothing!
    '''
    point_list = []
    filename = location + "_image_with_label.png"

    def onMouse(event, x, y, flags, param):
        global point_list
        if event == cv2.EVENT_LBUTTONDOWN:
            print("Point Recorded")
            cv2.circle(im, (x, y), 100, (255, 0, 0), -1)
            point_list.append((x, y))

    im = cv2.imread(filename)
    cv2.namedWindow("Map")
    cv2.setMouseCallback("Map", onMouse)

    while True:
        im = cv2.imread(filename)
        cv2.imshow("Map", im)
        k = cv2.waitKey(20) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()


def save_as_GIF(location, path_followed):
    '''
    This function is to save the path so followed
    or the solution of the path optimizer as a GIF!
    ** Parameters **
    location : *str*
             The location so chosen by the user
    path_followed : List - *int*
             Shortest path so followed to reach all
             end points
    ** Returns **
    Nothing! 
    '''
    images = []
    basename = location + "_image_with_label.png"
    shutil.copy(basename, basename.strip(".png") + "_trial.png")
    basename = basename.strip(".png") + "_trial.png"
    f_img = Image.open(basename).convert("RGB")
    for ele in path_followed:
        if ele in end_pt_list:
            x = round(2 * ele[1])
            y = round(2 * ele[0])
            f_img = Image.open(basename).convert("RGB")
            draw = ImageDraw.Draw(f_img)
            draw.ellipse((x-4, y-4, x+4, y+4), fill = 'GREEN', outline = 'blue' )
            f_img.save(basename)
            images.append(f_img)
        elif ele == start_pt_list:
            x = round(2 * ele[1])
            y = round(2 * ele[0])
            f_img = Image.open(basename).convert("RGB")
            draw = ImageDraw.Draw(f_img)
            draw.ellipse((x-4, y-4, x+4, y+4), fill = 'RED', outline = 'RED' )
            f_img.save(basename)
            images.append(f_img)
        else:
            x = round(2 * ele[1])
            y = round(2 * ele[0])
            f_img = Image.open(basename).convert("RGB")
            draw_path = ImageDraw.Draw(f_img)
            draw_path.ellipse((x-1, y-1, x+1, y+1), fill = (154, 205, 50) )
            f_img.save(basename)
            images.append(f_img)
    images[0].save(basename.strip(".png") + "_solution.gif", save_all=True, append_images=images[1:], optimize=False, duration=60, loop=0)


def mpl_cursor_verify(location):
    '''
    This is to verify if the coordinates we get from user clicks
    is the same s the coordinates we get from hovering the mouse over
    that point in that image using a mpldatacursor (mostly used for plots)
    ** Parameters **
    location : *str*
             The location so chosen by the user
    ** Returns **
    Nothing!
    '''
    im = plt.imread(location + "_image_with_label.png")
    plt.imshow(im)
    warnings.filterwarnings("ignore")
    mpldatacursor.datacursor(hover=True, bbox=dict(alpha=1, fc='w'), formatter="Here".format)
    plt.show()


def get_final_path(grid_from_img, start_pt, end_pt):
    '''
    As discussed in the objective of this project we first find the
    shortest distance between two points which is at first the start and
    any of the end points which is reached first. Now for the next piece of the
    final path this end point becomes the new start point and again you repeat
    the procedure for findining the shortest path between two points. This is
    repeated until the list of end points is empty i.e all the end points are
    visited.
    ** Parameters **
    grid_from_img : List of Lists : *int*
                   Grid we got from the image
    start_pt : Tuple : *int*
            Start point so selected by the user
    end_pt : List of tuples : *int*
             List of all end points selected by the user
    ** Returns **
    ITER : *int*
         Number of iterations took to reach all end points
    path_followed : List of tuples : *int*
         Path so followed to get the shortest distance between the start
         and all end points
    '''
    path_followed = []
    ITER = 0
    while len(end_pt) != 0:
        grid = Grid(grid_from_img, start_pt, end_pt)
        new_origin, path_followed_new = grid.shortest_path()
        path_followed += list(reversed(path_followed_new))
        start_pt = new_origin
        ITER += 1

    return(ITER, path_followed)


if __name__ == "__main__":
    # 1. To get the location and zoom amount from the user
    '''
    Try with
    location = Johns Hopkins University
    zoom = 15
    '''
    print("********** Welcome to Shortest Path Optimizer **********")
    print("\n" + "-" * 79)
    location = input("Where do you want to go? (Type in the location) : ")
    if location == '':
        print("Invalid Location")
    try:
        zoom = int(input("How close?! (Type in the zoom amount): "))
    except ValueError:
        print("Invalid zoom")

    # 2. To get the image of the location using Google API
    basename = locate_map(location, zoom)

    # 3. Convert the image to a grid with white as valid paths
    grid_from_img = img_to_grid(basename)

    # Get the start and end points
    print("\n" + "-" * 79)
    print("First step successful! Grid created from the Image of the location!")
    print("Left Click on the start point first, then all end points")
    print("Once done, Press Esc Key!")
    time.sleep(5)
    open_img(location)
    if len(point_list) == 0 or len(point_list) == 1:
        raise Exception("Insufficient Number of Points")
    start_pt = (int(point_list[0][1] / 2), int(point_list[0][0] / 2))
    end_pt = []
    for i in range(len(point_list)):
        if i != 0:
            end_pt.append((int(point_list[i][1] / 2), int(point_list[i][0] / 2)))
    print("\n" + "-" * 79)
    print("Second step successful! Start and End points Recorded !!")
    start_pt_list = copy.deepcopy(start_pt)
    end_pt_list = copy.deepcopy(end_pt)

    '''
    # Using MPL Data Cursor to verify coordinates
    verify_ans = input("Do you want to verify these coordinates (Y/N)? ")
    if verify_ans == 'Y':
        mpl_cursor_verify(location)
    '''

    # 4. To get the shortest path from the start to all end points
    MAXITER = len(end_pt) + 1
    ITER, path_followed = get_final_path(grid_from_img, start_pt, end_pt)
    if ITER <= MAXITER:
        print("\n" + "-" * 79)
        print("Congratulations SOLUTION FOUND")

        # 5. Saving the solution as a GIF
        save_as_GIF(location, path_followed)
        print("Solution saved as a GIF! Check your folders!")
    else:
        print("Sorry could not find the solution!")

    # 6. Ask and compute if shorter path required
    Cost_1 = Cost_Analysis(path_followed, zoom)
    distance_travel, fuel_amount, fuel_cost_original = Cost_1.cost_analysis()
    print("\n" + "-" * 79)
    print("The Fuel Cost Analysis include : ")
    print("Distance travelled : ", distance_travel)
    print("Amount of fuel consumed : , ", fuel_amount)
    print("Fuel Cost : ", fuel_cost_original)

    print("\n" + "-" * 79)
    comp_ans = input("Do you want to get even a shorter path (Y/N)? ")

    if comp_ans.lower() == "y":
        Path_Compare = Compare(grid_from_img, path_followed, start_pt_list, end_pt_list)
        ele, reduction, path = Path_Compare.max_reduce()
        Cost_2 = Cost_Analysis(path, zoom)
        distance_travel, fuel_amount, fuel_cost_new = Cost_2.cost_analysis()
        print("\n" + "-" * 79)
        print("The new Fuel Cost Analysis include : ")
        print("Distance travelled : ", distance_travel)
        print("Amount of fuel consumed : ", fuel_amount)
        print("Fuel Cost : ", fuel_cost_new)

        if reduction == 0:
            print("Could not find a much shorter path! Sorry!")
        else:
            end_pt_list.remove(ele)
            reduction = str(round(reduction, 2))
            print("Reduction % = ", reduction)
            print("\n" + "-" * 79)
            save_ans = input("Do you want to save the new path as your final path (Y/N)? ")
            if save_ans.lower() == 'y':
                save_as_GIF(location, path)
                print("Same file overwritten! Check your folders!")
            elif save_ans.lower() == 'n':
                pass
            else:
                raise Exception("Invalid Input")

    elif comp_ans.lower() == 'n':
        pass
    else:
        raise Exception("Invalid Input")
