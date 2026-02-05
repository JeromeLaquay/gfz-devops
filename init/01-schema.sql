-- Table users
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    name VARCHAR(255)
);

-- Table newsletter_subscribers
CREATE TABLE IF NOT EXISTS newsletter_subscribers (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
);

-- Table contact
CREATE TABLE IF NOT EXISTS contact (
    id BIGSERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    sujet VARCHAR(255),
    message TEXT NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table offres_emploi
CREATE TABLE IF NOT EXISTS offres_emploi (
    id BIGSERIAL PRIMARY KEY,
    titre VARCHAR(255) NOT NULL,
    type VARCHAR(100),
    localisation VARCHAR(255),
    duree VARCHAR(100),
    date_expiration DATE,
    resume TEXT
);

-- Table articles
CREATE TABLE IF NOT EXISTS articles (
    id BIGSERIAL PRIMARY KEY,
    titre VARCHAR(255) NOT NULL,
    image TEXT,
    contenu TEXT,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
