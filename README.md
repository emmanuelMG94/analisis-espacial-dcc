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

## 5. Como reproducir el experimento

Requisitos: Docker Desktop instalado y corriendo.

Construir la imagen:
    docker build -t geoanalysis-cli:dcc .

Ejecutar el analisis principal:
    docker run --rm -v ${PWD}/output:/app/output geoanalysis-cli:dcc

Los resultados se muestran en consola y se exportan a
output/resultados_moran.csv en tu maquina local.

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

## 8. Instrucciones para revision por pares

Un companero puede reproducir este experimento de dos formas:

Opcion A - Clonando el repositorio:
    git clone https://github.com/USUARIO/analisis-espacial-dcc.git
    cd analisis-espacial-dcc
    docker build -t geoanalysis-cli:dcc .
    docker run --rm geoanalysis-cli:dcc

Opcion B - Usando la imagen publicada en Docker Hub (mas rapido):
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
