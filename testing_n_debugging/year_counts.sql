
  SELECT
    EXTRACT(YEAR FROM CAST(posteddate AS date)) AS year,
    COUNT(*) AS row_count
  FROM public.comments
  WHERE EXTRACT(YEAR FROM CAST(posteddate AS date)) BETWEEN 1800 AND 2024
  GROUP BY year
  ORDER BY year DESC
