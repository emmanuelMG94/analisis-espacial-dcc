import sys
import geopandas as gpd
import libpysal
from libpysal.weights import Queen
from esda.moran import Moran

REFERENCIAS = {
    "CRIME": 0.50,
    "HOVAL": 0.18,
}
TOLERANCIA = 0.05

def validar():
    print("=== Validacion del experimento: Moran's I - Columbus, OH ===")
    print()

    ruta = libpysal.examples.get_path("columbus.shp")
    gdf = gpd.read_file(ruta)
    assert len(gdf) == 49, "Se esperaban 49 observaciones"
    print("[OK] Dataset cargado:", len(gdf), "observaciones")

    w = Queen.from_dataframe(gdf, use_index=False)
    w.transform = "r"

    todo_ok = True
    for variable, valor_ref in REFERENCIAS.items():
        y = gdf[variable].values
        moran = Moran(y, w)
        diferencia = abs(moran.I - valor_ref)
        estado = "OK" if diferencia <= TOLERANCIA else "FALLO"
        if diferencia > TOLERANCIA:
            todo_ok = False
        print("[" + estado + "]", variable, "Moran I =", round(moran.I, 4), "referencia", valor_ref, "diferencia", round(diferencia, 4))

    print()
    if todo_ok:
        print("=== VALIDACION EXITOSA: el experimento es reproducible ===")
    else:
        print("=== VALIDACION FALLIDA: revisar resultados ===")
    return todo_ok

if __name__ == "__main__":
    sys.exit(0 if validar() else 1)
