# utils.py
# Funciones de carga, análisis y generación del reporte.

import pandas as pd
from datetime import datetime


def cargar_datos(ruta_csv: str) -> pd.DataFrame:
    """
    Carga el CSV y valida que tenga las columnas necesarias.

    Args:
        ruta_csv: Ruta al archivo CSV.

    Returns:
        DataFrame con una columna extra 'total_venta' (cantidad * precio_unitario).

    Raises:
        FileNotFoundError: Si el archivo no existe.
        ValueError: Si faltan columnas obligatorias.
    """
    columnas_requeridas = {"fecha", "producto", "categoria", "cantidad", "precio_unitario"}

    try:
        df = pd.read_csv(ruta_csv, parse_dates=["fecha"])
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontro el archivo: {ruta_csv}")

    columnas_faltantes = columnas_requeridas - set(df.columns)
    if columnas_faltantes:
        raise ValueError(f"El CSV no tiene las columnas: {columnas_faltantes}")

    df["total_venta"] = df["cantidad"] * df["precio_unitario"]

    return df


def calcular_metricas(df: pd.DataFrame) -> dict:
    """
    Calcula las metricas del reporte a partir del DataFrame.

    Args:
        df: DataFrame con los datos de ventas.

    Returns:
        Diccionario con todas las metricas calculadas.
    """
    metricas = {}

    metricas["total_ventas"] = df["total_venta"].sum()
    metricas["total_transacciones"] = len(df)
    metricas["promedio_por_venta"] = df["total_venta"].mean()
    metricas["venta_maxima"] = df["total_venta"].max()
    metricas["venta_minima"] = df["total_venta"].min()

    ventas_por_producto = df.groupby("producto")["cantidad"].sum().sort_values(ascending=False)
    metricas["producto_mas_vendido"] = ventas_por_producto.index[0]
    metricas["unidades_producto_top"] = int(ventas_por_producto.iloc[0])
    metricas["ranking_productos"] = ventas_por_producto

    metricas["ventas_por_categoria"] = (
        df.groupby("categoria")["total_venta"]
        .sum()
        .sort_values(ascending=False)
    )

    df["mes"] = df["fecha"].dt.to_period("M")
    metricas["ventas_por_mes"] = (
        df.groupby("mes")["total_venta"]
        .sum()
        .sort_index()
    )

    if "vendedor" in df.columns:
        ventas_por_vendedor = df.groupby("vendedor")["total_venta"].sum().sort_values(ascending=False)
        metricas["top_vendedor"] = ventas_por_vendedor.index[0]
        metricas["ventas_top_vendedor"] = ventas_por_vendedor.iloc[0]
        metricas["ranking_vendedores"] = ventas_por_vendedor

    metricas["fecha_inicio"] = df["fecha"].min().strftime("%d/%m/%Y")
    metricas["fecha_fin"] = df["fecha"].max().strftime("%d/%m/%Y")

    return metricas


def generar_reporte(metricas: dict, ruta_salida: str) -> None:
    """
    Escribe el reporte en formato Markdown.

    Args:
        metricas: Diccionario con las metricas del analisis.
        ruta_salida: Ruta donde se guarda el archivo .md.
    """
    ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    lineas = []

    lineas.append("# Reporte de Ventas\n")
    lineas.append(f"**Generado el:** {ahora}  ")
    lineas.append(f"**Periodo:** {metricas['fecha_inicio']} - {metricas['fecha_fin']}\n")
    lineas.append("---\n")

    lineas.append("## Resumen\n")
    lineas.append("| Metrica                  | Valor          |")
    lineas.append("|--------------------------|----------------|")
    lineas.append(f"| Total facturado          | ${metricas['total_ventas']:,.2f} |")
    lineas.append(f"| Transacciones            | {metricas['total_transacciones']} |")
    lineas.append(f"| Promedio por transaccion | ${metricas['promedio_por_venta']:,.2f} |")
    lineas.append(f"| Venta mas alta           | ${metricas['venta_maxima']:,.2f} |")
    lineas.append(f"| Venta mas baja           | ${metricas['venta_minima']:,.2f} |")
    lineas.append("")

    lineas.append("## Producto mas vendido\n")
    lineas.append(
        f"**{metricas['producto_mas_vendido']}** — "
        f"{metricas['unidades_producto_top']} unidades vendidas.\n"
    )

    lineas.append("### Ranking por unidades\n")
    lineas.append("| Producto | Unidades |")
    lineas.append("|----------|----------|")
    for producto, unidades in metricas["ranking_productos"].items():
        lineas.append(f"| {producto} | {int(unidades)} |")
    lineas.append("")

    lineas.append("## Ventas por categoria\n")
    lineas.append("| Categoria | Total |")
    lineas.append("|-----------|-------|")
    for categoria, total in metricas["ventas_por_categoria"].items():
        lineas.append(f"| {categoria} | ${total:,.2f} |")
    lineas.append("")

    lineas.append("## Evolucion mensual\n")
    lineas.append("| Mes | Total |")
    lineas.append("|-----|-------|")
    for mes, total in metricas["ventas_por_mes"].items():
        lineas.append(f"| {mes} | ${total:,.2f} |")
    lineas.append("")

    if "ranking_vendedores" in metricas:
        lineas.append("## Vendedores\n")
        lineas.append(f"Mejor del periodo: **{metricas['top_vendedor']}** (${metricas['ventas_top_vendedor']:,.2f})\n")
        lineas.append("| Vendedor | Total |")
        lineas.append("|----------|-------|")
        for vendedor, total in metricas["ranking_vendedores"].items():
            lineas.append(f"| {vendedor} | ${total:,.2f} |")
        lineas.append("")

    lineas.append("---")
    lineas.append("*Generado con sales-report-generator*")

    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))

    print(f"Reporte guardado en: {ruta_salida}")
