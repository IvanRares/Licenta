import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from functions import calculate_ca, calculate_p, draw_color_map
import numpy as np
import pandas as pd
alpha, beta, gamma = 0.24, 1.4, 1/5.1

grid = np.array([
    [0,0,0,0,0,12,12,12,0,0,0,0,0,0,0],
    [0,0,13,9,9,12,12,20,6,0,0,0,0,0,0],
    [0,19,13,9,9,12,20,6,6,0,0,0,0,0,0],
    [0,13,13,9,9,20,20,20,6,0,0,0,0,0,0],
    [13,13,13,9,9,9,20,0,0,0,0,0,0,0,0],
    [13,13,13,5,5,5,5,0,0,0,0,0,0,0,0],
    [0,13,8,8,5,5,5,0,0,0,0,0,0,0,0],
    [0,8,0,0,17,17,5,0,0,0,0,0,0,0,0],
    [0,0,0,0,17,17,17,10,10,0,0,0,0,0,0],
    [0,0,0,0,17,17,18,10,10,0,0,0,0,0,0],
    [0,0,0,0,0,17,18,18,10,0,0,0,0,0,0],
    [0,0,0,0,0,17,7,7,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,7,7,1,1,0,0,0,0,0],
    [0,0,0,0,0,0,7,7,7,11,14,14,0,0,0],
    [0,0,15,0,0,0,0,7,7,4,14,14,0,0,0],
    [0,15,15,0,0,0,0,0,4,4,2,14,14,0,0],
    [0,15,15,0,0,0,0,0,0,4,4,2,14,14,0],
    [0,15,15,0,0,0,0,0,0,0,4,2,0,14,14],
    [0,15,15,0,0,0,0,0,0,0,0,3,0,0,14],
    [0,15,0,0,0,0,0,0,0,0,0,3,3,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,3,3,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,3,0,0,0],
    [0,0,0,0,0,0,16,16,0,16,16,3,0,0,0],
    [0,0,0,0,0,0,16,16,16,16,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,16,16,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,16,0,0,0,0,0]
])
days = 6*7
prediction_days=2*7

final_df = pd.read_csv('../data/italy/time_series_covid19_active_global.csv', usecols=range(4+days+prediction_days))
final_df= final_df[final_df['Country/Region']=='Italy']

fixed_columns = final_df.iloc[:, :4]
variable_columns = final_df.iloc[:, 4:]

train_infected=pd.concat([fixed_columns, variable_columns.iloc[:, :(days)]], axis=1)
test_infected=pd.concat([fixed_columns, variable_columns.iloc[:, (days):]], axis=1)
regions = pd.read_csv('../data/italy/regions.csv')

ca_infected = calculate_ca(days,grid,train_infected,regions)

delta_I = np.diff(ca_infected, axis=0)

p=calculate_p(ca_infected, grid, beta, gamma, alpha)

draw_color_map(grid,ca_infected,6,20,15,'spread_map.png')


