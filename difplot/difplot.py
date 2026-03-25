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


def difplot(xlist,
            ylist,
            xlabel,
            ylabel,
            figx = 15,
            figy = 10,
            fontSize=40,
            DPI = 300,
            tickDirection='in',
            tickSize=1,
            font='serif',
            lineWidth=1.5,
            borderWidth = 3,
            color='random',
            cmap = None,
            yflip=False,
            xscale='linear',
            yscale='linear',
            name='dif.png',
            xspan=[],
            yspan=[],
            linestyle=None,
            path='',
            vertical = None,
            leg=['best','20'],
            text=None,
            yTicks=[],
            xTicks=[],
            fill = [],
            usetex = True,
            zlist = None,
            contours=None,
            label_contours=False,
            labelled_contours=None,
            zlabel="z",
            labelSize=12,
            scatter=None): 
    '''plots a solved differential equation'''
    '''======PARAMETERS======'''
    #ylist takes an array of arrays, each entry is a list of yvalues to be plotted. Same for xlist
    #ylables takes an array of at least 1 entry each which labels the functions on y axis. If more than one function plotted on y axis
    #... then the first entry to both is the common label, which appear as the axes labels, and the following entries (at least two) should differentiate
    #... the functions on the y axis
    #yscaled and xscaled are booleans which if set to True, scale the y and x axes by Mpl
    #xspan and yspan control the ylims and xlims, if left blank, set automatically
    #color takes either an array of colors, or the string 'random' which plots each line with a random color

    _configure_rcparams(fontSize=fontSize, font=font, borderWidth=borderWidth, tickSize=tickSize, tickDirection=tickDirection, usetex=usetex, xtop=True, ytop=True)
    if linestyle is None:
        linestyle = ["solid"] * len(ylist)
    if color == 'random':
        if cmap is None:
            color = [f"#{random.randint(0, 0xFFFFFF):06X}" for _ in range(len(ylist))]
        else:
            colmap = cm.get_cmap(cmap)
            color = [colmap(i / max(len(ylist) - 1, 1)) for i in range(len(ylist))]


    fig = plt.figure(figsize=[figx,figy])
    axs = fig.subplots()
    
    if isinstance(ylabel,str):
        axs.set_ylabel(ylabel,fontsize =  fontSize,labelpad = 25)
        labely = False
        leg = False
    if isinstance(ylabel, (list, tuple, np.ndarray)):
        labely = True
        ylabels = [ylabel[i] for i in range(1,len(ylist)+1)]
        axs.set_ylabel(ylabel[0],fontsize =  fontSize,labelpad = 25)
   
    if not labely:
        for l, yy in enumerate(ylist):
            axs.plot(xlist[l], yy, color=color[l], linestyle=linestyle[l], linewidth=lineWidth)
    if labely:
        for l, yy in enumerate(ylist):
            axs.plot(xlist[l], yy, color=color[l], label=(ylabels[l]), linestyle=linestyle[l], linewidth=lineWidth)

    axs.set_xlabel(xlabel,fontsize =  fontSize,labelpad = 25)
    
    
    if xspan:
        axs.set_xlim(xspan[0], xspan[1])
    if yspan:
        axs.set_ylim(yspan[0], yspan[1])
    if yflip:
        axs.invert_yaxis()
    axs.set_xscale(xscale)
    axs.set_yscale(yscale)
    
    axs.minorticks_on()
    
    points = []
    
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

        
    # ==========================================================
    # Optional fill overlay
    # ==========================================================    
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
    # ==========================================================
    # Optional contour overlay
    # ==========================================================
    if contours is not None:

        try:
            levels, colors, linestyles = contours
        except Exception:
            levels = []
            colors = "black"
            linestyles = "solid"

        # Ensure zlist nested
        if not isinstance(zlist[0], (list, tuple, np.ndarray)):
            zlist = [zlist]

        Nz = len(zlist)

        # -------------------------
        # Normalize levels
        # -------------------------
        if not isinstance(levels, (list, tuple, np.ndarray)):
            levels = [levels]

        if not isinstance(levels[0], (list, tuple, np.ndarray)):
            levels = [levels] * Nz
        elif len(levels) != Nz:
            levels = [levels[0]] * Nz

        # -------------------------
        # Normalize styling safely
        # -------------------------
        def normalize_style(style, default):
            try:
                if isinstance(style, (list, tuple)):
                    if len(style) == Nz:
                        return style
                    if isinstance(style[0], (list, tuple)):
                        return style
                return [style] * Nz
            except Exception:
                return [default] * Nz

        colors = normalize_style(colors, "black")
        linestyles = normalize_style(linestyles, "solid")

        # -------------------------
        # Normalize labelled_contours
        # -------------------------
        if labelled_contours is None:
            labelled_contours = [None] * Nz
        elif not isinstance(labelled_contours, (list, tuple)):
            labelled_contours = [labelled_contours] * Nz
        elif not isinstance(labelled_contours[0], (list, tuple)):
            labelled_contours = [labelled_contours] * Nz
        elif len(labelled_contours) != Nz:
            labelled_contours = [labelled_contours[0]] * Nz

        # -------------------------
        # Draw contours
        # -------------------------
        for i, z in enumerate(zlist):
            temppoints = []

            for j, level in enumerate(levels[i]):
                val = float(level)
                val_str = f"{val:.2f}".rstrip("0").rstrip(".")
                val_0 = float(val_str)

                try:
                    c = colors[i][j] if isinstance(colors[i], (list, tuple)) else colors[i]
                except Exception:
                    c = "black"

                try:
                    ls = linestyles[i][j] if isinstance(linestyles[i], (list, tuple)) else linestyles[i]
                except Exception:
                    ls = "solid"

                cont = axs.contour(
                    xlist,
                    ylist,
                    z,
                    levels=[level],
                    colors=[c],
                    linestyles=[ls]
                    )
                for seglist in cont.allsegs:
                    for seg in seglist:
                        temppoints.append(seg)

                if label_contours[i]:

                    allowed = labelled_contours[i]

                    if allowed is None or val_0 in allowed:
                        

                        axs.clabel(
                            cont,
                            fmt={level: f"{zlabel} = {val_str}"},
                            inline=True,
                            fontsize=labelSize
                        )
            points.append(temppoints)

     # ==========================================================
    # Optional scatter overlay
    # ==========================================================
    if scatter is not None:

        # Normalize to list of scatter sets
        if not isinstance(scatter[0], (list, tuple, np.ndarray)):
            scatter = [scatter]

        marker_map = {
            'circle': 'o',
            'square': 's',
            'triangle': '^',
            'triangle_down': 'v',
            'diamond': 'D',
            'star': '*',
            'cross': 'x',
            'plus': '+'
        }

        for s in scatter:
            if len(s) < 5:
                continue

            xpoints = s[0]
            ypoints = s[1]
            symbol  = s[2]
            scolor  = s[3]
            ssize   = s[4]
            slabel  = s[5] if len(s) > 5 else 'Scatter points'
            xerr    = s[6] if len(s) > 6 else None
            yerr    = s[7] if len(s) > 7 else None

            marker = marker_map.get(symbol, symbol)

        if xerr is not None or yerr is not None:
            axs.errorbar(
                xpoints, ypoints,
                xerr=xerr, yerr=yerr,
                fmt=marker,
                color=scolor,
                markersize=np.sqrt(ssize),   # errorbar uses pts, scatter uses pts²
                capsize=4,
                capthick=1,
                elinewidth=1,
                label=slabel
            )
        else:
            axs.scatter(
                xpoints, ypoints,
                marker=marker,
                c=scolor,
                s=ssize,
                label=slabel
            )
    
    if leg:
        plt.legend(loc=leg[0], fontsize=leg[1])

    plt.savefig( path + name +  '.pdf',dpi=DPI, bbox_inches = "tight")
    return points
    
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
