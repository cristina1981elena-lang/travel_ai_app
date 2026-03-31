import json

def cargar_destinos():
    with open("data/destinos.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)

def recomendar_destinos(presupuesto, tipo_viaje):
    destinos = cargar_destinos()
    resultados = []

    for destino in destinos:
        puntuacion = 0

        if tipo_viaje in destino["tipo"]:
            puntuacion += 2

        if destino["precio_vuelo"] <= presupuesto:
            puntuacion += 1

        resultados.append({
            "ciudad": destino["ciudad"],
            "pais": destino["pais"],
            "precio_vuelo": destino["precio_vuelo"],
            "puntuacion": puntuacion
        })

    resultados.sort(key=lambda x: x["puntuacion"], reverse=True)

    return resultados[:3]