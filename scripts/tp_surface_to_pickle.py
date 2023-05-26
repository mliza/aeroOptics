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
data_dict         = { }

data_in             = tp.data.load_tecplot_szl(file_in_abs_path) 
data_variable_names = data_in.variable_names
zone_names          = data_in.zone_names 
# Load multiple files in one pickle file 
data_dict = { }
for i in data_variable_names:
    data_dict[i] = data_in.zone(zone_names[0]).values(i)[:] 

# Clear tecplot 
tp.new_layout()

# Store data in a dictionary 
pickle_out = open(file_out_abs_path, 'wb')
pickle.dump(data_dict, pickle_out) 
pickle_out.close() 
