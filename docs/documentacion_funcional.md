# PROYECTO DATAFUEL S.A. — DOCUMENTACIÓN FUNCIONAL

* **Versión:** 1.0
* **Proyecto:** DATAFUEL S.A. – Data Warehouse para la enseñanza de SQL, Power BI y Data Analytics
* **Autores (Grupo 5):**
  * Luciana Selene Agüero Lucero
  * Vanina Candelaria Sulca
  * Germán M. Zepeda
* **Fecha:** Septiembre 2026

---

## 1. Introducción
DATAFUEL S.A. es una empresa ficticia del sector energético creada con fines educativos para la enseñanza de herramientas de análisis de datos, modelado de bases de datos, SQL y Power BI.

La empresa se dedica a la comercialización de combustibles, lubricantes, insumos industriales y servicios técnicos, operando una red de estaciones de servicio y centros logísticos distribuidos en distintas regiones.

El objetivo del Data Warehouse es representar un escenario empresarial realista que permita desarrollar ejercicios de limpieza y transformación de datos, consultas SQL, modelado dimensional, análisis de indicadores y construcción de dashboards en Power BI.

---

## 2. Objetivos del Data Warehouse
El modelo fue diseñado para permitir el desarrollo de actividades relacionadas con:
* Modelado de datos
* Consultas SQL
* Power Query (Lenguaje M)
* Modelado en Power BI
* Creación de medidas DAX
* Limpieza y transformación de datos
* Análisis exploratorio
* Construcción de indicadores (KPIs)
* Visualización de información
* Análisis geográfico

---

## 3. Modelo de Negocio
DATAFUEL S.A. comercializa productos destinados al sector energético, abasteciendo tanto a clientes corporativos como a organizaciones públicas y privadas.

La empresa administra un catálogo de productos organizado por categorías, registra pedidos realizados por sus clientes y gestiona las operaciones comerciales a través de su equipo de ventas.

Además del proceso comercial, la organización controla sus activos físicos mediante estaciones de servicio, equipos industriales y planes de mantenimiento, integrando toda la información en un único Data Warehouse.

---

## 4. Pre-Entrega: Definición del Proyecto

### 4.1 Área de DATAFUEL S.A. Elegida
Se escogió el área de **Recursos Humanos**, focalizando principalmente en la gestión y rendimiento del personal comercial.

### 4.2 Tipo de Análisis
* **Enfoque:** Descriptivo (*"¿Qué pasó?"*)
* **Alcance:** Este tipo de análisis permitirá caracterizar la estructura demográfica y laboral del personal activo (antigüedad en la compañía, rangos etarios, cargos y distribución geográfica por ciudad y región), así como cuantificar el volumen histórico de operaciones gestionadas por cada colaborador.

### 4.3 Objetivo Principal del Análisis
Evaluar la estructura, antigüedad y desempeño operativo del equipo de colaboradores de DATAFUEL S.A. a partir de los registros de personal y transacciones comerciales, con el fin de detectar desequilibrios en la asignación de carga laboral, monitorear la eficiencia en el procesamiento de pedidos y proveer información para planes de capacitación y retención de talento.

### 4.4 Usuarios Destinados
* **Gerencia de Recursos Humanos:** Responsable de decisiones estratégicas de dotación, compensaciones y diseño de planes de carrera.
* **Jefatura de Personal y Desarrollo Organizacional:** Encargada del seguimiento operativo del desempeño, planes de capacitación y balance de carga de trabajo.
* **Dirección Comercial:** Interesada en la productividad por vendedor y cumplimiento de los tiempos de entrega pactados.

---

## 5. Modelo de Datos
El Data Warehouse de DATAFUEL S.A. está compuesto por dos Data Marts que representan los principales procesos de negocio de la organización:

| Data Mart | Objetivo | Tablas |
| :--- | :--- | :--- |
| **Data Mart Comercial** | Gestiona las operaciones de venta y comercialización de productos. | Categorías, Productos, Clientes, Empleados, Pedidos y Detalle de Pedidos. |
| **Data Mart de Infraestructura y Operaciones** | Gestiona los activos físicos de la empresa y el mantenimiento de las estaciones de servicio. | Proveedores, Estaciones, Equipos y Mantenimiento. |

