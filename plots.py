import plotly.graph_objects as go
import datetime
import pandas as pd
from plotly.subplots import make_subplots

soil_ranges = {
        'Temperature': [20, 30],  # Celsius
        'Moisture': [20, 40],  # VWC
        'Permittivity': [16, 23],  # time of an electromagnetic wave transmitted along a waveguide through the soil
        'Conductivity': [0.11, 0.57]  # dS/m
    }

# filter hours of the co2 plot over year - change here
start_hour = None
end_hour = None

def plot_mean_and_std_by_hour(df, num_to_compare, names, yaxis, show_legend=False, expected_acc=0, const_acc=False):
    """
    This function plots the mean and standard deviation of sensor data by hour. It takes the following arguments:
    df: DataFrame containing the sensor data.
    num_to_compare: Integer representing the number of sensors to compare (number of traces in each subplot).
    names: A list of strings representing the names of the sensor columns to be compared.
    title: The title of the plot.
    yaxis: The label for the y-axis.
    The function calculates the mean and standard deviation for each specified sensor and creates Plotly traces for each one.
    The resulting traces are returned in a list called Scatters.
    """
    mean_vars = []
    mean_vars_agg = []
    std_vars = []
    scatters = []

    last_date = df['Date'].max()
    last_date_data = df[df['Date'] == last_date]
    before_last_date_data = df[df['Date'] != last_date]

    for i in range(num_to_compare):
        mean_vars.append(last_date_data.groupby('Hour')[names[i]].mean())
        mean_vars_agg.append(before_last_date_data.groupby('Hour')[names[i]].mean())
        std_vars.append(last_date_data.groupby('Hour')[names[i]].std())

    for i in range(num_to_compare):
        if i == 1:
            yaxis = yaxis + " remote sensor"
        scatters.append(go.Scatter(x=mean_vars[i].index, y=mean_vars[i], name=yaxis))
        scatters.append(go.Scatter(x=std_vars[i].index, y=mean_vars[i] - std_vars[i], name="std",
                                   line=dict(color='grey'), showlegend=show_legend))
        scatters.append(go.Scatter(x=std_vars[i].index, y=mean_vars[i] + std_vars[i], name="std", line=dict(color='grey'),
                                   fill='tonexty', fillcolor='rgba(173, 216, 230, 0.3)', showlegend=False))
        # add aggregation line - all data before last date
        scatters.append(go.Scatter(x=mean_vars_agg[i].index, y=mean_vars_agg[i], name="aggregation line",
                                   showlegend=show_legend, line=dict(color='black')))

        # accuracy
        if expected_acc != 0:
            if const_acc:
                predicted_acc_p = mean_vars[i] + expected_acc
                predicted_acc_n = mean_vars[i] - expected_acc
            else:
                # in percents
                predicted_acc_p = mean_vars[i] + ((expected_acc / 100) * mean_vars[i])
                predicted_acc_n = mean_vars[i] - ((expected_acc / 100) * mean_vars[i])
            scatters.append(go.Scatter(x=mean_vars[i].index, y=predicted_acc_p, name='accuracy of sensor',
                                       line=dict(color='green'), showlegend=show_legend))
            scatters.append(go.Scatter(x=mean_vars[i].index, y=predicted_acc_n, name=yaxis, line=dict(color='green'),
                                       showlegend=False))
    return scatters


def plot_mean_over_year(df, sensor_name, start_hour=None, end_hour=None):
    """
    This function plots the mean value of a specific sensor over the course of a year. It takes the following arguments:

    df: DataFrame containing the sensor data.
    sensor_name: A string representing the name of the sensor column to plot.

    The function calculates the mean value of the specified sensor for each day of the year and creates a scatter plot to visualize the data.
    The x-axis represents dates, and the y-axis represents the mean value of the sensor. The plot is returned as a Plotly figure.

    """
    # Group data by day of the year and calculate the mean value
    sensor_data = df.loc[:, ['Date', sensor_name, 'Hour']]
    sensor_data['Date'] = pd.to_datetime(sensor_data['Date']).dt.date

    # Filter data by hour range if specified
    if start_hour is not None and end_hour is not None:
        sensor_data = sensor_data[(sensor_data['Hour'] >= start_hour) & (sensor_data['Hour'] <= end_hour)]

    mean_by_day = sensor_data.groupby('Date')[sensor_name].mean()

    # Create the plot
    scatter = go.Scatter(x=mean_by_day.index, y=mean_by_day.values, mode='markers + lines', name=sensor_name + " mean")

    return scatter


def plot_comparison_last_day_vs_agg_of_period_ago(df, sensor_name, months=1, days=2):
    """
    This function plots a comparison between the mean values of a specific sensor for the last day and the mean values
    aggregated over a certain number of months ago.
    It takes the following arguments:

    df: DataFrame containing the sensor data.
    sensor_name: A string representing the name of the sensor column to plot.
    months: (optional) Integer representing the number of months to aggregate data for comparison. The default value is 1.
    days: (optional) Integer representing the number of days ago to compare the last day's mean value. The default value is 2.

    The function calculates the mean value of the specified sensor for the last day and the mean value aggregated over
    the specified number of months ago.
    It then creates a Plotly trace for each mean value and returns the traces in a list called scatters.

    """
    sensor_data = df.loc[:, ['Date', sensor_name, 'dayOfYear', 'Hour']]
    sensor_data['Date'] = pd.to_datetime(sensor_data['Date']).dt.date
    period = pd.Timestamp.now().normalize() - pd.DateOffset(months=months)  # can be change here for more month
    sensor_data_for_period = sensor_data[sensor_data['Date'] >= period]
    mean_by_hour_period = sensor_data_for_period.groupby('Hour')[sensor_name].mean()

    sensor_data_last_day = sensor_data[sensor_data['Date'] == (datetime.date.today() - datetime.timedelta(days=days))]
    mean_by_hour_last_day = sensor_data_last_day.groupby('Hour')[sensor_name].mean()

    scatters = []
    scatters.append(go.Scatter(x=mean_by_hour_period.index, y=mean_by_hour_period, name=f"mean {months} months ago"))
    scatters.append(go.Scatter(x=mean_by_hour_last_day.index, y=mean_by_hour_last_day, name=f"mean of {days} days ago"))
    return scatters


