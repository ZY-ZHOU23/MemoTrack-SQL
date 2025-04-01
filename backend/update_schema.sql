-- Make category_id nullable in entries table
ALTER TABLE entries ALTER COLUMN category_id DROP NOT NULL;
