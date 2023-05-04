import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn.linear_model
import copy

def calculate_ca(days,grid,data, regions):
    ca = np.zeros((days, grid.shape[0], grid.shape[1]))
    region_population = regions[['ID', 'Cell Count']].set_index('ID').to_dict()[
        'Cell Count']
    for i in range(days):
        col_name = data.columns[i+4]
        region_cases = data[['Province/State', col_name]
                                ].set_index('Province/State').to_dict()[col_name]
        for j in range(grid.shape[0]):
            for k in range(grid.shape[1]):
                if grid[j, k] != 0:
                    region_id = grid[j, k]
                    cell_count = region_population[region_id]
                    region_name = regions.loc[regions['ID']
                                              == region_id, 'Region'].iloc[0]
                    cases = 0
                    if ',' in region_name:
                        region_list = region_name.split(',')
                        for sub_region in region_list:
                            sub_region = sub_region.strip()
                            cases += region_cases.get(sub_region, 0)
                    else:
                        cases = region_cases.get(region_name, 0)
                    ca[i, j, k] = cases / cell_count
    return ca

def fix_p(p, grid):
    one,center,north,east,south,west=range(6)
    rows, cols = p.shape[0], p.shape[1]
    for i in range(rows):
        for j in range(cols):
            if grid[i,j] == 0:
                p[i,j] = 0
            else:
                if i == 0:
                    p[i,j,north] = 0
                elif i == rows - 1:
                    p[i,j,south] = 0
                if j == 0:
                    p[i,j,west] = 0
                elif j == cols - 1:
                    p[i,j,east] = 0
                if i > 0 and grid[i-1,j] == 0:
                    p[i,j,north] = 0
                if j < cols - 1 and grid[i,j+1] == 0:
                    p[i,j,east] = 0
                if i < rows - 1 and grid[i+1,j] == 0:
                    p[i,j,south] = 0
                if j > 0 and grid[i,j-1] == 0:
                    p[i,j,west] = 0
    return p

def calculate_p(ca_infected, grid, alpha, beta, gamma):
    p = np.zeros((len(ca_infected) - 1, grid.shape[0], grid.shape[1], 6))
    for i in range(1, len(ca_infected)):
        current_day = ca_infected[i - 1]
        north = np.zeros_like(current_day)
        north[1:] = current_day[:-1]
        south = np.zeros_like(current_day)
        south[:-1] = current_day[1:]
        east = np.zeros_like(current_day)
        east[:, :-1] = current_day[:, 1:]
        west = np.zeros_like(current_day)
        west[:, 1:] = current_day[:, :-1]
        current_cell = np.stack(
            [np.ones_like(current_day), current_day, north, east, south, west], axis=-1)
        p[i - 1] = np.concatenate((current_cell[..., :1],
                                  current_cell[..., 1:] * (beta - gamma - alpha)), axis=-1)
    for i in range(p.shape[0]):
        p[i]=fix_p(p[i], grid)
    return p
	
def predict_i(p, q):
    N, M, _ = p.shape
    delta_i = np.zeros((N, M))
    for j in range(N):
        for k in range(M):
            delta_i[j, k] = np.dot(p[j, k], q[j, k])
    return delta_i

def find_q(delta_i, p, grid):
    t, N, M = delta_i.shape
    q = np.zeros((N, M, 6))
    for j in range(N):
        for k in range(M):
            if grid[j,k]!=0:
                delta_i_jk = delta_i[:,j,k]
                p_jk = p[:,j,k,:]
                model = sklearn.linear_model.LinearRegression().fit(p_jk, delta_i_jk)
                q[j, k, :] = model.coef_
                q[j,k,0]=model.intercept_
    return q
	
def calculate_m_bar(m, grid):
    unique_values = np.unique(grid)
    m_bar = np.zeros_like(m)
    for value in unique_values:
        indices = np.where(grid == value)
        cell_count = len(indices[0])
        m_sum = round(np.sum(m[indices]))
        if m_sum<0.:
            m_sum=0.
        m_bar[grid == value] = m_sum / cell_count
    return m_bar

def calculate_m(m_bar,p_bar,q):
    return m_bar+predict_i(p_bar,q)

