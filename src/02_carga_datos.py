import pandas as pd
from sqlalchemy import create_engine
import urllib

server = r'LAPTOP-KM7AEC0L\SQLEXPRESS'
database = 'DATAFUEL_SA'
driver = 'ODBC Driver 17 for SQL Server'

params = urllib.parse.quote_plus(
    f'DRIVER={{{driver}}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'Trusted_Connection=yes;'
)

engine = create_engine(
    f'mssql+pyodbc:///?odbc_connect={params}'
)

archivos_tablas = {
    'data/raw/Clientes.csv': 'Clientes',
    'data/raw/Proveedores.csv': 'Proveedores',
    'data/raw/Categorias.csv': 'Categorias',
    'data/raw/Empleados.csv': 'Empleados',
    'data/raw/Estaciones.csv': 'Estaciones',
    'data/raw/Equipos.csv': 'Equipos',
    'data/raw/Mantenimientos.csv': 'Mantenimientos',
    'data/raw/Productos.csv': 'Productos',
    'data/raw/Pedidos.csv': 'Pedidos',
    'data/raw/Detalles de Pedidos.csv': 'DetallePedidos'
}


def convertir_fecha_espanol(serie, nombre_columna):
    meses = {
        'ene': '01',
        'feb': '02',
        'mar': '03',
        'abr': '04',
        'may': '05',
        'jun': '06',
        'jul': '07',
        'ago': '08',
        'sep': '09',
        'sept': '09',
        'oct': '10',
        'nov': '11',
        'dic': '12'
    }

    originales = serie.copy()

    serie = (
        serie
        .astype(str)
        .str.lower()
        .str.strip()
    )

    for mes, numero in meses.items():
        serie = serie.str.replace(
            f'-{mes}-',
            f'-{numero}-',
            regex=False
        )

    fechas = pd.to_datetime(
        serie,
        format='%d-%m-%Y',
        errors='coerce'
    )

    invalidas = fechas.isna()

    if invalidas.any():
        print(
            f"\n❌ Se encontraron fechas inválidas "
            f"en la columna {nombre_columna}:"
        )

        print(
            pd.DataFrame({
                'Valor original': originales[invalidas]
            })
        )

        raise ValueError(
            f"Hay fechas inválidas en {nombre_columna}."
        )

    return fechas


