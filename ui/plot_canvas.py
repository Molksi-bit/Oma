from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle
import at
import numpy as np
from at import RFCavity
from numpy import allclose
#from at.physics.rdt import get_rdts, RDTType


colors = {
    "beta_x": ["#1f77b4", "#aec7e8", "#005288"],
    "beta_y": ["#d62728", "#ff9896", "#800000"],
    "dispersion": ["#2ca02c", "#98df8a", "#006400"]
}




def calculate_linear(section):
    """This function calculates the data needed for the linear plot and table.
    ToDo: Write the godamn function you moron and stop procrastenating"""
    section = ensure_rf_and_radiation(section)
    angle = 0
    abs_angle = 0
    for elem in section:
        if hasattr(elem,"BendingAngle"):
            angle += np.rad2deg(elem.BendingAngle)
            abs_angle += np.rad2deg(np.abs(elem.BendingAngle))
    section = section.slice(slices= 500)
    refpts = list(range(len(section)))
    _,ringdata,twiss  = at.get_optics(section, refpts= refpts, get_chrom=True)
    beamdata, emit = at.ohmi_envelope(section)
    alpha_p = at.get_mcf(section)
    data_dict = {"s":twiss.s_pos,
                 "beta": [[twiss.beta[:,0],twiss.beta[:,1]],["βₓ","βᵧ"]],
                 "alpha": [[twiss.alpha[:,0],twiss.alpha[:,1]],["αₓ","αᵧ"]],
                 "disp":[[twiss.dispersion[:,0],twiss.dispersion[:,1]],["Dₓ","Dₓ ds"]],
                 "angle": angle,
                 "abs_angle":abs_angle,
                 "tunes" : ringdata.tune,
                 "chroma":ringdata.chromaticity,
                 "alpha_p": alpha_p,
                 "emittance": emit
                 }
    return data_dict


def linear_plot(data_list,section_list,labels=None, title= "Plot", x_label= "s[m]",y_label = "βₓ/βᵧ",callback = None):
    """Uses the data and creates a plot of betafunctions and dispersion.
    Returns: Plot Canvas"""
    figure = Figure(figsize=(6,4))
    gs = GridSpec(20,1,figure =figure)
    
    
    ax1 = figure.add_subplot(gs[0:5,0])
    ax2 = figure.add_subplot(gs[5:17,0],sharex = ax1)
    ax3 = figure.add_subplot(gs[17:,0],sharex = ax1)
    axes = [ax1,ax2,ax3]
    
    

    ax1.tick_params(labelbottom = False)
    ax2.set_ylabel(y_label)
    ax3.get_xaxis().set_visible(False)
    ax3.get_yaxis().set_visible(False)
    ax3.set_frame_on(False)
    figure.subplots_adjust(left=0.07, right=0.98, top=0.96, bottom=0.05,hspace=0)

    for i,data in enumerate(data_list):
        label = labels[i] if labels else f"Lattice {i+1}"
        ax1.plot(data["s"],data["disp"][0][0], label = label+ data["disp"][1][0], color = colors["dispersion"][i% len(colors["dispersion"])])
        ax2.plot(data["s"],data["beta"][0][0], label = label+ data["beta"][1][0], color = colors["beta_x"][i% len(colors["dispersion"])])
        ax2.plot(data["s"],data["beta"][0][1], label = label+ data["beta"][1][1], color = colors["beta_y"][i% len(colors["dispersion"])])
    ax1.set_ylim(bottom=0)
    ax2.set_ylim(bottom=0)
    max_s = max(data["s"][-1] for data in data_list)
    ax1.set_xlim(0, max_s)
    ax1.legend()
    ax2.legend()
    
    
    plot_magnet_structure(ax3, section_list)
    canvas = FigureCanvas(figure)
    def on_click(event):
        """This function handles click events on the plot.
        Updates the respective canvas to have a marker line at the x position of the click event.
        """
        if event.inaxes:
            x =event.xdata
            magnet = find_magnet_at_s(section_list[0],x)
            magnet_name = getattr(magnet, "FamName")
            values = {
                
                "s": x,
                "βₓ": np.interp(x, data_list[0]["s"], data_list[0]["beta"][0][0]),
                "αₓ": np.interp(x, data_list[0]["s"], data_list[0]["alpha"][0][0]),
                "βᵧ": np.interp(x, data_list[0]["s"], data_list[0]["beta"][0][1]),
                "αᵧ": np.interp(x, data_list[0]["s"], data_list[0]["alpha"][0][1]),
                "Dₓ":np.interp(x, data_list[0]["s"], data_list[0]["disp"][0][0]),
                "Dₓ'":np.interp(x, data_list[0]["s"], data_list[0]["disp"][0][1]),
                "magnet_name": magnet_name,
                "magnet" : magnet
            }
            if callback:
                callback(x, values)
            for ax in axes[:-1]:
                for line in ax.lines[:]:
                    if getattr(line, "_is_marker", False):
                        line.remove()
                if event.button != 3:
                    marker = ax.axvline(x=x, color='black', linestyle='--', lw = 1 )
                    marker._is_marker = True  
            for line in axes[-1].lines[:]:
                    if getattr(line, "_is_marker", False):
                        line.remove()
            if event.button != 3:
                marker = axes[-1].axvline(x=x,ymin=0,ymax=len(data_list)*0.3+0.2, color='black', linestyle='--', lw = 1 )
                marker._is_marker = True 
            canvas.draw()
            
    canvas.mpl_connect("button_press_event", on_click)
    return canvas

