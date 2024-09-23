def power_generated(area_available):
    # https://autosolar.co/paneles-solares-24v/panel-solar-550w-24v-monocristalino-ja-solar 
    powerPanelPV = 550
    areaPanelPV = 3 

    hps = 3.5 #valited in Pasto city

    numberPanelPV = m.ceil(area_available / areaPanelPV)
    powerPlantPV = numberPanelPV * 0.9 * powerPanelPV * hps / 1000
    return round(powerPlantPV), numberPanelPV

def sizing_battery_system(powerPlantPV):
    autonomy_days = 20/24
    nominal_voltage = 24 # https://autosolar.co/paneles-solares-24v/panel-solar-550w-24v-monocristalino-ja-solar 
    discharge_depth = 0.7 
    batCapacity = (powerPlantPV)* autonomy_days * nominal_voltage / (nominal_voltage * discharge_depth)
    Cbat = 60.6 # https://www.solarrun.com.au/wp-content/uploads/2022/09/Alpha-ESS-Datasheet.pdf
    num_batteries = batCapacity / Cbat
    return round(batCapacity), round(num_batteries)

def print_power_generated(place, power):
    print(f'Power generated in {place} = {power[0]} kWh/day with {power[1]} PV.')

def print_power_stored(place, power):
    print(f'Power stored in {place} = {power[0]} kWh with {power[1]} batteries.')

if __name__ == '__main__':
    import numpy as np
    import math as m

    print('\nCentros Comerciales\n')
    print_power_generated('CC Unico', power_generated(4800))
    print_power_generated('Alkosto parque Bolivar' , power_generated(1500))
    print_power_generated('CC Sebastian' , power_generated(430))
    print_power_generated('Alkosto centro' , power_generated(830))
    print_power_generated('Comfamiliar centro' , power_generated(550))
    print('\nCentros Educativos\n')
    print_power_generated('Udenar torobajo' , power_generated(1480))
    print_power_generated('Udenar Vipri' , power_generated(760))
    print_power_generated('Liceo Udenar' , power_generated(235))
    print_power_generated('Unimar' , power_generated(294))
    print_power_generated('Udenar Alvernia' , power_generated(968))
    print_power_generated('Sena' , power_generated(595))
    print('\nCentros de Salud\n')
    print_power_generated('Hospital Departamental' , power_generated(874))
    print_power_generated('Hospital San Pedro' , power_generated(2081))
    print('\nParqueaderos públicos\n')
    print_power_generated('Terminal' , power_generated(1027))
    print_power_generated('Centro1' , power_generated(258))
    print_power_generated('Centro2' , power_generated(249))
    print_power_generated('Centro3' , power_generated(448))
    print('\nOtros\n')
    print_power_generated('Alcaldía Anganoy' , power_generated(1190))
    print_power_generated('Alcaldía Centro' , power_generated(320))
    print_power_generated('Policia Centro' , power_generated(370))
    print_power_generated('Ingeominas' , power_generated(214))
    print_power_generated('Corponariño' , power_generated(345))

    print('\nBanco de baterías\n')
    print('\nCentros Comerciales\n')
    print_power_stored('CC Unico', sizing_battery_system(power_generated(4800)[0]))
    print_power_stored('Alkosto parque Bolivar' , sizing_battery_system(power_generated(1500)[0]))
    print_power_stored('CC Sebastian' , sizing_battery_system(power_generated(430)[0]))
    print_power_stored('Alkosto centro' , sizing_battery_system(power_generated(830)[0]))
    print_power_stored('Comfamiliar centro' , sizing_battery_system(power_generated(550)[0]))
    print('\nCentros Educativos\n')
    print_power_stored('Udenar torobajo' , sizing_battery_system(power_generated(1480)[0]))
    print_power_stored('Udenar Vipri' , sizing_battery_system(power_generated(760)[0]))
    print_power_stored('Liceo Udenar' , sizing_battery_system(power_generated(235)[0]))
    print_power_stored('Unimar' , sizing_battery_system(power_generated(294)[0]))
    print_power_stored('Udenar Alvernia' , sizing_battery_system(power_generated(968)[0]))
    print_power_stored('Sena' , sizing_battery_system(power_generated(595)[0]))
    print('\nCentros de Salud\n')
    print_power_stored('Hospital Departamental' , sizing_battery_system(power_generated(874)[0]))
    print_power_stored('Hospital San Pedro' , sizing_battery_system(power_generated(2081)[0]))
    print('\nParqueaderos públicos\n')
    print_power_stored('Terminal' , sizing_battery_system(power_generated(1027)[0]))
    print_power_stored('Centro1' , sizing_battery_system(power_generated(258)[0]))
    print_power_stored('Centro2' , sizing_battery_system(power_generated(249)[0]))
    print_power_stored('Centro3' , sizing_battery_system(power_generated(448)[0]))
    print('\nOtros\n')
    print_power_stored('Alcaldía Anganoy' , sizing_battery_system(power_generated(1190)[0]))
    print_power_stored('Alcaldía Centro' , sizing_battery_system(power_generated(320)[0]))
    print_power_stored('Policia Centro' , sizing_battery_system(power_generated(370)[0]))
    print_power_stored('Ingeominas' , sizing_battery_system(power_generated(214)[0]))
    print_power_stored('Corponariño' , sizing_battery_system(power_generated(345)[0]))