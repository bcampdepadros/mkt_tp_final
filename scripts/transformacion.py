# # fact orders --> date, location, customer, store, channel

# # fact order items --> product, date, customer

# # fact shipments --> date, locations

# # fact web sessiones --> customer, date

# # fact nps --> customer, date, channel




# fact orders: sales_order  000

# fact order_items : sales_order, sales_order_items 000

# fact shipments : shipments  000

# fact web sessions : web_sessions   000

# fact nps : nps_response   000

# dim location : address, province 000

# dim customer : customer   000

# dim store : store   000

# dim channel : channel  000

# dim product : product, product_category 000

# dim date : calcular con python 

import pandas as pd

# 1 y 2: Carga el CSV de 'raw/' en la variable 'fact_orders'

fact_orders = pd.read_csv('raw/sales_order.csv')

# --- Adaptación de Fecha ---
# 2. Convertir 'order_date' a datetime
fact_orders['order_date'] = pd.to_datetime(fact_orders['order_date'], errors='coerce')

# 3. Crear la 'order_date_key' (formato YYYYMMDD como entero nullable)
fact_orders['order_date_key'] = fact_orders['order_date'].dt.strftime('%Y%m%d').astype('Int64')

# 4. (Recomendado) Eliminar la columna de fecha original
fact_orders = fact_orders.drop(columns=['order_date'])
# --- Fin Adaptación ---

# 3. Guarda la variable 'fact_orders' en la carpeta 'dw/'
fact_orders.to_csv('dw/fact_order.csv', index=False)


import os
# 1 y 2: Carga el CSV de 'raw/' en la variable 'fact_shipments'
fact_shipments = pd.read_csv('raw/shipment.csv')

# --- Adaptación de Fechas ---
# 2. Convertir ambas columnas a datetime
fact_shipments['shipped_at'] = pd.to_datetime(fact_shipments['shipped_at'], errors='coerce')
fact_shipments['delivered_at'] = pd.to_datetime(fact_shipments['delivered_at'], errors='coerce')

# 3. Crear las 'date_key' para ambas
fact_shipments['shipped_date_key'] = fact_shipments['shipped_at'].dt.strftime('%Y%m%d').astype('Int64')
fact_shipments['delivered_date_key'] = fact_shipments['delivered_at'].dt.strftime('%Y%m%d').astype('Int64')

# 4. (Recomendado) Eliminar las columnas originales
fact_shipments = fact_shipments.drop(columns=['shipped_at', 'delivered_at'])
# --- Fin Adaptación ---

# (Recomendado) Asegurarse de que la carpeta 'dw' exista
os.makedirs('dw', exist_ok=True)

# 3. Guarda la variable 'fact_shipments' en la carpeta 'dw/'
fact_shipments.to_csv('dw/fact_shipments.csv', index=False)


import os

# 1 y 2: Carga el CSV de 'raw/' en la variable 'web_sessions'
web_sessions = pd.read_csv('raw/web_session.csv')

# --- Adaptación de Fechas ---
# 2. Convertir ambas columnas a datetime
web_sessions['started_at'] = pd.to_datetime(web_sessions['started_at'], errors='coerce')
web_sessions['ended_at'] = pd.to_datetime(web_sessions['ended_at'], errors='coerce')

# 3. Crear las 'date_key' para ambas
web_sessions['started_date_key'] = web_sessions['started_at'].dt.strftime('%Y%m%d').astype('Int64')
web_sessions['ended_date_key'] = web_sessions['ended_at'].dt.strftime('%Y%m%d').astype('Int64')

# 4. (Recomendado) Eliminar las columnas originales
web_sessions = web_sessions.drop(columns=['started_at', 'ended_at'])
# --- Fin Adaptación ---

# (Recomendado) Asegurarse de que la carpeta 'dw' exista
os.makedirs('dw', exist_ok=True)

# 3. Guarda la variable 'web_sessions' en la carpeta 'dw/'
web_sessions.to_csv('dw/fact_web_sessions.csv', index=False)


import os

# 1 y 2: Carga el CSV de 'raw/' en la variable 'nps'
nps = pd.read_csv('raw/nps_response.csv')

# --- Adaptación de Fecha ---
# 2. Convertir 'responded_at' a datetime
nps['responded_at'] = pd.to_datetime(nps['responded_at'], errors='coerce')

