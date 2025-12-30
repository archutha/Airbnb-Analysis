# Airbnb-Analysis
This project explores key factors influencing Airbnb listings, such as price variations based on neighborhood, room type, and ratings. It includes data cleaning, exploratory data analysis (EDA), and visualizations to uncover insights and patterns in Airbnb listings.

## Features
- Python-based data analysis using pandas, numpy, matplotlib, seaborn, and plotly
- SQL-based data analysis using SQLite
- Comprehensive queries for price, availability, reviews, and host analysis
- Interactive Jupyter notebook with visualizations

## SQL Analysis

This project now includes SQL-based analysis capabilities. You can analyze the Airbnb data using SQL queries in addition to Python/pandas.

### Getting Started with SQL

1. **Create the database:**
   ```bash
   python create_database.py
   ```
   This will extract the CSV data from the zip file and create a SQLite database (`airbnb_data.db`).

2. **Run predefined SQL analysis:**
   ```bash
   python run_sql_analysis.py
   ```
   This will run a variety of SQL queries and display results including:
   - Basic statistics
   - Price analysis by neighbourhood and room type
   - Review ratings distribution
   - Host analysis
   - Booking policies
   - And more...

3. **Run custom SQL queries:**
   ```bash
   python run_sql_analysis.py --custom
   ```
   This opens an interactive mode where you can write and execute your own SQL queries.

4. **View all available queries:**
   See `airbnb_queries.sql` for a comprehensive collection of SQL queries organized by category.

### SQL Query Categories

The `airbnb_queries.sql` file contains queries for:
1. Basic Statistics
2. Price Analysis
3. Availability Analysis
4. Reviews Analysis
5. Host Analysis
6. Room Type Distribution
7. Booking Policies
8. Minimum Nights Analysis
9. Construction Year Analysis
10. Geographic Analysis
