import pandas as pd
from pathlib import Path

# Ruta a la carpeta DW (ajustá si la carpeta se llama distinto o está en otro lado)
base_path = Path("DW")

# =========================
# 1. LEER TODAS LAS TABLAS
# =========================
dim_channel = pd.read_csv(base_path / "dim_channel.csv")
dim_customer = pd.read_csv(base_path / "dim_customer.csv")
dim_date = pd.read_csv(base_path / "dim_date.csv")
dim_location = pd.read_csv(base_path / "dim_location.csv")
dim_product = pd.read_csv(base_path / "dim_product.csv")
dim_store = pd.read_csv(base_path / "dim_store.csv")

fact_nps = pd.read_csv(base_path / "fact_nps.csv")
fact_order_item = pd.read_csv(base_path / "fact_order_item.csv")
fact_order = pd.read_csv(base_path / "fact_order.csv")
fact_shipments = pd.read_csv(base_path / "fact_shipments.csv")
fact_web_sessions = pd.read_csv(base_path / "fact_web_sessions.csv")

# ======================================
# 2. PARTIMOS DE LA TABLA BASE: ORDER_ITEM
#    (una fila por ítem de pedido)
# ======================================
one_big = fact_order_item.copy()

# =========================
# 3. JOINS CON DIMENSIONES
# =========================

# 3.1 Canal
one_big = one_big.merge(
    dim_channel,
    on="channel_id",
    how="left",
    suffixes=("", "_channel")
)
# columnas nuevas: code, name del canal

# 3.2 Cliente
one_big = one_big.merge(
    dim_customer,
    on="customer_id",
    how="left",
    suffixes=("", "_customer")
)
# columnas nuevas: email, first_name, last_name, phone, status (cliente), created_at (cliente)

# 3.3 Producto
one_big = one_big.merge(
    dim_product,
    on="product_id",
    how="left",
    suffixes=("", "_product")
)
# columnas nuevas: sku, name (producto), category_name, etc.

# 3.4 Tienda
one_big = one_big.merge(
    dim_store,
    on="store_id",
    how="left",
    suffixes=("", "_store")
)
# columnas nuevas: name_store, address_id (de la tienda)

# 3.5 Ubicación de envío (shipping_address)
shipping_loc = dim_location.rename(columns={
    "address_id": "shipping_address_id",
    "line1": "shipping_line1",
    "line2": "shipping_line2",
    "city": "shipping_city",
    "province_id": "shipping_province_id",
    "postal_code": "shipping_postal_code",
    "country_code": "shipping_country_code",
    "created_at": "shipping_address_created_at",
    "name": "shipping_address_name",
    "code": "shipping_address_code",
})

one_big = one_big.merge(
    shipping_loc,
    on="shipping_address_id",
    how="left"
)

# 3.6 Ubicación de facturación (billing_address)
billing_loc = dim_location.rename(columns={
    "address_id": "billing_address_id",
    "line1": "billing_line1",
    "line2": "billing_line2",
    "city": "billing_city",
    "province_id": "billing_province_id",
    "postal_code": "billing_postal_code",
    "country_code": "billing_country_code",
    "created_at": "billing_address_created_at",
    "name": "billing_address_name",
    "code": "billing_address_code",
})

one_big = one_big.merge(
    billing_loc,
    on="billing_address_id",
    how="left"
)

# 3.7 Fecha de la orden (dim_date → prefijo order_)
dim_date_order = dim_date.rename(columns={
    "date_key": "order_date_key",
    "date": "order_date",
    "year": "order_year",
    "quarter": "order_quarter",
    "year_quarter": "order_year_quarter",
    "month": "order_month",
    "month_name": "order_month_name",
    "year_month": "order_year_month",
    "day": "order_day",
    "day_of_week": "order_day_of_week",
    "day_name": "order_day_name",
    "day_of_year": "order_day_of_year",
    "week_of_year": "order_week_of_year",
    "is_weekday": "order_is_weekday",
    "is_weekend": "order_is_weekend",
    "is_month_start": "order_is_month_start",
    "is_month_end": "order_is_month_end",
})

one_big = one_big.merge(
    dim_date_order,
    on="order_date_key",
    how="left"
)

# =================================
# 4. JOINS CON OTRAS TABLAS DE HECHOS
# =================================

# 4.1 fact_order: por si necesitás campos a nivel orden (si ya están, igual no molesta)
one_big = one_big.merge(
    fact_order,
    on="order_id",
    how="left",
    suffixes=("", "_order")
)

# 4.2 fact_shipments: info de envíos a partir del order_id
one_big = one_big.merge(
    fact_shipments,
    on="order_id",
    how="left",
    suffixes=("", "_shipment")
)

# 4.3 fact_nps: matcheamos por cliente + canal + fecha
#     supondremos que responded_date_key se refiere al día de la respuesta
fact_nps_join = fact_nps.copy()

one_big = one_big.merge(
    fact_nps_join,
    how="left",
    left_on=["customer_id", "channel_id", "order_date_key"],
    right_on=["customer_id", "channel_id", "responded_date_key"],
    suffixes=("", "_nps")
)

# 4.4 fact_web_sessions: matcheamos por cliente + fecha de inicio de sesión
fact_web_sessions_join = fact_web_sessions.copy()

one_big = one_big.merge(
    fact_web_sessions_join,
    how="left",
    left_on=["customer_id", "order_date_key"],
    right_on=["customer_id", "started_date_key"],
    suffixes=("", "_session")
)

# =================================
# 5. GUARDAR CSV FINAL
# =================================
output_path = base_path / "one_big_table.csv"
one_big.to_csv(output_path, index=False)

print(f"Archivo generado: {output_path.resolve()}")
print(f"Filas: {len(one_big):,}")
print(f"Columnas: {len(one_big.columns)}")
