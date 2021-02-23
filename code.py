###############
# En este trabajo se busca analizar la base de datos de precios de los 
# combustibles de Argentina 2017-2021, en particular de la nafta súper, 
# con el objetivo de determinar un índice de inflación.
# El dataset empleado tiene fecha de actualización 15/02/2021.
###############

import pandas as pd

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

###########
# Experimento tiempo
###########

import pandas as pd
#dt1 = pd.to_datetime("2017-01")
#dt2 = pd.to_datetime("2021-02")
#print(dt2-dt1)
dt4 = pd.date_range(start="2017-01",end="2017-03",freq="MS",closed="left")
#print(dt4)
dt3 = [(pd.date_range(start=fecha,periods=1,freq="D")) for fecha in dt4]
#print(dt3)
dt5 = [item for sublist in dt3 for item in sublist]
print(dt5)
dt6= dt5[0]
print(dt6)
print(dt4-dt6)
#start_date = datetime.date(2019, 9 , 30)
#number_of_days = 12
#date_list = [(start_date + datetime.timedelta(days = day)).isoformat() for day in range(number_of_days)]

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