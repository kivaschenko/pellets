DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS offers CASCADE;
DROP TABLE IF EXISTS goods;
DROP TABLE IF EXISTS goods_offers;
-- Create a schema to hold data
CREATE schema pellets_schema;
-- Create 'users' table
CREATE TABLE pellets_schema.users (
	user_id serial PRIMARY KEY,
	username VARCHAR ( 50 ) UNIQUE NOT NULL,
	password VARCHAR ( 50 ) NOT NULL,
	email VARCHAR ( 255 ) UNIQUE NOT NULL,
	created_on TIMESTAMP NOT NULL,
    last_login TIMESTAMP 
);
-- Create 'offers' table
CREATE TABLE pellets_schema.offers (
    id serial PRIMARY KEY,
    type_offer VARCHAR ( 10 ) NOT NULL,
    goods VARCHAR ( 120 ) NOT NULL,
    amount INTEGER NOT NULL,
    price NUMERIC NOT NULL,
    incoterms VARCHAR ( 5 ) NOT NULL,
    address VARCHAR ( 255 ) NOT NULL,
    create_on TIMESTAMP NOT NULL,
    expired_date DATE NOT NULL,
    -- BLOB
    image BYTEA,
    -- geometry
    -- geom POINT,
    -- foreign key
    user_id INTEGER NOT NULL,
    -- characteristics
    diameter INTEGER NOT NULL,
    length_min NUMERIC NOT NULL,
    length_max NUMERIC NOT NULL,
    bulk_density NUMERIC NOT NULL,
    net_calorific_value NUMERIC NOT NULL,
    moisture_content INTEGER NOT NULL,
    fines INTEGER NOT NULL,
    mechanical_durability NUMERIC NOT NULL,
    ash_content NUMERIC NOT NULL,
    ash_melting_temp INTEGER NOT NULL,
    chlorine_content NUMERIC,
    sulphur_content NUMERIC,
	nitrogen_content NUMERIC,
	copper_content NUMERIC,
	chromium_content NUMERIC,
	arsenic_content NUMERIC,
	cadmium_content NUMERIC,
	mercury_content INTEGER,
	lead_content INTEGER,
	nickel_content INTEGER,
    CONSTRAINT fk_offer_user
        FOREIGN KEY (user_id) 
        REFERENCES pellets_schema.users (user_id)
        ON DELETE SET NULL
);
-- Add a spatial column to the table
SELECT AddGeometryColumn (
    'pellets_schema',
    'offers',
    'geom',
    4326,
    'POINT',
    2
);
-- Create 'goods' table
CREATE TABLE pellets_schema.goods (
    id serial PRIMARY KEY,
    name VARCHAR ( 120 ) UNIQUE NOT NULL,
    body TEXT
);
-- Create 'goods_offers' table 
CREATE TABLE pellets_schema.goods_offers (
    goods_id INTEGER NOT NULL,
    offer_id INTEGER NOT NULL,
    PRIMARY KEY (goods_id, offer_id),
    CONSTRAINT fk_goods
        FOREIGN KEY (goods_id) 
        REFERENCES pellets_schema.goods (id)
        ON DELETE CASCADE,
    CONSTRAINT fk_offer
        FOREIGN KEY (offer_id) 
        REFERENCES pellets_schema.offers (id)
        ON DELETE CASCADE
);