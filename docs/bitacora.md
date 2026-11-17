# Bitácora de Desarrollo - DATAFUEL S.A.

## Sesión de Trabajo 4-10-2026

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
  
## Sesión de Trabajo  7-10-2026

### Problema en DetallePedidos
El CSV contiene combinaciones repetidas de IdPedido + IdProducto, pero, luego de inspeccionar la estructura física de la tabla con `EXEC sp_help 'DetallePedidos';` se observa que en SQL Server esa combinación está definida como clave primaria.
Por eso, el ETL falla al intentar cargar los datos.

Tenemos que:
  1. Modificar la estructura de DetallePedidos.
  2. Crear un IdDetalle como clave primaria.
  3. Mantener IdPedido e IdProducto como claves foráneas.
  4. Luego adaptar el ETL para cargar el CSV correctamente.

El script de alteración quedó documentado en el archivo correspondiente `alter_tablas_datafuel.sql`.

Se ejecutó el script de alteración de DetallePedidos, reemplazando la clave primaria compuesta por IdDetalle como clave subrogada autoincremental. Posteriormente se adaptó el ETL para permitir combinaciones repetidas de IdPedido + IdProducto y delegar la generación de IdDetalle a SQL Server. La carga completa del ETL finalizó correctamente.

## Sesión de Trabajo  12-10-2026

**Análisis de Negocio:** Ejecución de consultas SQL para responder preguntas comerciales. Los resultados y sus respectivos insights analíticos fueron integrados exitosamente en la documentación funcional.

## Sesión de Trabajo  5-11-2026

**Diseño e Implementación del Modelo Dimensional:** Transformación y estructuración del modelo relacional original en un Modelo Estrella (Star Schema) optimizado para análisis en Power BI.

**Descripción técnica:** 

- Se consolidó la tabla de hechos central FACT_Ventas (a partir de la unión de Pedidos y DetallePedidos), conteniendo las métricas cuantitativas del negocio (cantidades, precios, descuentos y montos facturados).
- Se definieron y conectaron las tablas dimensionales satélite: DIM_Clientes, DIM_Empleados, DIM_Productos y DIM_Calendario.
- Se establecieron relaciones unidireccionales de 1 a varios ($1:\infty$) con filtro cruzado único desde cada dimensión hacia la tabla de hechos, garantizando integridad referencial, consistencia en los filtros cruzados y un rendimiento analítico óptimo en DAX.

## Sesión de Trabajo  14-11-2026

**Creación de Medidas DAX y Configuración de KPIs Ejecutivos:** Implementación de la tabla técnica *Medidas* y construcción del bloque superior de indicadores clave de rendimiento (KPIs) en Power BI.

**Descripción técnica:**
- Se formularon en DAX las métricas principales del negocio: Total Facturado (SUM), Unidades Vendidas (SUM), Cantidad Pedidos (DISTINCTCOUNT) y Ticket Promedio (DIVIDE).
- Se maquetó la primera fila de tarjetas KPI en el lienzo, aplicando validación de datos cruzada contra consultas SQL previas ($2,46M facturados, 141.636 unidades, 4.612 pedidos y $533,87 de ticket medio).
- Se ajustó el formato de visualización (Callouts / Valores ➔ Mostrar unidades: Ninguno) para evitar el redondeo automático y exponer valores exactos requeridos por la gerencia.

## Sesión de Trabajo  15-11-2026

**Creación y Configuración del Dashboard:** Construcción de las solapas, configuración de visualizaciones e interacciones, y definición formal de KPIs.
