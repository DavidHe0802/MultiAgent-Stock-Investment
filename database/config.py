import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'stock_data.db')
STOCK_LIST_PATH = os.path.join(BASE_DIR, 'data', 'stock_list.csv')