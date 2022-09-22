# now we can pass the other argument to the method
# package imports
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# local imports
from support_resistance_indicator import SupportResistanceIndicator
 

# In this part we retrieve the filename of the dataframe from the terminal input
message = sys.argv

# we need to remove the filename argument from the function that is being called
filename = os.path.basename(__file__)
message.remove(filename)


# 1) Dataframe:
# we can now pass the dataframe as input for the next methods, we start by retrieving the dataframe using pandas
df = pd.read_pickle(message[0])
# 'dataframe_example.pickle'


# 2) Program Execution:
# next we are going to pass the dataframe to the main app.py main method

# we create a class instance to be able to use the methods of the class
support_resistance = SupportResistanceIndicator(df = df)

# we call the main function which will return the support and resistance horizontal levels
support_resistance_levels = support_resistance.main()

# displaying the support and resistance levels
print(f'The support and resistance levels are')
for level in support_resistance_levels:
    print(level)


# 3) Ploting:
# you can choose to comment this part out if you dont need to visualize the data, otherwise
# this allows you to see the support and resistance levels on a chart

# we plot the close prices of the dataframe
plt.plot(df['date'], df['close'])

# we add the support and resistance levels to the plot by looping through each of them
for value in support_resistance_levels:
    print(value)
    plt.axhline(y=value, color='r', linestyle='-')

# we show the plot
plt.show()