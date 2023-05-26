'''
    Date:   06/27/2021
    Author: Martin E. Liza
    File:   dataToPickle.py
    Def:    loads a tecplot file and outputs a 
            dictionary pickle file 
            
            ./dataToPickle.py "data_folder_in" "data_file_in.ext"

    Author          Date        Revision
    ------------------------------------------ 
    Martin E. Liza  06/27/2021  Initial Version.
    Martin E. Liza  07/14/2021  Added the capability to store the  
                                multi-dimensional array per zone.
'''
import tecplot as tp 
import numpy as np
import pickle 
import sys 
import os 
import IPython

# Inputs 
file_in_abs_path  = sys.argv[1] 
file_out_abs_path = sys.argv[2] 
files_in          = os.listdir(file_in_abs_path) 
data_dict         = { }


# Load multiple files in one pickle file 
for f in files_in: 
    f_name = f.split('.')[0]
    data_in             = tp.data.load_tecplot(os.path.join(file_in_abs_path, f)) 
    data_variable_names = data_in.variable_names
    zone_names          = data_in.zone_names 

    # Check if there is only 1 zone or multiple zones and 
    # initializes dictionary accordingly 
    if len(zone_names) == 1:
        data_dict[f_name] = { }
        z = zone_names[0] 
    else:
        for z in zone_names:
            data_dict[f_name][z] = { }
    
    # Load variables in the dictionary dict[file_in_name][zone][variable] 
    for v in data_variable_names:
        if len(zone_names) == 1:
            data_dict[f_name][v] = data_in.zone(z).values(v)[:] 
        else: 
            for z in zone_names:
                data_dict[f_name][z][v] = data_in.zone(z).values(v)[:] 

    # Clear tecplot 
    tp.new_layout()

# Store data in a dictionary 
pickle_out = open(file_out_abs_path, 'wb')
pickle.dump(data_dict, pickle_out) 
pickle_out.close() 
