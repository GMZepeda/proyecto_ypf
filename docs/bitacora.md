# Bitácora de Desarrollo - DATAFUEL S.A.

## Sesión de Trabajo - [4-10-2026]

### 1. Conexión a SQL Server
* Conexión establecida desde Python mediante SQLAlchemy y `pyodbc`.
* Servidor: `LAPTOP-KM7AEC0L\SQLEXPRESS`
* Base de datos: `DATAFUEL_SA`
* Autenticación: Windows (Trusted Connection).

### 2. Pipeline ETL (`src/02_carga_datos.py`)
* Implementación de un script en Python para extraer desde archivos CSV, transformar y cargar a SQL Server utilizando `pandas.to_sql()`.

### 3. Decisiones Técnicas y Transformaciones
* **Tablas Simples Originales:** Se decidió mantener las tablas transaccionales originales (`Clientes`, `Proveedores`, `Categorias`, `Empleados`, `Estaciones`, `Equipos`, `Mantenimientos`, `Productos`, `Pedidos`, `DetallePedidos`) preservando las restricciones de integridad y claves foráneas definidas en el DDL.
* **Mapeo de Columnas (Clientes):** Adaptación de nombres del CSV (ej. *Id. de cliente* a `IdCliente`) y corrección manual del código postal faltante para el cliente `PLAL2` (`01-012`).
* **Proveedores y Categorías:** Conservación de los IDs del CSV habilitando inserciones con `IDENTITY` en SQL Server.
* **Empleados:**
  * Eliminación de la columna `Jefe` (ausente en el esquema SQL).
  * Conversión de fechas en formato español (ej. `08-dic-1968`) a formato numérico/fecha.
  * Modificación de la columna `Notas` en SQL Server a `NVARCHAR(MAX)`.
* **Productos:**
  * Transformación del precio (ej. `29,70` a `29.70` tipo numérico).
  * Conversión de valores booleanos (`VERDADERO` / `FALSO` a `1` / `0`).
* **Pedidos:**
  * Generación sintética autorizada del atributo faltante `IdEstacion` mediante Python (`(df.index % 10) + 1`).
* **DetallePedidos (Situación Actual):**
  * Detección de filas duplicadas en el CSV original que comparten la misma combinación `(IdPedido, IdProducto)` pero con distintas métricas (cantidades, totales, costos).
  * **Acción pendiente:** Inspeccionar la estructura física de la tabla con `EXEC sp_help 'DetallePedidos';` en SSMS antes de refactorizar la clave primaria o incorporar una clave subrogada (`IdDetalle`).
  