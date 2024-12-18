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
import quantum

def gas_density(density_dict): # density_dict [kg/m^3]
    gas_amu_weight  = aero.air_atomic_mass()  # [g/mol]  
    avogadro_number = s_consts.N_A               # [particles/mol]  
    gas_density     = { }
    
    for i in density_dict: 
        gas_density[i] = (density_dict[i] * 10**3 * 
                               avogadro_number /
                               gas_amu_weight[i]) # [particles/m^3] 

    return gas_density #[particles/m^3] 

def index_of_refraction(gas_density_dict):
    pol_consts         = constants_tables.polarizability() # [m^3] 
    dielectric_const_0 = s_consts.epsilon_0                # [F/m] 
    density            = gas_density(gas_density_dict)     # [particles/m3]    
    n_const            = { }                               # [ ] 
    # Convert cgs to SI
    alpha_si = lambda x : x * (4 * np.pi * dielectric_const_0) #[F m2]

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

def tropina_aproximation(vibrational_number, rotational_number, molecule):
    electron_mass = s_consts.m_e
    electron_charge = s_consts.e
    spectroscopy_const = constants_tables.spectroscopy_constants(molecule)
    #resonance_distance = omega_gi - omega


# Calculate polarizability (uses equation 4 from the paper)
def buldakov_expansion(vibrational_number, rotational_number, molecule):
    # Load constants
    spectroscopy_const = constants_tables.spectroscopy_constants(molecule)
    derivative_const = constants_tables.polarizability_derivatives(molecule)
    be_we = spectroscopy_const['B_e'] / spectroscopy_const['omega_e']

    # Dunham potential energy constants
    (a_0, a_1, a_2) = quantum.potential_dunham_coef_012(molecule)
    a_3 = quantum.potential_dunham_coeff_m(a_1, a_2, 3)

    rotational_degeneracy = rotational_number * (rotational_number + 1)
    vibrational_degeneracy = 2 * vibrational_number + 1

    # Split in terms
    tmp_1 = be_we
    tmp_1 *= (-3 * a_1 * derivative_const['first'] +
             derivative_const['second'])
    tmp_1 *= vibrational_degeneracy 
    tmp_1 *= 1/2

    tmp_2 = be_we**2
    tmp_2 *= derivative_const['first']
    tmp_2 *= rotational_degeneracy
    tmp_2 *= 4

    tmp_31a = 7
    tmp_31a += (15 * vibrational_degeneracy**2) 
    tmp_31a *= a_1**3
    tmp_31a *= -3/8

    tmp_31b = 23
    tmp_31b += (39 * vibrational_degeneracy**2) 
    tmp_31b *= a_2
    tmp_31b *= a_1
    tmp_31b *=  1/4

    tmp_31c = 5
    tmp_31c += vibrational_degeneracy**2 
    tmp_31c *= a_3
    tmp_31c *= -15/4

    tmp_31 = derivative_const['first'] * (tmp_31a + tmp_31b + tmp_31c)

    tmp_32a = 7
    tmp_32a += (15 * vibrational_degeneracy**2)
    tmp_32a *= a_1**2
    tmp_32a *= 1/8

    tmp_32b = 5
    tmp_32b += vibrational_degeneracy**2
    tmp_32b *= a_2
    tmp_32b *- -3/4

    tmp_32 = derivative_const['second'] * (tmp_32a + tmp_32b)

    tmp_33 = 7
    tmp_33 += (15 * vibrational_degeneracy**2)
    tmp_33 *= a_1
    tmp_33 *= derivative_const['third']
    tmp_33 *= -1/24

    tmp_3 = (tmp_31 + tmp_32 + tmp_33) * be_we**2

    tmp_41 = 1 - a_2
    tmp_41 *= 24
    tmp_41 += (27 * a_1 * (1 + a_1))
    tmp_41 *= derivative_const['first']

    tmp_42 = (1 + 3 * a_1)
    tmp_42 *= derivative_const['second']
    tmp_42 *= -3

    tmp_43 = 1/8 * derivative_const['third']

    tmp_4 = (tmp_41 + tmp_42 + tmp_43) 
    tmp_4 *= rotational_degeneracy
    tmp_4 *= vibrational_degeneracy
    tmp_4 *= be_we**3

    return derivative_const['zeroth'] + tmp_1 + tmp_2 + tmp_3 + tmp_4


