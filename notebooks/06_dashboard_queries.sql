-- ============================================================
-- DASHBOARD: KPIs de Ventas
-- Ejecutar estas queries y usar "Add to Dashboard" en Databricks
-- ============================================================

-- 1. VENTAS MENSUALES (Gráfico de líneas / área)
SELECT 
  anio, 
  mes, 
  total_ventas,
  cantidad_transacciones,
  ticket_promedio
FROM catalogo_oro.ventas.kpi_ventas_mensual
ORDER BY anio, mes;

-- 2. VENTAS POR REGIÓN (Gráfico de barras / donut)
SELECT 
  region_cliente,
  total_ventas,
  ranking_ventas
FROM catalogo_oro.ventas.kpi_ventas_por_region
ORDER BY ranking_ventas;

-- 3. TOP 10 PRODUCTOS (Gráfico de barras horizontales)
SELECT 
  descripcion_producto,
  total_ventas,
  contribucion_porcentaje
FROM catalogo_oro.ventas.kpi_ventas_por_producto
ORDER BY total_ventas DESC
LIMIT 10;

-- 4. EVOLUCIÓN DEL TICKET PROMEDIO (Gráfico de líneas)
SELECT 
  CONCAT(anio, '-', LPAD(mes, 2, '0')) AS periodo,
  ticket_promedio
FROM catalogo_oro.ventas.kpi_ventas_mensual
ORDER BY anio, mes;

-- 5. TABLA DETALLE DE VENTAS RECIENTES (Tabla con filtros)
SELECT 
  v.codigo_cliente,
  c.nombres,
  c.apellido_paterno,
  c.region_cliente,
  p.descripcion_producto,
  v.unidades_venta,
  v.monto_venta,
  v.fecha_venta
FROM catalogo_plata.ventas.fact_ventas v
JOIN catalogo_plata.ventas.dim_cliente c ON v.codigo_cliente = c.codigo_cliente
JOIN catalogo_plata.ventas.dim_producto p ON v.codigo_producto = p.codigo_producto
ORDER BY v.fecha_venta DESC
LIMIT 100;

-- 6. DISTRIBUCIÓN DE VENTAS POR MES (Heatmap)
SELECT 
  anio,
  mes,
  total_ventas
FROM catalogo_oro.ventas.kpi_ventas_mensual
ORDER BY anio, mes;
