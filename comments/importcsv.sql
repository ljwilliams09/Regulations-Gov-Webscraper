CREATE TABLE comments_v2 (
    id TEXT,
    documentType TEXT,
    lastModifiedDate TEXT,
    withdrawn TEXT,
    agencyID TEXT,
    title TEXT,
    objectId TEXT,
    postedDate TEXT
)

COPY comments_v2
FROM '/Users/lucawilliams/Desktop/comment_data_v2.csv'
DELIMITER ','
CSV HEADER