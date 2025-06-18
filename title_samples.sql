-- @pgsql Chat Query Editor (localhost)

-- Only "comment on..."
SELECT comments.id, comments.title
FROM public.comments
WHERE title ILIKE 'comment on%'
ORDER BY random()
LIMIT 1000;

-- Excluding "comment on..."
SELECT comments.id, comments.title
FROM public.comments
WHERE title NOT ILIKE 'comment on %'
ORDER BY random()
LIMIT 1000;

-- Completely random sample
SELECT comments.id, comments.title
FROM public.comments
ORDER BY random()
LIMIT 1000;