def soil_table_data(df):
    """
    create the table of soil measures of the last day
    :param df:
    :return: table figure
    """
    # Get the last date in the DataFrame
    last_date = df['Date'].max()

    # Filter the DataFrame to get data for the last date
    last_date_data = df[df['Date'] == last_date]

    # List of sensor parameters
    sensors_names_in_df = ['T Soil Temp', 'T Soil Volume', 'T Soil Permitivity', 'TScon']
    soil_parameters = ['Temperature', 'Moisture', 'Permittivity', 'Conductivity']

    # Calculate the mean for each parameter on the last date
    parameter_means = [round(last_date_data[param].mean(),3) for param in sensors_names_in_df]
    # Construct the table data
    soil_data = {
        'Soil Measures': soil_parameters,
        'Value': parameter_means,
        'Measurement Units': ['Degrees [Celsius]', 'VWC - Ratio of water volume to unit volume of soil',
                              'Duration of electromagnetic wave transmission through soil [seconds]',
                              'EC – Electric Conductivity [dS/m]']
    }
    table_data = pd.DataFrame(soil_data)

    fill_color = []
    for value, param in zip(table_data['Value'], table_data['Soil Measures']):
        if soil_ranges[param][0] <= value <= soil_ranges[param][1]:
            fill_color.append(['#C2F3C7', '#C2F3C7'])
        else:
            fill_color.append(['#F8D2CA', '#F8D2CA'])

    transposed_fill_color = [list(column) for column in zip(*fill_color)]

    soil_table = go.Table(
        columnwidth=[85, 70, 300],
        header=dict(
            values=['<b>Soil Parameters</b>', '<b>Daily Average</b>', '<b>Units</b>'],
            line_color='lightgray',
            align='center',
            font=dict(size=16),
            height=27,
        ),
        cells=dict(
            values=[table_data['Soil Measures'], table_data['Value'], table_data['Measurement Units']],
            fill_color=transposed_fill_color,
            align='center',
            font=dict(size=16),
            height=25,

        )
    )

    return soil_table


def combine_all_daily_plots(df):
    """
    This function combines all the individual plots created by the previous functions into a single 2x2 grid of subplots.
    It takes the following arguments:

    df: DataFrame containing the sensor data.

    The function calls the previous plotting functions to create four separate plots for CO2 levels, temperature, light,
     and relative humidity. Then, it uses make_subplots from Plotly to arrange these plots in a 2x2 grid.
     The function updates axis labels, titles, and annotations for the final combined figure.
     Finally, it displays the figure using fig.show().

    """
    fig1 = plot_mean_and_std_by_hour(df, 1, ['Co2'], "CO2 levels", True, 1)
    fig2 = plot_mean_and_std_by_hour(df, 2, ['T 2m', 'TC_2'], "temperature",
                                     False, 0.1, True)
    fig3 = plot_mean_and_std_by_hour(df, 2, ['Light', 'Light_2'], "no of photons", False,
                                     7, True)
    fig4 = plot_mean_and_std_by_hour(df, 2, ['RH', 'RH_2'], "RH", False, 2)

    # Create subplots with a 2x2 grid layout
    fig = make_subplots(rows=4, cols=2,
                        specs=[[{}, {}], [{}, {}], [{"colspan": 2}, None],
                         [{"type": "table", "colspan": 2}, None]],
                        subplot_titles=['CO2 level by hour',
                                        'Temperature by hour',
                                        'Light level by hour',
                                        'Moisture percentage by hour',
                                        'Yearly Mean Value of CO2'
                                        ],
                        vertical_spacing=0.07,
                        horizontal_spacing=0.07
                        )

    # Add each graph to a specific position in the grid
    fig.add_traces(fig1, rows=1, cols=1)
    fig.add_traces(fig2, rows=1, cols=2)
    fig.add_traces(fig3, rows=2, cols=1)
    fig.add_traces(fig4, rows=2, cols=2)

    fig.update_yaxes(title_text="CO2 levels", row=1, col=1)
    fig.update_yaxes(title_text="Temperature (°C)", row=1, col=2)
    fig.update_yaxes(title_text="Light (photons)", row=2, col=1)
    fig.update_yaxes(title_text="RH", row=2, col=2)
    # fig.update_xaxes(title_text="hour")

    fig.update_layout(
        title="<b>Green Wall</b>",
        title_font_size=24,
        showlegend=True,
        margin=dict(l=40, r=40, t=100, b=20),
    )

    fig.add_annotation(
        xref="paper", yref="paper",
        x=1, y=1.07,
        text=(df["Date"].max()).strftime("<b>Data from: %d-%m-%Y</b>"),
        showarrow=False,
        font=dict(size=14)
    )

    # Add the plot - Co2 over year

    co2_plot = plot_mean_over_year(df, 'Co2', start_hour, end_hour)
    fig.add_traces(co2_plot, rows=3, cols=1)
    fig.update_yaxes(title_text="Mean Co2 value", row=3, col=1)
    fig.update_xaxes(title_text="Date", row=3, col=1)

    # Add the soil sensors data in table to row 3
    fig.add_trace(soil_table_data(df), row=4, col=1)

    #fig.show()
    return fig;
