-- 1. USERS table
CREATE TABLE tribe_users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(15),
    roles VARCHAR(50),
    skills TEXT,
    location VARCHAR(100),
    current_status VARCHAR(50)
);

-- 2. JOB_LISTERS table
CREATE TABLE job_listers (
    lister_id SERIAL PRIMARY KEY,
    user_id INT UNIQUE REFERENCES users(id),
    company_name VARCHAR(100),
    kyc_status VARCHAR(20) CHECK (kyc_status IN ('Pending', 'Verified', 'Rejected')),
    contact_email VARCHAR(100),
    contact_phone VARCHAR(15),
    created_at TIMESTAMP DEFAULT NOW()
);

-- 3. JOBS table
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    lister_id INT REFERENCES job_listers(lister_id),
    title VARCHAR(100),
    pay DECIMAL(10, 2),
    location VARCHAR(100),
    job_lat DECIMAL(9, 6),
    job_lon DECIMAL(9, 6),
    description TEXT
);

-- 4. APPLICATIONS table
CREATE TABLE tribe_applications (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    job_id INT REFERENCES jobs(id),
    status VARCHAR(20),
    applied_date TIMESTAMP DEFAULT NOW()
);
-- 1. IDENTIFICATION table
CREATE TABLE identification (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    id_type VARCHAR(50),
    id_number VARCHAR(100),
    doc_url TEXT,
    verified BOOLEAN
);

-- 2. FILTERS table
CREATE TABLE filters (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    skills TEXT,
    pay_range VARCHAR(50),
    distance VARCHAR(50),
    duration VARCHAR(50),
    time_availability VARCHAR(50)
);

-- 3. COMPLETED_JOBS table
CREATE TABLE completed_jobs (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    job_id INT REFERENCES jobs(id),
    rating INT CHECK (rating BETWEEN 1 AND 5),
    feedback TEXT,
    completed_date TIMESTAMP DEFAULT NOW()
);

create table studio_users(
 id INT PRIMARY KEY,
 name VARCHAR,
 phone VARCHAR,
 location VARCHAR
 );
-- Sellers table (PostgreSQL-compatible)
CREATE TABLE sellers (
    seller_id SERIAL PRIMARY KEY,
    user_id INT UNIQUE REFERENCES users(id),
    kyc_status VARCHAR(20) CHECK (kyc_status IN ('Pending', 'Verified', 'Rejected')),
    pickup_address VARCHAR(255),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    radius_km INT DEFAULT 10,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Products table (PostgreSQL-compatible)
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    category VARCHAR(100),
    subcategory VARCHAR(100),
    title VARCHAR(150),
    description TEXT,
    condition VARCHAR(20) CHECK (condition IN ('New', 'Used')),
    price DECIMAL(10,2),
    availability BOOLEAN
);

 create table _crypto_aead_det_encryptinventory(
 inventory_id INT PRIMARY KEY,
 seller_id INT,
 product_id INT,
 quantity_available INT,
 location VARCHAR,
 latitude DECIMAL(9,6),
 longitude DECIMAL(9,6),
 created_at TIMESTAMP DEFAULT NOW()
 );
 create table orders(
 id INT PRIMARY KEY,
 user_id INT,
 inventory_id INT,
 quantity INT,
 total_amount DECIMAL,
 payment_method VARCHAR,
 status VARCHAR,
 created_at TIMESTAMP
 );
 create table studio_reservations(
 id INT PRIMARY KEY,
 user_id INT,
 inventory_id INT,
 reservation_deposit DECIMAL,
 due_time TIMESTAMP,
 refund_percentage DECIMAL
 );
 create table studio_payments(
 id INT PRIMARY KEY,
 user_id INT,
 order_id INT,
 method VARCHAR,
 amount DECIMAL,
 status VARCHAR
 );
 

 CREATE TABLE pg_providers (
    provider_id SERIAL PRIMARY KEY,
    user_id INT UNIQUE REFERENCES users(id),
    provider_type VARCHAR(20) CHECK (provider_type IN ('Individual', 'Company')),
    kyc_status VARCHAR(20) CHECK (kyc_status IN ('Pending', 'Verified', 'Rejected')),
    bank_account VARCHAR(100),
    gst_number VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);
 CREATE TABLE properties (
    id SERIAL PRIMARY KEY,
    provider_id INT REFERENCES pg_providers(provider_id),
    location VARCHAR(100),
    room_type VARCHAR(10) CHECK (room_type IN ('Private', 'Shared')),
    budget_range VARCHAR(50),
    accessibility_features TEXT,
    images TEXT,
    house_rules TEXT
);
 CREATE TABLE room_units (
    unit_id SERIAL PRIMARY KEY,
    property_id INT REFERENCES properties(id),
    unit_type VARCHAR(20) CHECK (unit_type IN ('Single', 'Double', 'Dorm')),
    bed_count INT,
    current_status VARCHAR(20) CHECK (current_status IN ('Vacant', 'Booked', 'UnderMaintenance'))
);

 create table reservations(
 id INT PRIMARY KEY,
 user_id INT,
 property_id INT,
 status VARCHAR,
 deposit_paid BOOLEAN,
 timestamp TIMESTAMP,
 expiry_time TIMESTAMP
 );
 -- 1. Applications Table
CREATE TABLE applications (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    property_id INT REFERENCES properties(id),
    status VARCHAR(20) CHECK (status IN ('Pending', 'Accepted', 'Rejected'))
);

-- 2. Payments Table
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    method VARCHAR(20) CHECK (method IN ('UPI', 'Cash', 'Net Banking', 'Nia Wallet')),
    amount DECIMAL(10, 2),
    status VARCHAR(20),
    timestamp TIMESTAMP DEFAULT NOW()
);

