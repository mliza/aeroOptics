#!/opt/homebrew/bin/python3
'''
    Date:   03/26/2023
    Author: Martin E. Liza
    File:   constant_tables.py
    Def:

    Author          Date        Revision
    ----------------------------------------------------
    Martin E. Liza  03/26/2023  Initial version.
'''

# Gladstone-Dale constants 
def karl_2003(): #follows SU2 MutationPP format 
# https://arc.aiaa.org/doi/pdf/10.2514/6.2003-4252
    dict_out = { 'N'  : 0.301E-3,
                 'O'  : 0.182E-3,
                 'NO' : 0.221E-3,
                 'N2' : 0.238E-3,
                 'O2' : 0.190E-3 } #[m3/kg]
    return dict_out

# Polarizability
def polarizability(): #follows SU2 MutationPP format
    dict_out = { #'e-'  : 0.0, 
                 'N+'   : 0.559E-24,
                 'O+'   : 0.345E-24,
                 'NO+'  : 1.021E-24,
                 'N2+'  : 2.386E-24,
                 'O2+'  : 0.238E-24,
                 'N'    : 1.100E-24,
                 'O'    : 0.802E-24,
                 'NO'   : 1.700E-24,
                 'N2'   : 1.7403E-24,
                 'O2'   : 1.5689E-24 } # [cm^3]  
    return dict_out 

    
def polarizability_derivatives(molecule='N2'):
    # https://link.springer.com/content/pdf/10.1134/BF03355985.pdf
    """
    Constants below come from Buldakov Paper: 'Temperature Dependence of Polarizability
of Diatomic Homonuclear Molecules'. Reference for each constant are provided
below
    """
    dict_out = { }
    if molecule == 'H2':
        dict_out['zeroth'] = 0.7849 * 1E30 #https://edisciplinas.usp.br/pluginfile.php/4557662/mod_resource/content/1/CRC%20Handbook%20of%20Chemistry%20and%20Physics%2095th%20Edition.pdf
        dict_out['first'] = 0.90 * 1E30 #https://www.tandfonline.com/doi/abs/10.1080/00268978000103191
        dict_out['second'] = 0.49 * 1E30 #https://www.tandfonline.com/doi/abs/10.1080/00268978000103191 
        dict_out['third'] = -0.85 * 1E30 #https://www.tandfonline.com/doi/abs/10.1080/00268978000103191

    if molecule == 'N2':
        dict_out['zeroth'] = 1.7801 * 1E30 #https://edisciplinas.usp.br/pluginfile.php/4557662/mod_resource/content/1/CRC%20Handbook%20of%20Chemistry%20and%20Physics%2095th%20Edition.pdf
        dict_out['first'] = 1.86 * 1E30 #M. A. Buldakov, B. V. Korolev, I. I. Matrosov, and T. N. Popova, Opt. Spektrosk. 63, 775 (1987) MISSING REFERENCE 
        dict_out['second'] = 1.2 * 1E30 #M. A. Buldakov, B. V. Korolev, I. I. Matrosov, and T. N. Popova, Opt. Spektrosk. 63, 775 (1987) MISSING REFERENCE 
        dict_out['third'] = -4.6 * 1E30 #https://pubs.aip.org/aip/jcp/article-abstract/78/9/5287/777120/Theoretical-study-of-the-effects-of-vibrational?redirectedFrom=fulltext

    if molecule == 'O2':
        dict_out['zeroth'] = 1.6180 * 1E30 #https://edisciplinas.usp.br/pluginfile.php/4557662/mod_resource/content/1/CRC%20Handbook%20of%20Chemistry%20and%20Physics%2095th%20Edition.pdf
        dict_out['first'] = 1.76 * 1E30 #M. A. Buldakov, B. V. Korolev, I. I. Matrosov, and T. N. Popova, Opt. Spektrosk. 63, 775 (1987) MISSING REFERENCE 
        dict_out['second'] = 3.4 * 1E30 #M. A. Buldakov, B. V. Korolev, I. I. Matrosov, and T. N. Popova, Opt. Spektrosk. 63, 775 (1987) MISSING REFERENCE 
        dict_out['third'] = -23.7 * 1E30 #https://pubs.aip.org/aip/jcp/article-abstract/100/2/1297/482621/Frequency-dependent-polarizabilities-of-O2-and-van?redirectedFrom=fulltext

    return dict_out #[m^3]

def parameters_mean_polarizability(molecule='N2'):
    #https://onlinelibrary.wiley.com/doi/10.1002/bbpc.19920960517
    # Check reference in paper
    dict_out = { }
    if molecule == 'H2':
        dict_out['groundPolarizability'] = 0.80320 * 1E30 #[m^3]
        dict_out['groundFrequency'] = 2.1399 * 1E-16 # [1/s]
        dict_out['b'] = 5.87 * 1E6 # [1/K]
        dict_out['c'] = 7.544 * 1E9 # [1/K^2]

    if molecule == 'N2':
        dict_out['groundPolarizability'] = 1.7406 * 1E30 #[m^3]
        dict_out['groundFrequency'] = 2.6049 * 1E-16 # [1/s]
        dict_out['b'] = 1.8 * 1E6 # [1/K]
        dict_out['c'] = 0.683# [1/K^2]
        #dict_out['c'] = 0.0 
    if molecule == 'O2':
        dict_out['groundPolarizability'] = 1.5658 * 1E30 #[m^3]
        dict_out['groundFrequency'] = 2.1801 * 1E-16 # [1/s]
        dict_out['b'] = -2.369 * 1E6 # [1/K]
        dict_out['c'] = 8.687 * 1E9# [1/K^2]
    if molecule == 'Air':
        dict_out['groundPolarizability'] = 1.6970 * 1E30 #[m^3]
        dict_out['groundFrequency'] = 2.47044 * 1E-16 # [1/s]
        dict_out['b'] = 10.6 * 1E6 # [1/K]
        dict_out['c'] = 7.909 * 1E9# [1/K^2]

    return dict_out


    


