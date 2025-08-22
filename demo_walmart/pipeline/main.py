from utils import Extract, Load
extractor = Extract()
loader = Load()

try:
    df = extractor.read_data(r'demo_walmart\pipeline\Walmart_Sales.csv')
    print("Data extracted\n", df.head(5), "\n")
except Exception as e:
    raise ValueError(f"Error reading data: {e}")

try:
    loader.load_data(df)
except Exception as e:
    raise RuntimeError(f"Error loading data: {e}")