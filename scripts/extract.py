import pandas as pd

def extract_raw_data(file_name):
    """Lee un archivo CSV de la carpeta raw/."""
    try:
        df = pd.read_csv(f'raw/{file_name}')
        print(f"-> Extracted: {file_name}")
        return df
    except FileNotFoundError:
        print(f"Error: El archivo raw/{file_name} no existe.")
        return None

def get_orders_data():
    return extract_raw_data('sales_order.csv')

def get_shipments_data():
    return extract_raw_data('shipment.csv')

def get_web_sessions_data():
    return extract_raw_data('web_session.csv')

def get_nps_data():
    return extract_raw_data('nps_response.csv')

def get_simple_dims_data():
    """Retorna un diccionario con las tablas que no requieren transformación compleja."""
    return {
        'customer': extract_raw_data('customer.csv'),
        'store': extract_raw_data('store.csv'),
        'channel': extract_raw_data('channel.csv')
    }

def get_items_data():
    return extract_raw_data('sales_order_item.csv')

def get_location_data():
    return extract_raw_data('address.csv'), extract_raw_data('province.csv')

def get_product_data():
    return extract_raw_data('product.csv'), extract_raw_data('product_category.csv')