import tecplot as tp
import os
import numpy as np
import sys
from tecplot.exception import *
from tecplot.constant import *

# Initialization variables:
start_end_points = [(-0.02,0), (0,0)] # start point and end point in (x,y) format
num_points = 1000
var_to_plot = "Pressure_Coefficient"

# Run this script with "-c" to connect to the Tecplot 360 GUI on port 7600 (default)
# To enable connections in Tecplot 360, click on:
#   "Scripting" -> "PyTecplot Connections..." -> "Accept connections"
if '-c' in sys.argv:
    tp.session.connect()

# This script assumes that the current working directory is the location of the .py and .szplt files
working_dir = os.getcwd()
tp.data.load_tecplot_szl(os.path.join(working_dir , 'flow.szplt'))

# Activating the Tecplot 360 frames and setting up the contour plot
frame = tp.active_frame()
frame.activate()
plot = frame.plot()
dataset = frame.dataset
plot.contour(0).variable = dataset.variable(f"{var_to_plot}")
plot.show_contour = True
plot.contour(0).colormap_name = 'Sequential - Yellow/Green/Blue'

# Extract lines using the start, end, and # of points provided above
line = tp.data.extract.extract_line(start_end_points, num_points=num_points)
line.name = 'Line Extraction'

# Distance variable calculated for use in  in case the line extracted isn't along an axis
tp.data.operate.execute_equation('{Distance} = SQRT((x-%s)**2 + (y-%s)**2)'%(start_end_points[0][0], start_end_points[0][1]), zones=[line])

# The lines below will show the extacted slice mesh in the 2D Cartesian plot
plot.show_mesh = True
plot.fieldmap(0).mesh.show = False

# Creating the XY Line frame and activating it
frame = tp.active_page().add_frame()
frame.position = (3.0, 0.5)
frame.height = 2
frame.width = 4
plot = tp.active_frame().plot(PlotType.XYLine)
plot.activate()

# Adding the XY line map of interest
plot.delete_linemaps()
dataset = tp.active_frame().dataset
lmap = plot.add_linemap('data', line, x=dataset.variable('x'),
                        y=dataset.variable(f'{var_to_plot}'))
# Adding XY plot style and using best view fit
lmap.line.line_thickness = 2.0
plot.axes.viewport.left = 20
plot.axes.viewport.bottom = 20
plot.view.fit()

# Save Tecplot ascii file of the extracted line data:
tp.data.save_tecplot_ascii('line.dat', dataset=dataset,
                                zones=line, use_point_format=True)

# Export an image
tp.export.save_png("extract_line_x.png", region=ExportRegion.AllFrames,
                   width=3600, supersample=3)
