import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def plot_comparative(df):   
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].plot(df['Year'], df['DAC L1 case1'], label="DAC without energy cost", color="black")
    axes[0].plot(df['Year'], df['DAC L1 case2'], label="DAC with energy cost", color="#a4165f")
    axes[0].plot(df['Year'], df['DAC L1 case3'], label="DAC with energy cost - PV", color="#ea694e")
    axes[0].set_ylabel("Cost [USD]")
    axes[0].set_xlabel("Year")  
    axes[0].grid(True, linestyle="--", alpha=0.7)
    axes[0].legend()

    axes[1].plot(df['Year'], df['DAC L2 case1'], label="DAC without energy cost", color="black")
    axes[1].plot(df['Year'], df['DAC L2 case2'], label="DAC with energy cost", color="#a4165f")
    axes[1].plot(df['Year'], df['DAC L2 case3'], label="DAC with energy cost - PV", color="#ea694e")
    axes[1].set_title('L2')
    axes[1].set_xlabel("Year")  
    axes[1].grid(True, linestyle="--", alpha=0.7)
    axes[1].legend()

    axes[2].plot(df['Year'], df['DAC L3 case1'], label="DAC without energy cost", color="black")
    axes[2].plot(df['Year'], df['DAC L3 case2'], label="DAC with energy cost", color="#a4165f")
    axes[2].plot(df['Year'], df['DAC L3 case3'], label="DAC with energy cost - PV", color="#ea694e")
    axes[2].set_title('L3')
    axes[2].set_xlabel("Year")  
    axes[2].grid(True, linestyle="--", alpha=0.7)
    axes[2].legend()
    plt.tight_layout()
    plt.savefig('C:/Nohora/UniValle_project/pasto_case/results_netherlands/figures/dac_comparative.jpg')
    plt.close()

df_case1 = pd.read_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/cs_projections_Case1.csv')
plot_comparative(df_case1)