### Diagrama Entidad-Relación (DER)
![Diagrama Entidad-Relación](DER_DATAFUEL_SA.png)

### Decisiones Técnicas Tomadas en el Proceso de Análisis
* En la tabla **Productos**, se renombraron los campos `Categoria` por `IdCategoria` y `Proveedor` por `IdProveedor` para evitar confusiones en la implementación del DER.
* En la tabla **DetallePedidos**, se renombró `Producto` por `IdProducto` para mantener la coherencia relacional con las demás entidades.
* En la tabla **Pedidos**, se renombraron `Cliente` por `IdCliente` y `Empleado` por `IdEmpleado`.
* En la tabla **Cliente**, se renombró `NombreCompañia` por `NombreCompania` para evitar caracteres especiales en los metadatos y prevenir errores de sintaxis y codificación.
* En el **MER** se vincula `Estaciones` con `Empleados` en una relación de `1:N`. Si bien en el DER original se respetó el diseño base, esta relación se considera estratégica para el entendimiento relacional del área de Recursos Humanos.

---

## 6. Diccionario de Datos

### 6.1 Tabla: Categorías
Clasifica los productos comercializados por DATAFUEL S.A. en diferentes grupos para facilitar la gestión comercial, el control del inventario y el análisis de ventas.

**Información General:**
| Propiedad | Valor |
| :--- | :--- |
| Tipo de tabla | Dimensión |
| Clave primaria | `IdCategoria` |
| Cantidad de registros | 8 |
| Relación | Productos |

**Campos:**
| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `IdCategoria` | Entero | Identificador único de la categoría. |
| `NombreCategoria` | Texto | Nombre de la categoría del producto. |
| `Imagen` | Texto | URL de la imagen representativa de la categoría. |

**Reglas de negocio:**
* Cada producto pertenece a una única categoría.
* Una categoría puede contener múltiples productos.
* Las categorías forman parte del catálogo maestro y presentan baja frecuencia de actualización.

---

### 6.2 Tabla: Productos
Contiene el catálogo de productos comercializados por DATAFUEL S.A., incluyendo información relacionada con proveedores, categorías, precios e inventario.

**Información General:**
| Propiedad | Valor |
| :--- | :--- |
| Tipo de tabla | Dimensión |
| Clave primaria | `IdProducto` |
| Relaciones | Categorías, Proveedores, DetallePedidos |

**Campos:**
| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `IdProducto` | Entero | Identificador único del producto. |
| `NombreProducto` | Texto | Nombre comercial del producto. |
| `IdProveedor` | Entero | Proveedor principal del producto. |
| `IdCategoria` | Entero | Categoría a la que pertenece el producto. |
| `CantidadPorUnidad` | Texto | Presentación comercial (formatos y unidades de medida). |
| `PrecioPorUnidad` | Decimal / Moneda | Precio unitario del producto. |
| `UnidadesEnExistencia` | Entero | Stock disponible en almacén. |
| `UnidadesPedidas` | Entero | Cantidad comprometida en pedidos en curso. |
| `NivelNuevoPedido` | Entero | Punto de reposición del producto. |
| `Suspendido` | Booleano | Indica si el producto continúa comercializándose. |

**Reglas de negocio:**
* Cada producto pertenece a un único proveedor y a una única categoría.
* Los productos suspendidos permanecen en el catálogo histórico de ventas para preservar la integridad referencial.

---

### 6.3 Tabla: Clientes
Almacena la información de los clientes corporativos de DATAFUEL S.A., incluyendo datos de contacto y ubicación geográfica para análisis comercial.

**Información General:**
| Propiedad | Valor |
| :--- | :--- |
| Tipo de tabla | Dimensión |
| Clave primaria | `IdCliente` |
| Relaciones | Pedidos |

