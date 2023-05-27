import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *
import sys 
import os 
import IPython 

# Uncomment the following line to connect to a running instance of Tecplot 360:
# tp.session.connect()

# data_parser.py file_in_abs_path file_out_abs_path x1_value x2_value y1_value y2_value n_points  

# Inputs 
file_in_abs_path  = sys.argv[1] 
file_out_abs_path = sys.argv[2] 
x1_value          = sys.argv[3]
x2_value          = sys.argv[4]
y1_value          = sys.argv[5]
y2_value          = sys.argv[6]
n_points          = sys.argv[7] 

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
