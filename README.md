# Trabajo Práctico Final — Introducción al Marketing Online y los Negocios Digitales

Repositorio del trabajo práctico final de la materia.

**Consigna y documento principal:** [Trabajo Práctico Final](https://docs.google.com/document/d/15RNP3FVqLjO4jzh80AAkK6mUR5DOLqPxLjQxqvdzrYg/edit?usp=sharing)
**Diagrama Entidad Relación:** [DER](./assets/DER.png)




Proyecto Final — Data Warehouse de Marketing y Ventas
Introducción al Marketing Online y los Negocios Digitales — Trabajo Práctico Final Creación de un Data Warehouse (DW) en formato CSV a partir de múltiples fuentes de datos raw/, procesadas con Python/Pandas y listas para ser consumidas por un dashboard.



1) Objetivos

2) Diccionario de Datos y Modelo

3) Estructura del Repositorio

4) Requisitos e Instalación

5) Pipeline ETL 

6) Cómo ejecutar el proyecto



1) Objetivos

En este proyecto busco implementar un data warehouse en formato CSV. Mi objetivo es tomar los archivos de datos de la carpeta raw/, luego procesarlo con Python y Pandas, y por úlitmo genero un modelo de datos limpio (esquema estrella) en la carpeta dw/.

Este modelo permite consolidar la información de ventas, clientes, productos y marketing en un solo lugar, listo para ser analizado.

Entregables principales:

Scripts de Python (scripts/) para la carga y transformación (ETL) de cada tabla.

Un modelo de datos (Dimensiones y Hechos) en formato CSV en la carpeta dw/.

Un README en el que detallo el proceso y el modelo.


2) Diccionario de Datos y Modelo
Detallo el Esquema Estrella diseñado para este proyecto.

Claves: El modelo utiliza las claves de negocio originales (ej. customer_id, product_id, order_id) como claves primarias y foráneas. No se generan claves sustitutas (surrogate keys), con la excepción de la dimensión de tiempo.

Dimensión de Tiempo (dim_date):

Esta es una dimensión de conformación generada por el script scripts/create_dim_date.py, ya que no existe en los datos RAW.

Cubre el rango de 2023 a 2025.

Transformación de Fechas (ETL):

Todos los scripts que generan tablas de hechos (ej. process_orders.py) incluyen un paso para convertir las columnas de fecha/hora (ej. order_date) en la clave entera YYYYMMDD (ej. order_date_key).

Esto permite los JOINs directos con dim_date y optimiza el rendimiento en la herramienta de BI.

Denormalización en Dimensiones:

Para simplificar las consultas en el dashboard, algunas dimensiones se denormalizan durante el ETL:

dim_product: Se crea uniendo product.csv con product_category.csv. Incluye un self-join para obtener tanto el nombre de la categoría como el nombre de la categoría padre en la misma fila.

dim_location: Se crea uniendo address.csv con province.csv para incluir el nombre de la provincia.

DIMENSIONES (Dims)
Estas tablas describen el "quién, qué, dónde, cuándo" de los eventos de negocio.

dim_date

PK: date_key (INT)

Origen: Generada por scripts/create_dim_date.py.

Atributos: date, year, month, month_name, day_name, quarter, etc.

dim_customer

PK: customer_id

Origen: raw/customer.csv

dim_location

PK: address_id

Origen: raw/address.csv + raw/province.csv

dim_product

PK: product_id

Origen: raw/product.csv + raw/product_category.csv

dim_channel

PK: channel_id

Origen: raw/channel.csv

dim_store

PK: store_id

Origen: raw/store.csv

HECHOS (Facts)
Estas tablas registran los eventos de negocio (ventas, envíos, sesiones, etc.) y sus métricas.

fact_order

Grano: Un pedido.

Origen: raw/sales_order.csv

FK a Dim_Date: order_date_key (de order_date)

fact_order_item

Grano: Un ítem de producto dentro de un pedido.

Origen: raw/sales_order_item.csv + raw/sales_order.csv

FK a Dim_Date: order_date_key (obtenida del merge con sales_order)

fact_shipments
Grano: Un envío.

Origen: raw/shipment.csv

