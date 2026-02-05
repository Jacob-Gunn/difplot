'''imports'''
import os
import glob
import math
import random

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm, colors
from matplotlib.lines import Line2D
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Polygon, PathPatch
from matplotlib.path import Path
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset
from matplotlib.ticker import LogLocator, AutoMinorLocator, MultipleLocator


def _configure_rcparams(fontSize=14, font='serif', borderWidth=1, tickSize=1, tickDirection='in', usetex=False, xtop=True, ytop=True, labelSize=None):
    """Configure common matplotlib rcParams used by plotting helpers.

    Kept small and explicit to avoid repeating large rc blocks.
    """
    plt.rcParams.update({'font.size': fontSize, 'font.family': font})
    plt.rcParams['axes.linewidth'] = borderWidth

    # tick sizes
    plt.rcParams['xtick.major.size'] = 12 * tickSize
    plt.rcParams['xtick.major.width'] = 2 * tickSize
    plt.rcParams['xtick.minor.size'] = 8 * tickSize
    plt.rcParams['xtick.minor.width'] = 2 * tickSize

    plt.rcParams['ytick.major.size'] = 12 * tickSize
    plt.rcParams['ytick.major.width'] = 2 * tickSize
    plt.rcParams['ytick.minor.size'] = 8 * tickSize
    plt.rcParams['ytick.minor.width'] = 2 * tickSize

    if labelSize is not None:
        plt.rcParams['xtick.labelsize'] = labelSize
        plt.rcParams['ytick.labelsize'] = labelSize
    else:
        plt.rcParams['xtick.labelsize'] = fontSize
        plt.rcParams['ytick.labelsize'] = fontSize

    plt.rcParams['xtick.direction'] = tickDirection
    plt.rcParams['ytick.direction'] = tickDirection
    plt.rcParams['xtick.top'] = xtop
    plt.rcParams['ytick.right'] = ytop
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['text.usetex'] = usetex


