import matplotlib.pyplot as plt

def normalize_list(list):
    xmin = min(list)
    xmax = max(list)
    for i, x in enumerate(list):
        list[i] = (x - xmin) / (xmax - xmin)
    return list

def plot_list(list, axis_x, title, x_label, y_label):
    plt.plot(axis_x, list)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(True)
    plt.show()

def plot_group_list(lists, axis_x, legends, title, x_label, y_label):
    for i, x in lists:
        plt.plot(axis_x, x, label=legends[i])
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(True)
    plt.show()

def total_value_list(list, multiplier):
    list_multiplier = []
    for i in range(len(list)):
        list_multiplier.append(list[i] * multiplier)
    return list_multiplier

hour = list(range(1,25,1))

# http://www.scielo.org.co/scielo.php?script=sci_arttext&pid=S1657-42062015000200001
demanda_base_normalizada = [ 0.56, 0.50, 0.49, 0.48, 0.53, 0.67, 0.71, 0.71, 0.76, 0.80, 0.82, 0.84, 
                        0.80, 0.79, 0.80, 0.79, 0.79, 0.96, 1.00, 0.95, 0.88, 0.78, 0.69, 0.63 ]

pico_demanda_base = 1 #kWh -> Tomado de datos XM
demanda_base = total_value_list(demanda_base_normalizada, pico_demanda_base)
plot_list(demanda_base, hour, 'Perfil de demanda base', 'Hora', 'kWh')

demand_L1_h_normalizada = normalize_list([0.5, 0.45, 0.32, 0.25, 0.12, 0.05, 0.15, 0.29, 0.38, 0.47, 0.58, 0.675, 0.74, 0.812, 0.92, 0.835, 0.751, 0.69, 0.57, 0.42, 0.37, 0.26, 0.25, 0.24]) # curva L1 at home
demand_L1_w_normalizada = normalize_list([0.0, 0.0, 0.0, 0.0, 0.0, 0.35, 0.5, 0.69, 0.8, 0.87, 0.8, 0.75, 0.4, 0.3, 0.15, 0.05, 0.01, 0,0,0,0,0,0,0]) # curva L1 workplace
demand_L2_normalizada = normalize_list([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.03, 0.05, 0.25, 0.35, 0.5, 0.59, 0.52, 0.4, 0.35, 0.4, 0.6, 0.69, 0.8, 0.87, 0.75, 0.4, 0.1, 0.0])#curva L2 shopping mall
demand_L3_normalizada = normalize_list([0.05, 0.07, 0.08, 0.09, 0.150, 0.261, 0.273, 0.315, 0.425, 0.535, 0.55, 0.59, 0.52, 0.4, 0.35, 0.4, 0.6, 0.79, 0.9, 1, 0.85, 0.4, 0.1, 0.05])

demand_L1_h = total_value_list(demand_L1_h_normalizada, multiplier=45794/2)
demand_L1_w = total_value_list(demand_L1_w_normalizada, multiplier=45794/2)
demand_L2 = total_value_list(demand_L2_normalizada, multiplier=35732)
demand_L3 = total_value_list(demand_L3_normalizada, multiplier=62742)
demand_per_type_charge = [demand_L1_h, demand_L1_w, demand_L2, demand_L3]
legends = ['L1 residencial', 'L2 oficina', 'L3', 'L4']
plot_group_list(demand_per_type_charge, hour, legends, 'Perfil demanda VE por tipo de carga', 'Hora', 'kWh')