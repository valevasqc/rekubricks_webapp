import pandas as pd

# Read the Excel file
df = pd.read_excel("data/bricklink_pieces.xlsx")

print("=== EXCEL DEBUG INFO ===")
print(f"Total rows: {len(df)}")
print(f"Columns: {list(df.columns)}")
print("\n=== FIRST 5 ROWS ===")
print(df.head())

print("\n=== DATA TYPES ===")
print(df.dtypes)

print("\n=== NULL VALUES ===")
print(df.isnull().sum())

print("\n=== SAMPLE PROBLEMATIC ROWS ===")
# Check for rows with missing essential data
problematic = df[df['Piece_ID'].isnull() | df['Piece_Name'].isnull() | df['Image_URL'].isnull()]
if len(problematic) > 0:
    print("Found problematic rows:")
    print(problematic)
else:
    print("No obviously problematic rows found")

print("\n=== UNIQUE VALUES CHECK ===")
print(f"Unique Piece_ID count: {df['Piece_ID'].nunique()}")
print(f"Unique Piece_Name count: {df['Piece_Name'].nunique()}")
if 'Price' in df.columns:
    print(f"Price range: {df['Price'].min()} to {df['Price'].max()}")
if 'Category' in df.columns:
    print(f"Categories: {df['Category'].unique()}")