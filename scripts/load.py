import os

def load_to_dw(df, file_name):
    """Guarda un DataFrame en la carpeta dw/"""
    if df is None:
        print(f"Skipping {file_name} (No Data)")
        return

    os.makedirs('dw', exist_ok=True)
    
    path = f'dw/{file_name}'
    df.to_csv(path, index=False)
    print(f"-> Saved: {path}")