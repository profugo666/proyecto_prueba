-- Bronze incremental con COPY INTO (solo carga archivos nuevos)

COPY INTO catalogo_bronce.ventas.bronze_clientes
FROM '/Volumes/catalogo_bronce/ventas/archivos_ventas/clientes_1000.csv'
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true', 'delimiter' = '|', 'inferSchema' = 'true')
COPY_OPTIONS ('mergeSchema' = 'true');

COPY INTO catalogo_bronce.ventas.bronze_productos
FROM '/Volumes/catalogo_bronce/ventas/archivos_ventas/productos_100.csv'
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true', 'delimiter' = '|', 'inferSchema' = 'true')
COPY_OPTIONS ('mergeSchema' = 'true');

COPY INTO catalogo_bronce.ventas.bronze_ventas
FROM '/Volumes/catalogo_bronce/ventas/archivos_ventas/ventas_1000.csv'
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true', 'delimiter' = '|', 'inferSchema' = 'true')
COPY_OPTIONS ('mergeSchema' = 'true');