def difplot(ylist,xlist,xlabel,ylabels,figx = 15,figy = 10,fontSize=40,DPI = 300,tickDirection='in',tickSize=1,font='serif',lineWidth=1.5,borderWidth = 3,color='random',cmap = None,yflip=False,xscale='linear',yscale='linear',name='dif.png',xscaled=1,yscaled=1,Mline=False,xspan=[],yspan=[],linestyle=None,path='',top = False,Loc='best',vertical = None,leg=['best','10'],xminor=0,yminor=0,text=None,numTicksy=50,numTicksx = 50,yTicks=[],xTicks=[],fill = [],usetex = False):
    '''plots a solved differential equation'''
    '''======PARAMETERS======'''
    #ylist takes an array of arrays, each entry is a list of yvalues to be plotted. Same for xlist
    #ylables takes an array of at least 1 entry each which labels the functions on y axis. If more than one function plotted on y axis
    #... then the first entry to both is the common label, which appear as the axes labels, and the following entries (at least two) should differentiate
    #... the functions on the y axis
    #yscaled and xscaled are booleans which if set to True, scale the y and x axes by Mpl
    #xspan and yspan control the ylims and xlims, if left blank, set automatically
    #color takes either an array of colors, or the string 'random' which plots each line with a random color
    yl = ''
    xl = ''
    _configure_rcparams(fontSize=fontSize, font=font, borderWidth=borderWidth, tickSize=tickSize, tickDirection=tickDirection, usetex=usetex, xtop=True, ytop=True)
    if xscaled == 1:
        xscaled = [1] * (len(xlist) + 1)
    if yscaled == 1:
        yscaled = [1] * (len(ylist) + 1)
    if linestyle is None:
        linestyle = ["solid"] * len(ylist)
    if color == 'random':
        if cmap is None:
            color = [f"#{random.randint(0, 0xFFFFFF):06X}" for _ in range(len(ylist))]
        else:
            colmap = cm.get_cmap(cmap)
            color = [colmap(i / max(len(ylist) - 1, 1)) for i in range(len(ylist))]

    for l, arr in enumerate(xlist):
        xlist[l] = [i / xscaled[l] for i in arr]
    if xscaled != 1:
        xl = ''
    for l, arr in enumerate(ylist):
        ylist[l] = [i / yscaled[l] for i in arr]
    if yscaled != 1:
        yl = ''
    fig = plt.figure(figsize=[figx,figy])
    axs = fig.subplots()
    if top != False:
        ax2 = axs.twiny()   
    if len(ylabels) == 1:
        axs.plot(xlist[0], ylist[0], color=color[0], label=(ylabels[0] + ' vs ' + xlabel), linestyle=linestyle[0], linewidth=lineWidth)
        if Mline:
            if 'aT' in globals() and 'M1' in globals():
                axs.plot([aT(M1) for _ in range(10)], [ylist[0][int(np.size(ylist[0]) / 10) * i] for i in range(10)], linestyle="dashed", linewidth=lineWidth)
            else:
                print('Mline requested but aT or M1 not defined; skipping Mline')
        if top is not False:
            ax2.plot(xlist[0], ylist[0], color='None', linestyle=linestyle[0], linewidth=lineWidth)
    else:
        for l, yy in enumerate(ylist):
            if l > len(ylabels) - 2:
                axs.plot(xlist[l], yy, color=color[l], linestyle=linestyle[l], linewidth=lineWidth)
            else:
                axs.plot(xlist[l], yy, color=color[l], label=(ylabels[l + 1]), linestyle=linestyle[l], linewidth=lineWidth)
            if top is not False:
                ax2.plot(xlist[l], yy, color='None', linewidth=lineWidth)
        if Mline:
            if 'aT' in globals() and 'M1' in globals():
                axs.plot([aT(M1) for _ in range(10)], [ylist[0][int(np.size(ylist[0]) / 10) * i] for i in range(10)], linestyle="dashed")
            else:
                print('Mline requested but aT or M1 not defined; skipping Mline')
    axs.set_xlabel(xlabel+xl,fontsize =  fontSize,labelpad = 25)
    axs.set_ylabel(ylabels[0],fontsize =  fontSize,labelpad = 25)
    if xspan:
        axs.set_xlim(xspan[0], xspan[1])
    if yspan:
        axs.set_ylim(yspan[0], yspan[1])
    if yflip:
        axs.invert_yaxis()
    axs.set_xscale(xscale)
    axs.set_yscale(yscale)
    
    axs.minorticks_on()

    if np.size(ylabels) != 1:
        ylabels = [ylabels[i] for i in range(1, np.size(ylabels))]
    if leg:
        plt.legend(ylabels, loc=leg[0], fontsize=leg[1])
    if vertical != None:
        for v in vertical:
            plt.axvline(x=v[0], ymin=v[1], ymax=v[2],color=v[3],linestyle = v[4])
    if text != None:
        for t in text:
            plt.text(t[0],t[1],t[2],rotation=t[4],color = t[3],size=t[5])
    if xTicks:
        plt.xticks(xTicks)
    if yTicks:
        plt.yticks(yTicks)
    for tick in axs.get_xticklabels(minor = False):
        tick.set_y(-0.01)  # Adjust y-position of the tick labels

        
        
    for f in fill:
        if f[2] == None:
            # Create a polygon from the contour line
            polygon = Polygon(np.column_stack((f[0], f[1])), closed=True, edgecolor='none')
            
            # Use Path to create a mask outside the contour polygon
            fpath = Path(polygon.get_xy())
            outer_path = Path([
                [axs.get_xlim()[0], axs.get_ylim()[0]],
                [axs.get_xlim()[0], axs.get_ylim()[1]],
                [axs.get_xlim()[1], axs.get_ylim()[1]],
                [axs.get_xlim()[1], axs.get_ylim()[0]],
                [axs.get_xlim()[0], axs.get_ylim()[0]],
                    ])
            
            # Define a combined path that subtracts the contour path from the outer rectangle path
            combined_path = Path.make_compound_path(outer_path, fpath)
            
            # Add a patch for shading outside the contour region
            outside_patch = PathPatch(combined_path, facecolor=f[3], edgecolor='none', alpha=f[4])
            axs.add_patch(outside_patch)
        else:
            plt.fill_between(f[0], f[1], f[2], color=f[3], alpha=f[4])
    

    plt.savefig( path + name +  '.pdf',dpi=DPI, bbox_inches = "tight")
    
