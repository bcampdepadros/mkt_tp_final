import scripts.extract as extract
import scripts.transform as transform
import scripts.load as load

def run_etl_pipeline():
    print("=== INICIANDO PROCESO ETL ===")

    # 1. Fact Orders
    raw_orders = extract.get_orders_data()
    dw_orders = transform.transform_fact_orders(raw_orders)
    load.load_to_dw(dw_orders, 'fact_order.csv')

    # 2. Fact Shipments
    raw_shipments = extract.get_shipments_data()
    dw_shipments = transform.transform_fact_shipments(raw_shipments)
    load.load_to_dw(dw_shipments, 'fact_shipments.csv')

    # 3. Fact Web Sessions
    raw_ws = extract.get_web_sessions_data()
    dw_ws = transform.transform_web_sessions(raw_ws)
    load.load_to_dw(dw_ws, 'fact_web_sessions.csv')

    # 4. Fact NPS
    raw_nps = extract.get_nps_data()
    dw_nps = transform.transform_nps(raw_nps)
    load.load_to_dw(dw_nps, 'fact_nps.csv')

    # 5. Dimensiones Simples (Customer, Store, Channel)
    simple_dims = extract.get_simple_dims_data()
    for name, df in simple_dims.items():
        load.load_to_dw(df, f'dim_{name}.csv')

    # 6. Fact Order Items (Requiere Merge)
    raw_items = extract.get_items_data()
    dw_order_items = transform.transform_fact_order_items(raw_items, raw_orders)
    load.load_to_dw(dw_order_items, 'fact_order_item.csv')

    # 7. Dim Location (Requiere Merge)
    raw_addr, raw_prov = extract.get_location_data()
    dw_location = transform.transform_dim_location(raw_addr, raw_prov)
    load.load_to_dw(dw_location, 'dim_location.csv')

    # 8. Dim Product (Requiere Merge Complejo)
    raw_prod, raw_cat = extract.get_product_data()
    dw_product = transform.transform_dim_product(raw_prod, raw_cat)
    load.load_to_dw(dw_product, 'dim_product.csv')

    # 9. Dim Date (Generada)
    dw_date = transform.generate_dim_date()
    load.load_to_dw(dw_date, 'dim_date.csv')

    print("=== PROCESO ETL FINALIZADO CON ÉXITO ===")

if __name__ == "__main__":
    run_etl_pipeline()