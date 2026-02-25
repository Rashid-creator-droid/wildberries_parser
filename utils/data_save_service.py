import pandas as pd

def save_products_to_excel(products_data: list, filename="products.xlsx"):

    df = pd.DataFrame(products_data)

    df.to_excel(filename, index=False)
    print(f"Saved {len(products_data)} products to {filename}")