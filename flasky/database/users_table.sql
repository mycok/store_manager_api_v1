
CREATE TABLE IF NOT EXISTS users (
  user_id TEXT NOT NULL,
  username VARCHAR(255) DEFAULT NULL,
  email VARCHAR(255) DEFAULT NULL,
  password VARCHAR(255) DEFAULT NULL,
  role VARCHAR(255) DEFAULT 'Admin',
  created_timestamp TIMESTAMP DEFAULT NOW()
);
-- INSERT INTO users (user_id, username, email, password, role) values ('9627135611406336821', 'Mich', 'sss@r.com', '$2a$12$tjE8pOWbFnZuqxR42fI0lufwDXJAezC6kWSmJay2BqQtaAiW9ZZuC', 'Admin');