CREATE TABLE IF NOT EXISTS items (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  price NUMERIC(10,2) NOT NULL
);

INSERT INTO items (name, price) VALUES
('Cuaderno', 1990.00),
('Lápiz', 500.00),
('Mochila', 15990.00);
