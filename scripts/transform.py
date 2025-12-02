import pandas as pd


def transform_fact_orders(df_orders):
    if df_orders is None: return None
    df = df_orders.copy()
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df['order_date_key'] = df['order_date'].dt.strftime('%Y%m%d').astype('Int64')
    df = df.drop(columns=['order_date'])
    return df

def transform_fact_shipments(df_shipments):
    if df_shipments is None: return None
    df = df_shipments.copy()
    df['shipped_at'] = pd.to_datetime(df['shipped_at'], errors='coerce')
    df['delivered_at'] = pd.to_datetime(df['delivered_at'], errors='coerce')
    df['shipped_date_key'] = df['shipped_at'].dt.strftime('%Y%m%d').astype('Int64')
    df['delivered_date_key'] = df['delivered_at'].dt.strftime('%Y%m%d').astype('Int64')
    df = df.drop(columns=['shipped_at', 'delivered_at'])
    return df

def transform_web_sessions(df_ws):
    if df_ws is None: return None
    df = df_ws.copy()
    df['started_at'] = pd.to_datetime(df['started_at'], errors='coerce')
    df['ended_at'] = pd.to_datetime(df['ended_at'], errors='coerce')
    df['started_date_key'] = df['started_at'].dt.strftime('%Y%m%d').astype('Int64')
    df['ended_date_key'] = df['ended_at'].dt.strftime('%Y%m%d').astype('Int64')
    df = df.drop(columns=['started_at', 'ended_at'])
    return df

def transform_nps(df_nps):
    if df_nps is None: return None
    df = df_nps.copy()
    df['responded_at'] = pd.to_datetime(df['responded_at'], errors='coerce')
    df['responded_date_key'] = df['responded_at'].dt.strftime('%Y%m%d').astype('Int64')
    df = df.drop(columns=['responded_at'])
    return df


def transform_fact_order_items(df_items, df_orders):
    if df_items is None or df_orders is None: return None
    orders_temp = df_orders.copy()
    orders_temp['order_date'] = pd.to_datetime(orders_temp['order_date'], errors='coerce')
    orders_temp['order_date_key'] = orders_temp['order_date'].dt.strftime('%Y%m%d').astype('Int64')
    orders_temp = orders_temp.drop(columns=['order_date'])
    

    fact_order_items = pd.merge(df_items, orders_temp, on='order_id', how='left')
    return fact_order_items

def transform_dim_location(df_addresses, df_provinces):
    if df_addresses is None or df_provinces is None: return None
    dim_location = pd.merge(df_addresses, df_provinces, on='province_id', how='left')
    return dim_location

def transform_dim_product(df_products, df_categories):
    if df_products is None or df_categories is None: return None
    
    cats = df_categories.copy()
    cats.rename(columns={'name': 'category_name'}, inplace=True)
    
    parent_names = cats[['category_id', 'category_name']].rename(columns={
        'category_id': 'parent_id',
        'category_name': 'parent_category_name'
    })
    
    categories_full = pd.merge(cats, parent_names, on='parent_id', how='left')
    
    dim_product = pd.merge(df_products, categories_full, on='category_id', how='left')
    return dim_product


def generate_dim_date(start_year='2023', end_year='2025'):
    print("Generando dim_date...")
    start_date = f'{start_year}-01-01'
    end_date = f'{end_year}-12-31'
    dates = pd.date_range(start_date, end_date, freq='D')
    dim_date = pd.DataFrame(dates, columns=['date'])

    spanish_locale = 'es_ES.UTF-8'
    
    dim_date['date_key'] = dim_date['date'].dt.strftime('%Y%m%d').astype(int)
    dim_date['year'] = dim_date['date'].dt.year
    dim_date['quarter'] = dim_date['date'].dt.quarter
    dim_date['month'] = dim_date['date'].dt.month
    dim_date['day'] = dim_date['date'].dt.day
    dim_date['day_of_week'] = dim_date['date'].dt.dayofweek
    dim_date['day_of_year'] = dim_date['date'].dt.dayofyear
    dim_date['week_of_year'] = dim_date['date'].dt.isocalendar().week.astype(int)

    try:
        dim_date['month_name'] = dim_date['date'].dt.month_name(locale=spanish_locale)
        dim_date['day_name'] = dim_date['date'].dt.day_name(locale=spanish_locale)
    except:
        dim_date['month_name'] = dim_date['date'].dt.month_name()
        dim_date['day_name'] = dim_date['date'].dt.day_name()
        
    dim_date['year_quarter'] = dim_date['year'].astype(str) + '-Q' + dim_date['quarter'].astype(str)
    dim_date['year_month'] = dim_date['date'].dt.strftime('%Y-%m')
    dim_date['is_weekday'] = dim_date['day_of_week'] < 5
    dim_date['is_weekend'] = dim_date['day_of_week'] >= 5
    dim_date['is_month_start'] = dim_date['date'].dt.is_month_start
    dim_date['is_month_end'] = dim_date['date'].dt.is_month_end

    column_order = [
        'date_key', 'date', 'year', 'quarter', 'year_quarter', 'month', 
        'month_name', 'year_month', 'day', 'day_of_week', 'day_name', 
        'day_of_year', 'week_of_year', 'is_weekday', 'is_weekend', 
        'is_month_start', 'is_month_end'
    ]
    return dim_date[column_order]