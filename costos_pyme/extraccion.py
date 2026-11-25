"""Extracción y transformación de cotizaciones del BCRA."""

import pandas as pd
import requests

URL_COTIZACIONES = "https://api.bcra.gob.ar/estadisticascambiarias/v1.0/Cotizaciones"
MONEDAS_DE_INTERES = ("USD", "REF")
COLUMNAS = ["fecha", "codigo_moneda", "descripcion", "tipo_pase", "tipo_cotizacion"]


def extraer_cotizaciones(fecha: str) -> dict:
    """Pide al BCRA las cotizaciones de una fecha (AAAA-MM-DD) y devuelve el JSON."""
    respuesta = requests.get(URL_COTIZACIONES, params={"fecha": fecha}, timeout=30)
    respuesta.raise_for_status()
    return respuesta.json()


def transformar_cotizaciones(datos: dict, monedas=MONEDAS_DE_INTERES) -> pd.DataFrame:
    """Convierte el JSON del BCRA en una tabla limpia, solo con las monedas de interés."""
    resultados = datos.get("results") or {}
    detalle = resultados.get("detalle") or []

    if not detalle:
        return pd.DataFrame(columns=COLUMNAS)

    df = pd.DataFrame(detalle).rename(
        columns={
            "codigoMoneda": "codigo_moneda",
            "tipoPase": "tipo_pase",
            "tipoCotizacion": "tipo_cotizacion",
        }
    )
    df["fecha"] = pd.to_datetime(resultados["fecha"]).date()
    df = df[df["codigo_moneda"].isin(monedas)]
    return df[COLUMNAS].reset_index(drop=True)


if __name__ == "__main__":
    print(transformar_cotizaciones(extraer_cotizaciones("2026-11-24")))