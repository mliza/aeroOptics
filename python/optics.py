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
def buldakov_polarizability(molecule='N2'):
    # This will be Inputs
    vibrational_number = 1
    rotational_number = 5
    # Load constants
    spectroscopy_const = constants_tables.spectroscopy_constants(molecule)
    derivative_const = constants_tables.polarizability_derivatives(molecule)
    be_we = spectroscopy_const['b_e'] / spectroscopy_const['omega_e']
    Y_10 = wavenumber_to_meter(spectroscopy_const['omega_e'])
    Y_20 = -wavenumber_to_meter(spectroscopy_const['omega_xe'])
    Y_30 = wavenumber_to_meter(spectroscopy_const['omega_ye']) 
    rotational_degeneracy = rotational_number * (rotational_number + 1)
    vibrational_degeneracy = 2 * vibrational_number + 1

    # Split in terms
    tmp_1 = be_we
    tmp_1 *= (-3 * Y_10 * derivative_const['first'] +
             derivative_const['second'])
    tmp_1 *= vibrational_degeneracy 
    tmp_1 *= 1/2

    tmp_2 = be_we**2
    tmp_2 *= derivative_const['first']
    tmp_2 *= rotational_degeneracy
    tmp_2 *= 4

    tmp_31a = 7
    tmp_31a += (15 * vibrational_degeneracy**2) 
    tmp_31a *= Y_10**3
    tmp_31a *= -3/8

    tmp_31b = 23
    tmp_31b += (39 * vibrational_degeneracy**2) 
    tmp_31b *= Y_20
    tmp_31b *= Y_10
    tmp_31b *=  1/4

    tmp_31c = 5
    tmp_31c += vibrational_degeneracy**2 
    tmp_31c *= Y_30
    tmp_31c *= -15/4

    tmp_31 = derivative_const['first'] * (tmp_31a + tmp_31b + tmp_31c)

    tmp_32a = 5
    tmp_32a += vibrational_degeneracy**2
    tmp_32a *= Y_20
    tmp_32a *- -3/4

    tmp_32b = 7
    tmp_32b += (15 * vibrational_degeneracy**2)
    tmp_32b *= Y_10**2
    tmp_32b *= 1/8

    tmp_32 = derivative_const['second'] * (tmp_32a + tmp_32b)

    tmp_33 = 7
    tmp_33 += (15 * vibrational_degeneracy**2)
    tmp_33 *= Y_10
    tmp_33 *= derivative_const['third']
    tmp_33 *= -1/24

    tmp_3 = (tmp_31 + tmp_32 + tmp_33) * be_we**2

    tmp_41 = 1 - Y_20
    tmp_41 *= 24
    tmp_41 += (27 * Y_10 * (1 + Y_10))
    tmp_41 *= derivative_const['first']

    tmp_42 = (1 + 3 * Y_10)
    tmp_42 *= derivative_const['second']
    tmp_42 *= -3

    tmp_43 = 1/8 * derivative_const['third']

    tmp_4 = (tmp_41 + tmp_42 + tmp_43) 
    tmp_4 *= rotational_degeneracy
    tmp_4 *= vibrational_degeneracy
    tmp_4 *= be_we**3

    IPython.embed(colors = 'Linux')
    return derivative_const['zeroth'] + tmp_1 + tmp_2 + tmp_3 + tmp_4






    