def difSubPlot(ylist,xlist,xlabel,ylabels,figx = 15,figy = 10,fontSize=40,tickDirection='in',tickSize=1,font='serif',lineWidth=1.5,borderWidth = 3,color='random',xscale='linear',yscale='linear',name='dif.png',xspan=[],yspan=[],linestyle=None,path='Figures/',top = False,Loc='best',vertical = None,leg=['best','10'],xminor=0,yminor=0,text=None,numTicksy=50,numTicksx = 50):
    '''plots a subplot with same arguments as difplot except no option to scale, Mline, flip or cmap'''
    _configure_rcparams(fontSize=fontSize, font=font, borderWidth=borderWidth, tickSize=tickSize, tickDirection=tickDirection, usetex=False, xtop=True, ytop=True)
    if linestyle is None:
        linestyle = [["solid"] * len(ylist[0]), ["solid"] * len(ylist[1])]
    if color == 'random':
        color = [
            [f"#{random.randint(0, 0xFFFFFF):06X}" for _ in range(len(ylist[0]))],
            [f"#{random.randint(0, 0xFFFFFF):06X}" for _ in range(len(ylist[1]))],
        ]
    fig, axs = plt.subplots(2,figsize=[figx,figy])
    if top != False:
        ax2 = axs.twiny()  
    for i in range(0,len(ylabels)):
        if len(ylabels[i])==1:
            axs[i].plot(xlist[i][0],ylist[i][0],color=color[i][0],label=(ylabels[i][0]+' vs ' + xlabel),linestyle=linestyle[i][0],linewidth = lineWidth)
            if top != False:
                ax2.plot(xlist[i][0],ylist[i][0],color='None',linestyle=linestyle[i][0],linewidth = lineWidth)
        else:
            for l in range(0 ,len(ylist[i])):
                if l > len(ylabels[i])-2:
                    axs[i].plot(xlist[i][l],ylist[i][l],color=color[i][l],linestyle=linestyle[i][l],linewidth = lineWidth)
                else:
                    axs[i].plot(xlist[i][l],ylist[i][l],color=color[i][l],label=ylabels[i][l+1],linestyle=linestyle[i][l],linewidth = lineWidth)
                if top != False:
                    ax2.plot(xlist[i][l],ylist[i][l],color='None',linewidth = lineWidth)
    axs[0].set_xlabel(xlabel[0],fontsize =  fontSize)
    axs[0].set_ylabel(ylabels[0],fontsize=fontSize)
    axs[1].set_xlabel(xlabel[1],fontsize =  fontSize)
    axs[1].set_ylabel(ylabels[1],fontsize=fontSize)
    if xspan !=[]:
        axs[0].set_xlim(xspan[0][0],xspan[0][1])
        axs[1].set_xlim(xspan[1][0],xspan[1][1])
    if yspan !=[]:
        axs[0].set_ylim(yspan[0][0],yspan[0][1])  
        axs[1].set_ylim(yspan[1][0],yspan[1][1])  
    axs[0].set_xscale(xscale)
    axs[0].set_yscale(yscale)
    axs[1].set_xscale(xscale)
    axs[1].set_yscale(yscale)
    if top != False:
        ax2.set_xscale(xscale)
        ax2.set_xticklabels([str(round(float(top[0](ax2.get_xticks()[i])/M1),2)) for i in range(0,np.size(ax2.get_xticks()))])
        ax2.set_xlabel(top[1])
        #ax2.xaxis.set_major_formatter(FormatStrFormatter('{x:,.2f}'))
    #plt.tight_layout()
    if np.size(ylabels) != 1:
        ylabels[0] = [ylabels[0][i] for i in range(1,np.size(ylabels[0]))]
        ylabels[1] = [ylabels[1][i] for i in range(1,np.size(ylabels[1]))]
    if leg != False:
        axs[0].legend(ylabels[0],loc=leg[0][0],fontsize=leg[0][1])
        axs[1].legend(ylabels[1],loc=leg[1][0],fontsize=leg[1][1])
    if vertical != None:
        for v in vertical[0]:
            axs[0].axvline(x=v[0], ymin=v[1], ymax=v[2],color=v[3],linestyle = v[4])
        for v in vertical[1]:
            axs[1].axvline(x=v[0], ymin=v[1], ymax=v[2],color=v[3],linestyle = v[4])
    if text != None:
        for t in text[0]:
            axs[0].text(t[0],t[1],t[2],rotation=t[4],color = t[3],size=t[5])
        for t in text[1]:
            axs[0].text(t[0],t[1],t[2],rotation=t[4],color = t[3],size=t[5])
    plt.savefig(path + name + '.jpeg')
    

    
