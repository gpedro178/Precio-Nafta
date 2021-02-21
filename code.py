###############
# En este trabajo se busca analizar la base de datos de precios de los 
# combustibles de Argentina 2017-2021, en particular de la nafta súper, 
# con el objetivo de determinar un índice de inflación.
# El dataset empleado tiene fecha de actualización 15/02/2021.
###############

import pandas as pd

archivoCSV = pd.read_csv("Precio-Nafta/precios-historicos.csv")
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

#print(df_YPF.info())
#print(df_YPF.describe().apply(lambda s: s.apply('{0:.2f}'.format)))

# .apply(lambda s: s.apply('{0:.2f}'.format)) permitirá mostrar el resultado del
# .describe() en formato decimal redondeado a 2 decimales

# .describe() con la función "max" mostró que hay uno o más valores anormales
# en la columna "precios"

# Buscando todos los valores anormales, en este caso cualquier valor "precio"
# por encima de 100 se considera anormal
#print(df_YPF[df_YPF["precio"] > 100])
#indiceErrorPrecios = (df_YPF[df_YPF["precio"] > 100]).index

# Función para corregir el error decimal en la tabla
def div_100(x) :
    if (x > 100) :
        return (x / 100)
    else :
        return x
# Reemplazando valores erroneos con la función
df_YPF["precio"] = [div_100(x) for x in df_YPF["precio"]]

# Revisando corrección (requiere remover "#" de la línea 35)
#print(df_YPF.loc[indiceErrorPrecios])

df_YPF = df_YPF[["precio","fecha_vigencia","producto"]]

# Traduciendo fecha para Python con to_datetime de Pandas
df_YPF["fecha_vigencia"] = pd.to_datetime(df_YPF["fecha_vigencia"])

# Eliminando fechas inferiores a 2017-01-01 y superiores a 2021-02-15 
indiceErrorFechas = (df_YPF[ \
    (df_YPF["fecha_vigencia"] < "2017-01-01") | \
    (df_YPF["fecha_vigencia"] > "2021-02-15") \
        ]).index

df_YPF = df_YPF.drop(indiceErrorFechas)


####### FOR LATER, serie de datos bastante mala

#df_YPF = df_YPF[["precio","fecha_vigencia","producto","provincia"]]
#df_YPF = df_YPF[df_YPF["producto"]=="Nafta (súper) entre 92 y 95 Ron"]
#df_YPF = df_YPF[df_YPF["provincia"]=="CORDOBA"]
#df_YPF = df_YPF[["precio","fecha_vigencia"]]
# Traduciendo fecha para Python con to_datetime de Pandas
#df_YPF["fecha_vigencia"] = pd.to_datetime(df_YPF["fecha_vigencia"])

# Eliminando fechas inferiores a 2017-01-01 y superiores a 2021-02-15 
#indiceErrorFechas = (df_YPF[ \
#    (df_YPF["fecha_vigencia"] < "2017-01-01") | \
#    (df_YPF["fecha_vigencia"] > "2021-02-15") \
#        ]).index

#df_YPF = df_YPF.drop(indiceErrorFechas)
#df_YPF = df_YPF.groupby(["fecha_vigencia"]).max()
#df_YPF = df_YPF.groupby(df_YPF["fecha_vigencia"].dt.to_period("m")).max()
#print(df_YPF)
#df_YPF.plot(x="fecha_vigencia", y="precio")