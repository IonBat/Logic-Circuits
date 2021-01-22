# -*- coding: utf-8 -*-
"""
Created on Sat Sep 20 08:52:47 2014

cbco rev 2 Dec 8, 2017
@author: CBCO
"""

"""
Software

Installing Anaconda
1. Visit https://www.anaconda.com/download/
2. Download Python 3.6 version. Choose 64 bit for computer with 64 bit hardware.
3. Register in Anaconda Cloud.

From anaconda, access Spyder editor. Its website is https://spyder-ide.github.io


Installing ProTeXt

1. Visit http://tug.org/protext/
2. click  download the self-extracting protext.exe file  and it will bring \
you to http://mirror.pregi.net/tex-archive/systems/windows/protext/
Download ProTeXt-3.1.8-051917.exe or protext.exe This file is 2.5 GB

From ProTeXt run set up, install MikText first then install TexStudio.
MikText Website is https://miktex.org.
TexStudio Website is at https://www.texstudio.org


Library

import numpy as np  # NumPy (multidimensional arrays, linear algebra, ...)
import scipy as sp  # SciPy (signal and image processing library)

import matplotlib as mpl          # Matplotlib (2D/3D plotting library)
import matplotlib.pyplot as plt   # Matplotlib's pyplot: MATLAB-like syntax
from pylab import *               # Matplotlib's pylab interface
ion()                             # Turned on Matplotlib's interactive mode

import guidata                    # GUI generation for easy dataset editing and display

import guiqwt                     # Efficient 2D data-plotting features
import guiqwt.pyplot as plt_      # guiqwt's pyplot: MATLAB-like syntax
plt_.ion()                        # Turned on guiqwt's interactive mode


Within Spyder, this interpreter also provides:
    * special commands (e.g. %ls, %pwd, %clear)
    * system commands, i.e. all commands starting with '!' are subprocessed
      (e.g. !dir on Windows or !ls on Linux, and so on)

@Article{Hunter:2007,
  Author    = {Hunter, J. D.},
  Title     = {Matplotlib: A 2D graphics environment},
  Journal   = {Computing In Science \& Engineering},
  Volume    = {9},
  Number    = {3},
  Pages     = {90--95},
  abstract  = {Matplotlib is a 2D graphics package used for Python
  for application development, interactive scripting, and
  publication-quality image generation across user
  interfaces and operating systems.},
  publisher = {IEEE COMPUTER SOC},
  year      = 2007
}

"""


import sys
import string

import numpy as np  # NumPy (multidimensional arrays, linear algebra, ...)
import scipy as sp  # SciPy (signal and image processing library)

from numpy           import linspace


from matplotlib.collections import PatchCollection
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

# MatPlot Library


import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.backend_bases import FigureCanvasBase
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.axis import Axis

from matplotlib.pyplot import figure, show, axes, text, cla, draw, annotate
from matplotlib.pyplot import subplots_adjust, plot, subplot, gca, axis
from matplotlib.pyplot import show, stem, setp, hist, savefig

from matplotlib.text import Text
from matplotlib.pyplot import polar

def adjLTX(s):
    return "$"+latex(s)+"$"


def OnClickAction(self,event):
    print ("OnClick event","X = ",event.xdata,"Y = ",event.ydata)
    print ("button = ", event.button , " \n")


def PressKeyAction(self,event):
    print ("OnClick event","X = ",event.xdata,"Y = ",event.ydata)
    print ("key = ", event.key, " \n")
    print ("Button = ",self.button, " x = ",self.x, " y = ",self.y)


#CC Library

class Space2D:


    def __init__(self,click,press,title="2D Figure",sz=(10,8),fc='w'):

        self.title=title
        self.sz   =sz
        self.fc   =fc
        self.Fig2D=figure(
            self.title,figsize=self.sz,
            facecolor=self.fc)           #define the figure
        self.ax = axes()
        self.ax.set_title("Plot")
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        
  
        self.ev= [
            'resize_event',      'draw_event',          'key_press_event',
            'key_release_event', 'button_press_event',  'button_release_event',
            'scroll_event',      'motion_notify_event', 'pick_event',
            'idle_event',        'figure_enter_event',  'figure_leave_event',
            'axes_enter_event',  'axes_leave_event',    'close_event']
        self.handleOnClick  = self.Fig2D.canvas.mpl_connect(self.ev[4], self.OnClick)
        self.handleClose    = self.Fig2D.canvas.mpl_connect(self.ev[14],self.Close)
        self.handlePressKey = self.Fig2D.canvas.mpl_connect(self.ev[2], self.PressKey)
        self.x=0;self.y=0;
        self.key=''
        self.button=0
        self.CountButton=[0,0,0]  #CountButton[0] for button 1
                                  #CountButton[1] for button 2
                                  #CountButton[2] for button 3
        self.cmd=''               #command buffer
        self.OnClickAction=click
        self.PressKeyAction=press

    def OnClick(self,event):
        self.OnClickAction(self,event)
        draw()

    def PressKey(self,event):
        self.PressKeyAction(self,event)
        draw()

    def Close(self,event):
        self.Fig2D.canvas.mpl_disconnect(self.hOnClick)
        self.Fig2D.canvas.mpl_disconnect(self.hClose)
        self.Fig2D.canvas.mpl_disconnect(self.hPressKey)


