-- Migration pour rendre la colonne password nullable et ajouter reset_token
-- À exécuter si la table users existe déjà avec une contrainte NOT NULL sur password

-- Rendre la colonne password nullable
ALTER TABLE users ALTER COLUMN password DROP NOT NULL;

-- Ajouter la colonne reset_token si elle n'existe pas
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'reset_token'
    ) THEN
        ALTER TABLE users ADD COLUMN reset_token VARCHAR(255);
    END IF;
END $$;
