# import matplotlib
# matplotlib.use('TkAgg')
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# from matplotlib.figure import Figure
# import tkinter as tk
# import tkinter.ttk as ttk
# import sys
#
# class Application(tk.Frame):
#     def __init__(self, master=None):
#         tk.Frame.__init__(self,master)
#         self.createWidgets()
#
#     def createWidgets(self):
#         fig=plt.figure(figsize=(8,8))
#         ax=fig.add_axes([0.1,0.1,0.8,0.8],polar=True)
#         canvas=FigureCanvasTkAgg(fig,master=root)
#         canvas.get_tk_widget().grid(row=0,column=1)
#         canvas.show()
#
#         self.plotbutton=tk.Button(master=root, text="plot", command=lambda: self.plot(canvas,ax))
#         self.plotbutton.grid(row=0,column=0)
#
#     def plot(self,canvas,ax):
#         for line in sys.stdout: #infinite loop, reads data of a subprocess
#             theta=line[1]
#             r=line[2]
#             ax.plot(theta,r,linestyle="None",maker='o')
#             canvas.draw()
#             ax.clear()
#             #here set axes
#
# root=tk.Tk()
# app=Application(master=root)
# app.mainloop()

import pyformulas as pf
import matplotlib.pyplot as plt
import numpy as np
import time

fig = plt.figure()

canvas = np.zeros((480,640))
screen = pf.screen(canvas, 'Sinusoid')

start = time.time()
while True:
    now = time.time() - start

    x = np.linspace(now-2, now, 100)
    y = np.sin(2*np.pi*x) + np.sin(3*np.pi*x)
    plt.xlim(now-2,now+1)
    plt.ylim(-3,3)
    plt.plot(x, y, c='black')

    # If we haven't already shown or saved the plot, then we need to draw the figure first...
    fig.canvas.draw()

    image = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    screen.update(image)