def contplot(xlist,ylist,zlist,xlabel,ylabel,zlabel,figx = 15,figy = 10,vmax=0,vmin= 0,fontSize=20,contours = None,zlist2 = [],alt = ['None'],tickDirection='in',tickSize=1,font='serif',lineWidth=1.5,borderWidth = 3,color='random',cmap='PuBu_r',xscale='linear',yscale='linear',name='dif.png',xspan=[],yspan=[],linestyle=None,path='Figures/',top = False,Loc='best',vertical = None,leg=['best','10'],returnPoints = False,text=None,logColors=True,lines=[],inLine = False,legend_boolean = None,algorithm = 'mpl2014',labelSize = 15):
    '''plots a subplot with same arguments as difplot except no option to scale, Mline, flip or cmap'''
    plt.rcParams.update({'font.size': fontSize,'font.family':font})
    plt.rcParams['axes.linewidth'] = borderWidth

    #x ticks dimension
    plt.rcParams['xtick.major.size'] = 12*tickSize
    plt.rcParams['xtick.major.width'] = 2*tickSize
    plt.rcParams['xtick.minor.size'] = 8*tickSize
    plt.rcParams['xtick.minor.width'] = 2*tickSize
    
    
    
    #y ticks dimension
    plt.rcParams['ytick.major.size'] = 12*tickSize
    plt.rcParams['ytick.major.width'] = 2*tickSize
    plt.rcParams['ytick.minor.size'] = 8*tickSize
    plt.rcParams['ytick.minor.width'] = 2*tickSize
    
    
    
    #tick direction
    plt.rcParams['xtick.direction'] = tickDirection
    plt.rcParams['ytick.direction'] = tickDirection
    
    plt.rcParams['xtick.labelsize'] = labelSize  # Adjust as needed
    plt.rcParams['ytick.labelsize'] = labelSize  # Adjust as needed
    
    
    
    #other options
    plt.rcParams['xtick.top'] = False
    plt.rcParams['ytick.right'] = False
    plt.rcParams['axes.unicode_minus'] = False

    plt.rcParams['text.usetex'] = False
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['mathtext.fontset'] = 'cm'  # Computer Modern
    plt.rcParams['mathtext.rm'] = 'Times New Roman'
    plt.rcParams['mathtext.it'] = 'Times New Roman:italic'

    

    
    plt.rcParams['font.weight'] = 'normal'
    plt.rcParams['axes.labelweight'] = 'normal'  # Axis label font weight
    plt.rcParams['mathtext.default'] = 'regular'  # Ensure math text is not bold


    
    if legend_boolean == None:
        legend_boolean = [True for i in contours[0][1]]
    
    legend_labels,legend_lines = [],[]
    fig, ax = plt.subplots(1, 1,figsize=[figx,figy])
    
    contour_points = []

    if logColors:
        if vmax != 0 and vmin != 0:
            Norm = colors.LogNorm(vmax=vmax, vmin=vmin)
        else:
            Norm = colors.LogNorm()
    else:
        if vmax != 0 and vmin != 0:
            Norm = colors.Normalize(vmax=vmax, vmin=vmin)
        else:
            Norm = colors.Normalize()
    for C in contours:
        cont = ax.contour(xlist,ylist,zlist,levels=[C[0]],linestyles = C[2],colors = C[1],linewidths = lineWidth,algorithm = algorithm)
        if inLine == True:
            ax.clabel(cont, inline=True, fontsize=leg[1],fmt = zlabel)
        elif legend_boolean[0] == True:
            legend_lines.append(Line2D([0], [0], color=C[1][0], linestyle=C[2], linewidth=lineWidth))
            legend_labels.append(zlabel)
            
        if returnPoints == True:
            for collection in cont.collections:
                for path in collection.get_paths():
                    contour_points.append(path.vertices)  # path.vertices is a 2D array of points (x, y)

    
        for j in range(0,len(zlist2)):
            cont2 = ax.contour(xlist,ylist,zlist2[j],levels=[C[0]],linestyles = C[j+3],colors = C[1][j+1],algorithm = algorithm)    
            if inLine == True:
                ax.clabel(cont2, inline=inLine, fontsize=leg[1],fmt = leg[2][j])
            elif legend_boolean[j + 1] == True:
                legend_lines.append(Line2D([0], [0], color=C[1][j + 1], linestyle=C[j+ 3], linewidth=lineWidth))
                legend_labels.append(leg[2][j])
            if returnPoints == True:
                for collection in cont2.collections:
                    for path in collection.get_paths():
                        contour_points.append(path.vertices)  # path.vertices is a 2D array of points (x, y)
        
    ax.legend(legend_lines, legend_labels,loc = leg[0],fontsize = leg[1])
        
    ax.set_yscale(yscale)
    ax.set_xscale(xscale)
    ax.set_xlabel(xlabel,fontsize =  fontSize)
    ax.set_ylabel(ylabel,fontsize =  fontSize)

    
    ax.minorticks_on()



    if xspan !=[]:
        ax.set_xlim(xspan[0],xspan[1])
    if yspan !=[]:
        ax.set_ylim(yspan[0],yspan[1])   


    if text != None:
        for t in text:
            ax.text(t[0],t[1],t[2],rotation=t[4],color = t[3],size = t[5])
    for l in lines:
        ax.plot(l[0],l[1],color=l[2],linestyle=l[3])
    if alt != ['None']:
        for a in alt:
            ax.contour(a[0],a[1],a[2],levels=[a[3]],colors = a[4],linestyles = a[5],linewidths = a[6])
    if vertical != None:
        for v in vertical:
            plt.axvline(x=v[0], ymin=v[1], ymax=v[2],color=v[3],linestyle = v[4])
    
    
    if returnPoints == True:
        return contour_points
    else:
        plt.savefig(path + name + '.pdf')
    
        
    
    