# Calculate polarizability as temperature
"""
    DOI: 10.1002/bbpc.19920960517 
    DOI: 10.1134/BF03355985
"""
def kerl_polarizability_temperature(*args, **kargs):
    if args:
        temperature_K = args[0] 
        molecule = args[1]
        wavelength_nm = args[2]

    if kargs:
        temperature_K = kargs['temperature_K']
        molecule = kargs['molecule']
        wavelength_nm = kargs['wavelength_nm']

    # Check sizes
    mean_const = constants_tables.kerl_interpolation(molecule)
    angular_frequency = (2 * np.pi * s_consts.speed_of_light /
                         (wavelength_nm * 1E-9))

    tmp = mean_const['c'] * temperature_K**2
    tmp += mean_const['b'] * temperature_K
    tmp += 1
    tmp *= mean_const['groundPolarizability']
    tmp /= (1 - (angular_frequency / mean_const['groundFrequency'])**2)

    return tmp

# http://walter.bislins.ch/bloge/index.asp?page=Deriving+Equations+for+Atmospheric+Refraction
def atmospheric_index_of_refraction(altitude, vaporPressure=0): 
    atmospheric_prop = Atmosphere(altitude)
    temperature      = atmospheric_prop.temperature #[K]
    pressure         = atmospheric_prop.pressure * 0.01 #[mbar]
    K_1              = 79 #[K/mbar]
    K_2              = 4800 #[K]

    refractivity =  K_2 * vaporPressure / temperature
    refractivity += pressure
    refractivity *= (K_1 / temperature)
    refractivity *= 10**-6

    return refractivity + 1 

def atmospheric_gladstoneDaleConstant(altitude=0.0, gas_composition_dict=None):
    atmospheric_prop = Atmosphere(altitude)
    density          = atmospheric_prop.density * 1E3   #[g/m3]
    num_density      = atmospheric_prop.number_density  #[particles/m3]
    gladstone_const  = Gladstone_Dale()                 #[m3/kg]
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
        tmp += gas_composition_dict[i] * gladstone_const[i] 

    return tmp 

def Gladstone_Dale(gas_density_dict=None): # [kg/m3
    gas_amu_weight   = aero.air_atomic_mass()       # [g/mol]
    avogadro_number  = s_consts.N_A                 # [particles/mol]
    dielectric_const = s_consts.epsilon_0           # [F/m]
    gd_consts        = constants_tables.karl_2003() # [m3/kg]
    pol_consts       = constants_tables.polarizability() #[m^3]

    # Convert CGS to SI 
    pol_consts.update({n: 4 * np.pi * dielectric_const * pol_consts[n]
                       for n in pol_consts.keys()}) # [Fm^2]

    # Calculate Gladstone dale
    gladstone_dale_const = { }
    for i in pol_consts:
        gladstone_dale_const[i] = ( pol_consts[i] / (2 * dielectric_const) * 
                (avogadro_number / gas_amu_weight[i]) * 1E3 ) #[m3/kg]

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

    ## Inputs ##
    temperature_K = 2000
    vibrational_number = 2
    rotational_number = 3
    molecule = 'N2'

    (a_0, a_1, a_2) = quantum.potential_dunham_coef_012(molecule='N2')
    a_3 = quantum.potential_dunham_coeff_m(a_1, a_2, 3)
    print(f'N2:  a_0 = {a_0:.4}, a_1 = {a_1:.4}, a_2 = {a_2:.4}, a_3 = {a_3:.4}')
    (a_0, a_1, a_2) = quantum.potential_dunham_coef_012(molecule='O2')
    a_3 = quantum.potential_dunham_coeff_m(a_1, a_2, 3)
    print(f'O2:  a_0 = {a_0:.4}, a_1 = {a_1:.4}, a_2 = {a_2:.4}, a_3 = {a_3:.4}')


    kerl_pola = kerl_polarizability_temperature(temperature_K=temperature_K,
                                                molecule=molecule,
                                                wavelength_nm=633)

    buldakov_pola = buldakov_expansion(vibrational_number=vibrational_number,
                                            rotational_number=rotational_number,
                                            molecule=molecule)




    # MAKING PLOTS #
    plt.plot(index, altitude*1E-3, linewidth=2.5) 
    plt.xlabel('Index of refraction $[\;]$')
    plt.ylabel('Altitude $[km]$') 
    plt.ticklabel_format(useOffset=False, style='plain')
    plt.savefig('/Users/martin/Desktop/atmospheric_optics.png',
                bbox_inches='tight', dpi=300) 
    plt.close() 
    # MAKING PLOTS #

