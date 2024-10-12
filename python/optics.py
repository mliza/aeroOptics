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
import pickle
import molmass
import os 
import sys 
import IPython
import constants_tables 
import numpy as np
import matplotlib.pyplot as plt 
import scipy.constants as s_consts 
from ambiance import Atmosphere #package for atmosphere properties 

# My Packages 
scripts_path   = os.environ.get('SCRIPTS')
python_scripts = os.path.join(scripts_path, 'Python')
sys.path.append(python_scripts) 
import helper_functions as helper 
import aerodynamic_functions as aero

def gas_density(density_dict): # density_dict [kg/m^3]
    gas_amu_weight  = aero.air_atomic_mass()  # [g/mol]  
    avogadro_number = s_consts.N_A               # [particles/mol]  
    gas_density     = { }
    
    for i in density_dict: 
        strip_key = i.strip('+') # remove ion names
        gas_density[i] = (density_dict[i] * 10**3 * 
                               avogadro_number /
                               gas_amu_weight[strip_key]) # [particles/m^3] 

    # Sum all gas density values 
    '''
    gas_density['total'] = 0.0
    for gas_density_val in gas_density.values():
        gas_density['total'] += gas_density_val
    '''
    return gas_density #[particles/m^3] 

def index_of_refraction(gas_density_dict):
    pol_consts         = constants_tables.polarizability() # [cm^3] 
    dielectric_const_0 = s_consts.epsilon_0                # [F/m] 
    density            = gas_density(gas_density_dict)     # [particles/m3]    
    n_const            = { }                               # [ ] 
    # Convert cgs to SI
    alpha_si = lambda x : x * (4 * np.pi * dielectric_const_0) * 1E-6 #[F m2]

    for i in gas_density_dict: 
        # Convert alpha_cgs to alpha_si 
        alpha      = alpha_si(pol_consts[i]) 
        n_const[i] = (alpha * density[i]) #(a_i N_i)

    # add all n_i 
    temp = 0.0
    for i in n_const.values():
        temp += i 

    n_return = { }
    n_return['dilute'] = 1 + temp / (2 * dielectric_const_0) 
    n_temp             = temp / (3 * dielectric_const_0)
    n_return['dense']  = ( (2 * n_temp + 1) / (1 - n_temp) )**0.5
    # Note np.sqrt(-1) does not detect complex 

    return n_return 

def reflectivity(n_const, n_incident=1.0):
# Normal Freznel equation 
    reflectivity  = { }
    reflectivity['dilute'] = ( (n_incident - n_const['dilute']) / 
                               (n_incident + n_const['dilute']) )**2 
    reflectivity['dense']  = ( (n_incident - n_const['dense']) / 
                               (n_incident + n_const['dense']) )**2 
    return reflectivity 
    

def dielectric_material_const(n_const): 
    # n ~ sqrt(e_r)  
    dielectric_const_0   = s_consts.epsilon_0 # [F/m] 
    dielectric           = { }
    dielectric['dilute'] = dielectric_const_0 * n_const['dilute']**2
    dielectric['dense']  = dielectric_const_0 * n_const['dense']**2
    return dielectric 

def optical_path_length(n_solution, distance):
    OPL           = { }
    OPL['dilute'] = n_solution['dilute'] * distance
    OPL['dense']  = n_solution['dense'] * distance
    return OPL 

# Calculate polarizability (uses equation 4 from the paper)
def buldakov_method(T_vib=2280):
    a = 2

# Calculate polarizability as temperature
"""
    DOI: 10.1002/bbpc.19920960517 
    DOI: 10.1134/BF03355985
"""
def kerl_polarizability(wavelength_nm=633, temperature_K=1000):
    mean_const_N2 = constants_tables.parameters_mean_polarizability('N2')
    mean_const_O2 = constants_tables.parameters_mean_polarizability('O2')
    frequency_Hz = [2 * np.pi * s_consts.speed_of_light / (wavelength_nm * 1E-9)]
    const_polarizability = constants_tables.polarizability() #[cm^3]
    wavenumber = 1 / (wavelength_nm * 1E-9)

    #frequency_Hz = [3 * 1E-15]
    for i in frequency_Hz:
        # Calculate N2
        tmp_N2 = mean_const_N2['c'] * temperature_K**2
        tmp_N2 += mean_const_N2['b'] * temperature_K
        tmp_N2 += 1
        tmp_N2 *= mean_const_N2['groundPolarizability']
        tmp_N2 /= (1-(i / mean_const_N2['groundFrequency'])**2)

        omegaRatio_N2 = mean_const_N2['c'] * temperature_K**2
        omegaRatio_N2 += mean_const_N2['b'] * temperature_K
        omegaRatio_N2 += 1 
        omegaRatio_N2 *= mean_const_N2['groundPolarizability'] 
        omegaRatio_N2 /= (1.765 * 1E-30)
        omega_N2 = np.sqrt((omegaRatio_N2 - 1) * mean_const_N2['groundFrequency']**2)
        lambda_N2 = (s_consts.speed_of_light / omega_N2) * 1E9  

        # Calculate O2
        tmp_O2 = mean_const_O2['c'] * temperature_K**2
        tmp_O2 += mean_const_O2['b'] * temperature_K
        tmp_O2 += 1
        tmp_O2 *= mean_const_O2['groundPolarizability']
        tmp_O2 /= (1-(i / mean_const_O2['groundFrequency'])**2)

        omegaRatio_O2 = mean_const_O2['c'] * temperature_K**2
        omegaRatio_O2 += mean_const_O2['b'] * temperature_K
        omegaRatio_O2 += 1 
        omegaRatio_O2 *= mean_const_O2['groundPolarizability'] 
        omegaRatio_O2 /= (1.605 * 1E-30) 
        omega_O2 =  np.sqrt((omegaRatio_O2 - 1) *
                            mean_const_O2['groundFrequency']**2)
        lambda_O2 = (s_consts.speed_of_light / omega_O2) * 1E9  


        

    IPython.embed(colors = "Linux")






