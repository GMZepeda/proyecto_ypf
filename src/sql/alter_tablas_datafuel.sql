-- Selecciona la base de datos sobre la que se van a ejecutar las instrucciones.
USE DATAFUEL_SA;
GO

-- Modifica la columna Notas de la tabla Empleados para permitir almacenar
-- una cantidad de texto mucho mayor (hasta el límite de NVARCHAR(MAX)).
ALTER TABLE Empleados
ALTER COLUMN Notas NVARCHAR(MAX);
GO

-- 1. Eliminar la restricción de Clave Primaria compuesta actual.
-- (Asegurate de que el nombre coincida con el de tu DDL original,
-- por ejemplo: PK_DetallePedidos)
ALTER TABLE dbo.DetallePedidos DROP CONSTRAINT PK_DetallePedidos;
GO

-- 2. Agregar la columna IdDetalle como clave primaria autoincremental.
-- IDENTITY(1,1) hace que SQL Server genere automáticamente los valores:
-- comienza en 1 y aumenta de a 1 por cada nuevo registro.
-- NOT NULL impide que la columna quede sin valor.
ALTER TABLE dbo.DetallePedidos
ADD IdDetalle INT IDENTITY(1,1) NOT NULL;
GO

-- 3. Crear nuevamente la Clave Primaria de la tabla.
-- Ahora IdDetalle será la clave primaria única de cada registro.
-- CLUSTERED indica que SQL Server organizará físicamente el índice
-- de la tabla en función de esta clave primaria.
ALTER TABLE dbo.DetallePedidos
ADD CONSTRAINT PK_DetallePedidos PRIMARY KEY CLUSTERED (IdDetalle);
GO
