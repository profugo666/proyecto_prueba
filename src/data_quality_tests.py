from pyspark.sql import SparkSession
import sys

spark = SparkSession.builder.appName("DataQualityTests").getOrCreate()

TESTS = [
    ("bronze_clientes_not_null", 
     "SELECT COUNT(*) FROM catalogo_bronce.ventas.bronze_clientes WHERE codigo_cliente IS NULL", 0),
    ("bronze_ventas_positive", 
     "SELECT COUNT(*) FROM catalogo_bronce.ventas.bronze_ventas WHERE monto_venta <= 0", 0),
    ("plata_dim_cliente_unique", 
     "SELECT COUNT(*) - COUNT(DISTINCT codigo_cliente) FROM catalogo_plata.ventas.dim_cliente", 0),
    ("plata_fact_ventas_integrity", 
     "SELECT COUNT(*) FROM catalogo_plata.ventas.fact_ventas v LEFT JOIN catalogo_plata.ventas.dim_cliente c ON v.codigo_cliente = c.codigo_cliente WHERE c.codigo_cliente IS NULL", 0),
    ("oro_kpi_not_empty", 
     "SELECT COUNT(*) FROM catalogo_oro.ventas.kpi_ventas_mensual", 1),
]

print("🔍 EJECUTANDO TESTS DE CALIDAD DE DATOS")
print("="*60)

failed = 0
for test_name, query, expected in TESTS:
    result = spark.sql(query).collect()[0][0]
    status = "✅ PASS" if result == expected else "❌ FAIL"
    if result != expected:
        failed += 1
    print(f"{status} | {test_name}: resultado={result}, esperado={expected}")

print("="*60)
if failed > 0:
    print(f"💥 {failed} TESTS FALLARON")
    sys.exit(1)
else:
    print("🎉 TODOS LOS TESTS PASARON")
