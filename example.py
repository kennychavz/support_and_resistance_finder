# package imports
import pandas as pd
import matplotlib.pyplot as plt

# local imports
from support_resistance_indicator import SupportResistanceIndicator

# this is an example of how to run the python software for a given dataframe

# 1) Dataframe:
# first you need a dataframe, we have one set as example in this repository but any dataframe
# works as long as you have between 500-1500 points in the dataframe, this dataframe is loaded up using pickle
df = pd.read_pickle('dataframe_example.pickle')


# 2) Program Execution:
# next we are going to pass the dataframe to the main app.py main method

# we create a class instance to be able to use the methods of the class
support_resistance = SupportResistanceIndicator(df = df)

# we call the main function which will return the support and resistance horizontal levels
support_resistance_levels = support_resistance.main()


# 3) Ploting:
# you can choose to comment this part out if you dont need to visualize the data, otherwise
# this allows you to see the support and resistance levels on a chart

# we plot the close prices of the dataframe
plt.plot(df.index, df['close'])

# we add the support and resistance levels to the plot by looping through each of them
for value in support_resistance_levels:
    print(value)
    plt.axhline(y=value, color='r', linestyle='-')

# we show the plot
plt.show()