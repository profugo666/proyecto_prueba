from pyspark.sql import SparkSession
import os
import sys

spark = SparkSession.builder.appName("PipelineVentas").getOrCreate()

# sys.argv[0] funciona en spark_python_task donde __file__ no existe
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

ejecutar_archivo_sql("notebooks/03_crear_bronze.sql", "BRONZE: Carga desde volumen")
ejecutar_archivo_sql("notebooks/04_pipeline_plata.sql", "PLATA: Modelo estrella")
ejecutar_archivo_sql("notebooks/05_pipeline_oro.sql", "ORO: KPIs y agregaciones")

print("\n" + "="*60)
print("🎉 PIPELINE COMPLETADO EXITOSAMENTE")
print("="*60)
