import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from functions import calculate_ca, calculate_p, draw_color_map
import numpy as np
import pandas as pd
alpha, beta, gamma = 0.24, 1.4, 1/5.1

grid = np.array([
    [0,0,0,0,14,14,14,0,0,0,0,0,0,0],
    [0,0,0,0,14,14,14,14,0,0,8,8,0,0],
    [0,0,0,0,0,14,14,14,8,8,8,8,8,0],
    [0,0,5,5,5,5,6,14,8,8,8,8,8,0],
    [0,0,5,5,5,5,5,5,8,4,8,4,4,0],
    [0,0,5,5,5,5,5,5,13,4,4,4,4,0],
    [0,5,5,5,9,5,5,5,13,13,4,3,4,0],
    [0,9,9,9,9,5,5,13,13,13,4,4,4,0],
    [9,9,9,9,9,9,5,13,13,13,13,4,4,0],
    [9,9,9,9,7,7,15,15,15,13,12,12,12,12],
    [9,9,9,9,7,7,15,15,15,15,12,12,12,12],
    [0,9,10,10,7,7,2,15,15,12,12,0,0,0],
    [0,10,10,10,7,2,2,2,2,2,0,0,0,0],
    [0,10,10,10,7,1,2,2,2,2,0,0,0,0],
    [0,11,11,10,1,1,1,2,2,2,2,0,0,0],
    [0,0,0,1,1,1,1,2,2,2,2,2,0,0],
    [0,0,0,1,1,1,2,2,2,2,2,0,0,0],
    [0,0,0,1,1,1,1,2,2,2,2,0,0,0],
    [0,0,0,1,0,1,2,2,2,0,2,0,0,0]
])
days =6*7
prediction_days=2*7

final_df = pd.read_csv('../data/germany/time_series_covid19_active_global.csv', usecols=range(4+days+prediction_days))
final_df= final_df[final_df['Country/Region']=='Germany']

fixed_columns = final_df.iloc[:, :4]
variable_columns = final_df.iloc[:, 4:]

train_infected=pd.concat([fixed_columns, variable_columns.iloc[:, :(days)]], axis=1)
test_infected=pd.concat([fixed_columns, variable_columns.iloc[:, (days):]], axis=1)
regions = pd.read_csv('../data/germany/regions.csv')

ca_infected = calculate_ca(days,grid,train_infected,regions)

delta_I = np.diff(ca_infected, axis=0)

p=calculate_p(ca_infected, grid, beta, gamma, alpha)

draw_color_map(grid,ca_infected,6,14,20,'spread_map.png')


