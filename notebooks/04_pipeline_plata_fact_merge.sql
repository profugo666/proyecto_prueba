-- Fact Ventas: MERGE incremental (ejecutar en corridas subsecuentes)
MERGE INTO catalogo_plata.ventas.fact_ventas AS target
USING (
  SELECT
    codigo_cliente,
    codigo_producto,
    CAST(unidades_venta AS INT) AS unidades_venta,
    CAST(fecha_venta AS DATE) AS fecha_venta,
    CAST(monto_venta AS DECIMAL(15,2)) AS monto_venta,
    current_timestamp() AS fecha_carga,
    md5(concat(codigo_cliente, codigo_producto, unidades_venta, fecha_venta, monto_venta)) AS venta_id
  FROM catalogo_bronce.ventas.bronze_ventas
  WHERE monto_venta > 0
) AS source
ON target.venta_id = source.venta_id
WHEN NOT MATCHED THEN INSERT *;
