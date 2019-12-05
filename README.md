
# Welcome to the Shortest-Path-Between-Multiple-Pick-up-Points-in-a-Map-Optimiser

## Who would want to use this?
If you're carpooling with a bunch of friends, you might want to choose the shortest path that connects all the pick-up or drop off destinations so that you dont end up driving in circles or up and down the same street unnecessarily. What's that? You don't have friends because you're busy running an Uber-like company and need to make sure your vehicles drive the optimum route so that you reach the most customers in the least amount of time using the least amount of fuel. Wait what?! Your company did'nt work out and you decided to move into the public transportation sector and have been asked to knock off a few bust stops so that the new bus route caters to the busier parts of town. If you are any of these people, then you're in luck because our code can help you out!

## How it works?
1. The user inputs the location in which all the pick-up/drop-off locations are found. The google maps API gets the map of the requested location <br>
3. It turns the map into a black and white version of itself. <br>
4. For the code to run well for large maps, we create a mask of 4 pixels which moves through the whole image. The mask averages out the pixels in it. If the average is non-zero then a value of 1 is assigned to a corresponding location in a 2D-array. This array represents our map in a grid form. <br>
5. The user inputs the multiple locations they want the path to be optimised around. <br>
6. The grid is then passed into the path-searching grid solver which is based off of the breadth first search algorithm. <br>
7. ...
8. The code then produces a gif of the path through all the stops. <br>
9. In addition, it finds out the stop that most decreases the distance travelled and offers to remove it from the solution path. This is useful when deciding if the removal of a single stop can make a large difference when time of travel is concerned and if it warrants the need of another vehicle for whom this additional stop will not make a difference. The code can also calculate the actual distance travelled based on the zoom level and pixels travelled and the cost of fuel consumption. <br>

## What the user needs to do?
1. The user needs to download the following python files from the repository into a folder: 
<p align="center">
   <strong> Grid_Solver_2.py, Map_to_GRid.py and Comparison_EndPts.py </strong>
</p> 
2. The user will need to enter the location (of the region in which they wish to travel) in line #"INSERT LINE NUMBER". You can either enter the location name (eg. "Baltimore", "Johns Hopkins University", "Oerlikon, Zurich", "3333 North Charles Street, Baltimore", etc.) or the latitude and longitude (eg. "47.65,-119.42"). Whatever format you choose, make sure you enclose it within double quotations. You can also adjust the zoom level of the region you want the code to run in. Zoom levels are rational numbers that typically lie between 1 and 21 (eg. 10.5, 19.1, 20, etc.). Some maps may have more information at higher zoom levels than others <br>
```markdown
if __name__ == "__main__":
    location = 'Johns Hopkins University'
    zoom = 15
    ...
```

3. Run the code and wait for a pop-up of the map to show up. Once this happens right click ONLY on the road parts of the map that are closest to the stop points that you want. Once you have clicked on all the points you want, press the ESC key to exit the pop-up window.<br>
### The map that shows up in the pop-up window <br>
![alt test](Screenshot (14).png) <br>
### The code records every point clicked <br>
![alt test](Screenshot (15).png) <br>
<br>
4. The code will find the solution path for you and store multiple images in the current directory.<br>

The files that will be of most use to you will be: location_image_with_label_trial_solution.gif and            location_image_with_label_trial.png; where location is what you've entered before. <br>

### location_image_with_label_trial.png -- a png file drawing the solution
![alt test](Johns Hopkins University_image_with_label_trial.png) <br>
  For your information, the other image files found, were used by the code:
### location_image_with_label.png -- a map that contains the labels of the regions and the stop points entered in by the user <br>
![alt test](Johns Hopkins University_image_with_label.png) <br>
### location_image_without_label_black&white.png -- a black and white version of the map for the code to create a grid <br>
![alt test](Johns Hopkins University_image_without_label_black&white.png) <br>
### location_image_without_label_recreated_grid.png -- the grid version of the map <br>
![alt test](Johns Hopkins University_image_without_label_recreated_grid.png) <br>
### location_image_without_label.png -- the map without labels which the code uses to create the black and white version of the map <br>
![alt test](Johns Hopkins University_image_without_label.png)

## Shortcomings:
The algorithm is not perfect. It cannot distinguish between 2 way roads and 1 way roads, so a path can go in both directions on a 1 way road. If your map has highways in it, the algorithm is going to treat it like a regular road which means that a path can cut into and leave a highway anywhere (which does not translate well into real life situations)