# 3. Crear la 'responded_date_key'
nps['responded_date_key'] = nps['responded_at'].dt.strftime('%Y%m%d').astype('Int64')

# 4. (Recomendado) Eliminar la columna original
nps = nps.drop(columns=['responded_at'])
# --- Fin Adaptación ---

# (Recomendado) Asegurarse de que la carpeta 'dw' exista
os.makedirs('dw', exist_ok=True)

# 3. Guarda la variable 'nps' en la carpeta 'dw/'
nps.to_csv('dw/fact_nps.csv', index=False)



import os

# 1 y 2: Carga el CSV de 'raw/' en la variable 'customer'
customer = pd.read_csv('raw/customer.csv')

# (Recomendado) Asegurarse de que la carpeta 'dw' exista
os.makedirs('dw', exist_ok=True)

# 3. Guarda la variable 'customer' en la carpeta 'dw/'
customer.to_csv('dw/dim_customer.csv', index=False)



import os

# 1 y 2: Carga el CSV de 'raw/' en la variable 'store'
store = pd.read_csv('raw/store.csv')

# (Recomendado) Asegurarse de que la carpeta 'dw' exista
os.makedirs('dw', exist_ok=True)

# 3. Guarda la variable 'store' en la carpeta 'dw/'
store.to_csv('dw/dim_store.csv', index=False)




import os

# 1 y 2: Carga el CSV de 'raw/' en la variable 'channel'
channel = pd.read_csv('raw/channel.csv')

# (Recomendado) Asegurarse de que la carpeta 'dw' exista
os.makedirs('dw', exist_ok=True)

# 3. Guarda la variable 'channel' en la carpeta 'dw/'
channel.to_csv('dw/dim_channel.csv', index=False)


import os

# 1. Cargar los dos archivos CSV que se necesitan
orders = pd.read_csv('raw/sales_order.csv')
items = pd.read_csv('raw/sales_order_item.csv')

# --- Adaptación de Fecha (en la tabla 'orders' ANTES del merge) ---
# 2. Convertir 'order_date' a datetime
orders['order_date'] = pd.to_datetime(orders['order_date'], errors='coerce')

# 3. Crear la 'order_date_key'
orders['order_date_key'] = orders['order_date'].dt.strftime('%Y%m%d').astype('Int64')

# 4. Eliminar la columna de fecha original para no duplicar
orders_transformed = orders.drop(columns=['order_date'])
# --- Fin Adaptación ---

# 2. Crear 'fact_order_items' combinando los dos DataFrames
# Se usa 'order_id' como la columna en común.
# Se añaden las columnas de 'orders' a la tabla 'items'.
fact_order_items = pd.merge(items, orders, on='order_id', how='left')

# (Recomendado) Asegurarse de que la carpeta 'dw' exista
os.makedirs('dw', exist_ok=True)

# 3. Guardar la nueva tabla combinada en la carpeta 'dw/'
fact_order_items.to_csv('dw/fact_order_item.csv', index=False)



import os

# 1. Cargar los dos archivos CSV que se necesitan
addresses = pd.read_csv('raw/address.csv')
provinces = pd.read_csv('raw/province.csv')

# 2. Crear 'dim_location' combinando los dos DataFrames
# Se usa 'province_id' como la columna en común.
# 'how='left'' asegura que mantengamos todas las direcciones de 'address.csv'
# y les añadamos la información de 'province.csv' donde coincida.
dim_location = pd.merge(addresses, provinces, on='province_id', how='left')

# (Recomendado) Asegurarse de que la carpeta 'dw' exista
os.makedirs('dw', exist_ok=True)

# 3. Guardar la nueva tabla combinada en la carpeta 'dw/'
dim_location.to_csv('dw/dim_location.csv', index=False)



import os

# 1. Cargar los dos archivos CSV que se necesitan
products = pd.read_csv('raw/product.csv')
categories = pd.read_csv('raw/product_category.csv')

# --- 2. Preparar la tabla de categorías (El Self-Join) ---

# Renombramos 'name' en categorías para que sea claro
categories.rename(columns={'name': 'category_name'}, inplace=True)

# Creamos una "copia" de la tabla de categorías solo para los nombres de los padres.
# Esta tabla servirá como "diccionario" para buscar el nombre del 'parent_id'.
parent_names = categories[['category_id', 'category_name']].rename(columns={
    'category_id': 'parent_id',         # La usaremos para unir con 'parent_id'
    'category_name': 'parent_category_name' # El nombre que queremos obtener
})