def colplot(xlist,ylist,zlist,xlabel,ylabel,zlabel,figx = 15,figy = 10,vmax=0,vmin= 0,fontSize=20,contours = None,zlist2 = [],alt = ['None'],tickDirection='in',tickSize=1,font='serif',lineWidth=1.5,borderWidth = 3,color='random',cmap='PuBu_r',xscale='linear',yscale='linear',name='dif.png',xspan=[],yspan=[],linestyle=None,path='Figures/',top = False,Loc='best',vertical = None,leg=['best','10'],text=None,logColors=True,lines=[],inLine = False,legend_boolean = None,returnPoints = False):
    '''plots a subplot with same arguments as difplot except no option to scale, Mline, flip or cmap'''
    plt.rcParams.update({'font.size': fontSize,'font.family':font})
    plt.rcParams['axes.linewidth'] = borderWidth
    plt.rcParams.update({
    "text.usetex": True,             # Enable LaTeX rendering
    "font.family": "serif",          # Use a serif font by default
    "text.latex.preamble": r"\usepackage{amsmath}",  # Optional, for advanced math formatting
})

    #x ticks dimension
    plt.rcParams['xtick.major.size'] = 12*tickSize
    plt.rcParams['xtick.major.width'] = 2*tickSize
    plt.rcParams['xtick.minor.size'] = 8*tickSize
    plt.rcParams['xtick.minor.width'] = 2*tickSize
    
    
    
    #y ticks dimension
    plt.rcParams['ytick.major.size'] = 12*tickSize
    plt.rcParams['ytick.major.width'] = 2*tickSize
    plt.rcParams['ytick.minor.size'] = 8*tickSize
    plt.rcParams['ytick.minor.width'] = 2*tickSize
    
    
    
    #tick direction
    plt.rcParams['xtick.direction'] = tickDirection
    plt.rcParams['ytick.direction'] = tickDirection
    
    plt.rcParams['xtick.labelsize'] = fontSize
    plt.rcParams['ytick.labelsize'] = fontSize
    
    
    
    #other options
    plt.rcParams['xtick.top'] = True
    plt.rcParams['ytick.right'] = True
    plt.rcParams['axes.unicode_minus'] = False
    contour_points = []
    
    if legend_boolean is None:
        legend_boolean = [True] * len(contours[0][1])

    legend_labels, legend_lines = [], []
    fig, ax = plt.subplots(1, 1, figsize=[figx, figy])
    if logColors:
        if vmax != 0 and vmin != 0:
            Norm = colors.LogNorm(vmax=vmax, vmin=vmin)
        else:
            Norm = colors.LogNorm()
    else:
        if vmax != 0 and vmin != 0:
            Norm = colors.Normalize(vmax=vmax, vmin=vmin)
        else:
            Norm = colors.Normalize()

    pcm = ax.pcolor(xlist, ylist, zlist, cmap=cmap, shading='auto', norm=Norm)
    
    for C in contours:
        cont = ax.contour(xlist,ylist,zlist,levels=[C[0]],linestyles = C[2],colors = C[1][0],linewidths = lineWidth)
        if inLine == True:
            ax.clabel(cont, inline=True, fontsize=leg[1],fmt = zlabel)
        elif legend_boolean[0] == True:
            legend_lines.append(Line2D([0], [0], color=C[1][0], linestyle=C[2], linewidth=lineWidth))
            legend_labels.append(zlabel)
        if returnPoints == True:
            for collection in cont.collections:
                for path in collection.get_paths():
                    contour_points.append(path.vertices)
    
        for j in range(0,len(zlist2)):
            cont2 = ax.contour(xlist,ylist,zlist2[j],levels=[C[0]],linestyles = C[j+3],colors = C[1][j+1])    
            if inLine == True:
                ax.clabel(cont2, inline=inLine, fontsize=leg[1],fmt = leg[2][j])
            elif legend_boolean[j + 1] == True:
                legend_lines.append(Line2D([0], [0], color=C[1][j + 1], linestyle=C[j+ 3], linewidth=lineWidth))
                legend_labels.append(leg[2][j])
            if returnPoints == True:
                for collection in cont2.collections:
                    for path in collection.get_paths():
                        contour_points.append(path.vertices)
        
    ax.legend(legend_lines, legend_labels,loc = leg[0],fontsize = leg[1])
    ax.minorticks_on()   
 
    if xscale == 'log':
        ax.set_xscale(xscale)
        ax.xaxis.set_minor_locator(LogLocator())
    
    if yscale == 'log':
        ax.set_yscale(yscale)
        ax.xaxis.set_minor_locator(LogLocator())

        
        
    ax.set_xlabel(xlabel,fontsize =  fontSize)
    ax.set_ylabel(ylabel,fontsize =  fontSize)
    
    
    if xspan !=[]:
        ax.set_xlim(xspan[0],xspan[1])
    if yspan !=[]:
        ax.set_ylim(yspan[0],yspan[1])   


    if text != None:
        for t in text:
            ax.text(t[0],t[1],t[2],rotation=t[4],color = t[3],size = t[5])
    for l in lines:
        ax.plot(l[0],l[1],color=l[2],linestyle=l[3])
    if alt != ['None']:
        for a in alt:
            ax.contour(a[0],a[1],a[2],levels=[a[3]],colors = a[4],linestyles = a[5],linewidths = a[6])
    if vertical != None:
        for v in vertical:
            plt.axvline(x=v[0], ymin=v[1], ymax=v[2],color=v[3],linestyle = v[4])
    
    for tick in ax.get_xticklabels(minor = False):
        tick.set_y(-0.01)  # Adjust y-position of the tick labels

    if returnPoints == True:
        return contour_points
    else: 
        plt.savefig(path + name + '.pdf')
    
