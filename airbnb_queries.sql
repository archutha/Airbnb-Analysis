-- SQL Queries for Airbnb Data Analysis
-- These queries can be used to analyze the Airbnb dataset using SQL

-- Note: Price data is stored as text with '$' and spaces (e.g., '$100 ')
-- To use price in calculations, use: CAST(REPLACE(REPLACE(price, '$', ''), ' ', '') AS REAL)
-- This pattern is used consistently throughout the queries below.

-- ============================================================================
-- 1. BASIC STATISTICS
-- ============================================================================

-- Get total number of listings
SELECT COUNT(*) as total_listings 
FROM airbnb_listings;

-- Get summary statistics
SELECT 
    COUNT(*) as total_listings,
    COUNT(DISTINCT host_id) as unique_hosts,
    COUNT(DISTINCT neighbourhood_group) as neighbourhood_groups,
    COUNT(DISTINCT neighbourhood) as neighbourhoods,
    COUNT(DISTINCT room_type) as room_types
FROM airbnb_listings;


-- ============================================================================
-- 2. PRICE ANALYSIS
-- ============================================================================

-- Average price by neighbourhood group
-- Note: Price is stored as text with '$' and spaces, needs cleaning
SELECT 
    neighbourhood_group,
    COUNT(*) as listings_count,
    AVG(CAST(REPLACE(REPLACE(price, '$', ''), ' ', '') AS REAL)) as avg_price,
    MIN(CAST(REPLACE(REPLACE(price, '$', ''), ' ', '') AS REAL)) as min_price,
    MAX(CAST(REPLACE(REPLACE(price, '$', ''), ' ', '') AS REAL)) as max_price
FROM airbnb_listings
WHERE price IS NOT NULL AND price != ''
GROUP BY neighbourhood_group
ORDER BY avg_price DESC;

-- Average price by room type
SELECT 
    room_type,
    COUNT(*) as listings_count,
    AVG(CAST(REPLACE(REPLACE(price, '$', ''), ' ', '') AS REAL)) as avg_price,
    MIN(CAST(REPLACE(REPLACE(price, '$', ''), ' ', '') AS REAL)) as min_price,
    MAX(CAST(REPLACE(REPLACE(price, '$', ''), ' ', '') AS REAL)) as max_price
FROM airbnb_listings
WHERE price IS NOT NULL AND price != ''
GROUP BY room_type
ORDER BY avg_price DESC;

-- Top 10 most expensive neighbourhoods
SELECT 
    neighbourhood,
    neighbourhood_group,
    COUNT(*) as listings_count,
    AVG(CAST(REPLACE(REPLACE(price, '$', ''), ' ', '') AS REAL)) as avg_price
FROM airbnb_listings
WHERE price IS NOT NULL AND price != ''
GROUP BY neighbourhood, neighbourhood_group
HAVING listings_count >= 10
ORDER BY avg_price DESC
LIMIT 10;


-- ============================================================================
-- 3. AVAILABILITY ANALYSIS
-- ============================================================================

-- Average availability by neighbourhood group
SELECT 
    neighbourhood_group,
    COUNT(*) as listings_count,
    AVG(availability_365) as avg_availability,
    MIN(availability_365) as min_availability,
    MAX(availability_365) as max_availability
FROM airbnb_listings
WHERE availability_365 IS NOT NULL
GROUP BY neighbourhood_group
ORDER BY avg_availability DESC;

-- Listings with high availability (available more than 300 days)
SELECT 
    COUNT(*) as high_availability_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM airbnb_listings), 2) as percentage
FROM airbnb_listings
WHERE availability_365 > 300;


-- ============================================================================
-- 4. REVIEWS ANALYSIS
-- ============================================================================

-- Average number of reviews by room type
SELECT 
    room_type,
    COUNT(*) as listings_count,
    AVG(number_of_reviews) as avg_reviews,
    AVG(review_rate_number) as avg_rating,
    AVG(reviews_per_month) as avg_reviews_per_month
FROM airbnb_listings
WHERE number_of_reviews IS NOT NULL
GROUP BY room_type
ORDER BY avg_reviews DESC;

-- Top 10 most reviewed listings
SELECT 
    name,
    host_name,
    neighbourhood_group,
    neighbourhood,
    room_type,
    number_of_reviews,
    review_rate_number,
    CAST(REPLACE(REPLACE(price, '$', ''), ' ', '') AS REAL) as price
FROM airbnb_listings
WHERE number_of_reviews IS NOT NULL
ORDER BY number_of_reviews DESC
LIMIT 10;

-- Review rating distribution
SELECT 
    review_rate_number as rating,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM airbnb_listings WHERE review_rate_number IS NOT NULL), 2) as percentage
FROM airbnb_listings
WHERE review_rate_number IS NOT NULL
GROUP BY review_rate_number
ORDER BY rating DESC;


