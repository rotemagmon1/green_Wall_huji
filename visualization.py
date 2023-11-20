
from plots import *
from pre_process import *

# for test in computer do not have connection to the data add test=True in create_df parameters
df = create_df()
combine_all_daily_plots(df).show()




