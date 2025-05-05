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

def on_click(event,axes, data):
    """This function handles click events on the plot.
    Updates the respective canvas to have a marker line at the x position of the click event.
    
    ToDo: make the marker appear at the same position for all coordinate systems """
    if event.inaxes:
        x =event.xdata
        values = {
            
        }
        for ax in axes:
            for line in ax.lines[:]:
                if getattr(line, "_is_marker", False):
                    line.remove()

            marker = ax.axvline(x=x, color='black', linestyle='--', lw = 1 )
            marker._is_marker = True  
            event.canvas.draw()
        s = data["s"]
        functions = []
        values = {name: np.interp(x,s,np.array(data[name])) for name in functions}


def calculate_linear(section):
    """This function calculates the data needed for the linear plot and table.
    ToDo: Write the godamn function you moron and stop procrastenating"""
    pass
def linear_plot(section, title= "Plot", x_label= "s[m]",y_label = "βₓ/βᵧ",callback = None):
    """Uses the data and creates a plot of betafunctions and dispersion.
    Returns: Plot Canvas
    ToDo: Move out the calculation part here"""
    figure = Figure(figsize=(6,4))
    gs = GridSpec(20,1,figure =figure)
    
    
    ax1 = figure.add_subplot(gs[0:5,0])
    ax2 = figure.add_subplot(gs[5:17,0],sharex = ax1)
    ax3 = figure.add_subplot(gs[17:,0],sharex = ax1)
    axes = [ax1,ax2,ax3]
    
    

    section = section.slice(slices= 700)
    refpts = list(range(len(section)))
    #calculation part
    _,_,twiss  = at.get_optics(section, refpts= refpts, get_chrom=False)
    #
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
    canvas.mpl_connect("button_press_event", on_click)
    return canvas

def calculate_nonlin(lattice):
    """This function calculates important nonlinear parameters for the nonlinear plots.
    Returns. Data dictionary with the s-positions and Chromaticity and Momentum Compaction contributions.
    ToDo: Kicker contributions and full curves and not just contributions"""
    lattice = lattice.slice(slices = 700)
    refpts = list(range(len(lattice)))
    _,_,elemdata = at.get_optics(lattice,refpts=refpts,get_w = True )
    s = elemdata.s_pos
    beta_x = elemdata.beta[:,0]
    beta_y = elemdata.beta[:,1]
    disp = elemdata.dispersion[:,0]
    dsdisp = elemdata.dispersion[:,1]
    dbeta_x = elemdata.dbeta[:,0]
    dbeta_y = elemdata.dbeta[:,1]
    ddisp = elemdata.ddispersion[:,0]

    k1_array = np.zeros_like(s)
    k2_array = np.zeros_like(s)
    bend_array = np.zeros_like(s)
    bend_array += 0.01
    for i, elem in enumerate(lattice):
        if elem.__class__.__name__ == "Quadrupole":
            k1_array[i] = getattr(elem, "K",0.0)
        elif elem.__class__.__name__ == "Sextupole":
            k2_array[i] = getattr(elem,"H", 0.0)
        elif elem.__class__.__name__ == "Dipole":
            bend_array[i] = getattr(elem, "BendingAngle", 0.0)

    chrom1_x = k1_array*beta_x
    chrom1_y = k1_array*beta_y

    chrom1_x_sext = k2_array*beta_x*disp
    chrom1_y_sext = k2_array*beta_y*disp

    chrom2_x = k1_array*dbeta_x/2
    chrom2_y = k1_array*dbeta_y/2

    chrom2_x_sext = k2_array*dbeta_x*disp +k2_array*beta_x*ddisp/2
    chrom2_y_sext = k2_array*dbeta_y*disp +k2_array*beta_y*ddisp/2

    alpha0 = disp/bend_array
    alpha1_1 = (dsdisp**2)/2
    alpha1_2 = ddisp/bend_array

    data_dict = {"s":s,
                 "chrom1": [[chrom1_x,chrom1_y],["X1ₓ","X1ᵧ"]],
                 "chrom1_sext": [[chrom1_x_sext,chrom1_y_sext],["X1Sₓ","X1Sᵧ"]],
                 "chrom2":[[chrom2_x,chrom2_y],["X2ₓ","X2ᵧ"]],
                 "chrom2_sext":[[chrom2_x_sext,chrom2_y_sext],["X2Sₓ","X2Sᵧ"]],
                 "alpha0": [[alpha0],["α0"]],
                 "alpha1_1": [[alpha1_1], ["α1 ds"]],
                 "alpha1_2": [[alpha1_2], [ "α1 dE"]]
                 }
    return data_dict

def nonlinear_plot(data,function,lattice, y_label = " - "):
    """This function uses the calculated data dictionary and creates a plot of the chosen function and section.
    Returns: Figure Canvas"""
    figure = Figure(figsize=(6,4))
    gs = GridSpec(20,1,figure =figure)
    ax1 = figure.add_subplot(gs[0:19,0])
    ax2 = figure.add_subplot(gs[19:,0],sharex = ax1)
    axes = [ax1,ax2]

    ax1.tick_params(labelbottom = False)
    ax1.set_xlabel("")
    ax1.set_ylabel(y_label)

    s = data.get("s", [])

    if len(s) > 1:
        ax1.set_xlim(0, max(s))
    else:
        ax1.set_xlim(0, 1)

    figure.subplots_adjust(left=0.07, right=0.98, top=0.96, bottom=0.02,hspace=0)
    ax2.get_xaxis().set_visible(False)
    ax2.get_yaxis().set_visible(False)
    ax2.set_frame_on(False)
    if len(s) > 1:
        for i in range(len(data[function][0])):
            ax1.plot(s, data[function][0][i], label=data[function][1][i])
        ax1.legend()
    else:
        ax1.text(0.5, 0.5, "Keine Daten", ha="center", va="center", transform=ax1.transAxes)
    plot_magnet_structure(ax2, lattice)
    canvas = FigureCanvas(figure)
    
    canvas.mpl_connect("button_press_event", on_click)
    return canvas




def plot_magnet_structure(ax, lattice):
    """
    This function creates a visual representation of the magnet arrangement by colored bars on the given axes object.
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

def get_max_contribution(data,function,lattice,top_n=1):
    """This function gets the top n magnets contributing to the given function.
    Returns: Tuple of magnet name, contribution value, position, magnetic field value
    ToDo: contributions for multiple functions or negative max values."""
    y = np.array(data[function][0][0])
    #z = np.array(data[function][0][1])
    s = np.array(data["s"])
    
    top_indices = np.argsort(y)[-top_n:][::-1]
    #top_indices.append(np.argsort(z)[-top_n:][::-1])

    results = []
    for idx in top_indices:
        s_pos = s[idx]
        value = y[idx]
        magnet = find_magnet_at_s(lattice, s_pos)
        magnet_name = getattr(magnet, "FamName")
        magnet_value ={}
        if hasattr(magnet,"Bendingangle"):
            magnet_value = magnet.Bendingangle
        elif hasattr(magnet,"K"):
            magnet_value = magnet.K
        elif hasattr(magnet,"H"):
            magnet_value = magnet.H
        results.append(( magnet_name,value,s_pos,  magnet_value))
    return results

def find_magnet_at_s(lattice, s_pos):
    """This function finds the element, located at s_pos.
    Returns: Element"""
    spos = np.cumsum([elem.Length for elem in lattice])
    start_spos = np.concatenate(([0], spos[:-1]))
    for elem, s_start, s_end in zip(lattice, start_spos, spos):
        if s_start <= s_pos < s_end:
            return elem
    return None