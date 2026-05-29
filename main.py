# main.py
# Punto de entrada del generador de reportes de ventas.
#
# Uso:
#   python main.py
#   python main.py --input data/mi_archivo.csv --output reports/reporte.md

import argparse
import os
import sys
from datetime import datetime

from utils import cargar_datos, calcular_metricas, generar_reporte


def parsear_argumentos():
    """
    Define y procesa los argumentos de línea de comandos.
    Permite cambiar el archivo de entrada y salida sin tocar el código.
    """
    parser = argparse.ArgumentParser(
        description="Genera un reporte de ventas en Markdown a partir de un CSV."
    )
    parser.add_argument(
        "--input",
        default="data/sample.csv",
        help="Ruta al archivo CSV (default: data/sample.csv)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Ruta de salida del reporte (default: reports/reporte_YYYY-MM-DD.md)",
    )
    return parser.parse_args()


def construir_ruta_salida(ruta_custom: str | None) -> str:
    """
    Devuelve la ruta de salida del reporte.
    Si no se especifica una, genera el nombre con la fecha actual.
    """
    if ruta_custom:
        return ruta_custom

    os.makedirs("reports", exist_ok=True)
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    return f"reports/reporte_{fecha_hoy}.md"


def main():
    args = parsear_argumentos()
    ruta_entrada = args.input
    ruta_salida = construir_ruta_salida(args.output)

    # Cargar datos
    print(f"Leyendo datos desde: {ruta_entrada}")
    try:
        df = cargar_datos(ruta_entrada)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"{len(df)} transacciones cargadas.")

    # Calcular metricas
    metricas = calcular_metricas(df)

    print(f"Total facturado:      ${metricas['total_ventas']:>12,.2f}")
    print(f"Promedio por venta:   ${metricas['promedio_por_venta']:>12,.2f}")
    print(f"Producto mas vendido: {metricas['producto_mas_vendido']}")
    print(f"Categoria lider:      {metricas['ventas_por_categoria'].index[0]}")

    # Generar reporte
    print(f"\nGenerando reporte en: {ruta_salida}")
    generar_reporte(metricas, ruta_salida)


if __name__ == "__main__":
    main()