def calculate_nonlin(lattice):
    """This function calculates important nonlinear parameters for the nonlinear plots.
    Returns. Data dictionary with the s-positions and Chromaticity and Momentum Compaction contributions.
    ToDo: Kicker contributions and full curves and not just contributions"""
    nslice = 500
    lattice = lattice.slice(slices = nslice)
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
    k3_array = np.zeros_like(s)
    bend_array = np.zeros_like(s)
    entry_kick = np.zeros_like(s)
    exit_kick = np.zeros_like(s)
    bend_array += 0.01
    for i, elem in enumerate(lattice):
        if hasattr(elem, "K"):
            k1_array[i] = elem.K
        if hasattr(elem, "PolynomB")and len(elem.PolynomB)>2:
            k2_array[i] = 2*elem.PolynomB[2]
        if hasattr(elem, "PolynomB")and len(elem.PolynomB)>3:
            k3_array[i] = 6*elem.PolynomB[3]
        if hasattr(elem, "BendingAngle"):
            rho = elem.Length/2/np.sin(elem.BendingAngle/2)
            entry_kick[i]= -np.tan(elem.EntranceAngle)/rho
            exit_kick[i] = -np.tan(elem.ExitAngle)/rho
            bend_array[i] = elem.BendingAngle

    
    ds = np.diff(s)
    


    chrom1_x_quad = -k1_array*beta_x
    chrom1_y_quad = k1_array*beta_y

    chrom1_x_sext = k2_array*beta_x*disp
    chrom1_y_sext = -k2_array*beta_y*disp

    chrom1_x = chrom1_x_quad + chrom1_x_sext
    chrom1_y = chrom1_y_quad + chrom1_y_sext

    chrom1_totx = 1/np.pi/4 * np.sum(chrom1_x_quad[:-1]*ds)
    chrom1_toty = 1/np.pi/4 * np.sum(chrom1_y_quad[:-1]*ds)

    chrom2_x_quad = k1_array*dbeta_x/2
    chrom2_y_quad = k1_array*dbeta_y/2

    chrom2_x_sext = k2_array*dbeta_x*disp +k2_array*beta_x*ddisp/2
    chrom2_y_sext = k2_array*dbeta_y*disp +k2_array*beta_y*ddisp/2

    chrom2_x_oct = k3_array*beta_x*disp**2/2
    chrom2_y_oct = k3_array*beta_y*disp**2/2

    chrom2_x = chrom2_x_quad + chrom2_x_sext + chrom2_x_oct
    chrom2_y = chrom2_y_quad + chrom2_y_sext + chrom2_y_oct

    alpha0 = disp/bend_array
    
    alpha1_1 = (dsdisp**2)/2
    alpha1_2 = ddisp/bend_array
    alpha1 = alpha1_1 +alpha1_2

    alpha1_tot = np.sum(alpha1*s[-1]/nslice)

    data_dict = {"s":s,
                 "chrom1_tot": [[chrom1_totx,chrom1_toty],["",""]],
                 "chrom1": [[chrom1_x,chrom1_y],["X1ₓ","X1ᵧ"]],
                 "chrom1_quad": [[chrom1_x_quad,chrom1_y_quad],["X1Qₓ","X1Qᵧ"]],
                 "chrom1_sext": [[chrom1_x_sext,chrom1_y_sext],["X1Sₓ","X1Sᵧ"]],
                 "chrom2":[[chrom2_x,chrom2_y],["X2ₓ","X2ᵧ"]],
                 "chrom2_quad":[[chrom2_x_quad,chrom2_y_quad],["X2Qₓ","X2Qᵧ"]],
                 "chrom2_sext":[[chrom2_x_sext,chrom2_y_sext],["X2Sₓ","X2Sᵧ"]],
                 "chrom2_oct":[[chrom2_x_oct,chrom2_y_oct],["X2Oₓ","X2Oᵧ"]],
                 "alpha0": [[alpha0],["α0"]],
                 "alpha1_tot": [[alpha1_tot],[""]],
                 "alpha1": [[alpha1],["α1"]],
                 "alpha1_1": [[alpha1_1], ["α1 ds"]],
                 "alpha1_2": [[alpha1_2], [ "α1 dE"]]
                 }
    return data_dict