class Space3D:

    def __init__(self,click,press,title="3D Figure",sz=(10,6),fc='w'):

        self.title=title
        self.sz   =sz
        self.fc   =fc
        self.Fig3D=figure(
            self.title,figsize=self.sz,
            facecolor=self.fc)           #define the figure
        self.ax = Axes3D(self.Fig3D)
        self.ax.set_title('Cartesian Coordinate System')
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_zlabel('z')
        self.ev= [
            'resize_event',      'draw_event',          'key_press_event',
            'key_release_event', 'button_press_event',  'button_release_event',
            'scroll_event',      'motion_notify_event', 'pick_event',
            'idle_event',        'figure_enter_event',  'figure_leave_event',
            'axes_enter_event',  'axes_leave_event',    'close_event']
        self.handleOnClick  = self.Fig3D.canvas.mpl_connect(self.ev[4], self.OnClick)
        self.handleClose    = self.Fig3D.canvas.mpl_connect(self.ev[14],self.Close)
        self.handlePressKey = self.Fig3D.canvas.mpl_connect(self.ev[2], self.PressKey)
        self.x=0;self.y=0;self.z=0
        self.seg=10
        self.PointSize=0.1
        self.key=''
        self.ShowAxes()
        self.button=0
        self.CountButton=[0,0,0]  #CountButton[0] for button 1
                                  #CountButton[1] for button 2
                                  #CountButton[2] for button 3
        self.cmd=''               #command buffer
        self.OnClickAction=click
        self.PressKeyAction=press


    def OnClick(self,event):
        M=self.ax.get_proj()
        print( "M =",M)
        print( "Azimuth = ",self.ax.azim, "Elevation = ",self.ax.elev)
        self.Gen3DCoord(event.xdata,event.ydata)
        print( "OnClick event\n2d Coordinates: ","X2d = ",
              event.xdata,"Y2d = ",event.ydata)
        print( "3D Coordinates: x = ", self.x,"y = ",self.y,"z = ",self.z)
        self.button=event.button
        self.OnClickAction(self)
        draw()

    def PressKey(self,event):
        self.key=event.key
        print("key ", event.key)
        if event.key.isalnum:
            self.PressKeyAction(self)
        draw()

    def Close(self,event):
        self.Fig3D.canvas.mpl_disconnect(self.hOnClick)
        self.Fig3D.canvas.mpl_disconnect(self.hClose)
        self.Fig3D.canvas.mpl_disconnect(self.hPressKey)



    def ShowAxes(self):
        self.ax.text(0,0,0," 0")
        self.ax.plot(
            [self.seg,-self.seg, 0,        0,        0, 0,        0,        0], # x
            [       0,        0, 0, self.seg,-self.seg, 0,        0,        0], # y
            [       0,        0, 0,        0,        0, 0, self.seg,-self.seg], # z
        color='y');
        self.ax.text( self.seg,        0,        0,  ' x')
        self.ax.text(        0, self.seg,        0,  ' y')
        self.ax.text(        0,        0, self.seg,  ' z')
        self.ax.text(-self.seg,        0,        0,  '-x')
        self.ax.text(        0,-self.seg,        0,  '-y')
        self.ax.text(        0,        0,-self.seg,  '-z')


    def PlotPoint(self):
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = self.PointSize * np.outer(np.cos(u), np.sin(v))+self.x
        y = self.PointSize * np.outer(np.sin(u), np.sin(v))+self.y
        z = self.PointSize * np.outer(np.ones(np.size(u)), np.cos(v))+self.z
        self.ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='k',alpha=.5)
        self.ax.text(self.x,self.y,self.z,
                '   ('+str(self.x)+', '+ str(self.y)+', '+str(self.z)+')')

    def PlotLine(self,From=np.mat([0,0,0]),To=np.mat([0,0,1])):
        F=From.copy();F=F.round(2)
        T=To.copy();T=T.round(2)
        X=[F.item(0),F.item(0)+T.item(0)]
        Y=[F.item(1),F.item(1)+T.item(1)]
        Z=[F.item(2),F.item(2)+T.item(2)]
        self.ax.plot(X,Y,Z)
        self.ax.text(X[1],Y[1],Z[1],
            '('+str(X[1])+','+str(Y[1])+','+str(Z[1])+')')

    def Gen3DCoord(self,xd,yd):
        print( "xd = ",xd,"yd = ",yd)
        s=self.ax.format_coord(xd, yd);
        print( "format coord: ",s)
        s=s.split(',')
        print("s: ",s)
        if len(s) > 2:
            s0=s[0].strip();print("s0: ",s0)
            s1=s[1].strip();print("s1: ",s1)
            s2=s[2].strip();print("s2: ",s2)
            n1=float(s0[2:])
            n2=float(s1[2:])
            n3=float(s2[2:])
            self.x=round(n1,4)
            self.y=round(n2,4)
            self.z=round(n3,4)

    def NB(self,s):   #Nota Bene
        self.ax.text(self.x,self.y,self.z,s)


