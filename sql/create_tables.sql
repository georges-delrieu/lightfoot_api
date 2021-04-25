-- Importing UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Creation of footprint table
CREATE TABLE IF NOT EXISTS footprint (
  id INT NOT NULL,
  category varchar(250) NOT NULL,
  subcategory varchar(250) NOT NULL,
  item varchar(250) NOT NULL,
  footprint DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (id)
);


-- Loading CSV
COPY footprint("id", 
            "category", 
            "subcategory", 
            "item", 
            "footprint") 
FROM '/data/my_records.csv' DELIMITERS ',' CSV HEADER;

