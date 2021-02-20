import pandas as pd
import datetime as dtime

archivoCSV = pd.read_csv("Precio-Nafta/precios-historicos.csv")
dataFrame = pd.DataFrame(archivoCSV)

# Seleccionamos columnas útiles, filtramos por "YPF", modificamos la fecha para
# no incluir tiempo y asignamos tipos de datos
columnasUtiles = ["provincia","producto","precio","fecha_vigencia",
    "empresabandera"]
dataFrame = dataFrame[columnasUtiles]
df_YPF = dataFrame[dataFrame["empresabandera"] == "YPF"]
df_YPF["fecha_vigencia"] = [fecha[0:10] for fecha \
    in df_YPF["fecha_vigencia"]]
df_YPF = df_YPF.convert_dtypes()

#print(df_YPF.info())
#print(df_YPF.describe().apply(lambda s: s.apply('{0:.2f}'.format)))
#
# .apply(lambda s: s.apply('{0:.2f}'.format)) permitirá mostrar el resultado del
# .describe() en formato decimal redondeado a 2 decimales

# .describe() con la función "max" mostró que hay uno o más valores anormales
# en la columna"precios"

# Buscando todos los valores anormales, en este caso cualquier valor 
# por encima de 100

print(df_YPF[df_YPF["precio"] > 100])
a = (df_YPF.index[df_YPF["precio"] > 100]).index.tolist()
print(a)
def div_100(x) :
    if (x > 100) :
        (x / 100)

df_YPF["precio"] = [div_100(x) for x in df_YPF["precio"]]

#print(df_YPF.loc[["1","2","3"]])

#df_YPF["precios"] = [ x for x in df_YPF[df_YPF["precio"] > 100]]

df_YPF = df_YPF[["precio","fecha_vigencia"]]
#df_YPF["fecha_vigencia"] = [fecha[0:10] for fecha in \
#    df_YPF["fecha_vigencia"]]
#print(df_YPF)
