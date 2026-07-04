# Analisis de Autocorrelacion Espacial - Moran's I (Entorno Contenerizado)

**Autor:** Emmanuel Morales Garcia
**Curso:** Contenerizacion de Aplicaciones - Doctorado en Ciencias de la Computacion, UV
**Unidad 3 - Implementacion de un entorno contenerizado**

---

## 0. Justificacion: por que este problema se resuelve con contenedores

El analisis de autocorrelacion espacial depende de un stack de librerias
cientificas con dependencias binarias complejas: GDAL (base de GeoPandas),
PySAL y su sublibreria esda. Es comun que el mismo script produzca errores
distintos entre Windows, Linux o macOS por conflictos de version de GDAL a
nivel de sistema operativo.

Contenerizar este experimento resuelve:

1. Aislamiento de dependencias: la imagen fija exactamente las versiones de
   GeoPandas, PySAL, esda y GDAL usadas.
2. Reproducibilidad para revision por pares: un companero ejecuta el mismo
   experimento sin replicar manualmente el entorno de desarrollo.
3. Portabilidad: la imagen corre igual en cualquier equipo con Docker,
   sin importar el sistema operativo host.

## 1. Descripcion del experimento

Este proyecto ejecuta un analisis de autocorrelacion espacial (indice de
Moran I) sobre el dataset academico de Columbus, Ohio, comparando dos
variables: CRIME (criminalidad residencial) y HOVAL (valor de vivienda).
El experimento corre completamente en consola (sin interfaz web), lo que
lo hace ligero y facil de reproducir en cualquier equipo.

## 2. Metodologia

1. Se carga el dataset columbus.shp (incluido en libpysal).
2. Se construye una matriz de pesos espaciales de contiguidad tipo Queen.
3. Se calculan estadisticas descriptivas completas (media, desviacion,
   varianza, mediana, rango, coeficiente de variacion) para CRIME y HOVAL.
4. Se calcula el indice de Moran I para cada variable.
5. Se comparan los resultados entre ambas variables.
6. Se exportan los resultados a un archivo CSV.

## 3. Arquitectura del entorno contenerizado

Un solo contenedor basado en python:3.11-slim, con GeoPandas, PySAL y esda
instalados. No requiere red, puertos ni base de datos externa: es
autocontenido y corre con un solo comando.

## 4. Disponibilidad de datos de entrada

El dataset (Columbus, Ohio, 49 observaciones) es un dataset academico
estandar de estadistica espacial, distribuido dentro de la libreria
libpysal.examples. No requiere descarga externa ni credenciales.

## 5. Como ejecutarlo

Requisito unico: Docker Desktop instalado y corriendo.

### Opcion A - Sin clonar nada, directo desde Docker Hub (mas rapido)

    docker pull emmanuel94/geoanalysis-cli:dcc
    mkdir output
    docker run --rm -v ${PWD}/output:/app/output emmanuel94/geoanalysis-cli:dcc

### Opcion B - Clonando el repositorio y construyendo localmente

    git clone https://github.com/emmanuelMG94/analisis-espacial-dcc.git
    cd analisis-espacial-dcc
    docker build -t geoanalysis-cli:dcc .
    mkdir output
    docker run --rm -v ${PWD}/output:/app/output geoanalysis-cli:dcc

### Opcion C - Usando Docker Compose (si ya clonaste el repo)

    docker compose up --build

En cualquiera de las tres opciones, los resultados se muestran en consola
y se exportan a output/resultados_moran.csv en tu maquina local.

### Correr la validacion

    docker run --rm emmanuel94/geoanalysis-cli:dcc python validate.py

Debe finalizar con el mensaje "VALIDACION EXITOSA".

## 6. Validacion y pruebas

El script validate.py compara el indice de Moran I calculado contra
valores de referencia conocidos (CRIME ~0.50, HOVAL ~0.18), con una
tolerancia de 0.05.

Ejecucion:
    docker run --rm geoanalysis-cli:dcc python validate.py

Debe finalizar con el mensaje "VALIDACION EXITOSA".

## 7. Imagenes publicadas

Imagen publicada en Docker Hub bajo la cuenta emmanuel94:
- emmanuel94/geoanalysis-cli:dcc

Para desplegar sin reconstruir localmente:
    docker pull emmanuel94/geoanalysis-cli:dcc
    docker run --rm emmanuel94/geoanalysis-cli:dcc



Que debe verificar el revisor:
1. Que el analisis muestre 49 observaciones cargadas.
2. Que Moran I para CRIME sea aproximadamente 0.50 y para HOVAL
   aproximadamente 0.18.
