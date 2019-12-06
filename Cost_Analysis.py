'''
To do a Fuel Cost Analysis for the Pool ride
Author : Prabhjot Kaur
This Class carries out a fuel cost analysis
Inorder to get a brief idea of total costs so spend
in reaching in all the end points.
Especially usefull in budget planning and even gives the driver
a good estimate of whether he has enough fuel to go to all the points
-- The first step to be carried out is the get meters per pixel from the image
According to Google API the zoom level changes the meters per pixel
So we collect data from Google Maps and carry out a curve fitting optimizing
to get meters per pixel as a function of zoom
-- Once we get this function then we carry find the value of meters per pixel
for the given zoom
--  Depending upon the fuel cost and milege of the car so feeded in the code
this then calculates the total amount of fuel consumed and the cost of the same

This is benificially when you want to compare two paths in terms of fuel cost
which is a better factor for comparison than the total length
'''
# import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np


class Cost_Analysis:
    '''
    This class as explained above performs a fuel cost analysis for the so
    path followed
    '''

    def __init__(self, path_followed, zoom):
        '''
        Initialises the Cost_Analysis Class object

        ** Parameters **
        self : Object of the class
        path_followed : List of tuples : *int*
                The path so folllowed from the start to all the end points
        zoom : *int*
             Zoom level for the Google Image so chosen by the user

        ** Returns **
        Nothing!
        '''
        self.path = path_followed
        self.zoom = zoom
        # m_p is meters to pixel
        # Intially initialised to None
        self.m_p = None

    def zoom_pixel_dist_reg(self):
        '''
        This function relates the zoom level to number of pixels
        and the distance it represents, thus carrying out a curve fitting
        to get the function parameters (found that exponential function fits
        the data the best).

        ** Parameters **
        None

        ** Returns **
        None


        From Google Maps data we get for
        Zoom Pixel Distance(m)
        3     163   1609000
        4     163   804672
        5     133   321869
        14    90    500
        15    70    200
        16    140   200
        17    140   100
        Here we perform Curve fitting using Scipy
        '''
        def func(x, a, b, c):
            return(a * np.exp(-b * x) + c)
        Map = {"Zoom": [3, 4, 5, 14, 15, 16, 17],
               "Meter_Pixel": [9871.2, 4936.6, 2420.1, 5.56, 2.86, 1.43, 0.72]}

        X = np.asarray(Map["Zoom"])
        Y = np.asarray(Map["Meter_Pixel"])
        p_opt, p_cov = curve_fit(func, X, Y)
        '''
        plt.plot(X, func(X, *p_opt), 'r-'
        , label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(p_opt))
        plt.plot(X, Y, '*r', label="Samples")
        plt.show()
        '''
        self.m_p = func(self.zoom, *p_opt)

    def cost_analysis(self):
        '''
        This function performs fuel cost analysis for the path so followed
        As we explained the fuel cost and milege of the vehicle is already
        feeded (general value assumed )

        ** Parameters **
        None

        ** Returns **
        distance_traveled : *Float*
                Net distance travelled by the vehicle for that path in miles
        fuel_consumed : *Float*
                Amount of fuel consumed in  gallons
        Net_fuel_cost : *Float*
                The final fuel cost so calculated
        '''

        # Assuming fuel cost as 2.6$ per gallon
        fuel_cost = 2.6
        # Assuming average Milege of the car is 24.7 miles per gallon
        milege = 24.7
        # Each step is two pixels
        self. zoom_pixel_dist_reg()
        distance_traveled = self.m_p * len(self.path) * 2
        # Above is in meters
        distance_traveled *= 0.000621371
        fuel_consumed = distance_traveled * milege
        Net_fuel_cost = fuel_cost * fuel_consumed

        return(distance_traveled, fuel_consumed, Net_fuel_cost)


if __name__ == "__main__":
    '''
    path_followed = np.arange(100)
    zoom = 10
    Regression = Cost_Analysis(path_followed, zoom)
    final_cost = Regression.cost_analysis()
    print(final_cost)
    '''
    pass
