import requests

# Configura tu API key de GraphHopper
GH_API_KEY = "75c75bed-7113-4289-be7d-9f930f99e418"

# Función para obtener las coordenadas geográficas de una ciudad
def obtener_coordenadas(ciudad):
    url = f"https://nominatim.openstreetmap.org/search?format=json&city={ciudad}&country=Chile"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and data:
        # Seleccionar la primera coincidencia y obtener las coordenadas
        latitud = data[0]['lat']
        longitud = data[0]['lon']
        return latitud, longitud
    else:
        raise ValueError("No se pudieron obtener las coordenadas de la ciudad.")

# Función para obtener la distancia y duración del viaje entre dos ciudades
def obtener_datos_viaje(origen, destino):
    origen_lat, origen_lon = obtener_coordenadas(origen)
    destino_lat, destino_lon = obtener_coordenadas(destino)

    url = f"https://graphhopper.com/api/1/route?point={origen_lat},{origen_lon}&point={destino_lat},{destino_lon}&vehicle=car&locale=es&key={GH_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and 'paths' in data:
        path = data['paths'][0]
        distancia_km = path['distance'] / 1000.0  # Convertir de metros a kilómetros
        duracion_segundos = path['time'] / 1000.0  # Convertir de milisegundos a segundos
        return distancia_km, duracion_segundos
    else:
        error_message = data.get('message', 'No se pudo obtener la ruta.')
        raise ValueError(f"Error de la API: {error_message}")

# Función para calcular el consumo de combustible
def calcular_combustible(distancia_km, consumo_por_km=0.08):
    # Suponemos un consumo promedio de 8 litros cada 100 km (0.08 litros por km)
    return distancia_km * consumo_por_km

# Función principal
def main():
    while True:
        origen = input("Ingrese la Ciudad de Origen (o 'q' para salir): ").strip()
        if origen.lower() == 'q':
            print("Saliendo del programa.")
            break
        destino = input("Ingrese la Ciudad de Destino (o 'q' para salir): ").strip()
        if destino.lower() == 'q':
            print("Saliendo del programa.")
            break

        try:
            distancia_km, duracion_segundos = obtener_datos_viaje(origen, destino)
            duracion_horas = int(duracion_segundos // 3600)
            duracion_minutos = int((duracion_segundos % 3600) // 60)
            duracion_restante_segundos = int(duracion_segundos % 60)
            combustible_litros = calcular_combustible(distancia_km)

            print(f"\nDistancia entre {origen} y {destino}: {distancia_km:.2f} km")
            print(f"Duración del viaje: {duracion_horas} horas, {duracion_minutos} minutos y {duracion_restante_segundos} segundos")
            print(f"Combustible requerido: {combustible_litros:.2f} litros\n")

        except ValueError as e:
            print(e)
        except Exception as e:
            print("Error al obtener los datos del viaje:", e)

if __name__ == "__main__":
    main()