def nonlinear_plot(data_list,function,section_list,labels, y_label = " - ",callback =None):
    """This function uses the calculated data dictionary and creates a plot of the chosen function and section.
    Returns: Figure Canvas"""
    figure = Figure(figsize=(6,4))
    gs = GridSpec(20,1,figure =figure)
    ax1 = figure.add_subplot(gs[0:18,0])
    ax2 = figure.add_subplot(gs[18:,0],sharex = ax1)
    axes = [ax1,ax2]

    ax1.tick_params(labelbottom = False)
    ax1.set_ylabel(y_label)
    figure.subplots_adjust(left=0.07, right=0.98, top=0.96, bottom=0.02,hspace=0)
    ax2.get_xaxis().set_visible(False)
    ax2.get_yaxis().set_visible(False)
    ax2.set_frame_on(False)

    for i,data in enumerate(data_list):
        s = data.get("s", [])
        label = labels[i] if labels else f"Lattice {i+1}" 
        for k in range(len(data[function][0])):
            ax1.plot(s, data[function][0][k], label=label+ " " +data[function][1][k])
        ax1.legend()
    max_s = max(data["s"][-1] for data in data_list)
    ax1.set_xlim(0, max_s)
    plot_magnet_structure(ax2, section_list)
    canvas = FigureCanvas(figure)
    counter = 1
    def on_click(event):
        """This function handles click events on the plot.
        Updates the respective canvas to have a marker line at the x position of the click event.
        """
        nonlocal counter
        if event.inaxes:
            x =event.xdata
            values = {"s":x}
            for i in range(len(data[function][0])):
                values[data[function][1][i]] = np.interp(x, data["s"], data[function][0][i])
            if callback:
                callback(x, values,function)
            for ax in axes[:-1]:
                for line in ax.lines[:]:
                    if getattr(line, "_is_marker", False):
                        line.remove()
                if event.button == 1:
                    marker = ax.axvline(x=x, color='black', linestyle='--', lw = 1 )
                    marker._is_marker = True  
            for line in axes[-1].lines[:]:
                    if getattr(line, "_is_marker", False):
                        line.remove()
            if event.button == 1:
                marker = axes[-1].axvline(x=x,ymin=0,ymax=len(data_list)*0.3+ 0.2, color='black', linestyle='--', lw = 1 )
                marker._is_marker = True 
            if event.button == 2: 
                lines = axes[0].lines
                if len(lines) < 2:
                    return
                for line in lines:
                    line.set_visible(True)
                if counter == 1:
                    lines[1].set_visible(False) 
                elif counter == 2:
                    lines[0].set_visible(False)

                counter = (counter + 1) % 3
                
            canvas.draw()
    canvas.mpl_connect("button_press_event", on_click)
    return canvas




