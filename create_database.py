"""
Script to create SQLite database from Airbnb CSV data.
This allows for SQL-based analysis of the Airbnb dataset.
"""

import sqlite3
import pandas as pd
import zipfile
import os


def create_airbnb_database(csv_file='Airbnb_Open_Data (1).csv', 
                           zip_file='Airbnb_Open_Data (1).zip',
                           db_file='airbnb_data.db'):
    """
    Create SQLite database from Airbnb CSV data.
    
    Parameters:
    -----------
    csv_file : str
        Path to the CSV file
    zip_file : str
        Path to the zip file containing CSV (if CSV doesn't exist)
    db_file : str
        Path to the SQLite database file to create
    """
    
    # Extract CSV from zip if it doesn't exist
    if not os.path.exists(csv_file) and os.path.exists(zip_file):
        print(f"Extracting {csv_file} from {zip_file}...")
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall('.')
    
    # Read CSV file
    print(f"Reading {csv_file}...")
    df = pd.read_csv(csv_file)
    
    # Clean column names for SQL compatibility
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.lower()
    
    # Create SQLite database
    print(f"Creating database {db_file}...")
    conn = sqlite3.connect(db_file)
    
    # Write dataframe to SQL
    df.to_sql('airbnb_listings', conn, if_exists='replace', index=False)
    
    # Create indexes for better query performance
    print("Creating indexes...")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_neighbourhood_group 
        ON airbnb_listings(neighbourhood_group)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_room_type 
        ON airbnb_listings(room_type)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_neighbourhood 
        ON airbnb_listings(neighbourhood)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_price 
        ON airbnb_listings(price)
    ''')
    
    conn.commit()
    
    # Print summary
    cursor.execute('SELECT COUNT(*) FROM airbnb_listings')
    count = cursor.fetchone()[0]
    print(f"\nDatabase created successfully!")
    print(f"Total records: {count}")
    
    # Show table schema
    cursor.execute("PRAGMA table_info(airbnb_listings)")
    columns = cursor.fetchall()
    print("\nTable columns:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
    
    conn.close()
    print(f"\nDatabase saved to: {db_file}")


if __name__ == '__main__':
    create_airbnb_database()
