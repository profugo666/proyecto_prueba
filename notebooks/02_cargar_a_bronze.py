from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import AlreadyExists, BadRequest, ResourceAlreadyExists
from databricks.sdk.service.catalog import VolumeType

w = WorkspaceClient()

try:
    w.schemas.create(catalog_name="catalogo_bronce", name="ventas")
    print("Schema 'ventas' creado en catalogo_bronce")
except (AlreadyExists, BadRequest):
    print("Ya existe, continuando...")

try:
    w.volumes.create(
        catalog_name="catalogo_bronce",
        schema_name="ventas",
        name="archivos_ventas",
        volume_type=VolumeType.MANAGED,
    )
    print("Volumen 'archivos_ventas' creado en catalogo_bronce.ventas")
except (AlreadyExists, BadRequest, ResourceAlreadyExists):
    print("Ya existe, continuando...")

# --- Subir archivos CSV al volumen ---

import os

volume_path = "/Volumes/catalogo_bronce/ventas/archivos_ventas"
files = [
    "data/clientes_100.csv",
    "data/clientes_1000.csv",
    "data/productos_100.csv",
    "data/ventas_1000.csv",
]

for file in files:
    dest_path = f"{volume_path}/{os.path.basename(file)}"
    with open(file, "rb") as f:
        w.files.upload(file_path=dest_path, contents=f)
    print(f"Subido: {dest_path}")
