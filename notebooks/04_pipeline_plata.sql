-- Crear tabla dim_cliente
CREATE OR REPLACE TABLE catalogo_plata.ventas.dim_cliente
USING DELTA
AS
SELECT DISTINCT
  codigo_cliente,
  nombres,
  apellido_paterno,
  apellido_materno,
  sexo,
  fecha_nacimiento,
  region_cliente,
  descripcion_region,
  current_timestamp() AS fecha_carga
FROM catalogo_bronce.ventas.bronze_clientes;

-- Crear tabla dim_producto
CREATE OR REPLACE TABLE catalogo_plata.ventas.dim_producto
USING DELTA
AS
SELECT DISTINCT
  codigo_producto,
  descripcion_producto,
  CAST(valor_unitario AS DECIMAL(12,2)) AS valor_unitario,
  current_timestamp() AS fecha_carga
FROM catalogo_bronce.ventas.bronze_productos;

-- Crear tabla fact_ventas
CREATE OR REPLACE TABLE catalogo_plata.ventas.fact_ventas
USING DELTA
AS
SELECT
  v.codigo_cliente,
  v.codigo_producto,
  CAST(v.unidades_venta AS INT) AS unidades_venta,
  CAST(v.fecha_venta AS DATE) AS fecha_venta,
  CAST(v.monto_venta AS DECIMAL(15,2)) AS monto_venta,
  current_timestamp() AS fecha_carga
FROM catalogo_bronce.ventas.bronze_ventas v
WHERE v.monto_venta > 0;
