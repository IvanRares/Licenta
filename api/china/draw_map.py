import sys
from pathlib import Path
sys.path.append(str(Path(script_dir).resolve().parent.parent))
from functions import draw_map
import numpy as np
import pandas as pd
alpha, beta, gamma = 0.24, 1.4, 1/5.1
output_image_paths = []

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

image_path = draw_map(grid,10,5)
output_image_paths.append(image_path)


