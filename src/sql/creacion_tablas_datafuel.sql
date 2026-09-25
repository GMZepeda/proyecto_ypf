-- Script DDL: Creación de BD y Tablas

CREATE DATABASE DATAFUEL_SA;
GO

USE DATAFUEL_SA;
GO
-- Creación de Tablas Dimensionales

-- Dimensión Clientes
CREATE TABLE Clientes (
    IdCliente NVARCHAR(100) NOT NULL,
    NombreCompania NVARCHAR(100) NOT NULL,
    NombreContacto NVARCHAR(50) NOT NULL,
    CargoContacto NVARCHAR(50) NOT NULL,
    Direccion NVARCHAR(50) NOT NULL,
    Ciudad NVARCHAR(50) NOT NULL,
    Region NVARCHAR(50) NULL,
    CodigoPostal NVARCHAR(50) NOT NULL,
    Pais NVARCHAR(50) NOT NULL,
    Telefono NVARCHAR(50) NOT NULL,
    Fax NVARCHAR(50) NULL,
    CONSTRAINT PK_Clientes PRIMARY KEY CLUSTERED (IdCliente)
);

GO

-- Dimensión Proveedores
CREATE TABLE Proveedores (
    IdProveedor INT IDENTITY(1,1) NOT NULL,
    NombreProveedor NVARCHAR(100) NOT NULL,
    Ciudad NVARCHAR(50) NOT NULL,
    Telefono NVARCHAR(50) NOT NULL,
    Email NVARCHAR(50) NOT NULL,
    CONSTRAINT PK_Proveedores PRIMARY KEY CLUSTERED (IdProveedor)
);
GO

-- Dimensión Categorías
CREATE TABLE Categorias (
    IdCategoria INT IDENTITY(1,1) NOT NULL,
    NombreCategoria NVARCHAR(100) NOT NULL,
    Imagen NVARCHAR(100) NULL,
    CONSTRAINT PK_Categorias PRIMARY KEY CLUSTERED (IdCategoria)
);
GO
-- Dimensión Empleados
CREATE TABLE Empleados (
    IdEmpleado INT IDENTITY(1,1) NOT NULL,
    Apellidos NVARCHAR(50) NOT NULL,
    Nombre NVARCHAR(50) NOT NULL,
    Cargo NVARCHAR(50) NOT NULL,
    Tratamiento NVARCHAR(50) NOT NULL,
    FechaNacimiento DATE NOT NULL,
    FechaContratacion DATE NOT NULL,
    Direccion NVARCHAR(50) NOT NULL,
    Ciudad NVARCHAR(50) NOT NULL,
    Region NVARCHAR(50) NULL,
    CodigoPostal NVARCHAR(50) NOT NULL,
    Pais NVARCHAR(50) NOT NULL,
    TelefonoDomicilio NVARCHAR(50) NOT NULL,
    Extension INT NOT NULL,
    Notas NVARCHAR(50) NOT NULL,
    CONSTRAINT PK_Empleados PRIMARY KEY CLUSTERED (IdEmpleado)
);
GO

-- Dimensión Estaciones
CREATE TABLE Estaciones (
    IdEstacion INT IDENTITY(1,1) NOT NULL,
    NombreEstacion NVARCHAR(100) NOT NULL,
    Ciudad NVARCHAR(50) NOT NULL,
    Provincia NVARCHAR(50) NULL,
    Tipo NVARCHAR(100) NOT NULL,
    FechaApertura DATE NOT NULL,
    CONSTRAINT PK_Estaciones PRIMARY KEY CLUSTERED (IdEstacion)
);

GO

-- Dimensión Equipos
CREATE TABLE Equipos (
    IdEquipo INT IDENTITY(1,1) NOT NULL,
    TipoEquipo NVARCHAR(100) NOT NULL,
    Modelo NVARCHAR(100) NOT NULL,
    Estado NVARCHAR(100) NULL,
    IdEstacion INT NOT NULL,
    CONSTRAINT PK_Equipos PRIMARY KEY CLUSTERED (IdEquipo),
    CONSTRAINT FK_Equipos_Estaciones FOREIGN KEY (IdEstacion) REFERENCES Estaciones(IdEstacion)
);
GO

