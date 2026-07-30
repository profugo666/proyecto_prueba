from pyspark.sql import SparkSession
import os
import sys

spark = SparkSession.builder.appName("PipelineVentasIncremental").getOrCreate()

SCRIPT_PATH = os.path.abspath(sys.argv[0])
BASE_DIR = os.path.dirname(os.path.dirname(SCRIPT_PATH))

def ejecutar_archivo_sql(ruta_relativa, descripcion):
    ruta = os.path.join(BASE_DIR, ruta_relativa)
    print(f"\n{'='*60}")
    print(f"🚀 {descripcion}")
    print(f"📄 {ruta}")
    print(f"{'='*60}")
    
    with open(ruta, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    statements = []
    for stmt in contenido.split(';'):
        lines = [l for l in stmt.split('\n') if not l.strip().startswith('--')]
        sql = '\n'.join(lines).strip()
        if sql:
            statements.append(sql)
    
    for i, sql in enumerate(statements, 1):
        print(f"   📌 Statement {i}/{len(statements)}: {sql[:60]}...")
        spark.sql(sql)
        print(f"      ✅ OK")
    
    print(f"\n✅ {descripcion} -> COMPLETADO")

# Pipeline incremental completo
ejecutar_archivo_sql("notebooks/03_crear_bronze_incremental.sql", "BRONZE: COPY INTO incremental (solo archivos nuevos)")
ejecutar_archivo_sql("notebooks/04_pipeline_plata_merge_incremental.sql", "PLATA: MERGE dimensiones + CREATE fact con venta_id")
ejecutar_archivo_sql("notebooks/04_pipeline_plata_fact_merge.sql", "PLATA: MERGE incremental en fact_ventas")
ejecutar_archivo_sql("notebooks/05_pipeline_oro_incremental.sql", "ORO: MERGE incremental KPIs mensual/producto + INSERT OVERWRITE region")

print("\n" + "="*60)
print("🎉 PIPELINE INCREMENTAL COMPLETADO EXITOSAMENTE")
print("="*60)
print("\nNota: En la PRIMERA ejecucion, 04_pipeline_plata_merge_incremental.sql")
print("      hace CREATE OR REPLACE de fact_ventas con venta_id.")
print("      En ejecuciones subsecuentes, el MERGE solo inserta ventas nuevas.")