def read(path,master = [],output = 0,dtype = float,mi = 10000,length = 9,neg = 1, ref = [],size = None):
    Ys = []
    Mtemp,Mcheck = [],[]
    filetemp,iterable = '',[]
    sort = False 
    if master != []:
        for m in master:
            ms = f'{m:.1e}'
            ms = path + ms + '.txt'
            iterable.append([float(m), ms])
    else:
        for filename in glob.glob(path + "*"):
            name = os.path.basename(filename)[:length]
            iterable.append([float(name),filename])
        sort = True
    for it in iterable:
        Ystemp = []
        M, Mstring = it[0], f'{it[0]:.1e}'
        if ref:
            Mcheck.append(float(Mstring))
        data = np.genfromtxt(it[1], dtype=dtype)
        if output == 3:
            print(f'Reading file {Mstring}')
        if size is None:
            size = len(data)
        for j in range(0, size):
            nan = False
            if np.size(data[j]) != 1:
                for k in range(0, np.size(data[j])):
                    if np.isnan(data[j][k]):
                        if output != 1:
                            print(f'Nan detected in {Mstring}')
                        nan = True
                if j <= mi and not nan:
                    datareal = [data[j][k].real for k in range(0, np.size(data[j]))]
                    Ystemp.append(neg * datareal)
            else:
                if j <= mi and not nan and not np.isnan(data[j]):
                    Ystemp.append(neg * data[j].real)
                else:
                    pass
        Mtemp.append(M)
        Ys.append(Ystemp)
    if ref:
        for m in ref:
            ms = f'{m:.1e}'
            if float(ms) in Mcheck:
                pass
            else:
                if output != 1:
                    print(f'Missing mass {m} detected')
    if sort:
        sorted_indices = sorted(range(len(Mtemp)), key=lambda i: Mtemp[i])
        Msorted = [Mtemp[i] for i in sorted_indices]
        Ysorted = [Ys[i] for i in sorted_indices]
        return [Msorted, Ysorted]
    else:
        return [Mtemp, Ys]
    
