#package imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statistics
from scipy.signal import argrelextrema

#local imports
import config as config
#from disk import Disk
from plot import Plot
from historical_data import HistoricalData
from xabcd import xabcd

class SupportResistanceIndicator():

    def __init__(self, df, order, big_peak_order) -> None:
        
        self.df = df
        self.order = order
        self.big_peak_order = big_peak_order

        #we find the standard deviation of the instrument used
        self.standard_deviation = statistics.stdev(self.df['close'])
        print(self.standard_deviation)

        #class instances
        self.plot = Plot()


    def main(self):

        # this method finds the peaks inside of our data
        self.find_peaks()

        # this method will find the peaks that come back the most
        self.find_repeted_peaks()

        self.quantity__big_peaks()

        #we refine the quantity peaks
        self.refine_peaks()

        #we plot the dataframe and its peaks to visually see whats happening
        #self.plot.dataframe_and_peaks_and_support(self.df, self.peaks_with_high_frequency, self.big_peaks_with_high_frequency)

        # we are going to be putting all of the peaks into one list
        self.final_peaks = []
        self.final_peaks.join(self.peaks_with_high_frequency)
        self.final_peaks.join(self.big_peaks_with_high_frequency)
        self.delete_duplicates()

        #self.plot.dataframe_and_levels(self.df, self.final_peaks)



        #we plot the candlestick data with the horizontal support lines


    # this method is used to find peaks
    def find_peaks(self):

        # Find local peaks
        self.df['min'] = self.df.iloc[argrelextrema(self.df.low.values, np.less_equal,
                            order = self.order)[0]]['low']
        self.df['max'] = self.df.iloc[argrelextrema(self.df.high.values, np.greater_equal, 
                            order = self.order)[0]]['high']

        # Find BIG local peaks
        self.df['big_min'] = self.df.iloc[argrelextrema(self.df.low.values, np.less_equal,
                            order = self.big_peak_order)[0]]['low']
        self.df['big_max'] = self.df.iloc[argrelextrema(self.df.high.values, np.greater_equal, 
                            order = self.big_peak_order)[0]]['high']
    

    # this is to find the absolute max and mins
    def abs_peaks(self):

        pass
        # self.abs_peaks = []

        # abs_min = {
        #     'value':'na',
        #     'index':'na'

        # # finding the absolute max and min
        # for index in range(len(self.df)):
            
        #     # checking for min


    #this method is used to quantity the peaks and find the ones that come up the most
    def find_repeted_peaks(self):

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

        print(self.peaks)

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


        #this method is used to eliminate duplicates when choosing the self peaks
        self.peaks_with_high_frequency = list(set(self.peaks_with_high_frequency))


    #this method is going to check that peaks that are too close together get turned into one
    def refine_peaks(self):

        #we need to order the list
        self.peaks_with_high_frequency.sort()
        
        #we loop to find the first point
        for index_1 in range(len(self.peaks_with_high_frequency)):

            #we loop to find the second point
            for index_2 in range(index_1 + 1, len(self.peaks_with_high_frequency)):

                #we loop to find the third point
                for index_3 in range(index_2 + 1, len(self.peaks_with_high_frequency)):

                    peak_3 = self.peaks_with_high_frequency[index_3]

                    peak_1 = self.peaks_with_high_frequency[index_1]


                #we need the distance from the first to the third point to be below a certain standard deviation
                if abs(peak_3 - peak_1) > self.standard_deviation * 0.5:
                    continue

                # if the distance is lower then we remove the first peak and the second peak
                self.peaks_with_high_frequency.remove(peak_3)
                self.peaks_with_high_frequency.remove(peak_1)

        #this method is going to check that peaks that are too close together get turned into one
    def refine_big_peaks(self):

        #we need to order the list
        self.big_peaks_with_high_frequency.sort()
        
        #we loop to find the first point
        for index_1 in range(len(self.big_peaks_with_high_frequency)):

            #we loop to find the second point
            for index_2 in range(index_1 + 1, len(self.big_peaks_with_high_frequency)):

                #we loop to find the third point
                for index_3 in range(index_2 + 1, len(self.big_peaks_with_high_frequency)):

                    big_peak_3 = self.big_peaks_with_high_frequency[index_3]

                    big_peak_1 = self.big_peaks_with_high_frequency[index_1]


                #we need the distance from the first to the third point to be below a certain standard deviation
                if abs(big_peak_3 - big_peak_1) > self.standard_deviation * 0.5:
                    continue

                # if the distance is lower then we remove the first peak and the second peak
                self.big_peaks_with_high_frequency.remove(big_peak_3)
                self.big_peaks_with_high_frequency.remove(big_peak_1)

        #we only take the middle point as the sample data is small enoough to fit
    
    

    #this method is used to quantity the peaks and find the ones that come up the most
    def quantity__big_peaks(self):

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

        print(self.big_peaks)

        #next we need to quantify these peaks, by checking the frequency of each and highlighting those that stand out

        # here we keep a dictionary of the values that have already been used
        self.big_peaks_with_high_frequency = []

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
                    self.big_peaks_with_high_frequency.append(value_1)

        #this method is used to eliminate duplicates when choosing the self peaks
        self.big_peaks_with_high_frequency = list(set(self.big_peaks_with_high_frequency))

    ## to finish this, make sure to transform list into list of dictionary, order the list in terms of values
    ## then we find 3 succesibe points and only check if its in order BRB, if it is then we check that if the 
    ## blue values are close together, then we are going to remove the red part inside

    #this method is used to remove red points that might be between blue point 
    def remove_red_points_between_blue_points(self):

        #first we need to create a unified peak point
        self.unified_peaks = []

        #we append both peak lists
        self.unified_peaks.append(self.peaks_with_high_frequency)
        self.unified_peaks.append(self.big_peaks_with_high_frequency)

        #we sort the list
        self.unified_peaks.sort()

        #we loop to find the first point
        for index_1 in range(len(self.unified_peaks)):

            #we loop to find the second point
            for index_2 in range(index_1 + 1, len(self.unified_peaks)):

                #we loop to find the third point
                for index_3 in range(index_2 + 1, len(self.unified_peaks)):

                    big_peak_3 = self.unified_peaks[index_3]
                    big_peak_1 = self.unified_peaks[index_1]

                    #we need to skip the iterations that when big peak 3 and big peak 1 

    # this method is used to remove duplicate levels of support/ resistance
    def remove_duplicate_levels(self):

        # first we need to order the list of peaks
        print(self.final_peaks)
        self.final_peaks

instrument = 'USD_CAD'

data_point = 160

print(f' instrument is {instrument} and data point is {data_point}')
historical_data = HistoricalData()
df = historical_data.retrieve_forex_historical_data_converted(instrument, data_point, 'D')

#calling support resistance block
order = 5
big_peak_order = 40
support_resistance = SupportResistanceIndicator(df, order, big_peak_order)
support_resistance.main()


    