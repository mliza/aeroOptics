#!/opt/homebrew/bin/python3.9
'''
    Date:   03/26/2023
    Author: Martin E. Liza
    File:   optics.py
    Def:

    Author		Date		Revision
    ----------------------------------------------------
    Martin E. Liza	03/26/2023	Initial version.
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
import astropy.constants as a_consts
from ambiance import Atmosphere #package for atmosphere properties 

# My Packages 
scripts_path   = os.environ.get('SCRIPTS')
python_scripts = os.path.join(scripts_path, 'Python')
sys.path.append(python_scripts) 
from helper_class import *
from aerodynamics_class import *  

# Loading my classes 
aero   = Aero()
helper = Helper()

def gas_density(density_dict): # density_dict [kg/m^3]
    gas_amu_weight  = aero.air_molecular_mass()  # [g/mol]  
    avogadro_number = s_consts.N_A               # [particles/mol]  
    gas_density     = { }
    for mol_name in gas_amu_weight: 
      gas_density[mol_name] = (density_dict[mol_name] * 10**3 * 
                               avogadro_number /
                               gas_amu_weight[mol_name]) # [particles/m^3] 

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
    n_const              = { }                               # [ ] 
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
# https://link.springer.com/article/10.1134/BF03355985 
def polarizability_constant(T_vib=2280):
    # These should be inputs <?>  
    rotational_qn  = [5, 15, 21];        #[ ] 
    vibrational_qn = np.arange(0, 46, 1) #[ ]  

    # Physical constants  
    boltzmann_const      = s_consts.Boltzmann      #[J/K]  
    plancks_const        = s_consts.Planck         #[Js]  
    speed_of_light       = s_consts.speed_of_light #[m/s]
    dielectric_const_vac = s_consts.epsilon_0      #[F/m] 

    # Algorithm Constants (Buldakov), move this to a table outside  
    # Constants below are for O2 (tab 1) from main paper
    a_e  = 1.61E-30  #[m^3] DOI: 10.1002/bbpc.19920960517 
    a_e1 = 1.76E-30  #[m^3] https://ui.adsabs.harvard.edu/abs/1987OptSp..63..460B/exportcitation  
    a_e2 = 3.40E-30  #[m^3] https://ui.adsabs.harvard.edu/abs/1987OptSp..63..460B/exportcitation
    a_e3 = -23.7E-30 #[m^3] DOI: 10.1063/1.467256
    B_e  = 1.4376766 #[m^3] From NIST/2T code NOTE: Note sure what this is 
    # NOTE: From Dhuram, below eq. 2 
    #reduced_mass =
    #equilibrium_nuclear_separation = 
    # B_e = ( plancks_const / (8 * np.pi * reduced_mass * 
            #  equilibrium_nuclear_separation * speed_of_light) )
    # NOTE: From Dhuram, below eq. 2 

    # Species properties 
    T_vib = T_vib #[K], Nonequilibrium Gas Dynamics and 
                        #Molecular Simulations (Boyd), Table 2.4 
    vibrational_frequency = (boltzmann_const / plancks_const) * T_vib  #[Hz] 


    # NOTE: Not sure what this is  
    # Y_{i,j}, i = vibrational QN, and j = rotational quantum number 
    alpha_e = 0.01593  #[1/cm], classical frequency of small oscillations  
    omega_e = 1580.193 #[1/cm]



    # NOTE: Check where they come from 
    # Calculate constants using approximations 
    # Dunham approximation, DOI: 10.1103/PhysRev.41.721, Eq. 19 
    a_1 = -( alpha_e * omega_e / (6 *B_e**2) ) - 1 
    a_2 = (5/4) * a_1**2 - (2/3) * ( ) 
    




# http://walter.bislins.ch/bloge/index.asp?page=Deriving+Equations+for+Atmospheric+Refraction
def atmospheric_index_of_refraction(altitude): 
    atmospheric_prop = Atmosphere(altitude)
    temperature      = atmospheric_prop.temperature #[K]
    pressure         = atmospheric_prop.pressure * 0.01 #[mbar]

    # Calculate refractive coefficient 
    refractivity = 79 * pressure / temperature 
    index_of_refraction = refractivity * 1E-6 + 1

    return index_of_refraction 

def Gladstone_Dale():
    gas_amu_weight   = aero.air_molecular_mass()    # [g/mol]  
    avogadro_number  = s_consts.N_A                 # [particles/mol]  
    dielectric_const = s_consts.epsilon_0           # [F/m] 
    gd_consts        = constants_tables.karl_2003() # [m3/kg]
    pol_consts       = constants_tables.polarizability() #[cm^3] 
    #[m3/kg] * species[kg/m3] = [ ] 

if __name__ == "__main__":
    altitude = np.linspace(0, 81E3, 1000)
    dielectric_const_0   = s_consts.epsilon_0 # [F/m] 
    index = atmospheric_index_of_refraction(altitude) 


    # MAKING PLOTS #
    plt.plot(index, altitude*1E-3, linewidth=2.5) 
    plt.xlabel('Index of refraction $[\;]$')
    plt.ylabel('Altitude $[km]$') 
    plt.ticklabel_format(useOffset=False, style='plain')
    plt.savefig('/Users/martin/Desktop/atmospheric_optics.png',
                bbox_inches='tight', dpi=300) 
    plt.close() 
    # MAKING PLOTS #