def read1D(path,master = [],output = 0,dtype = float,mi = 10000,correct = False,length = 9,neg = 1, ref = []):
    vals,fileVals = [],[]
    filetemp,iterable = '',[]
    
    for filename in glob.glob(path + "*"):
        name = os.path.basename(filename)[:length]
        iterable.append([float(name), filename])
    sort = True
    for it in iterable:
        valstemp = []
        fileVal, nameString = it[0], f'{it[0]:.1e}'
        if output == 3:
            print(f'Reading file {nameString}')

        data = np.genfromtxt(it[1], dtype=dtype)
        if np.size(data) != 1:
            nantag = False
            for i in range(0, np.size(data)):
                if np.issubdtype(np.dtype(dtype), np.complexfloating):
                    data[i] = float(data[i].real)
                if np.isnan(data[i]):
                    if output != 1:
                        print(f'Nan detected in {nameString}')
                    nantag = True
            if not nantag:
                vals.append(data)
                fileVals.append(fileVal)
        else:
            if np.issubdtype(np.dtype(dtype), np.complexfloating):
                data = float(data.real)

            if np.isnan(data):
                if output != 1:
                    print(f'Nan detected in {nameString}')
                pass
            else:
                vals.append(data)
                fileVals.append(fileVal)
    sorted_indices = sorted(range(len(fileVals)), key=lambda i: fileVals[i])
    valSorted = [vals[i] for i in sorted_indices]
    fileSorted = [fileVals[i] for i in sorted_indices]
    return [valSorted,fileSorted]
    