-- ============================================================================
-- 5. HOST ANALYSIS
-- ============================================================================

-- Top 10 hosts with most listings
SELECT 
    host_id,
    host_name,
    host_identity_verified,
    COUNT(*) as total_listings,
    AVG(CAST(REPLACE(REPLACE(price, '$', ''), ' ', '') AS REAL)) as avg_price,
    AVG(review_rate_number) as avg_rating
FROM airbnb_listings
GROUP BY host_id, host_name, host_identity_verified
ORDER BY total_listings DESC
LIMIT 10;

-- Verified vs unverified hosts
SELECT 
    host_identity_verified,
    COUNT(DISTINCT host_id) as unique_hosts,
    COUNT(*) as total_listings,
    AVG(review_rate_number) as avg_rating
FROM airbnb_listings
WHERE host_identity_verified IS NOT NULL
GROUP BY host_identity_verified;


-- ============================================================================
-- 6. ROOM TYPE DISTRIBUTION
-- ============================================================================

-- Distribution of room types by neighbourhood group
SELECT 
    neighbourhood_group,
    room_type,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY neighbourhood_group), 2) as percentage
FROM airbnb_listings
WHERE neighbourhood_group IS NOT NULL AND room_type IS NOT NULL
GROUP BY neighbourhood_group, room_type
ORDER BY neighbourhood_group, count DESC;


-- ============================================================================
-- 7. BOOKING POLICIES
-- ============================================================================

-- Distribution of cancellation policies
SELECT 
    cancellation_policy,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM airbnb_listings WHERE cancellation_policy IS NOT NULL), 2) as percentage
FROM airbnb_listings
WHERE cancellation_policy IS NOT NULL
GROUP BY cancellation_policy
ORDER BY count DESC;

-- Instant bookable vs non-instant bookable
SELECT 
    instant_bookable,
    COUNT(*) as count,
    AVG(CAST(REPLACE(REPLACE(price, '$', ''), ' ', '') AS REAL)) as avg_price,
    AVG(review_rate_number) as avg_rating
FROM airbnb_listings
WHERE instant_bookable IS NOT NULL
GROUP BY instant_bookable;


-- ============================================================================
-- 8. MINIMUM NIGHTS ANALYSIS
-- ============================================================================

-- Distribution of minimum nights requirements
SELECT 
    CASE 
        WHEN minimum_nights = 1 THEN '1 night'
        WHEN minimum_nights BETWEEN 2 AND 3 THEN '2-3 nights'
        WHEN minimum_nights BETWEEN 4 AND 7 THEN '4-7 nights'
        WHEN minimum_nights BETWEEN 8 AND 30 THEN '1-4 weeks'
        WHEN minimum_nights > 30 THEN 'More than 1 month'
        ELSE 'Unknown'
    END as min_nights_category,
    COUNT(*) as count,
    AVG(CAST(REPLACE(REPLACE(price, '$', ''), ' ', '') AS REAL)) as avg_price
FROM airbnb_listings
WHERE minimum_nights IS NOT NULL
GROUP BY min_nights_category
ORDER BY avg_price DESC;


-- ============================================================================
-- 9. CONSTRUCTION YEAR ANALYSIS
-- ============================================================================

-- Average price by construction year (grouped by decade)
SELECT 
    CAST((construction_year / 10) * 10 AS INTEGER) as decade,
    COUNT(*) as listings_count,
    AVG(CAST(REPLACE(REPLACE(price, '$', ''), ' ', '') AS REAL)) as avg_price,
    AVG(review_rate_number) as avg_rating
FROM airbnb_listings
WHERE construction_year IS NOT NULL AND price IS NOT NULL
GROUP BY decade
ORDER BY decade DESC;


-- ============================================================================
-- 10. GEOGRAPHIC ANALYSIS
-- ============================================================================

-- Listings by country
SELECT 
    country,
    country_code,
    COUNT(*) as listings_count,
    AVG(CAST(REPLACE(REPLACE(price, '$', ''), ' ', '') AS REAL)) as avg_price
FROM airbnb_listings
WHERE country IS NOT NULL
GROUP BY country, country_code
ORDER BY listings_count DESC;

-- Top 20 neighbourhoods by number of listings
SELECT 
    neighbourhood,
    neighbourhood_group,
    COUNT(*) as listings_count,
    AVG(CAST(REPLACE(REPLACE(price, '$', ''), ' ', '') AS REAL)) as avg_price,
    AVG(review_rate_number) as avg_rating,
    AVG(availability_365) as avg_availability
FROM airbnb_listings
WHERE neighbourhood IS NOT NULL
GROUP BY neighbourhood, neighbourhood_group
ORDER BY listings_count DESC
LIMIT 20;