FKs a Dim_Date: shipped_date_key (de shipped_at), delivered_date_key (de delivered_at)

fact_web_sessions

Grano: Una sesión web.

Origen: raw/web_session.csv

FKs a Dim_Date: started_date_key (de started_at), ended_date_key (de ended_at)

fact_nps

Grano: Una respuesta de NPS.

Origen: raw/nps_response.csv

FK a Dim_Date: responded_date_key (de responded_at)

3) Estructura del Repositorio
.
├── README.md
├── requirements.txt
├── .gitignore
│
├── scripts/                # Scripts de Python (ETL)
│   ├── create_dim_date.py
│   ├── process_customer.py
│   ├── process_location.py
│   ├── process_product.py
│   ├── process_channel.py
│   ├── process_store.py
│   ├── process_orders.py
│   ├── process_order_items.py
│   ├── process_shipments.py
│   ├── process_sessions.py
│   └── process_nps.py
│
├── raw/                    # Datos fuente (CSV originales)
│   ├── sales_order.csv
│   ├── sales_order_item.csv
│   ├── customer.csv
│   ├── product.csv
│   ├── product_category.csv
│   ├── address.csv
│   ├── province.csv
│   ├── channel.csv
│   ├── store.csv
│   ├── shipment.csv
│   ├── web_session.csv
│   └── nps_response.csv
│
├── dw/                     # Data Warehouse (Salida de los scripts)
│   ├── dim_date.csv
│   ├── dim_customer.csv
│   ├── dim_location.csv
│   ├── dim_product.csv
│   ├── dim_channel.csv
│   ├── dim_store.csv
│   ├── fact_order.csv
│   ├── fact_order_item.csv
│   ├── fact_shipments.csv
│   ├── fact_web_sessions.csv
│   └── fact_nps.csv
│
└── assets/                 # (Carpeta para capturas de pantalla)
    └── dashboard_kpis.png
4) Requisitos e Instalación
Versión recomendada de Python: 3.9+

Entorno virtual (recomendado)
Bash

# Crear el entorno
python -m venv .venv

# Activar en Windows
.venv\Scripts\activate

# Activar en macOS / Linux
source .venv/bin/activate
Dependencias
El proyecto solo requiere Pandas.

Plaintext

# requirements.txt
pandas
Instalación:

Bash

pip install -r requirements.txt
5) Pipeline ETL (scripts)
El proceso de ETL se compone de varios scripts en la carpeta scripts/, diseñados para ser ejecutados desde la carpeta raíz del proyecto.

create_dim_date.py:

Acción: Genera dw/dim_date.csv desde cero.

Rango: 2023-01-01 a 2025-12-31.

Debe ejecutarse primero.

Scripts de Dimensiones (ej. process_customer.py, process_product.py):

Acción: Leen uno o más archivos de raw/, realizan las uniones necesarias (dim_product, dim_location) y guardan el resultado limpio en dw/.

Scripts de Hechos (ej. process_orders.py, process_shipments.py):

Acción: Leen los archivos de raw/, convierten todas las columnas de fecha a claves YYYYMMDD (ej. shipped_date_key), y guardan el resultado en dw/.

6) Cómo ejecutar el proyecto
Con el entorno activado y las dependencias instaladas, ejecuta los scripts desde la carpeta raíz del proyecto.

Bash

# 1. Asegúrate de que todos los CSV fuente estén en ./raw
# 2. Asegúrate de que la carpeta ./dw exista (los scripts la crearán si no)

# 3. EJECUTAR PRIMERO: Creación de la Dimensión de Tiempo
python scripts/create_dim_date.py

# 4. Ejecutar scripts de Dimensiones (el orden no importa)
python scripts/process_customer.py
python scripts/process_location.py
python scripts/process_product.py
python scripts/process_channel.py
python scripts/process_store.py

# 5. Ejecutar scripts de Hechos (el orden no importa)
python scripts/process_orders.py
python scripts/process_order_items.py
python scripts/process_shipments.py
python scripts/process_sessions.py
python scripts/process_nps.py
Si todo sale bien, la carpeta dw/ contendrá todos los CSVs finales, listos para ser consumidos.



