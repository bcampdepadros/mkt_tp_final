import pandas as pd
import os

print("Iniciando el procesamiento de datos...")

# --- 1. Definir las rutas ---
RAW_DIR = 'raw'
DW_DIR = 'DW'
os.makedirs(DW_DIR, exist_ok=True)
print(f"Carpeta '{DW_DIR}' asegurada.")

# --- 2. PROCESO: Dimensión Clientes (dim_customer) ---
print("\nProcesando Dimensión Clientes...")
try:
    customer_path = os.path.join(RAW_DIR, 'customer.csv')
    df_customer = pd.read_csv(customer_path)
    
    # Guardar la dimensión en el DW
    output_path = os.path.join(DW_DIR, 'dim_customer.csv')
    df_customer.to_csv(output_path, index=False)
    print("¡Éxito! 'dim_customer.csv' guardado.")

except FileNotFoundError:
    print(f"ERROR (Customer): No se encontró el archivo en {customer_path}")
except Exception as e:
    print(f"Ocurrió un error (Customer): {e}")


# --- 3. PROCESO: Hechos de Ventas (fact_sales) ---
print("\nProcesando Hechos de Ventas...")
try:
    # Cargar el archivo de pedidos
    sales_path = os.path.join(RAW_DIR, 'sales_order.csv')
    df_sales = pd.read_csv(sales_path)
    print("Cargado 'sales_order.csv' con éxito.")

    # Transformación 1: Filtrar por estados de pedido válidos
    # (Solo contamos ventas 'PAID' o 'FULFILLED')
    estados_validos = ['PAID', 'FULFILLED']
    df_sales_validas = df_sales[df_sales['status'].isin(estados_validos)].copy()
    print(f"Filtrando por {estados_validos}. Quedan {len(df_sales_validas)} ventas válidas.")

    # Transformación 2: Asegurar tipos de datos correctos
    # Convertimos 'order_date' a tipo fecha (crucial para Looker Studio)
    df_sales_validas['order_date'] = pd.to_datetime(df_sales_validas['order_date'])
    
    # (Recomendado: extraer partes de la fecha para los filtros del dashboard)
    df_sales_validas['order_year'] = df_sales_validas['order_date'].dt.year
    df_sales_validas['order_month'] = df_sales_validas['order_date'].dt.month
    
    print("Convertida 'order_date' a datetime y añadidas columnas de fecha.")

    # Guardar la tabla de hechos en el DW
    # Esta tabla será la fuente principal para tu KPI de Ventas
    output_sales_path = os.path.join(DW_DIR, 'fact_sales.csv')
    df_sales_validas.to_csv(output_sales_path, index=False)
    
    print(f"¡Éxito! Archivo de ventas guardado en: {output_sales_path}")

except FileNotFoundError:
    print(f"ERROR (Sales): No se encontró el archivo en {sales_path}. Revisa el nombre.")
except Exception as e:
    print(f"Ocurrió un error (Sales): {e}")

print("\n--- Procesamiento de ETL completado ---")