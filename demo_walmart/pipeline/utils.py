import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import uuid


class Extract:
    def read_data(self, file_path:str) -> pd.DataFrame:
        df = pd.read_csv(file_path)
        df = df[['Store', 'Date', 'Weekly_Sales']]
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
        df['Date'] = df['Date'].dt.date

        df.rename(
            columns={
                'Store': 'store',
                'Date': 'sale_date',
                'Weekly_Sales': 'weekly_sales'
            }, inplace=True)
        return df

class Load:
    def __init__(self):
        self.conn_str = "postgresql://root:root@localhost:5433/test"
    
    def load_data(self, df: pd.DataFrame):
        try:
            with psycopg2.connect(self.conn_str) as conn:   # auto-commit/rollback on exit
                with conn.cursor() as cur:                  # auto-close cursor
                    insert_query = """
                        INSERT INTO public.landing_sales (store, sale_date, weekly_sales)
                        VALUES %s
                        ON CONFLICT (store, sale_date) DO NOTHING
                    """
                    data_tuples = df[['store', 'sale_date', 'weekly_sales']].to_records(index=False).tolist()
                    execute_values(cur, insert_query, data_tuples)
        except Exception as e:
            print(f"Error inserting data: {e}")
            raise