# http://walter.bislins.ch/bloge/index.asp?page=Deriving+Equations+for+Atmospheric+Refraction
def atmospheric_index_of_refraction(altitude): 
    atmospheric_prop = Atmosphere(altitude)
    temperature      = atmospheric_prop.temperature #[K]
    pressure         = atmospheric_prop.pressure * 0.01 #[mbar]

    # Calculate refractive coefficient 
    refractivity = 79 * pressure / temperature
    index_of_refraction = refractivity * 1E-6 + 1

    return index_of_refraction

def atmospheric_gladstoneDaleConstant(altitude=0.0, gas_composition_dict=None):
    atmospheric_prop = Atmosphere(altitude)
    density          = atmospheric_prop.density * 1E3   #[g/m3]
    num_density      = atmospheric_prop.number_density  #[particles/m3]
    gladstone_const  = Gladstone_Dale()                 #[m3/kg]
    atomic_mass      = aero.air_atomic_mass()           #[g/mol]
    avogadro_number  = s_consts.N_A                     #[particles/mol]

    if gas_composition_dict == None:
        gas_composition_dict = { }
        gas_composition_dict['N'] = 0.0
        gas_composition_dict['O'] = 0.0
        gas_composition_dict['NO'] = 0.0
        gas_composition_dict['N2'] = 0.79
        gas_composition_dict['O2'] = 0.21

    tmp = 0
    for i in gas_composition_dict.keys():
        #tmp += gas_composition_dict[i] * atomic_mass[i] * gladstone_const[i]
        tmp += gas_composition_dict[i] * gladstone_const[i] 

    #return tmp * num_density / (density * avogadro_number) #[m3/kg]
    return tmp 


def Gladstone_Dale(gas_density_dict=None): # [kg/m3
    gas_amu_weight   = aero.air_atomic_mass()       # [g/mol]
    avogadro_number  = s_consts.N_A                 # [particles/mol]
    dielectric_const = s_consts.epsilon_0           # [F/m]
    gd_consts        = constants_tables.karl_2003() # [m3/kg]
    pol_consts       = constants_tables.polarizability() #[cm^3]

    # Convert CGS to SI 
    pol_consts.update({n: 4 * np.pi * dielectric_const * 1E-6 * pol_consts[n]
                       for n in pol_consts.keys()}) # [Fm^2]

    # Calculate Gladstone dale
    gladstone_dale_const = { }
    for i in pol_consts:
        strip_key = i.strip('+') # remove ion names
        gladstone_dale_const[i] = ( pol_consts[i] / (2 * dielectric_const) * 
                (avogadro_number / gas_amu_weight[strip_key]) * 1E3 ) #[m3/kg]

    gladstone_dale_dict = { }
    if not gas_density_dict:
        return gladstone_dale_const #[m^3/kg]
    else:
        gladstone_dale_dict['gladstone_dale'] = 0.0
        for i in gas_density_dict:
            gladstone_dale_dict[i] = ((gladstone_dale_const[i] *
                                       gas_density_dict[i]) /
                                      sum(gas_density_dict.values()))
            gladstone_dale_dict['gladstone_dale'] += gladstone_dale_const[i] * gas_density_dict[i]
        gladstone_dale_dict['gladstone_dale'] /= sum(gas_density_dict.values())

        return gladstone_dale_dict #[m3/kg]

if __name__ == "__main__":
    gd = Gladstone_Dale()
    gd.update({n: np.round(gd[n] * 1E4, 3) for n in gd.keys()})
    altitude = np.linspace(0, 81E3, 1000)
    dielectric_const_0   = s_consts.epsilon_0 # [F/m] 
    index = atmospheric_index_of_refraction(altitude) 
    gd_s = atmospheric_gladstoneDaleConstant(altitude) 

    kerl_polarizability(wavelength_nm=633, temperature_K=1000)
    #kerl_polarizability(wavelength_nm=0.0273, temperature_K=1000) #for N2
    #kerl_polarizability(wavelength_nm=1.49E-5, temperature_K=1000) #for O2


    # MAKING PLOTS #
    plt.plot(index, altitude*1E-3, linewidth=2.5) 
    plt.xlabel('Index of refraction $[\;]$')
    plt.ylabel('Altitude $[km]$') 
    plt.ticklabel_format(useOffset=False, style='plain')
    plt.savefig('/Users/martin/Desktop/atmospheric_optics.png',
                bbox_inches='tight', dpi=300) 
    plt.close() 
    # MAKING PLOTS #

