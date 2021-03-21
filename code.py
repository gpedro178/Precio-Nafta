###############
# En este trabajo se busca analizar la base de datos de precios de los 
# combustibles de Argentina 2017-2021, en particular de la nafta súper, 
# con el objetivo de determinar un índice de inflación.
# El dataset empleado tiene fecha de actualización 15/02/2021.
###############

import pandas as pd
import matplotlib.pyplot as plt

archivoCSV = pd.read_csv("/home/gpedro/Curso_Python/Precio-Nafta/precios-historicos.csv")
dataFrame = pd.DataFrame(archivoCSV)

# Seleccionamos columnas útiles, filtramos por "YPF", asignamos tipos de datos 
# y modificamos la fecha para no incluir hora 
columnasUtiles = ["provincia","producto","precio","fecha_vigencia",
    "empresabandera"]
dataFrame = dataFrame[columnasUtiles]
df_YPF = dataFrame[dataFrame["empresabandera"] == "YPF"]
df_YPF = df_YPF.convert_dtypes()
df_YPF["fecha_vigencia"] = [fecha[0:10] for fecha \
    in df_YPF["fecha_vigencia"]]

# Creando un .CSV menos pesado para subir a Repl.it
#df_YPF.to_csv("data_Reducida.csv",index=False)

#print(df_YPF.info())
#print(df_YPF.describe().apply(lambda s: s.apply('{0:.2f}'.format)))

# .apply(lambda s: s.apply('{0:.2f}'.format)) permitirá mostrar el resultado del
# .describe() en formato decimal redondeado a 2 decimales

# .describe() con la función "max" mostró que hay uno o más valores anormales
# en la columna "precios"

#################
# Buscando los Valores Anormales
#################

# En este caso cualquier valor "precio"
# por encima de 100 o menor a 5 se considerará anormal

indiceErrorPrecios = (df_YPF[ \
    (df_YPF["precio"] > 100) | \
    (df_YPF["precio"] < 5) \
        ]).index

#print(df_YPF.loc[indiceErrorPrecios])

df_YPF = df_YPF.drop(indiceErrorPrecios)

# Traduciendo fecha para Python con to_datetime de Pandas
df_YPF["fecha_vigencia"] = pd.to_datetime(df_YPF["fecha_vigencia"])

# Eliminando fechas inferiores a 2017-01-01 y superiores a 2021-02-15 debido 
# a que la serie no debería tener valores en esos rangos.
indiceErrorFechas = (df_YPF[ \
    (df_YPF["fecha_vigencia"] < "2017-01-01") | \
    (df_YPF["fecha_vigencia"] > "2021-02-15") \
        ]).index

df_YPF = df_YPF.drop(indiceErrorFechas)

# Aparentemente hay estaciones de servicio usando el formato dd-mm-yyyy y hay
# otras utilizando el formato mm-dd-yyyy, lo que causa errores en la serie, 
# se eliminarán los primeros 12 días para corregir este problema.

auxiliarFechas = pd.date_range(start="2017-01",end="2021-03",freq="D",closed="left")

listaFechasParaBorrar = []
for dia in auxiliarFechas:
    if dia.day <= 12:
        listaFechasParaBorrar.append(dia)

listaFechasParaBorrar = pd.to_datetime(listaFechasParaBorrar)

indiceFechasParaBorrar = (df_YPF[df_YPF["fecha_vigencia"]\
    .isin(listaFechasParaBorrar)\
        ]).index

df_YPF = df_YPF.drop(indiceFechasParaBorrar)

# Filtramos por Nafta Súper y por Prov de BS AS
df_YPF = df_YPF[["precio","fecha_vigencia","producto","provincia"]]
df_YPF_NS = df_YPF[df_YPF["producto"]=="Nafta (súper) entre 92 y 95 Ron"]
df_YPF_NS_BSAS = df_YPF_NS[df_YPF_NS["provincia"]=="BUENOS AIRES"]

# Tomamos solo columnas precio y fecha
df_YPF_NS_BSAS = df_YPF_NS_BSAS[["precio","fecha_vigencia"]]

# Agrupamos precios por fechas tomando el máximo de cada fecha para intentar 
# disminuir el error de carga de datos de las estaciones de servicio
df_YPF_NS_BSAS = df_YPF_NS_BSAS.groupby(["fecha_vigencia"]).max()

#print(df_YPF_NS_BSAS)

# Gráfico preliminar de la serie
df_YPF_NS_BSAS.plot()

# Gráfico con nuevo formato
plt.style.use("bmh")

fig, axs = plt.subplots(figsize=(10, 4))

df_YPF_NS_BSAS.plot.line(ax=axs, lw=1)

axs.set_ylabel("Precio por Litro")
axs.set_xlabel("Fecha de Lectura")
axs.set_title("Nafta Súper YPF", fontsize=18)

plt.show()