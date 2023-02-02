import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

def draw_plot():
    # Read data from file
    df = pd.read_csv('epa-sea-level.csv')

    # Create scatter plot
    plt.scatter(df['Year'], df['CSIRO Adjusted Sea Level'])
    
    # Create first line of best fit
    ols_1 = linregress(df[['Year', 'CSIRO Adjusted Sea Level']])
    range_1 = pd.RangeIndex(start=df['Year'].min(), stop=2051, step=1)
    plt.plot(range_1, range_1 * ols_1.slope + ols_1.intercept, '-r')
    
    # Create second line of best fit
    ols_2 = linregress(df[df['Year']>=2000][['Year', 'CSIRO Adjusted Sea Level']])
    range_2 = pd.RangeIndex(start=2000, stop=2051, step=1)
    plt.plot(range_2, range_2 * ols_2.slope + ols_2.intercept, '-b')
    
    # Add labels and title
    plt.xlabel('Year')
    plt.ylabel('Sea Level (inches)')
    plt.title('Rise in Sea Level')

    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()
