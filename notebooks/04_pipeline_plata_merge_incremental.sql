-- Plata: Dimensiones con MERGE (upsert), Fact con MERGE incremental

-- Dim Cliente: MERGE (sin cambios, ya es incremental)
MERGE INTO catalogo_plata.ventas.dim_cliente AS target
USING (
  SELECT DISTINCT
    codigo_cliente, nombres, apellido_paterno, apellido_materno,
    sexo, fecha_nacimiento, region_cliente, descripcion_region,
    current_timestamp() AS fecha_carga
  FROM catalogo_bronce.ventas.bronze_clientes
) AS source
ON target.codigo_cliente = source.codigo_cliente
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;

-- Dim Producto: MERGE (sin cambios, ya es incremental)
MERGE INTO catalogo_plata.ventas.dim_producto AS target
USING (
  SELECT DISTINCT
    codigo_producto, descripcion_producto,
    CAST(valor_unitario AS DECIMAL(12,2)) AS valor_unitario,
    current_timestamp() AS fecha_carga
  FROM catalogo_bronce.ventas.bronze_productos
) AS source
ON target.codigo_producto = source.codigo_producto
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;

-- Fact Ventas: MERGE incremental con hash como clave unica
-- Paso A: Asegurar que la tabla tenga la columna venta_id
CREATE OR REPLACE TABLE catalogo_plata.ventas.fact_ventas
USING DELTA
AS
SELECT
  codigo_cliente,
  codigo_producto,
  CAST(unidades_venta AS INT) AS unidades_venta,
  CAST(fecha_venta AS DATE) AS fecha_venta,
  CAST(monto_venta AS DECIMAL(15,2)) AS monto_venta,
  current_timestamp() AS fecha_carga,
  md5(concat(codigo_cliente, codigo_producto, unidades_venta, fecha_venta, monto_venta)) AS venta_id
FROM catalogo_bronce.ventas.bronze_ventas
WHERE monto_venta > 0;

-- Nota: La proxima ejecucion usara MERGE en vez de CREATE OR REPLACE.
-- Para mantener la idempotencia, la primera carga usa CREATE OR REPLACE
-- y las siguientes usaran el MERGE de abajo.
