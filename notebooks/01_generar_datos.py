import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "faker", "-q"])

import os
import pandas as pd
from faker import Faker
from datetime import date, timedelta

fake = Faker("es_ES")

os.makedirs("data", exist_ok=True)

# --- CLIENTES 100 ---

clientes_100 = []
for i in range(1, 101):
    codigo = f"CLI-{i:03d}"
    nombres = fake.first_name()
    apellido_p = fake.last_name()
    apellido_m = fake.last_name()
    sexo = fake.random_element(["M", "F"])
    fecha_inicio = date(1950, 1, 1)
    fecha_fin = date(2005, 12, 31)
    delta = (fecha_fin - fecha_inicio).days
    fecha_nac = fecha_inicio + timedelta(days=fake.random_int(min=0, max=delta))

    clientes_100.append({
        "codigo_cliente": codigo,
        "nombres": nombres,
        "apellido_paterno": apellido_p,
        "apellido_materno": apellido_m,
        "sexo": sexo,
        "fecha_nacimiento": fecha_nac,
    })

df_100 = pd.DataFrame(clientes_100)
df_100.to_csv("data/clientes_100.csv", sep="|", index=False, encoding="utf-8")
print(f"clientes_100.csv creado: {len(df_100)} registros")

# --- CLIENTES 1000 ---

regiones = ["Norte", "Sur", "Este", "Oeste", "Centro"]
clientes_1000 = []

for i in range(1, 1001):
    if i <= 100:
        reg = clientes_100[i - 1]
        codigo = reg["codigo_cliente"]
        nombres = reg["nombres"]
        apellido_p = reg["apellido_paterno"]
        apellido_m = reg["apellido_materno"]
        sexo = reg["sexo"]
        fecha_nac = reg["fecha_nacimiento"]
    else:
        codigo = f"CLI-{i:03d}"
        nombres = fake.first_name()
        apellido_p = fake.last_name()
        apellido_m = fake.last_name()
        sexo = fake.random_element(["M", "F"])
        fecha_inicio = date(1950, 1, 1)
        fecha_fin = date(2005, 12, 31)
        delta = (fecha_fin - fecha_inicio).days
        fecha_nac = fecha_inicio + timedelta(days=fake.random_int(min=0, max=delta))

    region = fake.random_element(regiones)
    clientes_1000.append({
        "codigo_cliente": codigo,
        "nombres": nombres,
        "apellido_paterno": apellido_p,
        "apellido_materno": apellido_m,
        "sexo": sexo,
        "fecha_nacimiento": fecha_nac,
        "region_cliente": region,
        "descripcion_region": f"Región {region}",
    })

df_1000 = pd.DataFrame(clientes_1000)
df_1000.to_csv("data/clientes_1000.csv", sep="|", index=False, encoding="utf-8")
print(f"clientes_1000.csv creado: {len(df_1000)} registros")

# --- PRODUCTOS 100 ---

productos_descripciones = [
    "Laptop Dell XPS", "Mouse Logitech MX", "Teclado Mecánico Redragon",
    "Monitor Samsung 27\"", "Auriculares Sony WH", "Webcam Logitech C920",
    "Disco Duro SSD 1TB", "Memoria RAM 16GB", "Procesador AMD Ryzen 7",
    "Tarjeta Gráfica RTX 4070", "Fuente de Poder 750W", "Gabinete Cooler Master",
    "Router TP-Link AX", "Impresora HP Laser", "Parlantes JBL Bluetooth",
    "Tablet Samsung Galaxy", "Celular iPhone 15", "Cable HDMI 2m",
    "Cargador USB-C 65W", "Pendrive SanDisk 128GB",
]

productos = []
for i in range(1, 101):
    codigo = f"PROD-{i:03d}"
    desc = fake.random_element(productos_descripciones)
    valor = fake.random_int(min=1000, max=500000)
    productos.append({
        "codigo_producto": codigo,
        "descripcion_producto": desc,
        "valor_unitario": valor,
    })

df_prod = pd.DataFrame(productos)
df_prod.to_csv("data/productos_100.csv", sep="|", index=False, encoding="utf-8")
print(f"productos_100.csv creado: {len(df_prod)} registros")

# --- VENTAS 1000 ---

precio_por_producto = {p["codigo_producto"]: p["valor_unitario"] for p in productos}
codigos_cliente = [f"CLI-{i:03d}" for i in range(1, 1001)]
codigos_producto = [p["codigo_producto"] for p in productos]

ventas = []
for _ in range(1000):
    cod_cli = fake.random_element(codigos_cliente)
    cod_prod = fake.random_element(codigos_producto)
    unidades = fake.random_int(min=1, max=50)
    fecha_inicio_venta = date(2023, 1, 1)
    fecha_fin_venta = date(2025, 12, 31)
    delta_venta = (fecha_fin_venta - fecha_inicio_venta).days
    fecha_venta = fecha_inicio_venta + timedelta(days=fake.random_int(min=0, max=delta_venta))
    monto = unidades * precio_por_producto[cod_prod]

    ventas.append({
        "codigo_cliente": cod_cli,
        "codigo_producto": cod_prod,
        "unidades_venta": unidades,
        "fecha_venta": fecha_venta,
        "monto_venta": monto,
    })

df_ventas = pd.DataFrame(ventas)
df_ventas.to_csv("data/ventas_1000.csv", sep="|", index=False, encoding="utf-8")
print(f"ventas_1000.csv creado: {len(df_ventas)} registros")
