"""
Run SQL queries on the Airbnb database and display results.
This script demonstrates how to use SQL for data analysis.
"""

import sqlite3
import pandas as pd
import os


# SQL helper for cleaning price strings (removes '$' and spaces)
CLEAN_PRICE_SQL = "CAST(REPLACE(REPLACE(price, '$', ''), ' ', '') AS REAL)"


def run_query(db_file, query, description=""):
    """
    Run a SQL query and display results.
    
    Parameters:
    -----------
    db_file : str
        Path to the SQLite database file
    query : str
        SQL query to execute
    description : str
        Description of the query
    """
    if description:
        print(f"\n{'='*80}")
        print(f"{description}")
        print(f"{'='*80}")
    
    try:
        with sqlite3.connect(db_file) as conn:
            df = pd.read_sql_query(query, conn)
            print(df.to_string())
            print(f"\nRows returned: {len(df)}")
    except Exception as e:
        print(f"Error executing query: {e}")


def run_all_queries(db_file='airbnb_data.db'):
    """
    Run a selection of interesting queries from the SQL file.
    
    Parameters:
    -----------
    db_file : str
        Path to the SQLite database file
    """
    
    if not os.path.exists(db_file):
        print(f"Database file '{db_file}' not found!")
        print("Please run create_database.py first to create the database.")
        return
    
    print("Airbnb Data Analysis using SQL")
    print("="*80)
    
    # Query 1: Basic Statistics
    query1 = """
    SELECT 
        COUNT(*) as total_listings,
        COUNT(DISTINCT host_id) as unique_hosts,
        COUNT(DISTINCT neighbourhood_group) as neighbourhood_groups,
        COUNT(DISTINCT neighbourhood) as neighbourhoods,
        COUNT(DISTINCT room_type) as room_types
    FROM airbnb_listings;
    """
    run_query(db_file, query1, "1. Basic Statistics")
    
    # Query 2: Average Price by Neighbourhood Group
    query2 = f"""
    SELECT 
        neighbourhood_group,
        COUNT(*) as listings_count,
        ROUND(AVG({CLEAN_PRICE_SQL}), 2) as avg_price,
        ROUND(MIN({CLEAN_PRICE_SQL}), 2) as min_price,
        ROUND(MAX({CLEAN_PRICE_SQL}), 2) as max_price
    FROM airbnb_listings
    WHERE price IS NOT NULL AND price != ''
    GROUP BY neighbourhood_group
    ORDER BY avg_price DESC;
    """
    run_query(db_file, query2, "2. Average Price by Neighbourhood Group")
    
    # Query 3: Average Price by Room Type
    query3 = f"""
    SELECT 
        room_type,
        COUNT(*) as listings_count,
        ROUND(AVG({CLEAN_PRICE_SQL}), 2) as avg_price,
        ROUND(MIN({CLEAN_PRICE_SQL}), 2) as min_price,
        ROUND(MAX({CLEAN_PRICE_SQL}), 2) as max_price
    FROM airbnb_listings
    WHERE price IS NOT NULL AND price != ''
    GROUP BY room_type
    ORDER BY avg_price DESC;
    """
    run_query(db_file, query3, "3. Average Price by Room Type")
    
    # Query 4: Top 10 Most Expensive Neighbourhoods
    query4 = f"""
    SELECT 
        neighbourhood,
        neighbourhood_group,
        COUNT(*) as listings_count,
        ROUND(AVG({CLEAN_PRICE_SQL}), 2) as avg_price
    FROM airbnb_listings
    WHERE price IS NOT NULL AND price != ''
    GROUP BY neighbourhood, neighbourhood_group
    HAVING listings_count >= 10
    ORDER BY avg_price DESC
    LIMIT 10;
    """
    run_query(db_file, query4, "4. Top 10 Most Expensive Neighbourhoods (min 10 listings)")
    
    # Query 5: Review Rating Distribution
    query5 = """
    SELECT 
        review_rate_number as rating,
        COUNT(*) as count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM airbnb_listings WHERE review_rate_number IS NOT NULL), 2) as percentage
    FROM airbnb_listings
    WHERE review_rate_number IS NOT NULL
    GROUP BY review_rate_number
    ORDER BY rating DESC;
    """
    run_query(db_file, query5, "5. Review Rating Distribution")
    
    # Query 6: Top 10 Hosts with Most Listings
    query6 = f"""
    SELECT 
        host_id,
        host_name,
        host_identity_verified,
        COUNT(*) as total_listings,
        ROUND(AVG({CLEAN_PRICE_SQL}), 2) as avg_price,
        ROUND(AVG(review_rate_number), 2) as avg_rating
    FROM airbnb_listings
    GROUP BY host_id, host_name, host_identity_verified
    ORDER BY total_listings DESC
    LIMIT 10;
    """
    run_query(db_file, query6, "6. Top 10 Hosts with Most Listings")
    
    # Query 7: Room Type Distribution by Neighbourhood Group
    query7 = """
    SELECT 
        neighbourhood_group,
        room_type,
        COUNT(*) as count,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY neighbourhood_group), 2) as percentage
    FROM airbnb_listings
    WHERE neighbourhood_group IS NOT NULL AND room_type IS NOT NULL
    GROUP BY neighbourhood_group, room_type
    ORDER BY neighbourhood_group, count DESC;
    """
    run_query(db_file, query7, "7. Room Type Distribution by Neighbourhood Group")
    
    # Query 8: Cancellation Policy Distribution
    query8 = f"""
    SELECT 
        cancellation_policy,
        COUNT(*) as count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM airbnb_listings WHERE cancellation_policy IS NOT NULL), 2) as percentage
    FROM airbnb_listings
    WHERE cancellation_policy IS NOT NULL
    GROUP BY cancellation_policy
    ORDER BY count DESC;
    """
    run_query(db_file, query8, "8. Cancellation Policy Distribution")
    
    # Query 9: Top 20 Neighbourhoods by Number of Listings
    query9 = f"""
    SELECT 
        neighbourhood,
        neighbourhood_group,
        COUNT(*) as listings_count,
        ROUND(AVG({CLEAN_PRICE_SQL}), 2) as avg_price,
        ROUND(AVG(review_rate_number), 2) as avg_rating,
        ROUND(AVG(availability_365), 2) as avg_availability
    FROM airbnb_listings
    WHERE neighbourhood IS NOT NULL
    GROUP BY neighbourhood, neighbourhood_group
    ORDER BY listings_count DESC
    LIMIT 20;
    """
    run_query(db_file, query9, "9. Top 20 Neighbourhoods by Number of Listings")
    
    print("\n" + "="*80)
    print("Analysis complete!")
    print("="*80)


def custom_query(db_file='airbnb_data.db'):
    """
    Interactive mode to run custom SQL queries.
    
    Parameters:
    -----------
    db_file : str
        Path to the SQLite database file
    """
    
    if not os.path.exists(db_file):
        print(f"Database file '{db_file}' not found!")
        print("Please run create_database.py first to create the database.")
        return
    
    print("\nCustom Query Mode")
    print("="*80)
    print("Enter your SQL query (or 'exit' to quit):")
    print("Example: SELECT * FROM airbnb_listings LIMIT 5;")
    print()
    
    while True:
        query = input("SQL> ").strip()
        
        if query.lower() == 'exit':
            break
        
        if not query:
            continue
        
        try:
            with sqlite3.connect(db_file) as conn:
                df = pd.read_sql_query(query, conn)
                print("\nResults:")
                print(df.to_string())
                print(f"\nRows returned: {len(df)}\n")
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--custom':
        custom_query()
    else:
        run_all_queries()
