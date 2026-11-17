# PROYECTO DATAFUEL S.A.

## Descripción del Proyecto
DATAFUEL S.A. es una empresa ficticia del sector energético diseñada para un entorno académico y profesional de Data Analytics e Inteligencia Artificial. El proyecto implementa un Data Warehouse completo dividido en dos Data Marts orientados a la gestión comercial y a la infraestructura operativa.

## Estructura del Repositorio
- `dashboards/`: Almacena los tableros interactivos desarrollados en Power BI.
- `data/`: Contiene los datos crudos y procesados *(excluido del control de versiones mediante `.gitignore`)*.
- `docs/`: Documentación funcional, diccionario de datos y diagrama Entidad-Relación (DER).
- `notebooks/`: Cuadernos de Jupyter para análisis exploratorio (EDA) y prototipado.
- `src/`: Código fuente modularizado (scripts de Python, consultas SQL y transformaciones en Power Query).

## Tecnologías Utilizadas
- SQL Server / T-SQL (Gestionado mediante **SQL Server Management Studio**)
- Python (Pandas)
- Power BI & Power Query (Lenguaje M)
- Git & GitHub

## Dashboard en Power BI

El dashboard interactivo fue desarrollado en **Power BI Desktop**, utilizando como base el modelo dimensional en estrella de **DATAFUEL S.A.**

Se encuentran disponibles los siguientes entregables del proyecto:

- **Reporte completo en PDF:** [Ver / Descargar DATAFUEL_Dashboard.pdf](./docs/DATAFUEL_Dashboard.pdf)
- **Archivo fuente editable (.pbix):** [Descargar DATAFUEL_Dashboard.pbix](./docs/DATAFUEL_Dashboard.pbix)
- **Documentación funcional:** [Consultar documentacion_funcional.md](./docs/documentacion_funcional.md)

> **Nota:** Debido a que no se cuenta con una suscripción a Power BI Service para publicar el informe en la web, se proporciona el reporte exportado en formato PDF, junto con el archivo fuente (.pbix), que permite abrir, explorar y modificar el dashboard localmente mediante Power BI Desktop.