def cargar_datos():

    print("Iniciando pipeline ETL sobre tablas simples...")

    for archivo, tabla in archivos_tablas.items():

        try:

            print(
                f"\nExtrayendo {archivo} "
                f"y cargando en la tabla {tabla}..."
            )

            if tabla in ['Categorias', 'Empleados']:
                encoding = 'latin-1'
            else:
                encoding = 'utf-8-sig'

            df = pd.read_csv(
                archivo,
                encoding=encoding,
                sep=';'
            )

            # =========================
            # CLIENTES
            # =========================

            if tabla == 'Clientes':

                df = df.rename(columns={
                    'Id. de cliente': 'IdCliente',
                    'Nombre de compañía': 'NombreCompania',
                    'Nombre del contacto': 'NombreContacto',
                    'Cargo del contacto': 'CargoContacto',
                    'Dirección': 'Direccion',
                    'Región': 'Region',
                    'Código postal': 'CodigoPostal',
                    'País': 'Pais',
                    'Teléfono': 'Telefono'
                })

                df.loc[
                    df['IdCliente'] == 'PLAL2',
                    'CodigoPostal'
                ] = '01-012'

            # =========================
            # EMPLEADOS
            # =========================

            elif tabla == 'Empleados':

                df = df.rename(columns={
                    'Id. de empleado': 'IdEmpleado',
                    'Fecha de nacimiento': 'FechaNacimiento',
                    'Fecha de contratación': 'FechaContratacion',
                    'Dirección': 'Direccion',
                    'Región': 'Region',
                    'Código postal': 'CodigoPostal',
                    'País': 'Pais',
                    'Teléfono de domicilio': 'TelefonoDomicilio',
                    'Extensión': 'Extension'
                })

                df = df.drop(
                    columns=['Jefe'],
                    errors='ignore'
                )

                df['FechaNacimiento'] = convertir_fecha_espanol(
                    df['FechaNacimiento'],
                    'FechaNacimiento'
                )

                df['FechaContratacion'] = convertir_fecha_espanol(
                    df['FechaContratacion'],
                    'FechaContratacion'
                )

            # =========================
            # PRODUCTOS
            # =========================

            elif tabla == 'Productos':

                df = df.rename(columns={
                    'Id. de producto': 'IdProducto',
                    'Nombre de producto': 'NombreProducto',
                    'Proveedor': 'IdProveedor',
                    'Categoria': 'IdCategoria',
                    'Cantidad por unidad': 'CantidadPorUnidad',
                    'Precio por unidad': 'PrecioPorUnidad',
                    'Unidades en existencia': 'UnidadesEnExistencia',
                    'Unidades pedidas': 'UnidadesPedidas',
                    'Nivel de nuevo pedido': 'NivelNuevoPedido'
                })

                df['PrecioPorUnidad'] = (
                    df['PrecioPorUnidad']
                    .astype(str)
                    .str.strip()
                    .str.replace(',', '.', regex=False)
                )

                df['PrecioPorUnidad'] = pd.to_numeric(
                    df['PrecioPorUnidad'],
                    errors='raise'
                )

                df['Suspendido'] = (
                    df['Suspendido']
                    .astype(str)
                    .str.strip()
                    .str.upper()
                    .map({
                        'VERDADERO': 1,
                        'FALSO': 0
                    })
                )

                if df['Suspendido'].isna().any():

                    raise ValueError(
                        "Se encontraron valores inválidos "
                        "en la columna Suspendido."
                    )

            # =========================
            # PEDIDOS
            # =========================

            elif tabla == 'Pedidos':

                df = df.rename(columns={
                    'Id# de pedido': 'IdPedido',
                    'Cliente': 'IdCliente',
                    'Empleado': 'IdEmpleado',
                    'Fecha de pedido': 'FechaPedido',
                    'Forma de env?': 'FormaEnvio',
                    'Fecha de entrega': 'FechaEntrega'
                })

                df['IdEstacion'] = (
                    df.index % 10
                ) + 1

            # =========================
            # DETALLE DE PEDIDOS
            # =========================

            elif tabla == 'DetallePedidos':

                df = df.rename(columns={
                    'Iddepedido': 'IdPedido',
                    'Producto': 'IdProducto'
                })

                # IdPedido + IdProducto ya no forman la clave primaria.
                # Las combinaciones repetidas son válidas y no deben
                # detener la carga del ETL.

                duplicados = df[
                    df.duplicated(
                        subset=['IdPedido', 'IdProducto'],
                        keep=False
                    )
                ]

                if not duplicados.empty:

                    print(
                        "\n⚠️ Se encontraron combinaciones repetidas "
                        "de IdPedido + IdProducto."
                    )

                    print(
                        duplicados[
                            [
                                'IdPedido',
                                'IdProducto',
                                'Cantidad',
                                'Descuento',
                                'Total',
                                'CostosDirectos',
                                'CostosIndirectos'
                            ]
                        ].to_string(index=False)
                    )

                else:

                    print(
                        "✓ No se encontraron combinaciones repetidas "
                        "de IdPedido + IdProducto."
                    )

            # =========================
            # DETECTAR IDENTITY
            # =========================

            with engine.connect() as conn:

                resultado = conn.exec_driver_sql(
                    """
                    SELECT COUNT(*)
                    FROM sys.identity_columns
                    WHERE object_id = OBJECT_ID(?)
                    """,
                    (f'dbo.{tabla}',)
                )

                tiene_identity = resultado.scalar() > 0

            # =========================
            # CARGAR DATOS
            # =========================

            # Solo se utiliza IDENTITY_INSERT cuando el DataFrame
            # contiene explícitamente la columna Identity.
            # En DetallePedidos no ocurre esto porque IdDetalle
            # es generado automáticamente por SQL Server.

            if tiene_identity and tabla != 'DetallePedidos':

                with engine.begin() as conn:

                    conn.exec_driver_sql(
                        f"SET IDENTITY_INSERT dbo.{tabla} ON"
                    )

                    df.to_sql(
                        tabla,
                        con=conn,
                        if_exists='append',
                        index=False
                    )

                    conn.exec_driver_sql(
                        f"SET IDENTITY_INSERT dbo.{tabla} OFF"
                    )

            else:

                df.to_sql(
                    tabla,
                    con=engine,
                    if_exists='append',
                    index=False
                )

            print(
                f"✓ {tabla} cargada correctamente."
            )

        except Exception as e:

            print(
                f"\n❌ Error durante la carga de {tabla}:"
            )

            print(e)

            break

    print("\nPipeline ETL finalizado.")


if __name__ == '__main__':
    cargar_datos()