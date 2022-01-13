SELECT  start_station_name, count(duration) as num_trips
FROM    `bigquery-public-data`.london_bicycles.cycle_hire
WHERE   duration >= @min_duration
GROUP BY start_station_name
ORDER BY num_trips DESC
LIMIT 10