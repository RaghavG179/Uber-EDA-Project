CREATE DATABASE uber_project;
USE uber_project;

CREATE TABLE uber_requests (
    request_id INT,
    pickup_point VARCHAR(20),
    driver_id INT,
    status VARCHAR(50),
    request_timestamp DATETIME,
    drop_timestamp DATETIME
);

SELECT COUNT(*) FROM uber_requests;

-- 📊 Query 1: Total ride requests grouped by status (Completed, Cancelled, No Cars Available)
SELECT status, COUNT(*) AS total_requests
FROM uber_requests
GROUP BY status;

-- 📊 Query 2: Count how many requests came from each pickup point (City vs Airport)
SELECT pickup_point, COUNT(*) AS total_requests
FROM uber_requests
GROUP BY pickup_point;

-- 📊 Query 3: Number of ride requests per hour of the day
SELECT HOUR(request_timestamp) AS request_hour, COUNT(*) AS total_requests
FROM uber_requests
GROUP BY request_hour
ORDER BY request_hour;

-- 📊 Query 4: Cancellation rate per hour of the day
SELECT 
  HOUR(request_timestamp) AS request_hour,
  COUNT(*) AS total_requests,
  SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) AS cancellations,
  ROUND(SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS cancellation_percent
FROM uber_requests
GROUP BY request_hour
ORDER BY request_hour;

-- 📊 Query 5: No Cars Available rate per hour
SELECT 
  HOUR(request_timestamp) AS request_hour,
  COUNT(*) AS total_requests,
  SUM(CASE WHEN status = 'No Cars Available' THEN 1 ELSE 0 END) AS no_cars,
  ROUND(SUM(CASE WHEN status = 'No Cars Available' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS unavailability_percent
FROM uber_requests
GROUP BY request_hour
ORDER BY request_hour;

-- 📊 Query 6: Time Slot-wise distribution of all request statuses
SELECT 
  CASE 
    WHEN HOUR(request_timestamp) < 4 THEN 'Night'
    WHEN HOUR(request_timestamp) < 8 THEN 'Early Morning'
    WHEN HOUR(request_timestamp) < 12 THEN 'Morning'
    WHEN HOUR(request_timestamp) < 16 THEN 'Afternoon'
    WHEN HOUR(request_timestamp) < 20 THEN 'Evening'
    ELSE 'Late Night'
  END AS time_slot,
  COUNT(*) AS total_requests,
  SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled,
  SUM(CASE WHEN status = 'No Cars Available' THEN 1 ELSE 0 END) AS no_cars,
  SUM(CASE WHEN status = 'Trip Completed' THEN 1 ELSE 0 END) AS completed,
  ROUND(SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS cancel_rate,
  ROUND(SUM(CASE WHEN status = 'No Cars Available' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS no_car_rate
FROM uber_requests
GROUP BY time_slot
ORDER BY FIELD(time_slot, 'Early Morning', 'Morning', 'Afternoon', 'Evening', 'Late Night', 'Night');

-- 📊 Query 7: Overall fulfillment rate (percentage of trips completed)
SELECT 
  ROUND(SUM(CASE WHEN status = 'Trip Completed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS fulfillment_rate_percent
FROM uber_requests;

-- 📊 Query 8: Cancellation percentage by pickup point (City vs Airport)
SELECT 
  pickup_point,
  COUNT(*) AS total_requests,
  SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled,
  ROUND(SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS cancellation_rate
FROM uber_requests
GROUP BY pickup_point;

-- 📊 Query 9: No Cars Available percentage by pickup point
SELECT 
  pickup_point,
  COUNT(*) AS total_requests,
  SUM(CASE WHEN status = 'No Cars Available' THEN 1 ELSE 0 END) AS no_cars,
  ROUND(SUM(CASE WHEN status = 'No Cars Available' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS no_car_rate
FROM uber_requests
GROUP BY pickup_point;

-- 📊 Query 10: Average ride request volume per hour slot
SELECT 
  HOUR(request_timestamp) AS hour,
  COUNT(*) AS total_requests,
  ROUND(AVG(COUNT(*)) OVER (), 2) AS avg_requests_per_hour
FROM uber_requests
GROUP BY hour
ORDER BY hour;