3. Que docker run --rm geoanalysis-cli:dcc python validate.py termine
   con el mensaje "VALIDACION EXITOSA".

## 9. Estructura del repositorio

analisis-espacial/fase1-cli/
    README.md
    Dockerfile
    requirements.txt
    analisis.py
    validate.py
## 5b. Ejecucion con Docker Compose (alternativa)

Ademas de docker build / docker run, el proyecto incluye un
docker-compose.yml para levantar el experimento con un solo comando:

    docker compose up --build

Esto construye la imagen y ejecuta el analisis, generando el CSV en la
carpeta output/ del host, igual que con docker run.

## 10. Observables del experimento

En esta seccion describo que debe observar un companero al reproducir mi
experimento, distinguiendo entre resultados deterministicos (deben ser
identicos en cualquier ejecucion) y resultados estocasticos (varian
ligeramente entre ejecuciones por depender de simulaciones aleatorias).

### Observables deterministicos (deben coincidir exactamente)

| Observable | Contexto / que representa | Resultado esperado |
|---|---|---|
| Numero de observaciones | Filas del dataset Columbus, OH cargadas | 49 |
| Media de CRIME | Promedio de criminalidad residencial | 35.1288 |
| Media de HOVAL | Promedio de valor de vivienda | 38.4362 |
| Moran I de CRIME | Grado de autocorrelacion espacial de la criminalidad. Es un calculo directo sobre datos fijos con matriz de pesos Queen, no depende de aleatoriedad. | 0.5002 |
| Moran I de HOVAL | Grado de autocorrelacion espacial del valor de vivienda. Mismo tipo de calculo directo. | 0.1801 |
| Valor esperado bajo H0 (EI) | Valor teorico de Moran I si no existiera autocorrelacion espacial | -0.0208 |

Estos valores deben salirle identicos a cualquier companero, sin importar
su maquina o cuantas veces ejecute el experimento, porque son el resultado
de una formula matematica aplicada sobre datos que no cambian. Si a
alguien le sale un valor distinto en estos observables, es se al de un
error real de reproduccion (version de libreria distinta, dataset
corrupto, o algun cambio en mi codigo), no una variacion normal.

### Observables estocasticos (varian ligeramente entre ejecuciones)

| Observable | Contexto / que representa | Rango esperado |
|---|---|---|
| z-score de CRIME | Significancia estadistica del Moran I, calculada con un test de permutaciones aleatorias (999 simulaciones por defecto en esda) | Aproximadamente entre 4.5 y 6.0 |
| p-valor (p_sim) de CRIME | Probabilidad de que el patron espacial observado se deba al puro azar | Tipicamente 0.001 a 0.01 (siempre menor a 0.05, es decir, significativo) |
| z-score de HOVAL | Mismo test de permutaciones aplicado a HOVAL | Aproximadamente entre 1.8 y 2.5 |
| p-valor (p_sim) de HOVAL | Significancia estadistica de la autocorrelacion en HOVAL | Tipicamente 0.01 a 0.03 (significativo, pero mas debil que CRIME) |

Estos numeros cambian en cada corrida porque el test de significancia usa
permutaciones aleatorias de los datos (simulacion de Monte Carlo) para
estimar que tan improbable es el patron observado respecto al azar. Esta
variacion es esperada y no significa que algo este mal, mientras el valor
se mantenga dentro del rango razonable y la conclusion final (significativo
o no) no cambie.

Corri mi propio experimento varias veces para comprobar esto:

| Ejecucion | Moran I (CRIME) | z-score (CRIME) | p-valor (CRIME) |
|---|---|---|---|
| 1 | 0.5002 | 5.7496 | 0.0010 |
| 2 | 0.5002 | 5.6168 | 0.0010 |
| 3 | 0.5002 | 5.3680 | 0.0010 |
| 4 | 0.5002 | 5.6036 | 0.0010 |

Como se ve, mi Moran I se mantuvo identico en las cuatro corridas, mientras
que el z-score vario cada vez por la aleatoriedad de la simulacion, sin
que eso afectara la conclusion final del analisis.

### Reporte en el foro de debate:

1. El valor de Moran I que obtuvo para CRIME y HOVAL (debe coincidir con
   el que yo reporto arriba).
2. El z-score y p-valor que le salieron (pueden diferir un poco de los
   mios, y explico por que: son permutaciones aleatorias).
3. Si la conclusion final (existe o no existe autocorrelacion espacial
   significativa) le coincidio con la que yo reporte.
4. Cualquier diferencia en los observables deterministicos, indicando su
   sistema operativo y version de Docker, para que pueda investigar la
   causa.
