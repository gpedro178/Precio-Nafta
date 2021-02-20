import pandas as pd
import datetime as dtime

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
# en la columna"precios"

# Buscando todos los valores anormales, en este caso cualquier valor "precio"
# por encima de 100

#print(df_YPF[df_YPF["precio"] > 100])
#indiceError = (df_YPF[df_YPF["precio"] > 100]).index

# Función para corregir el error decimal en la tabla
def div_100(x) :
    if (x > 100) :
        return (x / 100)
    else :
        return x
# Reemplazando valores erroneos con la función
df_YPF["precio"] = [div_100(x) for x in df_YPF["precio"]]

# Revisando corrección (requiere remover "#" de la línea 30)
#print(df_YPF.loc[indiceError])

df_YPF = df_YPF[["precio","fecha_vigencia"]]