# Calculate polarizability as temperature
"""
    DOI: 10.1002/bbpc.19920960517 
    DOI: 10.1134/BF03355985
"""
"""
def kerl_polarizability_temperature(temperature_K=1000, molecule='N2', 
                                    wavelength_nm=633):
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


# Irikura: 10.1063/1.2436891
def zero_point_energy(spectroscopy_const_in):
    scope_var = (spectroscopy_const_in['alpha_e'] *
                 spectroscopy_const_in['omega_e'] /
                 spectroscopy_const_in['b_e'])
    tmp = spectroscopy_const_in['omega_e'] / 2
    tmp -= spectroscopy_const_in['omega_xe'] / 2
    tmp += spectroscopy_const_in['omega_ye'] / 8
    tmp += spectroscopy_const_in['b_e'] / 4
    tmp += scope_var / 12 
    tmp += scope_var**2 / (144 * spectroscopy_const_in['b_e'])

    return tmp #[1/cm] 

def partition_function(temperature_K, vibrational_number,
                                   rotational_number, molecule):
    degeneracy = 2 * rotational_number + 1
    hamiltonian_k = vibrational_energy_k(vibrational_number, molecule)
    hamiltonian_k += rotational_energy_k(vibrational_number,
                                   rotational_number, molecule)
    partition_function = degeneracy * np.exp(
                                    -wavenumber_to_joules(hamiltonian_k) / 
                                    (temperature_K * s_consts.k))
    return partition_function #[ ]


# Tropina 10.2514/6.2018-3904
def probability_of_state(temperature_K, vibrational_number,
                         rotational_number, molecule):

    numerator = partition_function(temperature_K, vibrational_number,
                                   rotational_number, molecule)

    denominator = 0.0
    for v in range(vibrational_number + 1):
        for j in range(rotational_number + 1):
            denominator += partition_function(temperature_K, v, j,
                                                        molecule)

    return numerator / denominator #[ ]



def tropina_polarizability():
    electric_charge = s_consts.e #[C]
    electron_mass = s_consts.m_e #[kg]




def vibrational_energy_k(vibrational_number, molecule):
    spectroscopy_constants = constants_tables.spectroscopy_constants(molecule)
    # Calculates the vibrational energy in units of wave number
    tmp_vib = vibrational_number + 1/2
    vib_energy_k = tmp_vib**2
    vib_energy_k *= -spectroscopy_constants['omega_xe']
    vib_energy_k += (spectroscopy_constants['omega_e'] * tmp_vib) #[cm^-1]

    return vib_energy_k 

def rotational_energy_k(vibrational_number, rotational_number, molecule):
    spectroscopy_constants = constants_tables.spectroscopy_constants(molecule)
    gas_amu_weight  = aero.air_atomic_mass()  # [g/mol] 
    # Calculates the rotational energy in units of wave number
    rot_energy_k = (vibrational_number + 1/2)
    rot_energy_k *= -spectroscopy_constants['alpha_e']
    rot_energy_k += spectroscopy_constants['b_e']
    rot_energy_k *= rotational_number
    rot_energy_k *= (rotational_number + 1) #[cm^-1]

    return rot_energy_k

def tranlational_energy(principal_number_x, principal_number_y,
                        principal_number_z):
    A = 5


# Kayser units
def wavenumber_to_electronvolt(wavenumber_cm):
    return wavenumber_to_joules(wavenumber_cm) / s_consts.eV #[eV]

def wavenumber_to_joules(wavenumber_cm):
    return wavenumber_cm * s_consts.c * 10**2 * s_consts.h #[J]

def wavenumber_to_meter(wavelength_cm):
    return wavelength_cm * 100








if __name__ == "__main__":
    gd = Gladstone_Dale()
    gd.update({n: np.round(gd[n] * 1E4, 3) for n in gd.keys()})
    altitude = np.linspace(0, 81E3, 1000)
    dielectric_const_0   = s_consts.epsilon_0 # [F/m]
    index = atmospheric_index_of_refraction(altitude)
    gd_s = atmospheric_gladstoneDaleConstant(altitude)

    #buldakov_polarizability(molecule='N2')

    prob_states = probability_of_state(temperature_K=1000,
                                        vibrational_number=2,
                                        rotational_number=3,
                                        molecule='N2')

    kerl_pola = kerl_polarizability_temperature(temperature_K=1000,
                                                molecule='N2',
                                                wavelength_nm=633)


    # MAKING PLOTS #
    plt.plot(index, altitude*1E-3, linewidth=2.5) 
    plt.xlabel('Index of refraction $[\;]$')
    plt.ylabel('Altitude $[km]$') 
    plt.ticklabel_format(useOffset=False, style='plain')
    plt.savefig('/Users/martin/Desktop/atmospheric_optics.png',
                bbox_inches='tight', dpi=300) 
    plt.close() 
    # MAKING PLOTS #

