#!/opt/homebrew/bin/python3.9
'''
    Date:   03/26/2023
    Author: Martin E. Liza
    File:   optics.py
    Def:

    Author          Date        Revision
    ----------------------------------------------------
    Martin E. Liza  03/26/2023  Initial version.
'''
import os 
import sys 
import pickle
import IPython
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

# My Packages 
scripts_path   = os.environ.get('SCRIPTS')
python_scripts = os.path.join(scripts_path, 'Python')
sys.path.append(python_scripts) 
import optics
import helper_functions as helper 
import aerodynamic_functions as aero


def plot_fields(df_in, gd_const, gds_vec, density_dict, 
                index_refraction, png_path, csv_in, pickle_flag=False):

    pickle_path = os.path.join(png_path, 'pickle') 
    # Plot Density
    fig = plt.figure()
    for i in density_dict.keys(): 
        plt.semilogx(df_in['time'], density_dict[i], linewidth=2, label=f'${i}$')
    plt.legend()
    plt.xlabel('Time $[s]$')
    plt.ylabel('Density $[kg/m^3]$')
    plt.savefig(os.path.join(png_path, 
                f'{csv_in}_densityTime.png'),
                format='png', bbox_inches='tight', dpi=1200)
    if pickle_flag:
        pickle.dump(fig, open(os.path.join(pickle_path,
                                f'{csv_in}_densityTime.pickle'), 'wb'))
    plt.close() 


    # Plot Specific Gladstone-Dale constant
    fig = plt.figure()
    for i in density_dict.keys(): 
        plt.semilogx(df_in['time'], gd_const[i]*1E4, linewidth=2, label=f'${i}$')
    plt.legend()
    plt.xlabel('Time $[s]$')
    plt.ylabel('GladstoneDale const $\\times 10^{-4}\,[m^3/kg]$')
    plt.savefig(os.path.join(png_path, 
                f'{csv_in}_gladstoneSpecificTime.png'),
                format='png', bbox_inches='tight', dpi=1200)
    if pickle_flag:
        pickle.dump(fig, open(os.path.join(pickle_path, 
                            f'{csv_in}_gladstoneSpecificTime.pickle'), 'wb'))
    plt.close()

    # Plot Temperatures
    fig = plt.figure()
    plt.semilogx(df_in['time'], df_in['Tt'], linewidth=2, label='$T_{tr}$')
    plt.semilogx(df_in['time'], df_in['Tv'], linewidth=2, label='$T_{vr}$')
    plt.ylabel('Temperature $[K]$')
    plt.xlabel('Time $[s]$')
    plt.legend()
    plt.savefig(os.path.join(png_path, 
                f'{csv_in}_temperatureTime.png'),
                format='png', bbox_inches='tight', dpi=1200)
    if pickle_flag:
        pickle.dump(fig, open(os.path.join(pickle_path, 
                    f'{csv_in}_gladstoneSpecificTime.pickle'), 'wb'))
    plt.close() 

    # Plot Index of Refraction
    fig = plt.figure()
    plt.semilogx(df_in['time'], index_refraction['dilute'], linewidth=2)
    plt.xlabel('Time $[s]$')
    plt.ylabel('Index of refraction $[\;]$')
    plt.savefig(os.path.join(png_path, 
                f'{csv_in}_indexOfRefractionTime.png'),
                format='png', bbox_inches='tight', dpi=1200)
    if pickle_flag:
        pickle.dump(fig, open(os.path.join(pickle_path, 
        f'{csv_in}_indexOfRefractionTime.pickle'), 'wb'))
    plt.close() 

    # Plot GD using density_dict and GD at sea level 
    fig = plt.figure()
    plt.semilogx(df_in['time'], gd_const['gladstone_dale'] * 1E4, linewidth=2,
    label='flow')
    plt.plot(df_in['time'], gds_vec * 1E4, linewidth=2, label='atm')
    plt.xlabel('Time $[s]$')
    plt.ylabel('GladstoneDale const $\\times 10^{-4}\,[m^3/kg]$')
    plt.legend()
    plt.savefig(os.path.join(png_path,
                f'{csv_in}_gladstonedaleConstTime.png'),
                format='png', bbox_inches='tight', dpi=1200)
    if pickle_flag:
        pickle.dump(fig, open(os.path.join(pickle_path, 
        f'{csv_in}_gladstonedaleConstTime.pickle'), 'wb'))
    plt.close() 


def get_density_dict(data_path : str, f_in : str) -> tuple[dict, object]:
    """
    Load csv files and returns a dictionary with all the densities
    """
    # Loads all csv
    df_in = pd.read_csv(os.path.join(data_path, f_in), index_col=False) 

    # Keys to ignore 
    gas_type = f_in.split('_')[1]
    ignore_keys = ("time", "Tt", "Tv", "e+")
    if gas_type in ("O2", "N2"):
        # (false_value, true_value) [condition]
        tmp = (("N", "N2", "NO"),("O", "O2", "NO"))[gas_type == "N2"]
        ignore_keys += tmp

    density_dict = { }
    # Create a density dictionary
    for density_key in df_in.keys():
        if density_key in ignore_keys:
            continue
        density_dict[density_key] = df_in[density_key].to_numpy()

    return density_dict, df_in

def main():
    data_path = '/Users/martin/Documents/Research/UoA/Projects/aeroOptics/data'
    data_out = 'outputFigures'
    files_in = os.listdir(data_path)

    for f_in in files_in: 
        density_dict, df_in = get_density_dict(data_path, f_in)

        # Gladstone-Dale constants and index of refraction using heath bath data
        gd_const = optics.Gladstone_Dale(density_dict)
        index_refraction = optics.index_of_refraction(density_dict)

        # Gladstone-Dale constant and index of refraction at sea level
        gd = optics.Gladstone_Dale()
        gds = optics.atmospheric_gladstoneDaleConstant(0.0) #[m]
        gds_vec = gds * np.ones(np.shape(df_in['time'])) 

        # Plot data fields 
        plot_fields(df_in, gd_const, gds_vec,
                    density_dict, index_refraction, data_out,
                    f_in.split('.')[0],
                    pickle_flag=True)

if __name__=="__main__":
    main()
