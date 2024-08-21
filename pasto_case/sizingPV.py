def power_generated(area_available):
    # https://autosolar.co/paneles-solares-24v/panel-solar-550w-24v-monocristalino-ja-solar 
    powerPanelPV = 550
    areaPanelPV = 3 

    hps = 3.5 #valited in Pasto city

    numberPanelPV = m.ceil(area_available / areaPanelPV)
    powerPlantPV = numberPanelPV * 0.9 * powerPanelPV * hps
    return round(powerPlantPV), numberPanelPV

def print_power_generated(place, power):
    print(f'Power generated in {place} = {power[0]} Wh/dia con {power[1]} paneles PV')

if __name__ == '__main__':
    import numpy as np
    import math as m

    print_power_generated('CC Unico', power_generated(4800))
    print_power_generated('Alkosto parque Bolivar' , power_generated(1500))
    print_power_generated('CC Sebastian' , power_generated(430))
    print_power_generated('Alkosto centro' , power_generated(830))
    print_power_generated('Comfamiliar centro' , power_generated(550))

    print_power_generated('Udenar' , power_generated(1480))
