CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    title TEXT,
    image TEXT,
    plot TEXT,
    embedding_plot VECTOR(1536),   
    embedding_title VECTOR(1536)
);

CREATE TABLE IF NOT EXISTS movies_local (
    id SERIAL PRIMARY KEY,
    title TEXT,
    image TEXT,
    plot TEXT,
    embedding_plot VECTOR(384),   
    embedding_title VECTOR(384)
);