# Unimos la tabla de categorías consigo misma (usando el 'parent_names' que creamos)
# para añadir el nombre del padre (parent_category_name).
categories_full = pd.merge(categories, parent_names, on='parent_id', how='left')

# --- 3. Crear dim_product ---

# Ahora unimos la tabla de productos con la tabla de categorías ya completada.
dim_product = pd.merge(products, categories_full, on='category_id', how='left')

# (Recomendado) Asegurarse de que la carpeta 'dw' exista
os.makedirs('dw', exist_ok=True)

# 4. Guardar la tabla final en 'dw/'
dim_product.to_csv('dw/dim_product.csv', index=False)









import os
# import locale # Descomentar si falla el método de 'locale='

print("Iniciando la creación de dim_date...")

# --- 1. Definir el rango de fechas ---
# El usuario pidió de 2023 a 2025 (inclusive)
start_date = '2023-01-01'
end_date = '2025-12-31'

# Crear el rango de fechas diarias
dates = pd.date_range(start_date, end_date, freq='D')

# Crear el DataFrame base
dim_date = pd.DataFrame(dates, columns=['date'])


# --- 2. Extraer atributos de las fechas (Feature Engineering) ---

# Locale para nombres en español
# (es_ES.UTF-8 es común, pero podría ser 'es_AR.UTF-8' o 'Spanish_Spain.1252' en Windows)
spanish_locale = 'es_ES.UTF-8' 

# Llaves y números
dim_date['date_key'] = dim_date['date'].dt.strftime('%Y%m%d').astype(int)
dim_date['year'] = dim_date['date'].dt.year
dim_date['quarter'] = dim_date['date'].dt.quarter
dim_date['month'] = dim_date['date'].dt.month
dim_date['day'] = dim_date['date'].dt.day
dim_date['day_of_week'] = dim_date['date'].dt.dayofweek  # 0=Lunes, 6=Domingo
dim_date['day_of_year'] = dim_date['date'].dt.dayofyear
dim_date['week_of_year'] = dim_date['date'].dt.isocalendar().week.astype(int)

# Nombres (intentar obtenerlos en español)
try:
    dim_date['month_name'] = dim_date['date'].dt.month_name(locale=spanish_locale)
    dim_date['day_name'] = dim_date['date'].dt.day_name(locale=spanish_locale)
except Exception as e:
    print(f"Advertencia: No se pudo usar el locale '{spanish_locale}' ({e}).")
    print("Usando nombres de mes/día en inglés por defecto.")
    # Fallback a inglés si el locale no está instalado en el sistema
    dim_date['month_name'] = dim_date['date'].dt.month_name()
    dim_date['day_name'] = dim_date['date'].dt.day_name()
    
# Nombres compuestos (ej. 2023-Q1, 2023-Ene)
dim_date['year_quarter'] = dim_date['year'].astype(str) + '-Q' + dim_date['quarter'].astype(str)
dim_date['year_month'] = dim_date['date'].dt.strftime('%Y-%m')

# Banderas (Flags) booleanas (True/False)
dim_date['is_weekday'] = dim_date['day_of_week'] < 5  # Lunes (0) a Viernes (4)
dim_date['is_weekend'] = dim_date['day_of_week'] >= 5 # Sábado (5) a Domingo (6)
dim_date['is_month_start'] = dim_date['date'].dt.is_month_start
dim_date['is_month_end'] = dim_date['date'].dt.is_month_end


# --- 3. Ordenar y Guardar ---

# Reordenar las columnas para que sean más legibles
column_order = [
    'date_key', 'date', 'year', 'quarter', 'year_quarter', 'month', 
    'month_name', 'year_month', 'day', 'day_of_week', 'day_name', 
    'day_of_year', 'week_of_year', 'is_weekday', 'is_weekend', 
    'is_month_start', 'is_month_end'
]
dim_date = dim_date[column_order]

# (Recomendado) Asegurarse de que la carpeta 'dw' exista
os.makedirs('dw', exist_ok=True)

# Guardar el archivo final
dim_date.to_csv('dw/dim_date.csv', index=False)

print("="*30)
print(f"¡Éxito! 'dim_date.csv' creado en la carpeta 'dw/'.")
print(f"Fechas desde: {start_date} hasta {end_date}")
print(f"Filas totales: {len(dim_date)}")
print("="*30)