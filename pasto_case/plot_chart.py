import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_radar_chart(data, metrics, title, yticks_value, yticks_name):
    N = len(metrics)
    theta = np.linspace(0, 2 * np.pi, N, endpoint=False)
    theta = np.concatenate([theta, [theta[0]]])
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
    
    ax.set_title(title, y=1.0, fontsize=8)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_rlabel_position(90)
    ax.spines['polar'].set_zorder(1)
    ax.spines['polar'].set_color('white')
    
    color_palette = ['#620062', '#a4165f', '#d54855', '#f4814b', '#ffbc4f', '#f9f871', '#00b6d6', '#006cbe']
        
    for idx, (i, row) in enumerate(data.iterrows()):
        values = row[metrics].values.flatten().tolist()
        values = values + [values[0]]
        ax.plot(theta, values, linewidth=1.0, linestyle='solid', label=row['Alternative'], marker='o', markersize=6, color=color_palette[idx % len(color_palette)])
        # ax.fill(theta, values, alpha=0.50, color=color_palette[idx % len(color_palette)])
    
    plt.yticks(yticks_value, yticks_name, color="black", size=8)
    plt.xticks(theta, metrics + [metrics[0]], color='black', size=8)
    plt.legend() 
    return fig


data_frame1 = pd.read_csv("C:\\Nohora\\UniValle_project\\pasto_case\\results\\result_AHP1.csv")
df1 = data_frame1.copy()
df1 = df1.drop(['Sum'], axis=1)
metrics = df1.columns[1:].tolist()

data_frame2 = pd.read_csv("C:\\Nohora\\UniValle_project\\pasto_case\\results\\result_AHP2.csv")
df2 = data_frame2.copy()
df2 = df2.drop(['Sum'], axis=1)

data_frame3 = pd.read_csv("C:\\Nohora\\UniValle_project\\pasto_case\\results\\result_AHP3.csv")
df3 = data_frame3.copy()
df3 = df3.drop(['Sum'], axis=1)

data_frame4 = pd.read_csv("C:\\Nohora\\UniValle_project\\pasto_case\\results\\result_AHP4.csv")
df4 = data_frame4.copy()
df4 = df4.drop(['Sum'], axis=1)

yticks_value = [0, 0.02, 0.04, 0.06, 0.08]
yticks_name = ["0", "0.02", "0.04", "0.06", "0.08"]
fig = plot_radar_chart(df1, metrics, '', yticks_value, yticks_name)
plt.savefig("C:\\Nohora\\UniValle_project\\pasto_case\\results\\index1")
plt.show()

yticks_value = [0, 0.075, 0.15, 0.225, 0.3]
yticks_name = ["0", "0.075", "0.15", "0.225", "0.3"]
fig = plot_radar_chart(df2, metrics, '', yticks_value, yticks_name)
plt.savefig("C:\\Nohora\\UniValle_project\\pasto_case\\results\\index2")
plt.show()

yticks_value = [0, 0.0225, 0.045, 0.0675, 0.09]
yticks_name = ["0", "0.0225", "0.045", "0.0675", "0.09"]
fig = plot_radar_chart(df3, metrics, '', yticks_value, yticks_name)
plt.savefig("C:\\Nohora\\UniValle_project\\pasto_case\\results\\index3")
plt.show()

yticks_value = [0, 0.0225, 0.045, 0.0675, 0.09]
yticks_name = ["0", "0.0225", "0.045", "0.0675", "0.09"]
fig = plot_radar_chart(df4, metrics, '', yticks_value, yticks_name)
plt.savefig("C:\\Nohora\\UniValle_project\\pasto_case\\results\\index4")
plt.show()