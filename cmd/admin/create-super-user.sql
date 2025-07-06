CREATE EXTENSION IF NOT EXISTS pgcrypto;
INSERT INTO users (id, email, hashed_password, is_active, role, created_at, updated_at) VALUES (
    gen_random_uuid(), 'admin@example.ru', crypt('123', gen_salt('bf')), TRUE, 'ADMIN', now(), now()
);