from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle
import at
import numpy as np


colors = {
    "beta_x": ["#1f77b4", "#aec7e8", "#005288"],
    "beta_y": ["#d62728", "#ff9896", "#800000"],
    "dispersion": ["#2ca02c", "#98df8a", "#006400"]
}


def linear_plot(section, title= "Plot", x_label= "s[m]",y_label = "βₓ/βᵧ"):
    figure = Figure(figsize=(6,4))
    gs = GridSpec(20,1,figure =figure)
    
    
    ax1 = figure.add_subplot(gs[0:5,0])
    ax2 = figure.add_subplot(gs[5:17,0],sharex = ax1)
    ax3 = figure.add_subplot(gs[17:,0],sharex = ax1)
    
    refpts = list(range(len(section)))
    _,_,twiss  = at.get_optics(section, refpts=refpts, get_chrom=False)
    
    #ax1.set_title(title)
    ax1.tick_params(labelbottom = False)
    ax1.set_xlabel("")
    ax1.plot(twiss.s_pos,twiss.dispersion[:,0], label = "Dₓ", color = colors["dispersion"][0])
    ax1.set_ylim(0)
    ax1.legend()
    figure.subplots_adjust(left=0.07, right=0.98, top=0.96, bottom=0.05,hspace=0)
    ax2.set_xlabel("")
    ax2.set_ylabel(y_label)
    ax2.set_xlim(0,max(twiss.s_pos))
    # ax2.set_ylim(min(min(twiss.betx),min(twiss.bety)),max(max(twiss.betx),max(twiss.bety)))
    ax2.plot(twiss.s_pos,twiss.beta[:,0], label = "βₓ", color = colors["beta_x"][0])
    ax2.plot(twiss.s_pos,twiss.beta[:,1], label = "βᵧ", color = colors["beta_y"][0])
    
    plot_magnet_structure(ax3, section)
    ax2.legend()
    ax3.get_xaxis().set_visible(False)
    ax3.get_yaxis().set_visible(False)
    ax3.set_frame_on(False)
    

    canvas = FigureCanvas(figure)
    
    return canvas


def nonlinear_plot(lattice):
    refpts = list(range(len(lattice)))
    _,_,elemdata = at.get_optics(lattice, )
    s = elemdata.s_pos
    beta_x = elemdata.beta[:,0]
    beta_y = elemdata.beta[:,1]
    disp = elemdata.dispersion[:,0]
    dbeta_x = elemdata.dbeta[:,0]
    dbeta_y = elemdata.dbeta[:,1]
    ddisp = elemdata.ddisperion[:,0]

    k1_array = np.zeros_like(s)
    k2_array = np.zeros_like(s)
    bend_array = np.zeros_like(s)
    for elem in lattice:
        if elem.__class__.__name__ == "Quadrupole":
            idx = (s >= elem.s_start) & (s <= elem.s_end)
            k1_array[idx] = elem.K
        elif elem.__class__.__name__ == "Sextupole":
            idx = (s >= elem.s_start) & (s <= elem.s_end)
            k1_array[idx] = elem.H

    chrom1_x = k1_array*beta_x
    chrom1_y = k1_array*beta_y

    chrom1_x_sext = k2_array*beta_x*disp
    chrom1_y_sext = k2_array*beta_y*disp

    chrom2_x = k1_array*dbeta_x/2
    chrom2_y = k1_array*dbeta_y/2

    chrom2_x_sext = k2_array*dbeta_x*disp +k2_array*beta_x*ddisp/2
    chrom2_x_sext = k2_array*dbeta_y*disp +k2_array*beta_y*ddisp/2




def plot_magnet_structure(ax, lattice):
    """
    Zeichnet farbige Balken zur Darstellung der Magnetstruktur im übergebenen Axes-Objekt.
    """
    color_map = {
        "drift": "#ffffff", 
        "quadrupole": "#e74c3c",  
        "sextupole": "#2ecc71",    
        "dipole": "#3498db",       
        "marker": "#f1c40f",       
    }


    y_base = 0.2 

    s_pos = 0.0  

    for elem in lattice:
        length = getattr(elem, "Length", 0.0)
        elem_type = elem.__class__.__name__.lower()

        color = color_map.get(elem_type, "#95a5a6")   # fallback: grau
        height = 0.2

        rect = Rectangle((s_pos, y_base), length, height, color=color)
        ax.add_patch(rect)

        s_pos += length
    ax.set_xlim(0, s_pos)