def calculate_p_bar(m_bar, alpha, beta, gamma, grid):
    north = np.zeros_like(m_bar)
    north[1:] = m_bar[:-1]
    south = np.zeros_like(m_bar)
    south[:-1] = m_bar[1:]
    east = np.zeros_like(m_bar)
    east[:, :-1] = m_bar[:, 1:]
    west = np.zeros_like(m_bar)
    west[:, 1:] = m_bar[:, :-1]
    aux = np.stack(
    [np.ones_like(m_bar),m_bar,north,east,south,west],axis=-1)
    new_p=np.concatenate((aux[...,:1],
                         aux[...,1:]*(beta-gamma-alpha)),axis=-1)
    return fix_p(new_p, grid)
	
def draw_map(grid,width,height):
    df = pd.DataFrame(grid)

    cmap = sns.diverging_palette(0, 250, as_cmap=True)
    color_map = cmap.from_list("", [(0, "lightblue"), (1, "white")], N=2)

    f, ax = plt.subplots(figsize=(width, height))
    plt.pcolormesh(df, cmap=color_map, vmin=0, vmax=1)

    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            horizontal = j < df.shape[1] - 1 and df.iloc[i, j] != df.iloc[i, j + 1]
            vertical = i < df.shape[0] - 1 and df.iloc[i, j] != df.iloc[i + 1, j]

            if horizontal:
                plt.plot([j + 1, j + 1], [i, i + 1], color="black", linewidth=3)
            elif j < df.shape[1] - 1:
                plt.plot([j + 1, j + 1], [i, i + 1], color="gray", linewidth=1)

            if vertical:
                plt.plot([j, j + 1], [i + 1, i + 1], color="black", linewidth=3)
            elif i < df.shape[0] - 1:
                plt.plot([j, j + 1], [i + 1, i + 1], color="gray", linewidth=1)

    plt.gca().invert_yaxis()
    plt.savefig('grid_map.png')
    plt.close()
	
def draw_borders(ax, grid):
    n, m = grid.shape
    for j in range(n):
        for k in range(m):
            horizontal = k < m - 1 and grid[j, k] != grid[j, k + 1]
            vertical = j < n - 1 and grid[j, k] != grid[j + 1, k]

            if horizontal:
                ax.plot([k + 1, k + 1], [j, j + 1], color="black", linewidth=3)
            elif k < m - 1:
                ax.plot([k + 1, k + 1], [j, j + 1], color="gray", linewidth=1)

            if vertical:
                ax.plot([k, k + 1], [j + 1, j + 1], color="black", linewidth=3)
            elif j < n - 1:
                ax.plot([k, k + 1], [j + 1, j + 1], color="gray", linewidth=1)

def draw_color_map(grid, ca_infected, number_of_weeks, width, height, name):
    color_grid = copy.deepcopy(ca_infected)
    for i in range(ca_infected.shape[0]):
        aux = color_grid[i]
        aux[np.where(grid == 0)] = -2
        color_grid[i] = aux

    boundaries = [-2, -1, 0.02127659574468084, 2, 25, 100, 500, 501]
    values = ['lightblue', 'white', 'lime', 'yellow', 'orange', 'darkorange', 'red']
    cmap = plt.matplotlib.colors.ListedColormap(values)
    norm = plt.matplotlib.colors.BoundaryNorm(boundaries, cmap.N)

    fig, axs = plt.subplots(number_of_weeks, 7, figsize=(width, height), sharex=True, sharey=True)
    cols = ['Day {}'.format(day + 1) for day in range(7)]
    rows = ['Week {}'.format(week + 1) for week in range(number_of_weeks)]

    for i, ax in enumerate(axs.flatten()):
        if i < 7 * number_of_weeks:
            ax.pcolormesh(color_grid[i, :, :], cmap=cmap, norm=norm, shading='flat')
            ax.set_ylim(color_grid[i, :, :].shape[0], 0)
            draw_borders(ax, grid)
        else:
            ax.axis('off')

        ax.set_xticks([])
        ax.set_yticks([])

    for ax, col in zip(axs[0], cols):
        ax.set_title(col)

    for ax, row in zip(axs[:, 0], rows):
        ax.set_ylabel(row, rotation=0, size='large', ha='right')

    plt.savefig(name)
    plt.close()