**Campos:**
| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `IdCliente` | Texto | Identificador alfanumérico único del cliente. |
| `NombreCompania` | Texto | Razón social del cliente. |
| `NombreContacto` | Texto | Persona de contacto principal. |
| `CargoContacto` | Texto | Cargo del contacto en su empresa. |
| `Direccion` | Texto | Dirección fiscal o comercial. |
| `Ciudad` | Texto | Ciudad sede. |
| `Region` | Texto | Provincia, estado o región (admite nulos). |
| `CodigoPostal` | Texto | Código postal. |
| `Pais` | Texto | País sede. |
| `Telefono` | Texto | Teléfono principal. |
| `Fax` | Texto | Número de fax (admite nulos). |

**Reglas de negocio:**
* Un cliente puede realizar múltiples pedidos a lo largo del tiempo.
* Permite análisis de segmentación territorial por país, región y ciudad.

---

### 6.4 Tabla: Empleados
Contiene la información del personal de DATAFUEL S.A., incluyendo datos personales, demográficos y laborales.

**Información General:**
| Propiedad | Valor |
| :--- | :--- |
| Tipo de tabla | Dimensión |
| Clave primaria | `IdEmpleado` |
| Relaciones | Pedidos |

**Campos:**
| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `IdEmpleado` | Entero | Identificador único del colaborador. |
| `Apellidos` | Texto | Apellidos del colaborador. |
| `Nombre` | Texto | Nombres del colaborador. |
| `Cargo` | Texto | Puesto desempeñado en la organización. |
| `Tratamiento` | Texto | Tratamiento formal de cortesía. |
| `FechaNacimiento` | Fecha | Fecha de nacimiento (permite cálculo etario). |
| `FechaContratacion` | Fecha | Fecha de ingreso (permite cálculo de antigüedad). |
| `Direccion` | Texto | Dirección de residencia. |
| `Ciudad` | Texto | Ciudad de residencia. |
| `Region` | Texto | Provincia o región de residencia. |
| `CodigoPostal` | Texto | Código postal. |
| `Pais` | Texto | País de residencia. |
| `TelefonoDomicilio` | Texto | Teléfono de contacto personal. |
| `Extension` | Entero | Número de interno telefónico corporativo. |
| `Notas` | Texto | Perfil profesional y trayectoria interna. |

**Reglas de negocio:**
* Un colaborador comercial puede gestionar múltiples pedidos.
* Las fechas de contratación y nacimiento son la base para indicadores demográficos de Recursos Humanos.

---

### 6.5 Tabla: Pedidos
Registra las cabeceras de transacciones comerciales, vinculando clientes, colaboradores responsables y tiempos logísticos.

**Información General:**
| Propiedad | Valor |
| :--- | :--- |
| Tipo de tabla | Hechos (Cabecera) |
| Clave primaria | `IdPedido` |
| Relaciones | Clientes, Empleados, DetallePedidos |

**Campos:**
| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `IdPedido` | Entero | Identificador único de la transacción. |
| `IdCliente` | Texto | Cliente que emite el pedido. |
| `IdEmpleado` | Entero | Vendedor responsable del pedido. |
| `FechaPedido` | Fecha / Hora | Fecha y hora de emisión de la orden. |
| `FormaEnvio` | Entero | Código de la modalidad logística de envío. |
| `FechaEntrega` | Fecha | Fecha prevista o efectiva de recepción. |

**Reglas de negocio:**
* Cada pedido es gestionado por un único empleado.
* La granularidad a nivel producto se resuelve en la tabla de detalle.

---

### 6.6 Tabla: Detalle de Pedidos
Contiene la granularidad de línea de producto por orden comercial, registrando volúmenes, descuentos aplicados y estructura de costos.

**Información General:**
| Propiedad | Valor |
| :--- | :--- |
| Tipo de tabla | Hechos (Líneas transaccionales) |
| Clave primaria | Compuesta (`IdPedido`, `IdProducto`) |
| Relaciones | Pedidos, Productos |