def sample(data, N, tol=1e-3, maxD=np.inf, max_iter=50,even = 100):
    """
    Downsample a 2D array [x, y] into N points preserving behaviour of y(x).
    Always covers full x-range and enforces maxD spacing.

    Parameters
    ----------
    data : np.ndarray
        Input array of shape (M, 2) with columns [x, y].
    N : int
        Number of output points (N > 2).
    tol : float
        Initial tolerance guess (will be adapted).
    maxD : float
        Maximum allowed difference in x between consecutive points.
    max_iter : int
        Maximum number of iterations to adjust tolerance.

    Returns
    -------
    np.ndarray
        Downsampled array of shape (N, 2).
    """
    x, y = data[:, 0], data[:, 1]

    def select_points(curr_tol):
        dx = np.diff(x)
        dy = np.diff(y)
        slope = np.abs(dy / dx)

        # emphasize steep slopes
        weights = slope / (curr_tol + slope)
        weights /= np.sum(weights)

        cdf = np.concatenate(([0], np.cumsum(weights)))
        target_cdf = np.linspace(0, 1, N-1)[1:-1]
        indices = np.searchsorted(cdf, target_cdf)

        return np.unique(np.concatenate(([0], indices, [len(x)-1])))

    # search bounds for tol
    low_tol, high_tol = 1e-12, 1e3
    used_tol = tol
    final_idx = None

    for _ in range(max_iter):
        idx = select_points(used_tol)

        # enforce maxD strictly
        enforced = [idx[0]]
        for j in idx[1:]:
            while x[j] - x[enforced[-1]] > maxD:
                # insert closest index satisfying maxD
                mid = np.searchsorted(x, x[enforced[-1]] + maxD)
                if mid >= j:  # avoid infinite loop
                    break
                enforced.append(mid)
            enforced.append(j)
        idx = np.array(enforced)

        # check constraints
        if len(idx) == N and np.all(np.diff(x[idx]) <= maxD) and x[idx[0]] == x[0] and x[idx[-1]] == x[-1]:
            final_idx = idx
            break

        # adjust tolerance
        if len(idx) > N:
            low_tol = used_tol
            used_tol = (used_tol + high_tol) / 2
        else:
            high_tol = used_tol
            used_tol = (used_tol + low_tol) / 2

    # fallback if no perfect solution
    if final_idx is None:
        idx = select_points(used_tol)
        # enforce range and maxD again
        enforced = [0]
        for j in idx[1:]:
            while x[j] - x[enforced[-1]] > maxD:
                mid = np.searchsorted(x, x[enforced[-1]] + maxD)
                if mid >= j:
                    break
                enforced.append(mid)
            enforced.append(j)
        enforced[-1] = len(x)-1
        idx = np.array(enforced)

        # trim/pad to exactly N while keeping range + maxD
        if len(idx) > N:
            keep = np.linspace(0, len(idx)-1, N, dtype=int)
            final_idx = idx[keep]
        else:
            extra = np.linspace(0, len(x)-1, N, dtype=int)
            final_idx = np.unique(np.sort(np.concatenate([idx, extra])))[:N]

    for j in range(1,even):
        index = int( j*((np.size(y)-1)/even))
        if index not in final_idx:
            final_idx = np.append(final_idx,index)
            
    for j in range(1,10):
        index,indexm = j,int( (np.size(y)-1) - j)
        if index not in final_idx:
            final_idx = np.append(final_idx,index)
            
            
    final_idx = sorted(final_idx)
    return data[final_idx]
