-- Oro: KPIs con MERGE incremental (excepto ranking que necesita recalcularse)

-- KPI Mensual: MERGE por (anio, mes)
MERGE INTO catalogo_oro.ventas.kpi_ventas_mensual AS target
USING (
  SELECT
    YEAR(fecha_venta) AS anio,
    MONTH(fecha_venta) AS mes,
    SUM(monto_venta) AS total_ventas,
    SUM(unidades_venta) AS total_unidades,
    CASE WHEN COUNT(*) > 0 THEN SUM(monto_venta) / COUNT(*) ELSE 0 END AS ticket_promedio,
    COUNT(*) AS cantidad_transacciones,
    current_timestamp() AS fecha_actualizacion
  FROM catalogo_plata.ventas.fact_ventas
  GROUP BY YEAR(fecha_venta), MONTH(fecha_venta)
) AS source
ON target.anio = source.anio AND target.mes = source.mes
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;

-- KPI Producto: MERGE por (codigo_producto)
MERGE INTO catalogo_oro.ventas.kpi_ventas_por_producto AS target
USING (
  WITH totales AS (
    SELECT SUM(monto_venta) AS total_general FROM catalogo_plata.ventas.fact_ventas
  )
  SELECT
    p.codigo_producto,
    p.descripcion_producto,
    SUM(v.monto_venta) AS total_ventas,
    SUM(v.unidades_venta) AS total_unidades,
    ROUND(SUM(v.monto_venta) / t.total_general * 100, 2) AS contribucion_porcentaje,
    current_timestamp() AS fecha_actualizacion
  FROM catalogo_plata.ventas.fact_ventas v
  JOIN catalogo_plata.ventas.dim_producto p ON v.codigo_producto = p.codigo_producto
  CROSS JOIN totales t
  GROUP BY p.codigo_producto, p.descripcion_producto, t.total_general
) AS source
ON target.codigo_producto = source.codigo_producto
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;

-- KPI Region: INSERT OVERWRITE (el ranking es global y debe recalcularse completo)
-- Nota: Son solo 5 regiones, el costo es minimo. El ranking depende de TODAS las regiones.
INSERT OVERWRITE catalogo_oro.ventas.kpi_ventas_por_region
SELECT
  c.region_cliente,
  SUM(v.monto_venta) AS total_ventas,
  SUM(v.unidades_venta) AS total_unidades,
  RANK() OVER (ORDER BY SUM(v.monto_venta) DESC) AS ranking_ventas,
  current_timestamp() AS fecha_actualizacion
FROM catalogo_plata.ventas.fact_ventas v
JOIN catalogo_plata.ventas.dim_cliente c ON v.codigo_cliente = c.codigo_cliente
GROUP BY c.region_cliente;
