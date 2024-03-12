import randomTrips

python randomTrips.py -n pasto_network.net.xml -e 520 --vehicle-class bus --prefix B -o bus.trips.xml
python randomTrips.py -n pasto_network.net.xml -e 3200 --vehicle-class passenger --prefix T -o taxi.trips.xml
python randomTrips.py -n pasto_network.net.xml -e 6200 --vehicle-class passenger --prefix P -o vehicle.trips.xml
python randomTrips.py -n pasto_network.net.xml -e 125000 --vehicle-class motorcycle --prefix M -o moto.trips.xml