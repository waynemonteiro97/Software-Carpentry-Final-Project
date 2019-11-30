# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 14:36:45 2019

@author: Wayne Monteiro
"""

'''
Final Software Carpentry Project
Contributors - Prabhjot K. Luthra, Wayne D. Monteiro
Convert the given Google Map Image into Grid
with just the roads
'''
from PIL import Image
from Grid_Solver import Grid
import requests

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
            if (pxl[0] <= 257 and pxl[0] >= 253 and pxl[1] <= 257 and pxl[1] >= 253 and pxl[2] <= 257 and pxl[2] >= 253) or (pxl[0] <= 255 and pxl[0] >= 245 and pxl[1] <= 245 and pxl[1] >= 220 and pxl[2] <= 180 and pxl[2] >= 100)  :
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
    img.close()
    IMG.close()

    return(new_arr)

def locate_map(location,zoom):

    api_key = "AIzaSyAJhA7-eaS4nEkNwJ9dktMnpnbZ4sFaaoA"
    url = "http://maps.googleapis.com/maps/api/staticmap?"
#    loc  = location
    center = location
#    zoom = zoom
    r = requests.get("https://maps.googleapis.com/maps/api/staticmap?key="+api_key+"&center="+location+"&zoom="+str(zoom)+"&format=png&maptype=roadmap&style=element:labels%7Cvisibility:off&style=feature:administrative.land_parcel%7Cvisibility:off&style=feature:administrative.neighborhood%7Cvisibility:off&size=1230x1230")
    s = requests.get("https://maps.googleapis.com/maps/api/staticmap?key="+api_key+"&center="+location+"&zoom="+str(zoom)+"&format=png&maptype=roadmap&size=1230x1230")
#    print (url +"center="+center+"&zoom="+str(zoom)+"&size=1024x768&key="+api_key)
    f = open(location + "_image_without_label.png","wb")
    f.write(r.content)
    f.close()
    g = open(location + "_image_with_label.png","wb")
    g.write(s.content)
    g.close()
    return (location + "_image_without_label.png")

if __name__ == "__main__":
    basename = locate_map("Udupi",15)    
#    basename = "sample_balt.png"
    grid_from_img = img_to_grid(basename)
#    print("Grid Generated")
#    start_pt = (0, 23)
#    end_pt = [(248, 301)]
#    grid = Grid(grid_from_img, start_pt, end_pt)
#    print("Object formed")
#    result, path_followed = grid.shortest_path()
#    print("Shortest path calculated")
#    filename = basename + "only_white.png"
#    IMG = Image.open(filename).convert("RGB")
#    if result:
#        print("Congo")
#        # print("Path followed : ")
##        print(list(reversed(path_followed)))
#        f_img = Image.open(basename).convert("RGB")
#        for i in path_followed:
#            x = round(2*i[1])
#            y = round(2*i[0])
#            f_img.putpixel((x, y), (0, 0, 0))
#        f_img.save(basename.strip(".png") + "_map_image_solution.png")
#            
#        for ele in path_followed:
#            if ele == start_pt:
#                grid_from_img[ele[0]][ele[1]] = 3
#            elif ele in end_pt:
#                print("Here")
#                grid_from_img[ele[0]][ele[1]] = 4
#            else:
#                grid_from_img[ele[0]][ele[1]] = 2
#        final_filename = basename.strip(".png") + "_path_followed"
#        save_as_grid(grid_from_img, final_filename, blockSize=20)
#        print("Image saved")
#    else:
#        print("Fail")