def plot_magnet_structure(ax, lattices):
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
    for lattice in lattices:
        for elem in lattice:
            length = getattr(elem, "Length", 0.0)
            elem_type = elem.__class__.__name__.lower()

            color = color_map.get(elem_type, "#95a5a6")   # fallback: grau
            height = 0.2

            rect = Rectangle((s_pos, y_base), length, height, color=color)
            ax.add_patch(rect)

            s_pos += length
        s_pos = 0.0
        y_base += 0.3
    

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

# def calculate_rdts(lattice):
#     lattice = lattice.slice(slices = 500)
#     refpts = list(range(len(lattice)))
#     _,_, elemdata = at.get_optics(lattice, refpts=refpts)
#     s = elemdata.s_pos
#     rdts_chrom = get_rdts(lattice, refpts, [RDTType.CHROMATIC])
#     rdts_geo = get_rdts(lattice, refpts, [RDTType.GEOMATRIC1])
#     data_dict = {
#         "s":s,
#         "rdts_chrom": [rdts_chrom,["H11001","H00111","H20001","H00201","H10002"]],#ausfüllen
#         "rdts_geo": [rdts_geo,["H21000","H30000","H10110","H10020","H10200"]]
#     }
#     return data_dict

def calculate_magnet_contribution(data, elements):
    s = data["s"]
    data_dict = {}


    for element in elements:
        #get the s indices
        s_start = element.pos
        s_end = element.pos + element.Length
        ds = np.diff(s[s_start:s_end])
        X1 = 0
        X1_Quad = 0
        X1_Sext = 0
        X2 =0 
        X2_Quad = 0
        X2_Sext = 0
        X2_Oct = 0
        alpha_0 =0 
        alpha_1 = 0
        alpha_1_1 = 0
        alpha_1_2 = 0
        data_dict[element.FamName] = [[X1,X1/data["X1_tot"]],[X1_Quad],[X1_Sext],[X2],[X2_Quad],[X2_Sext],[X2_Oct],[alpha_0],[alpha_1],[alpha_1_1],[alpha_1_2]]
    
    return data_dict

def calculate_rad_int():
    pass
    


def ensure_rf_and_radiation(ring, voltage=3e6, harmonic_number=360):
    """
    Stellt sicher, dass das Lattice eine RF-Kavität und Radiation aktiviert hat.
    Falls keine RF-Kavität vorhanden ist, wird eine standardmäßig ergänzt.
    """
    has_rf = any(isinstance(e, RFCavity) for e in ring)

    if not has_rf:
        energy = ring.energy 
        circumference = ring.get_s_pos()[-1]
        frequency = harmonic_number * 299792458 / circumference

        rf = RFCavity('RF', length=0, voltage=voltage,frequency=frequency, harmonic_number=harmonic_number,energy=energy)

        ring.append(rf)
        print("[info] RF-Kavität automatisch ergänzt.")

    # Radiation aktivieren (nur für Bending-Elemente)
    for elem in ring:
        if hasattr(elem, 'BendingAngle') and not getattr(elem, 'Radiation', False):
            elem.Radiation = True

    return ring
