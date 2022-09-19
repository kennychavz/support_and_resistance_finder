# package imports
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from support_resistance_indicator import SupportResistanceIndicator

# this is an example of how to run the python software for a given dataframe

# 1) dataframe:
# first you need a dataframe, we have one set as example in this repository but any dataframe
# works as long as you have between 500-1500 points in the dataframe, this dataframe is loaded up using pickle
df = pd.read_pickle('dataframe_example.pickle')

# 2) Program Execution:
# next we are going to pass the dataframe to the main app.py main method

# we create a class instance to be able to use the methods of the class

# variables
print(f' the lenght of the dataframe is {len(df)}')

# we create a class instance of the support resiststance indicator class
support_resistance = SupportResistanceIndicator(df = df)

# we call the main function which will return the support and resistance horizontal levels
support_resistance_levels = support_resistance.main()

# 

print(f' the support levels are {support_resistance_levels}')
print(df)

# we plot the close prices of the dataframe
plt.plot(df.index, df['close'])

print('hellloooooo')
# we add the horizontal levels to the plot
for value in support_resistance_levels:
    print(value)
    plt.axhline(y=value, color='r', linestyle='-')

plt.show()

# fig = go.Figure(data=[go.Candlestick(x=df['date'],
#                         open=df['open'],
#                         high=df['high'],
#                         low=df['low'],
#                         close=df['close'])])

# for value in support_resistance_levels:
#     print(value)
#     fig.update_layout(
#         shapes = [dict(
#                 x0 = df['date'][0],
#                 x1 = df['date'][561],
#                 y0= value,
#                 y1 = value,
#                 line_width=2)],
#     )


# #fig.show()