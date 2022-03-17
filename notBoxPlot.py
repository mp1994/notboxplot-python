#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

VALID_STYLES = ["boxes", "lines"]
COLOR_PAIRS = [["#fe9999", "#a7a7fc"], ["#EBF5FF", "#a2d2ff"]]

''' Drawing Function '''
def nbpi(x, xpos=1, w=0.2, ax=None, color=['#adb9e3', '#acdde7'], hatch=None, hatch_color="white", dotcolor='grey', dotsize=20, style="boxes"):

    # Used if style='lines'
    line_reduction_factor = 6.5
    hatch_big = None

    if style not in VALID_STYLES:
        raise ValueError("Invalid input: style must be one of the following: {}".format(VALID_STYLES))

    from matplotlib.patches import Rectangle as rect
    m,b1,b2,l1,l2 = boxValues(x)
    if ax is None:
        plt.figure(dpi=150)
        ax = plt.gca()
    if type(color) == int:
        color = COLOR_PAIRS[color]

    # Smaller (darker) box
    ax.add_patch(rect(xy=(xpos-w/2, b1), width=w, height=b2, alpha=1.0, zorder=2, facecolor=color[0], ec=hatch_color, linewidth=0, hatch=hatch))  
    # Bigger box
    if style == "lines":
        w = w/line_reduction_factor
        hatch_big = None
    else:
        hatch_big = hatch
    ax.add_patch(rect(xy=(xpos-w/2, l1), width=w, height=l2, alpha=1.0, zorder=1, facecolor=color[1], ec=hatch_color, linewidth=0, hatch=hatch_big))  
    # Median value: red line
    if style == "lines":
        w = w*line_reduction_factor
    ax.plot(np.linspace(xpos-w/2, xpos+w/2, 50), m*np.ones(50), 'r-', zorder=4) 
    # Scatter Points: randomize their x position to avoid overlapping
    ax.scatter(x=(xpos-w/4)*np.ones(len(x))+np.random.rand(len(x))*(w/2), y=np.array(x), c=dotcolor, marker='o', s=dotsize, zorder=3) 

    return ax

''' Helper function to compute the box-plot values '''
def boxValues(x):
    m = np.median(x)
    b1 = np.quantile(x, 0.25)
    b2 = np.quantile(x, 0.75)
    a = b1 - 1.5*(b2-b1)
    b = b2 + 1.5*(b2-b1)
    o1 = len(np.argwhere(x<a))  
    if o1 == 0:
        l1 = min(x)
    else:
        l1 = np.sort(x, axis=0)[o1]
    o2 = len(np.argwhere(x>b))  
    if o2 == 0:
        l2 = max(x)
    else:
        l2 = np.sort(x, axis=0)[-o2-1]
    b2 = b2-b1
    l2 = l2-l1
    return m, b1, b2, l1, l2

if __name__ == '__main__':
    # Generate some random data
    x = np.random.randn(100)    
    y = np.random.logistic(size=100)
    z = x + 2

    # First plot: get the axis object
    ax = notBoxPlot(x, xpos=0.75, hatch=None, style="lines")
    notBoxPlot(y, ax=ax, xpos=1.25, color=1, hatch="/", hatch_color="#FFAFCC", style="lines")
    notBoxPlot(z, ax=ax, xpos=1.75, hatch='x', hatch_color='#cccccc')
    # Plot settings
    ax.set_xticks([0.75,1.25,1.75])
    ax.set_xticklabels(["x", "y", "z"])

    # Show plot
    plt.show()
