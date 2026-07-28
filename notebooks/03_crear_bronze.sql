-- Crear tabla bronze de clientes
CREATE OR REPLACE TABLE catalogo_bronce.ventas.bronze_clientes
USING DELTA
AS
SELECT * FROM read_files(
  '/Volumes/catalogo_bronce/ventas/archivos_ventas/clientes_1000.csv',
  format => 'csv',
  header => true,
  delimiter => '|',
  inferSchema => true
);

-- Crear tabla bronze de productos
CREATE OR REPLACE TABLE catalogo_bronce.ventas.bronze_productos
USING DELTA
AS
SELECT * FROM read_files(
  '/Volumes/catalogo_bronce/ventas/archivos_ventas/productos_100.csv',
  format => 'csv',
  header => true,
  delimiter => '|',
  inferSchema => true
);

-- Crear tabla bronze de ventas
CREATE OR REPLACE TABLE catalogo_bronce.ventas.bronze_ventas
USING DELTA
AS
SELECT * FROM read_files(
  '/Volumes/catalogo_bronce/ventas/archivos_ventas/ventas_1000.csv',
  format => 'csv',
  header => true,
  delimiter => '|',
  inferSchema => true
);
