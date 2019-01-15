from matplotlib import pyplot as plt
import numpy as np

from PIL import Image
fig, ax = plt.subplots(2)
data = np.array([[100,100], [500,100], [1000, 400]])
small_points = ax[0].scatter(data[:,0], data[:,1])
im = plt.imread('../../../OneDrive/Pictures/IMG_1778.jpg')
ax[0].imshow(im)
large_points = ax[0].scatter(data[:, 0], data[:, 1], s=10)

# im = plt.imshow(np.random.rand(10,10)*255, interpolation=
# fig = plt.gcf()
# ax = plt.gca()

class EventHandler:
    def __init__(self, data):
        fig.canvas.mpl_connect("motion_notify_event", self.on_hover)
        fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.data = data

    def on_release(self, event):
        if event.inaxes!=ax[0]:
            return
        xi, yi = (int(round(n)) for n in (event.xdata, event.ydata))
        value = im[yi,xi]
        # color = im.cmap(im.norm(value))
        ax[1].scatter(np.ones(10)*1000, np.random.rand(10)*1000)
        print(xi, yi, value)  #,color)
        fig.canvas.draw_idle()


    def on_hover(self, event):
        if event.inaxes!=ax[0]:
            return
        if self.near_point(event.xdata, event.ydata):
            large_points.set_visible(True)

        else:
            large_points.set_visible(False)
        xi, yi = (int(round(n)) for n in (event.xdata, event.ydata))
        value = im[yi,xi]
        # color = im.cmap(im.norm(value))
        ax[1].scatter(np.ones(10)*500, np.random.rand(10)*1000)
        print(xi,yi,value)#,color)
        fig.canvas.draw_idle()

    def near_point(self, xdata, ydata):
        dist_x, dist_y = np.abs(self.data[:,0] - xdata), np.abs(self.data[:,1] - ydata)
        return any(dist_x < 100) and any(dist_y < 100)


handler = EventHandler(data)
plt.show()