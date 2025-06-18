CREATE TABLE IF NOT EXISTS comments (
    id TEXT,
    documentType TEXT,
    lastModifiedDate TEXT,
    withdrawn TEXT,
    agencyID TEXT,
    title TEXT,
    objectId TEXT,
    postedDate TEXT
);

COPY comments
FROM "/Users/lucawilliams/Desktop/comment_data.csv"
DELIMITER ','
CSV HEADER;