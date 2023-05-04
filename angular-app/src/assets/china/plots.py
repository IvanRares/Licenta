import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from functions import calculate_ca, calculate_m, calculate_m_bar, calculate_p, calculate_p_bar, draw_color_map, find_q
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
alpha, beta, gamma = 0.24, 1.4, 1/5.1

grid = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 14, 14, 10, 10, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 27, 27, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 14, 14, 14, 14, 10, 10, 10, 10],
    [0, 0, 0, 0, 0, 27, 27, 27, 27, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 14, 14, 14, 14, 10, 10, 10, 10],
    [0, 0, 0, 27, 27, 27, 27, 27, 27, 27, 0, 0, 0, 0, 0,
        0, 0, 14, 14, 14, 14, 14, 14, 17, 17, 10, 10],
    [27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 0, 0, 0,
        0, 0, 0, 14, 14, 14, 14, 14, 14, 14, 17, 17, 17],
    [27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 5, 5, 14, 14,
        14, 14, 14, 14, 14, 14, 2, 2, 18, 18, 18, 0, 0],
    [27, 27, 27, 27, 27, 27, 27, 27, 27, 20, 20, 5, 5,
        5, 5, 14, 14, 24, 24, 2, 2, 2, 2, 18, 0, 0, 0],
    [0, 27, 27, 27, 27, 26, 26, 26, 20, 20, 20, 20, 20,
        20, 5, 5, 19, 21, 24, 24, 22, 22, 22, 22, 0, 0, 0],
    [0, 26, 26, 26, 26, 26, 26, 26, 20, 20, 20, 20, 20,
        5, 5, 5, 21, 21, 11, 11, 11, 1, 1, 15, 0, 0, 0],
    [0, 26, 26, 26, 26, 26, 26, 26, 26, 26, 20, 20, 20,
        20, 5, 21, 21, 25, 12, 12, 11, 16, 1, 15, 0, 0, 0],
    [0, 0, 0, 26, 26, 26, 26, 26, 26, 26, 26, 20, 20, 20,
        25, 25, 25, 25, 12, 12, 12, 16, 23, 23, 0, 0, 0],
    [0, 0, 0, 0, 26, 26, 26, 26, 26, 26, 26, 25, 25, 25,
        25, 3, 3, 8, 13, 13, 16, 16, 4, 23, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 28, 28, 25, 25,
        25, 8, 8, 8, 13, 13, 13, 4, 4, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 28, 28, 25, 28,
        28, 28, 7, 7, 7, 7, 6, 6, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 28, 28, 28,
        28, 7, 7, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
])
days = 6*7
prediction_days=2*7
final_df = pd.read_csv('../data/china/time_series_covid19_active_global.csv', usecols=range(4+days+prediction_days))
final_df= final_df[final_df['Country/Region']=='China']

fixed_columns = final_df.iloc[:, :4]
variable_columns = final_df.iloc[:, 4:]

train_infected=pd.concat([fixed_columns, variable_columns.iloc[:, :(days)]], axis=1)
test_infected=pd.concat([fixed_columns, variable_columns.iloc[:, (days):]], axis=1)
regions = pd.read_csv('../data/china/regions.csv')

ca_infected = calculate_ca(days,grid,train_infected, regions)

delta_I = np.diff(ca_infected, axis=0)

p=calculate_p(ca_infected, grid, alpha, beta, gamma)

q = find_q(delta_I, p, grid)

_,counts=np.unique(grid,return_counts=True)
total_cells=counts[1:].sum()
prediction=np.zeros((days,grid.shape[0],grid.shape[1]))
m=ca_infected[0]
for i in range(1,days):
    m_bar=calculate_m_bar(m, grid)
    prediction[i-1]=m_bar
    m=calculate_m(m_bar,p[i-1],q)
prediction[-1]=calculate_m_bar(m, grid) 
sums=[ca_infected[i].sum()/total_cells for i in range(days)]
pred_sums=[prediction[i].sum()/total_cells for i in range(days)]

plt.plot(range(days),sums,label="actual")
plt.plot(range(days),pred_sums,label="pred")
plt.legend()
plt.savefig('first_weeks_plot.png')
plt.close()

actual=calculate_ca(prediction_days,grid,test_infected, regions)
m=actual[0]
prediction=np.zeros((prediction_days,grid.shape[0],grid.shape[1]))
for i in range(1,prediction_days):
    m_bar=calculate_m_bar(m, grid)
    prediction[i-1]=m_bar
    p_bar=calculate_p_bar(m_bar, alpha, beta, gamma, grid)
    m=calculate_m(m_bar,p_bar,q)
prediction[-1]=calculate_m_bar(m, grid) 
pred_sums=[prediction[i].sum()/258 for i in range(prediction_days)]
actual_sums=[actual[i].sum()/258 for i in range(prediction_days)]
plt.plot(range(prediction_days),pred_sums,label="pred")
plt.plot(range(prediction_days),actual_sums,label="actual")
plt.legend()
plt.savefig('prediction_weeks_plot.png')
plt.close()

draw_color_map(grid,actual,2,20,4,'actual_weeks_map.png')

draw_color_map(grid,prediction,2,20,4,'prediction_weeks_map.png')


