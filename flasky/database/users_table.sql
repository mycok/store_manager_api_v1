-- CREATE TYPE DESCP AS ENUM ('Admin', 'Attendant');


CREATE TABLE IF NOT EXISTS users (
  user_id TEXT NOT NULL PRIMARY KEY,
  username VARCHAR(255) DEFAULT NULL,
  email VARCHAR(255) DEFAULT NULL,
  password VARCHAR(255) DEFAULT NULL,
  role VARCHAR(255) DEFAULT 'Admin',
  created_timestamp TIMESTAMP DEFAULT NOW()
);

-- INSERT INTO users (user_id, username, email, password) VALUES(23489657345, 'kibuuka', 'me2@mail.com', '$2a$12$IQR112ysyLTUO1RfJWzkUejOLpJzz7xlGG.PykpYn9k72hnROEf.O
-- ');