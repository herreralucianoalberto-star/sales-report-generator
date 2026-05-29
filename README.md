# sales-report-generator

Script en Python que toma un CSV de ventas y genera un reporte en Markdown con las métricas básicas: total facturado, producto más vendido, desglose por categoría y evolución mensual.

Lo hice para automatizar algo que normalmente se haría a mano en Excel.

## Requisitos

- Python 3.10+
- pandas

```bash
pip install -r requirements.txt
```

## Uso

```bash
# Con el CSV de ejemplo incluido
python main.py

# Con tu propio archivo
python main.py --input data/mis_ventas.csv

# Definiendo también dónde guardar el reporte
python main.py --input data/mis_ventas.csv --output reports/enero.md
```

El reporte se guarda en `reports/reporte_YYYY-MM-DD.md`.

## Estructura del CSV

El archivo tiene que tener estas columnas:

```
fecha, producto, categoria, cantidad, precio_unitario
```

Las columnas `vendedor` y `region` son opcionales — si las incluyes, el reporte las usa.

## Estructura del proyecto

```
├── main.py          # punto de entrada
├── utils.py         # carga de datos, cálculos y generación del reporte
├── data/
│   └── sample.csv   # dataset de ejemplo
└── reports/         # aquí se guardan los reportes generados
```

## Ideas para extender el proyecto

- Exportar a `.xlsx` con openpyxl
- Graficar la evolución mensual con matplotlib
- Enviar el reporte por correo con smtplib
- Programarlo con cron para que corra solo cada semana
