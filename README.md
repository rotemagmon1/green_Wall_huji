# Green Wall
Green wall data visualization

*****************************
The plots
*****************************

* The comparison plots of Co2, temperature, light and RH are created by plot_mean_and_std_by_hour (the top four graphs).
The graph for each sensor shows the hourly average (in a different color for each sensor), 
with one standard deviation above and below shown in grey. 
In addition, the manufacturer's accuracy is shown for each sensor (in green),
and an aggregation line (in black) representing the yearly average per hour.
In the light, temperature and humidity sensors, there are two graphs, representing the close sensor and the far sensor.

* The Co2 mean over the last year plot is created by plot_mean_over_year (the wide graph).
The graph is by Date, and can be filtered by the code to specific range of hours (need to be confing at 
the top of plots.py.
(I tried in this plot to see if there is a decrease in the amount of carbon dioxide [Co2] in the room).

* The Soil measures table is created by soil_table_data.
Each line in the table is a soil parameter, the second column (value) is the average readout of the last day of the 
sensor, and the measurement unit is explained in the third column.
The line is in green color if the value is in the optimal range, and in red color if not.
The optimal ranges defined: 
 'Soil Temperature': [20, 30],  # Celsius
 'Soil Moisture': [20, 40],  # VWC
 'Soil Permittivity': [16, 23],  # Time of an electromagnetic wave transmitted along a waveguide through the soil
 'Soil Conductivity': [0.11, 0.57]  # dS/m

[these can be modified easily at the top in plots.py file.]

*****************************
The Data
*****************************

The Data frame consists all CSV files of the sensors from the folder.
There is a record for each minute, there is a column for each sensor.

*****************************
The Code
*****************************
the code is separated into 4 files:

1. pre_process.py 
Takes all the data (all csv files from /cs/labs/gavish/green_wall/data/) and creates a Pandas DataFrame,
and pre-processes the data: checks valid ranges (can be edited in the top of this file), changes columns, 
and edits the date column.
There is an option to use create_df(test=True) - on CSV with data of a specific day and run the project.

2. plots.py
Functions that create the different plots.
combine_all_daily_plots is the function that combines all subplots and allows them to be presented together.

3. visualization.py
Creates the data frame, and Runs combine_all_daily_plots.

4. automate
Updates the project from git and runs visualization.

*****************************
requirements.txt 
*****************************
to create and updated requirements.txt  file:
run in terminal when all packages are installed:
pip freeze > requirements.txt 