-- Dimensión Mantenimientos 
CREATE TABLE Mantenimientos (
    IdMantenimiento INT IDENTITY(1,1) NOT NULL,
    FechaMantenimiento DATE NOT NULL,
    TipoMantenimiento NVARCHAR(100) NOT NULL,
    Costo DECIMAL(18,2) NOT NULL,
    IdEquipo INT NOT NULL,
    CONSTRAINT PK_Mantenimientos PRIMARY KEY CLUSTERED (IdMantenimiento),
    CONSTRAINT FK_Mantenimientos_Equipos FOREIGN KEY (IdEquipo) REFERENCES Equipos(IdEquipo)
);
GO

-- Dimensión Productos
CREATE TABLE Productos (
    IdProducto INT IDENTITY(1,1) NOT NULL,
    NombreProducto NVARCHAR(100) NOT NULL,
    CantidadPorUnidad NVARCHAR(100) NOT NULL,
    PrecioPorUnidad DECIMAL(18,2) NOT NULL,
    UnidadesEnExistencia INT NOT NULL,
    UnidadesPedidas INT NOT NULL,
    NivelNuevoPedido INT NOT NULL,
    Suspendido BIT NOT NULL,
    IdProveedor INT NOT NULL,
    IdCategoria INT NOT NULL,
    CONSTRAINT PK_Productos PRIMARY KEY CLUSTERED (IdProducto),
    CONSTRAINT FK_Productos_Proveedores FOREIGN KEY (IdProveedor) REFERENCES Proveedores(IdProveedor),
    CONSTRAINT FK_Productos_Categorias FOREIGN KEY (IdCategoria) REFERENCES Categorias(IdCategoria)
);
GO

-- Creación de Tablas de Hechos

-- Tabla de Hechos Pedidos
CREATE TABLE Pedidos (
    IdPedido INT IDENTITY(1,1) NOT NULL,
    FechaPedido DATETIME NOT NULL,
    FormaEnvio INT NOT NULL,
    FechaEntrega DATE NOT NULL,
    IdCliente NVARCHAR(100) NOT NULL,
    IdEmpleado INT NOT NULL,
    IdEstacion INT NOT NULL,
    CONSTRAINT PK_Pedidos PRIMARY KEY CLUSTERED (IdPedido),
    CONSTRAINT FK_Pedidos_Clientes FOREIGN KEY (IdCliente) REFERENCES Clientes(IdCliente),
    CONSTRAINT FK_Pedidos_Empleados FOREIGN KEY (IdEmpleado) REFERENCES Empleados(IdEmpleado),
    CONSTRAINT FK_Pedidos_Estaciones FOREIGN KEY (IdEstacion) REFERENCES Estaciones(IdEstacion)
);

GO

-- Tabla de Hechos Detalle de Pedidos
CREATE TABLE DetallePedidos (
    Cantidad INT NOT NULL,
    Descuento DECIMAL(18,2) NOT NULL,
    Total DECIMAL(18,2) NOT NULL,
    CostosDirectos DECIMAL(18,2) NOT NULL,
    CostosIndirectos DECIMAL(18,2) NOT NULL,
    IdPedido INT NOT NULL,
    IdProducto INT NOT NULL,
-- PK compuesta por Pedido y Producto
    CONSTRAINT PK_DetallePedidos PRIMARY KEY (IdPedido, IdProducto),
    CONSTRAINT FK_DetallePedidos_Pedidos FOREIGN KEY (IdPedido) REFERENCES Pedidos(IdPedido),
    CONSTRAINT FK_DetallePedidos_Productos FOREIGN KEY (IdProducto) REFERENCES Productos(IdProducto)
);

