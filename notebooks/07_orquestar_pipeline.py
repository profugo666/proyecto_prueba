#!/usr/bin/env python3
"""
Orquestador del pipeline Lakehouse:
Bronze -> Plata -> Oro
Ejecuta los SQL files en secuencia, dividiendo cada archivo en statements individuales.
"""

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.sql import StatementState
import time
import sys

WAREHOUSE_ID = "fbb8dd33a77ca3f4"

PIPELINE = [
    ("notebooks/03_crear_bronze.sql", "BRONZE: Carga desde volumen"),
    ("notebooks/04_pipeline_plata.sql", "PLATA: Modelo estrella"),
    ("notebooks/05_pipeline_oro.sql", "ORO: KPIs y agregaciones")
]

def limpiar_comentarios(sql):
    """Elimina comentarios de linea simple (--)."""
    lines = []
    for line in sql.split('\n'):
        if not line.strip().startswith('--'):
            lines.append(line)
    return '\n'.join(lines).strip()

def dividir_sql(sql):
    """Divide SQL en statements individuales por ; ignorando ; dentro de strings."""
    statements = []
    current = []
    in_string = False
    string_char = None
    
    for char in sql:
        if char in ("'", '"'):
            if not in_string:
                in_string = True
                string_char = char
            elif char == string_char:
                in_string = False
                string_char = None
        
        if char == ';' and not in_string:
            stmt = ''.join(current)
            stmt_limpio = limpiar_comentarios(stmt)
            if stmt_limpio:
                statements.append(stmt_limpio)
            current = []
        else:
            current.append(char)
    
    # Ultimo statement (sin ; al final)
    stmt = ''.join(current)
    stmt_limpio = limpiar_comentarios(stmt)
    if stmt_limpio:
        statements.append(stmt_limpio)
    
    return statements

def ejecutar_statement(w, sql, idx, total):
    sql_clean = limpiar_comentarios(sql)
    if not sql_clean:
        return True
    
    preview = sql_clean.replace('\n', ' ')[:70]
    print(f"   📌 Statement {idx}/{total}: {preview}...")
    
    resp = w.statement_execution.execute_statement(
        warehouse_id=WAREHOUSE_ID,
        statement=sql_clean,
        wait_timeout="0s"
    )
    
    statement_id = resp.statement_id
    
    while True:
        status = w.statement_execution.get_statement(statement_id)
        state = status.status.state
        
        if state in [StatementState.SUCCEEDED, StatementState.FAILED, 
                     StatementState.CANCELED, StatementState.CLOSED]:
            break
        
        print(f"      Estado: {state}...", end="\r")
        time.sleep(2)
    
    if state == StatementState.SUCCEEDED:
        print(f"      ✅ OK")
        return True
    else:
        print(f"      ❌ FALLIDO")
        if status.status.error:
            err = str(status.status.error)
            print(f"         Error: {err[:300]}")
        return False

def ejecutar_archivo(file_path, descripcion):
    print(f"\n{'='*60}")
    print(f"🚀 {descripcion}")
    print(f"📄 Archivo: {file_path}")
    print(f"{'='*60}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        sql = f.read()
    
    statements = dividir_sql(sql)
    print(f"   🔢 Statements encontrados: {len(statements)}")
    
    if not statements:
        print("   ❌ No se encontraron statements ejecutables")
        return False
    
    w = WorkspaceClient()
    
    for i, stmt in enumerate(statements, 1):
        if not ejecutar_statement(w, stmt, i, len(statements)):
            return False
    
    print(f"\n✅ {descripcion} -> COMPLETADO")
    return True

def main():
    print("🏭 INICIANDO PIPELINE LAKEHOUSE")
    print(f"🎯 Warehouse: {WAREHOUSE_ID}")
    
    for file_path, descripcion in PIPELINE:
        if not ejecutar_archivo(file_path, descripcion):
            print("\n💥 PIPELINE DETENIDO POR ERROR")
            sys.exit(1)
    
    print("\n" + "="*60)
    print("🎉 PIPELINE COMPLETADO EXITOSAMENTE")
    print("="*60)

if __name__ == "__main__":
    main()
