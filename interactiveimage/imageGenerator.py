import math
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from pathlib import Path

class PlotThing:
    """This was created because I could not find the data attribute of a plot"""
    def __init__(self, plot, df): self.plot, self.dp, self.name, self.filename = plot, df[['x','y']].values, df['name'], df['filename']
    def compare(self, xdata, ydata): return max(np.abs(self.dp[0] - xdata), np.abs(self.dp[1] - ydata))
    def __repr__(self): return 'PlotThing({})'.format(self.dp)
    def set_visible(self, b:bool): self.plot.set_visible(b)

class EventHandler:
    def __init__(self, data, debug=False):
        fig.canvas.mpl_connect("motion_notify_event", self.on_hover)
        fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.data = data
        self.debug = debug

    def on_release(self, event):
        self.on_event(event, lambda: None, self.show_img)

    def on_hover(self, event):
        self.on_event(event, lambda: self.hide_points(), self.show_point)

    def on_event(self, event, precheck_lam, incheck_lam):
        if event.inaxes!=ax[0]:return
        precheck_lam()
        nearest = self.find_nearest(event.xdata, event.ydata)
        if 100 > nearest.compare(event.xdata, event.ydata):
            incheck_lam(nearest)
        fig.canvas.draw_idle()

    def show_img(self, nearest):
        ax[1].imshow(plt.imread(IMG_PATH / nearest.filename))

    def show_point(self, nearest):
        nearest.set_visible(True)

    def hide_points(self):
        for d in self.data: d.set_visible(False)

    def debug_print(self, event):
        xi, yi = (int(math.floor(n)) for n in (event.xdata, event.ydata))
        value = im[yi, xi]
        print(xi, yi, value)

    def find_nearest(self, xdata, ydata):
        sorted_list = sorted(self.data, key=lambda d:d.compare(xdata, ydata))
        return sorted_list[0]

if __name__ == "__main__":
    SOURCE_PATH = Path('../data/source.csv')
    IMG_PATH = Path('../data/images')
    im = plt.imread('../../../OneDrive/Pictures/IMG_1778.jpg')

    df = pd.read_csv(SOURCE_PATH)
    fig, ax = plt.subplots(2)
    data = df[['x','y']].values
    small_points = ax[0].scatter(data[:,0], data[:,1])
    ax[0].imshow(im)
    plots = [ax[0].scatter([d[0]], [d[1]], s=20) for d in data]
    plot_things = list(map(lambda x: PlotThing(x[0], x[1]), zip(plots, [d for n,d in df.iterrows()])))
    handler = EventHandler(plot_things)
    plt.show()