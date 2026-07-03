import geopandas as gpd
import libpysal
from libpysal.weights import Queen
from esda.moran import Moran
from datetime import datetime
import os

def analizar_variable(gdf, w, nombre_var):
    y = gdf[nombre_var].values
    moran = Moran(y, w)
    stats = gdf[nombre_var].describe()

    n = int(stats['count'])
    media = stats['mean']
    std = stats['std']
    varianza = gdf[nombre_var].var()
    minimo = stats['min']
    mediana = stats['50%']
    maximo = stats['max']
    rango = maximo - minimo
    cv = (std / media) * 100

    print(f'--- Estadisticas descriptivas: {nombre_var} ---')
    print(f'  n:                {n}')
    print(f'  media:            {media:.4f}')
    print(f'  desviacion std:   {std:.4f}')
    print(f'  varianza:         {varianza:.4f}')
    print(f'  minimo:           {minimo:.4f}')
    print(f'  mediana (Q2):     {mediana:.4f}')
    print(f'  maximo:           {maximo:.4f}')
    print(f'  rango:            {rango:.4f}')
    print(f'  coef. variacion:  {cv:.2f}%')
    print()

    print(f'--- Indice de Moran I: {nombre_var} ---')
    print(f'  Moran I:          {moran.I:.4f}')
    print(f'  Valor esperado:   {moran.EI:.4f}')
    print(f'  z-score:          {moran.z_sim:.4f}')
    print(f'  p-valor (sim):    {moran.p_sim:.4f}')

    if moran.p_sim < 0.05:
        interp = 'Existe autocorrelacion espacial estadisticamente significativa.'
    else:
        interp = 'No hay evidencia suficiente de autocorrelacion espacial.'
    print(f'  Interpretacion:   {interp}')
    print()

    return {
        'variable': nombre_var,
        'n': n,
        'media': media,
        'std': std,
        'varianza': varianza,
        'minimo': minimo,
        'mediana': mediana,
        'maximo': maximo,
        'rango': rango,
        'coef_variacion': cv,
        'moran_i': moran.I,
        'valor_esperado': moran.EI,
        'z_score': moran.z_sim,
        'p_valor': moran.p_sim,
        'interpretacion': interp,
    }

def main():
    inicio = datetime.now()
    print('=== Analisis de Autocorrelacion Espacial - Columbus, OH ===')
    print(f'Fecha de ejecucion: {inicio.strftime("%Y-%m-%d %H:%M:%S")}')
    print()

    ruta = libpysal.examples.get_path('columbus.shp')
    gdf = gpd.read_file(ruta)
    print(f'Observaciones cargadas: {len(gdf)}')
    print(f'Variables disponibles: {list(gdf.columns)}')
    print()

    w = Queen.from_dataframe(gdf, use_index=False)
    w.transform = 'r'
    print(f'Matriz de pesos espaciales: Queen contiguity, {w.n} unidades, {w.mean_neighbors:.2f} vecinos promedio')
    print()

    resultados = []
    resultados.append(analizar_variable(gdf, w, 'CRIME'))
    resultados.append(analizar_variable(gdf, w, 'HOVAL'))

    print('=== Comparacion entre variables ===')
    print(f'{"Variable":<10} {"Moran I":<10} {"p-valor":<10} {"Significativo":<15}')
    for r in resultados:
        sig = 'Si' if r['p_valor'] < 0.05 else 'No'
        print(f'{r["variable"]:<10} {r["moran_i"]:<10.4f} {r["p_valor"]:<10.4f} {sig:<15}')
    print()

    os.makedirs('/app/output', exist_ok=True)
    ruta_csv = '/app/output/resultados_moran.csv'
    with open(ruta_csv, 'w') as f:
        f.write('variable,n,media,std,varianza,minimo,mediana,maximo,rango,coef_variacion,moran_i,valor_esperado,z_score,p_valor,interpretacion\n')
        for r in resultados:
            linea = f'{r["variable"]},{r["n"]},{r["media"]:.4f},{r["std"]:.4f},{r["varianza"]:.4f},{r["minimo"]:.4f},{r["mediana"]:.4f},{r["maximo"]:.4f},{r["rango"]:.4f},{r["coef_variacion"]:.2f},{r["moran_i"]:.4f},{r["valor_esperado"]:.4f},{r["z_score"]:.4f},{r["p_valor"]:.4f},{r["interpretacion"]}\n'
            f.write(linea)

    fin = datetime.now()
    duracion = (fin - inicio).total_seconds()
    print(f'Resultados exportados a: {ruta_csv}')
    print(f'Duracion total: {duracion:.2f} segundos')
    print('=== Fin del analisis ===')

if __name__ == '__main__':
    main()