**Campos:**
| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `IdPedido` | Entero | Orden comercial asociada. |
| `IdProducto` | Entero | Producto comercializado. |
| `Cantidad` | Entero | Unidades vendidas. |
| `Descuento` | Decimal (Porcentaje) | Tasa de descuento aplicada sobre la línea. |
| `Total` | Decimal / Moneda | Importe facturado neto. |
| `CostosDirectos` | Decimal / Moneda | Costo directo imputado al lote. |
| `CostosIndirectos` | Decimal / Moneda | Costos operativos indirectos prorrateados. |

**Reglas de negocio:**
* Un pedido puede contener uno o más productos.
* Los costos directos e indirectos son la base para el margen de contribución y rentabilidad operativa.

---

### 6.7 Tabla: Proveedores
Almacena los proveedores estratégicos de insumos, repuestos y combustibles.

**Información General:**
| Propiedad | Valor |
| :--- | :--- |
| Tipo de tabla | Dimensión |
| Clave primaria | `IdProveedor` |
| Cantidad de registros | 10 |
| Relaciones | Productos |

**Campos:**
| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `IdProveedor` | Entero | Identificador único del proveedor. |
| `NombreProveedor` | Texto | Razón social o denominación comercial. |
| `Ciudad` | Texto | Ciudad de radicación. |
| `Telefono` | Texto | Teléfono de contacto comercial. |
| `Email` | Texto | Correo electrónico institucional. |

---

### 6.8 Tabla: Estaciones
Contiene la red de estaciones de servicio administradas por DATAFUEL S.A.

**Información General:**
| Propiedad | Valor |
| :--- | :--- |
| Tipo de tabla | Dimensión |
| Clave primaria | `IdEstacion` |
| Cantidad de registros | 10 |
| Relaciones | Pedidos, Equipos |

**Campos:**
| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `IdEstacion` | Entero | Identificador de la sucursal/estación. |
| `NombreEstacion` | Texto | Nombre de fantasía de la estación. |
| `Ciudad` | Texto | Ciudad donde opera. |
| `Provincia` | Texto | Provincia donde se ubica. |
| `Tipo` | Texto | Modalidad operativa (`Propia` o `Franquicia`). |
| `FechaApertura` | Fecha | Fecha de inauguración de la estación. |

---

### 6.9 Tabla: Equipos
Inventario de activos fijos e industriales instalados en cada estación.

**Información General:**
| Propiedad | Valor |
| :--- | :--- |
| Tipo de tabla | Dimensión |
| Clave primaria | `IdEquipo` |
| Cantidad de registros | 30 |
| Relaciones | Estaciones, Mantenimientos |

**Campos:**
| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `IdEquipo` | Entero | Identificador del activo físico. |
| `IdEstacion` | Entero | Estación de servicio donde opera. |
| `TipoEquipo` | Texto | Tipo de maquinaria (Surtidor, Tanque, Compresor GNC, Bomba, etc.). |
| `Modelo` | Texto | Modelo técnico o código de fabricante. |
| `Estado` | Texto | Condición de servicio (Disponible, En mantenimiento, Fuera de servicio). |

---

### 6.10 Tabla: Mantenimientos
Registro histórico de intervenciones y servicio técnico sobre los equipos de la red.

**Información General:**
| Propiedad | Valor |
| :--- | :--- |
| Tipo de tabla | Hechos (Eventos de servicio) |
| Clave primaria | `IdMantenimiento` |
| Cantidad de registros | 50 |
| Relaciones | Equipos |

**Campos:**
| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `IdMantenimiento` | Entero | Identificador único de la intervención. |
| `IdEquipo` | Entero | Equipo intervenido. |
| `FechaMantenimiento` | Fecha | Fecha de ejecución del servicio (período 2009–2020). |
| `TipoMantenimiento` | Texto | Categoría (Preventivo, Correctivo, Inspección, Calibración, Reemplazo). |
| `Costo` | Decimal / Moneda | Gasto incurrido en repuestos y mano de obra. |

---

## 7. Próximas Mejoras
* Implementación del **Modelo Estrella** optimizado para Power BI.
* Definición formal de **KPIs de negocio** y tablero de control.
* Creación del **Diccionario de medidas DAX**.
* Desarrollo y despliegue del **Dashboard interactivo**.