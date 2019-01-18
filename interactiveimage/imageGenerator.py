import math
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from pathlib import Path
SOURCE_PATH = Path('../data/source.csv')
IMG_PATH = Path('../data/images')
df = pd.read_csv(SOURCE_PATH)
fig, ax = plt.subplots(2)
data = df[['x','y']].values
small_points = ax[0].scatter(data[:,0], data[:,1])
im = plt.imread('../../../OneDrive/Pictures/IMG_1778.jpg')
ax[0].imshow(im)
plots = [ax[0].scatter([d[0]], [d[1]], s=20) for d in data]
class PlotThing:
    """This was created because I could not find the data attribute of a plot"""
    def __init__(self, plot, df): self.plot, self.dp, self.name, self.filename = plot, df[['x','y']].values, df['name'], df['filename']
    def compare(self, xdata, ydata): return max(np.abs(self.dp[0] - xdata), np.abs(self.dp[1] - ydata))
    def __repr__(self): return 'PlotThing({})'.format(self.dp)
    def set_visible(self, b:bool): self.plot.set_visible(b)
plot_things = list(map(lambda x: PlotThing(x[0], x[1]), zip(plots, [d for n,d in df.iterrows()])))

class EventHandler:
    def __init__(self, data):
        fig.canvas.mpl_connect("motion_notify_event", self.on_hover)
        fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.data = data

    def on_release(self, event):
        if event.inaxes!=ax[0]:
            return
        xi, yi = (int(round(n)) for n in (event.xdata, event.ydata))
        # value = im[yi,xi]
        # ax[1].scatter(np.ones(10)*1000, np.random.rand(10)*1000)
        # print(xi, yi, value)  #,color)
        nearest = self.find_nearest(event.xdata, event.ydata)
        # should have a check for the nearest one
        if 100 > nearest.compare(event.xdata, event.ydata):
            im = plt.imread(IMG_PATH/nearest.filename)
            ax[1].imshow(im)
        fig.canvas.draw_idle()


    def on_hover(self, event):
        if event.inaxes!=ax[0]:
            return
        for d in self.data:
            d.set_visible(False)
        # list(map(lambda d: d.set_visible(False), self.data))
        nearest = self.find_nearest(event.xdata, event.ydata)
        # should have a check for the nearest one
        if 100 > nearest.compare(event.xdata, event.ydata):
            nearest.set_visible(True)
        xi, yi = (int(math.floor(n)) for n in (event.xdata, event.ydata))
        value = im[yi,xi]
        # print([d.plot.get_visible() for d in self.data])
        # ax[1].scatter(np.ones(10)*500, np.random.rand(10)*1000)
        print(xi,yi,value)#,color)
        fig.canvas.draw_idle()

    def near_point(self, xdata, ydata):
        dist_x, dist_y = np.abs(self.data[:,0] - xdata), np.abs(self.data[:,1] - ydata)
        return any(dist_x < 100) and any(dist_y < 100)

    def find_nearest(self, xdata, ydata):
        sorted_list = sorted(self.data, key=lambda d:d.compare(xdata, ydata))
        # print(sorted_list)
        return sorted_list[0]


handler = EventHandler(plot_things)
plt.show()