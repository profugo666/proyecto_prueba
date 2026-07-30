# 🏭 Proyecto Ventas - Lakehouse Databricks

Pipeline de datos completo con arquitectura **Bronze-Plata-Oro** implementado en **Databricks** y orquestado con **GitHub Actions CI/CD**.

---

## 📋 Tabla de contenidos

- [Arquitectura](#arquitectura)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Tecnologías](#tecnologías)
- [Cómo ejecutar localmente](#cómo-ejecutar-localmente)
- [Pipeline CI/CD](#pipeline-cicd)
- [Dashboard](#dashboard)
- [Autor](#autor)

---

## 🏗️ Arquitectura

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   CSV Local     │────▶│  Volumen UC     │────▶│  Bronze Tables  │
│  (data/*.csv)   │     │ (archivos_ventas)│     │(catalogo_bronce)│
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                              ┌─────────────────────────┘
                              ▼
                       ┌─────────────────┐
                       │  Silver Tables  │
                       │ (catalogo_plata)│
                       │  Modelo Estrella│
                       │  MERGE + INSERT │
                       └─────────────────┘
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
        ┌──────────┐     ┌──────────┐     ┌──────────┐
        │KPI Mensual│     │KPI Región│     │KPI Prod. │
        │   (oro)   │     │   (oro)  │     │   (oro)  │
        └──────────┘     └──────────┘     └──────────┘
```

### Capas del Lakehouse

| Capa | Catálogo | Tablas | Tipo de carga |
|------|----------|--------|---------------|
| **Bronze** | `catalogo_bronce.ventas` | `bronze_clientes`, `bronze_productos`, `bronze_ventas` | `COPY INTO` (incremental) |
| **Plata** | `catalogo_plata.ventas` | `dim_cliente`, `dim_producto`, `fact_ventas` | `MERGE` (upsert) + `INSERT OVERWRITE` |
| **Oro** | `catalogo_oro.ventas` | `kpi_ventas_mensual`, `kpi_ventas_por_region`, `kpi_ventas_por_producto` | `CREATE OR REPLACE` |

---

## 📁 Estructura del proyecto

```
proyecto_prueba/
├── .github/
│   └── workflows/
│       └── databricks.yml          # CI/CD con GitHub Actions
├── config/
│   └── .gitkeep
├── data/                           # CSV generados (ignorados por git)
│   ├── clientes_100.csv
│   ├── clientes_1000.csv
│   ├── productos_100.csv
│   └── ventas_1000.csv
├── notebooks/
│   ├── 01_generar_datos.py         # Generación de datos sintéticos
│   ├── 02_cargar_a_bronze.py       # Carga inicial a volumen UC
│   ├── 03_crear_bronze_incremental.sql  # COPY INTO incremental
│   ├── 04_pipeline_plata_merge.sql      # MERGE dimensiones
│   ├── 05_pipeline_oro.sql               # KPIs y agregaciones
│   └── 06_dashboard_queries.sql          # Queries para AI/BI Dashboard
├── src/
│   ├── pipeline_job.py             # Orquestador del pipeline (job)
│   └── data_quality_tests.py       # Tests de calidad de datos
├── databricks.yml                  # Databricks Asset Bundle (DABs)
├── .gitignore
└── README.md                       # Este archivo
```

---

## 🛠️ Tecnologías

| Tecnología | Uso |
|------------|-----|
| **Databricks** | Lakehouse, Delta Lake, Unity Catalog, SQL Warehouse |
| **Databricks Asset Bundles** | Infraestructura como código (IaC) |
| **GitHub Actions** | CI/CD automatizado |
| **Python + Faker** | Generación de datos sintéticos |
| **Spark SQL** | Transformaciones en capas Bronze, Plata y Oro |
| **OpenCode** | IDE con agente de IA para desarrollo |

---

## 🚀 Cómo ejecutar localmente

### 1. Clonar el repositorio

```bash
git clone https://github.com/profugo666/proyecto_prueba.git
cd proyecto_prueba
```

### 2. Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
pip install databricks-sdk faker
```

### 3. Configurar Databricks CLI

```bash
databricks auth login --host https://dbc-d423249b-1c6b.cloud.databricks.com
```

### 4. Generar datos

```bash
python notebooks/01_generar_datos.py
```

### 5. Ejecutar pipeline local

```bash
python notebooks/07_orquestar_pipeline.py
```

### 6. Desplegar job en Databricks

```bash
databricks bundle deploy
databricks bundle run pipeline_ventas_lakehouse
```

---

## 🔄 Pipeline CI/CD

Cada push a `main` activa automáticamente:

1. **Validación** del bundle (`databricks bundle validate`)
2. **Despliegue** del job en Databricks (`databricks bundle deploy`)

El job está programado para ejecutarse **todos los días a las 6:00 AM (hora de Santiago)**.

![CI/CD Status](https://github.com/profugo666/proyecto_prueba/actions/workflows/databricks.yml/badge.svg)

---

## 📊 Dashboard

Las queries para el dashboard están en `notebooks/06_dashboard_queries.sql`. Para crear el dashboard en Databricks:

1. Ir a **SQL Editor** en tu workspace
2. Crear nuevo query y pegar el contenido de `06_dashboard_queries.sql`
3. Ejecutar cada query y usar **"Add to Dashboard"**
4. Configurar visualizaciones: líneas, barras, heatmap, tabla

---

## ✅ Tests de calidad

El pipeline incluye 5 tests automáticos que se ejecutan después de cada carga:

| Test | Descripción |
|------|-------------|
| `bronze_clientes_not_null` | Verifica que no hay clientes sin código |
| `bronze_ventas_positive` | Verifica que todas las ventas tienen monto > 0 |
| `plata_dim_cliente_unique` | Verifica unicidad de clientes en dimensión |
| `plata_fact_ventas_integrity` | Verifica integridad referencial fact → dim_cliente |
| `oro_kpi_not_empty` | Verifica que los KPIs tienen datos |

---

## 👤 Autor

**Manuel** — Ingeniero de Datos  
🔗 [GitHub](https://github.com/profugo666)

---

## 📄 Licencia

Proyecto de prueba para demostración de arquitectura Lakehouse con Databricks.
