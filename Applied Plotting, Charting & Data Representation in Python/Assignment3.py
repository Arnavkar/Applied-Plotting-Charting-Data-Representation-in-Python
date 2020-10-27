import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.gridspec as gridspec
from matplotlib.widgets import Slider, SpanSelector
from matplotlib.cm import ScalarMappable

#%matplotlib notebook

#Using sliders (draw rectangle with y limits in draw_bars function to show range)   
'''def upplim_update(val):
    ax1.cla()
    upp = Upplim.val
    if (upp<Lowlim.val):
        upp = Lowlim.val + 1
        Upplim.set_val(UppLim, upp)
    draw_bars(upp,Lowlim.val)
    #return upp


def lowlim_update(val):
    ax1.cla()
    low = Lowlim.val
    if(low > Upplim.val):
        low = Upplim.val-1
        Lowlim.set_val(LowLim, low)
    draw_bars(Upplim.val, low)  
    #return low

ax2 = fig.add_subplot(gs[1, 0])
Upplim = Slider(ax2, 'Y-limit \n Upper ', 0, 50000, valinit=upp, color='grey')
Upplim.on_changed(upplim_update)

ax3 = fig.add_subplot(gs[2, 0])
Lowlim = Slider(ax3, 'Y-limit\n Lower', 0, 50000, valinit=low, color='grey')
Lowlim.on_changed(lowlim_update)'''

def get_range():
    Range = [Lowlim.val, Upplim.val]
    return Range

def generate_df():
    np.random.seed(12345)
    # Generating Dataframe with relevant values 
    df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                       np.random.normal(43000,100000,3650), 
                       np.random.normal(43500,140000,3650), 
                       np.random.normal(48000,70000,3650)], 
                      index=[1992,1993,1994,1995])
    sample_size = len(df.columns)
    df['mean'] = df.mean(axis=1)
    df['std'] = df.std(axis = 1)
    df = df[['mean','std']]
    df['error_margin'] =  (1.96*(df['std']/(np.sqrt(sample_size))))# formula is Z value * std/(sqrt of n)
    #z value for 95% confidence interval is 1.96
    df['lower_margin'] = df['mean'] - df['error_margin']
    df['upper_margin'] = df['mean'] + df['error_margin']
    df['IQR'] = df['upper_margin'] - df['lower_margin']
    #used to get margins
    return df

def get_margin_list(): #get 2x4 list of upper and lower margins per year
    margins = []
    for i in range(0,4): 
        margins.append(df.iloc[i,3:5].tolist())
    return margins

def get_IQR_list():#Get list of ranges between upper and lower margin
    IQR = []
    for i in range(0,4):
        IQR.append(df.iloc[i,5])
    return IQR

def find_overlap(a,b):# find overlap between any two ranges , with min and max values in a list format
    val = max(0, min(a[1],b[1])) - max(a[0],b[0])
    #if range intersects, it will return a positive value indicative of intersection size
    if val < 0:
        val = 0
    #if range does not intersect, returns a negative value
    return val 

def get_overlap_list(arg): #function to find the overlap, returns a list with 4 values 
    margins = get_margin_list()
    overlap_values = []
    for item in margins:
        overlap_values.append(find_overlap(item,arg))
    return overlap_values

def onselect_function(min_value, max_value):
    Range = [min_value, max_value]
    rect.set_alpha(0) # remove initial range 
    # recolor bars 
    new_color_values = [float(b) / float(m) for b,m in zip(get_overlap_list(Range), get_IQR_list())]
    new_colors = my_cmap(new_color_values)
    #update bars
    plt.bar(df.index,df['mean'], yerr = df['error_margin'], capsize = 10, width = 0.7, color = new_colors,edgecolor = 'black')
    return min_value,max_value

df = generate_df()
current_range = [38000,45000]
#Plotting the underlying graph 
fig = plt.figure(figsize = (7,7))
fig.suptitle('Building a Custom Visualization (Hardest Option)',fontsize = 20)
ax = fig.add_subplot(1,1,1)

#set starting colors and set up color map with scalarmappable and color map
starting_color_values = [0.15,1,0.5,0]
my_cmap = plt.cm.get_cmap('Blues')
starting_color = my_cmap(starting_color_values) #retrieve colors from colormap
sm = ScalarMappable(cmap=my_cmap, norm=plt.Normalize(0,max(starting_color_values)))
sm.set_array([]) #convert to an array 
cbar = plt.colorbar(sm)
#set initial range to a visible span
rect = plt.axhspan(ymin = 38000, ymax = 45000, facecolor = 'grey', alpha = 0.3) 
#draw bars initially and set x axis params
bars = plt.bar(df.index,df['mean'], yerr = df['error_margin'], capsize = 10, width = 0.7, color = starting_color, edgecolor ='black')
ax.xaxis.set_ticks([1992,1993,1994,1995])
ax.tick_params(labelsize = 10)
# initialize span selector
span = SpanSelector(ax,
                    onselect = onselect_function,
                    direction='vertical',
                    minspan = 30, 
                    useblit = False, 
                    span_stays = True, 
                    button=1, rectprops={'facecolor':'grey','alpha': 0.3})

plt.show()





































