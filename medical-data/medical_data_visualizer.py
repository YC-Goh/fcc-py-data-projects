import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
df['bmi'] = df['weight'] / ((df['height'] / 100) ** 2)
df['overweight'] = (df['bmi'] > 25) * 1

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['cholesterol'] = (df['cholesterol'] > 1) * 1
df['gluc'] = (df['gluc'] > 1) * 1

# Drop incorrect data
mask_diastolic_wrong = df['ap_lo'] <= df['ap_hi']
mask_height_high = df['height'] <= df['height'].quantile(.975)
mask_height_low = df['height'] >= df['height'].quantile(.025)
mask_weight_high = df['weight'] <= df['weight'].quantile(.975)
mask_weight_low = df['weight'] >= df['weight'].quantile(.025)
df = df[mask_diastolic_wrong&mask_height_high&mask_height_low&mask_weight_high&mask_weight_low]

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars=['id', 'cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = df_cat.groupby(by=['cardio', 'variable', 'value']).agg('count')
    df_cat.columns = ['total']
    df_cat = df_cat.reset_index()
    
    # Draw the catplot with 'sns.catplot()'
    sns.set_theme()
    g = sns.catplot(df_cat.reset_index(), x='variable', y='total', hue='value', col='cardio', kind='bar', sharey=True)
    
    # Get the figure for the output
    fig = g.figure

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig

# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df.drop(columns=['bmi'])

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.array([ [ r <= c for c in range(corr.shape[1]) ] for r in range(corr.shape[0]) ])
    
    # Set up the matplotlib figure
    fig, ax = plt.subplots(1, 1)

    # Draw the heatmap with 'sns.heatmap()'
    sns.set_theme()
    sns.heatmap(data=corr, annot=True, fmt='.1f', annot_kws={'fontsize':'x-small'}, square=True, mask=mask)
    
    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
