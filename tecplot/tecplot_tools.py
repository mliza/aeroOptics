
import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *
import sys 
import os 
import pickle
import IPython 

# Uncomment the following line to connect to a running instance of Tecplot 360:
# tp.session.connect()

# data_parser.py file_in_abs_path file_out_abs_path x1_value x2_value y1_value y2_value n_points  

def data_cutter(struct_in):
    # Inputs 
    """
    file_in_abs_path  = sys.argv[1] 
    file_out_abs_path = sys.argv[2] 
    x1_value          = sys.argv[3]
    x2_value          = sys.argv[4]
    y1_value          = sys.argv[5]
    y2_value          = sys.argv[6]
    n_points          = sys.argv[7] 
    """
    file_in_abs_path  = struct_in['f_in'] 
    file_out_abs_path = struct_in['f_out'] 
    x1_value          = struct_in['x1']
    x2_value          = struct_in['x2']
    y1_value          = struct_in['y1']
    y2_value          = struct_in['y2']
    n_points          = struct_in['n'] 

    start_end_points = [(x1_value, y1_value), (x2_value, y2_value)]
    # This restart tecplot 
    tp.new_layout() 
    tp.data.load_tecplot_szl(file_in_abs_path)
    line      = tp.data.extract.extract_line(start_end_points,
                                             num_points=int(n_points))
    line.name = file_out_abs_path.split('.')[0].split('/')[-1]
    tp.data.operate.execute_equation('{Distance} = SQRT((x-%s)**2 + (y-%s)**2)'%(
                   start_end_points[0][0],  start_end_points[0][1]), zones=[line])
    dataset = tp.active_frame().dataset
    tp.data.save_tecplot_ascii(file_out_abs_path, dataset=dataset,
                                zones=line, use_point_format=True)

    tp.new_layout()

def tp_to_pickle(file_in_abs_path, file_out_abs_path):
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
