#package imports
import numpy as np
import pandas as pd
import statistics
from scipy.signal import argrelextrema


class SupportResistanceIndicator():

    def __init__(self, df, order = 30, big_peak_order = 70) -> None:

        self.df = df
        self.order = order
        self.big_peak_order = big_peak_order

        #we find the standard deviation of the instrument used by passing it the close prices
        self.standard_deviation = statistics.stdev(self.df['close']) 


    # this is the main method to run that will run the corresponding methods to find the support 
    # and resistance levels
    def main(self):

        # this method finds the peaks inside of our data
        self.find_peaks()

        # this method will find the peaks that come back the most
        self.find_repeated_peaks()

        # finally we delete horizontal levels that are very close to each other
        self.remove_duplicate_levels()

        # we return the peaks that came back multiple times (which are the support and resistance levels)
        return self.peaks_with_high_frequency


    # this method is used to find peaks
    def find_peaks(self):

        # Find local peaks
        self.df['min'] = self.df.iloc[argrelextrema(self.df.low.values, np.less_equal,
                            order = self.order)[0]]['low']
        self.df['max'] = self.df.iloc[argrelextrema(self.df.high.values, np.greater_equal, 
                            order = self.order)[0]]['high']

        # Find bigger local peaks (we do this by choosing local mins that have higher orders compared to the latter)
        self.df['big_min'] = self.df.iloc[argrelextrema(self.df.low.values, np.less_equal,
                            order = self.big_peak_order)[0]]['low']
        self.df['big_max'] = self.df.iloc[argrelextrema(self.df.high.values, np.greater_equal, 
                            order = self.big_peak_order)[0]]['high']
    

    #this method is used to quantity the peaks and find the ones that come up the most
    def find_repeated_peaks(self):

        # ~~~~~~ lower order peaks ~~~~~~~~~~~~

        # we start by finding the repeated peaks for the smaller peaks (with smaller order)
        self.peaks = []
        
        # here we are going to loop through all of the extrema and put them on a list
        for value in self.df['min']:

            #this line checks if the value is not a number, it will continue to the next iteration if thats the case, finding the first max
            if pd.isna(value) == True:
                continue
            
            # if the value is a real number then we are going to append it to the list
            self.peaks.append(value)

        # here we are going to loop through all of the extrema and put them on a list
        for value in self.df['max']:

            #this line checks if the value is not a number, it will continue to the next iteration if thats the case, finding the first max
            if pd.isna(value) == True:
                continue
            
            # if the value is a real number then we are going to append it to the list
            self.peaks.append(value)

        #next we need to quantify these peaks, by checking the frequency of each and highlighting those that stand out

        # here we keep a dictionary of the values that have already been used
        self.peaks_with_high_frequency = []

        # ~~~~~~~~~~~~ first loop ~~~~~~~~~~~~~~~
        #we are going to do a recursive loop to see how many points there are for each value, the idea behind this recursive loop
        # is that we are going to loop through the first peak, then loop after each point after it and check how many times this same number comes up
        for index_1 in range(len(self.peaks)):

            value_1 = self.peaks[index_1]

            # ~~~~~~~~~~~~ second loop ~~~~~~~~~~~~~~~
            # next we loop through the remaining points and see if there is another peak that is in the same range as the previous value
            for index_2 in range(index_1, len(self.peaks)):

                value_2 = self.peaks[index_2]

                #we check that the second value is near the first using a ratio of its standard deviation
                if value_1 - (self.standard_deviation * 4) <= value_2 <= value_1 + (self.standard_deviation * 4):

                    # ~~~~~~~~~~~~ third loop ~~~~~~~~~~~~~~~
                    #we loop a third time to get only values with 3 peaks
                    for index_2 in range(index_1, len(self.peaks)):

                        value_2 = self.peaks[index_2]

                        #we check that the second value is near the first using a ratio of its standard deviation
                        if value_1 - (self.standard_deviation * 4) <= value_2 <= value_1 + (self.standard_deviation * 4):

                            # ~~~~~~~~~~~~ fourth loop ~~~~~~~~~~~~~~~
                            #we loop a third time to get only values with 3 peaks
                            for index_3 in range(index_2, len(self.peaks)):

                                value_3 = self.peaks[index_3]

                                #we check that the second value is near the first using a ratio of its standard deviation
                                if value_2 - (self.standard_deviation * 4) <= value_3 <= value_2 + (self.standard_deviation * 4):

                                    #we add the value to the high_frequency peak values
                                    self.peaks_with_high_frequency.append(value_1)

        # ~~~~~ higher order peaks ~~~~~~~~~~

        # next we are going to perform the same thing but with the higher order peaks
        self.big_peaks = []
        
        # here we are going to loop through all of the extrema and put them on a list
        for value in self.df['big_min']:

            #this line checks if the value is not a number, it will continue to the next iteration if thats the case, finding the first max
            if pd.isna(value) == True:
                continue
            
            # if the value is a real number then we are going to append it to the list
            self.big_peaks.append(value)

        # here we are going to loop through all of the extrema and put them on a list
        for value in self.df['big_max']:

            #this line checks if the value is not a number, it will continue to the next iteration if thats the case, finding the first max
            if pd.isna(value) == True:
                continue
            
            # if the value is a real number then we are going to append it to the list
            self.big_peaks.append(value)

        #next we need to quantify these peaks, by checking the frequency of each and highlighting those that stand out

        # ~~~~~~~~~~~~ first loop ~~~~~~~~~~~~~~~
        #we are going to do a recursive loop to see how many points there are for each value, the idea behind this recursive loop
        # is that we are going to loop through the first peak, then loop after each point after it and check how many times this same number comes up
        for index_1 in range(len(self.big_peaks)):

            value_1 = self.big_peaks[index_1]

            # ~~~~~~~~~~~~ second loop ~~~~~~~~~~~~~~~
            # next we loop through the remaining points and see if there is another peak that is in the same range as the previous value
            for index_2 in range(index_1, len(self.big_peaks)):

                value_2 = self.big_peaks[index_2]

                #we check that the second value is near the first using a ratio of its standard deviation
                if value_1 - (self.standard_deviation * 0.70) <= value_2 <= value_1 + (self.standard_deviation * 0.70):

                    #we add the value to the high_frequency peak values
                    self.peaks_with_high_frequency.append(value_1)

        # we eliminate duplicates from the list of peaks with high frequency
        self.peaks_with_high_frequency = list(set(self.peaks_with_high_frequency))


    # this method is used to remove duplicate levels of support/ resistance
    def remove_duplicate_levels(self):

        # to remove the duplicates we are going to loop through every point and then check that 
        # no other point is in the viscinity of it by double looping throuhg the remaining points
        # and making sure it is beneath a certain ratio of the standard deviation

        # we order the list of peaks
        self.peaks_with_high_frequency.sort()

        # since we dont want to remove points of a list while looping through them, we will keep
        # a list of the values to remove here from the support and resistance levels
        list_of_values_to_remove = []

        # we loop through the points
        for i in range(len(self.peaks_with_high_frequency)):

            # we double loop to compare it to the other points
            for j in range(i + 1, len(self.peaks_with_high_frequency)):

                # this line checks that the second point is not lower than the first point plus
                # a standard deviation times a ratio (20% in this case)
                if self.peaks_with_high_frequency[i] + 0.25*self.standard_deviation >= self.peaks_with_high_frequency[j]:

                    # if this condition is met then we either keep the first point or the last depending
                    # on where on the loop we are

                    # if we are in the first half of points then we remove the second point
                    if j < len(self.peaks_with_high_frequency):
                        list_of_values_to_remove.append(self.peaks_with_high_frequency[j])

                    # if we are on the second half of the points then we remove the first point
                    if j > len(self.peaks_with_high_frequency):
                        list_of_values_to_remove.append(self.peaks_with_high_frequency[i])

        # once the loop is completed we can remove the levels from the main list

        print(list_of_values_to_remove)
        # but first we need to remove the duplicates from the list
        list_of_values_to_remove = list(dict.fromkeys(list_of_values_to_remove))
        print(list_of_values_to_remove)

        for value in list_of_values_to_remove:
            self.peaks_with_high_frequency.remove(value)


    