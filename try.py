import matplotlib
matplotlib.use('Agg')
from matplotlib.figure import Figure
import os
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle
from file_io.json_loader import load_file
import at
import numpy as np


input_folder = "jsons"
output_folder = "plots"
colors = {
    "beta_x": ["#1f77b4", "#aec7e8", "#005288"],
    "beta_y": ["#d62728", "#ff9896", "#800000"],
    "dispersion": ["#2ca02c", "#98df8a", "#006400"]
}
os.makedirs(output_folder, exist_ok=True)
def linear_plot(section, title= "Plot", x_label= "s[m]",y_label = "βₓ/βᵧ"):
    figure = Figure(figsize=(6,4))
    gs = GridSpec(20,1,figure =figure)
    
    
    ax1 = figure.add_subplot(gs[0:5,0])
    ax2 = figure.add_subplot(gs[5:17,0],sharex = ax1)
    ax3 = figure.add_subplot(gs[17:,0],sharex = ax1)
    
    

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
    
    return figure

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
def calculate_nonlin(lattice):
    lattice = lattice.slice(slices = 700)
    refpts = list(range(len(lattice)))
    _,_,elemdata = at.get_optics(lattice,refpts=refpts,get_w = True )
    s = elemdata.s_pos
    beta_x = elemdata.beta[:,0]
    beta_y = elemdata.beta[:,1]
    disp = elemdata.dispersion[:,0]
    dbeta_x = elemdata.dbeta[:,0]
    dbeta_y = elemdata.dbeta[:,1]
    ddisp = elemdata.ddispersion[:,0]

    k1_array = np.zeros_like(s)
    k2_array = np.zeros_like(s)
    bend_array = np.zeros_like(s)
    for i, elem in enumerate(lattice):
        if elem.__class__.__name__ == "Quadrupole":
            k1_array[i] = getattr(elem, "K",0.0)
        elif elem.__class__.__name__ == "Sextupole":
            k2_array[i] = getattr(elem,"H", 0.0)

    chrom1_x = k1_array*beta_x
    chrom1_y = k1_array*beta_y

    chrom1_x_sext = k2_array*beta_x*disp
    chrom1_y_sext = k2_array*beta_y*disp

    chrom2_x = k1_array*dbeta_x/2
    chrom2_y = k1_array*dbeta_y/2

    chrom2_x_sext = k2_array*dbeta_x*disp +k2_array*beta_x*ddisp/2
    chrom2_y_sext = k2_array*dbeta_y*disp +k2_array*beta_y*ddisp/2

    data_dict = {"s":s,
                 "chrom1": [[chrom1_x,chrom1_y],["X1ₓ","X1ᵧ"]],
                 "chrom1_sext": [[chrom1_x_sext,chrom1_y_sext],["X1Sₓ","X1Sᵧ"]],
                 "chrom2":[[chrom2_x,chrom2_y],["X2ₓ","X2ᵧ"]],
                 "chrom2_sext":[[chrom2_x_sext,chrom2_y_sext],["X2Sₓ","X2Sᵧ"]]}
    return data_dict

def nonlinear_plot(data,function,lattice, y_label = " - "):
    figure = Figure(figsize=(6,4))
    gs = GridSpec(20,1,figure =figure)
    ax1 = figure.add_subplot(gs[0:19,0])
    ax2 = figure.add_subplot(gs[19:,0],sharex = ax1)

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
        for i in range(2):
            ax1.plot(s, data[function][0][i], label=data[function][1][i])
        ax1.legend()
    else:
        ax1.text(0.5, 0.5, "Keine Daten", ha="center", va="center", transform=ax1.transAxes)
    plot_magnet_structure(ax2, lattice)
    
    return figure
file = "MAX_I.json"
if file.endswith(".json"):
    name = os.path.splitext(file)[0]
    json_path = os.path.join(input_folder, file)
    save_dir = os.path.join(output_folder, name)
    os.makedirs(save_dir, exist_ok=True)
    functions= ["chrom1","chrom1_sext","chrom2","chrom2_sext"]
    _,_,lattices = load_file(json_path)
    section= "sector"
    try:
        lin_plot = linear_plot(lattices[section])
        lin_plot.figure.savefig(os.path.join(save_dir, "linear.png"), dpi=150)
        data = calculate_nonlin(lattices[section])
        for function in functions:
            
            fig = nonlinear_plot(data,function,lattices[section])
            fig.figure.savefig(os.path.join(save_dir, f"{function}.png"),dpi =150)
    except Exception as e:
        print(f"Fehler bei datei {file}: {e}")