CREATE TABLE comments (
    id TEXT,
    documentType TEXT,
    lastModifiedDate TEXT,
    withdrawn TEXT,
    agencyID TEXT,
    title TEXT,
    objectId TEXT,
    postedDate TEXT
)

COPY COMMENTS
FROM '/Users/lucawilliams/Desktop/comment_data.csv'
DELIMITER ','
CSV HEADER