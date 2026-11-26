"""Extracción y transformación de tasas de interés para PyMEs (BCRA)."""

import pandas as pd
import requests

URL_SERIES = "https://api.bcra.gob.ar/estadisticas/v4.0/monetarias"

SERIES_PYME = {
    1921: "adelantos_cta_cte",
    1929: "documentos_sola_firma",
    1931: "documentos_descontados",
}

COLUMNAS = ["fecha", "id_variable", "serie", "tna", "tem"]


def extraer_tasa(id_variable: int, desde: str, hasta: str) -> dict:
    """Pide al BCRA los valores de una serie entre dos fechas (AAAA-MM-DD)."""
    respuesta = requests.get(
        f"{URL_SERIES}/{id_variable}",
        params={"desde": desde, "hasta": hasta},
        timeout=30,
    )
    respuesta.raise_for_status()
    return respuesta.json()


def transformar_tasa(datos: dict, id_variable: int) -> pd.DataFrame:
    """Convierte la respuesta del BCRA en una tabla con TNA y tasa efectiva mensual."""
    resultados = datos.get("results") or []
    detalle = resultados[0].get("detalle", []) if resultados else []

    if not detalle:
        return pd.DataFrame(columns=COLUMNAS)

    df = pd.DataFrame(detalle).rename(columns={"valor": "tna"})
    df["fecha"] = pd.to_datetime(df["fecha"]).dt.date
    df["id_variable"] = id_variable
    df["serie"] = SERIES_PYME.get(id_variable, "desconocida")
    df["tem"] = (df["tna"] * 30 / 365).round(4)

    return df[COLUMNAS].sort_values("fecha").reset_index(drop=True)


if __name__ == "__main__":
    for id_variable in SERIES_PYME:
        print(transformar_tasa(extraer_tasa(id_variable, "2026-08-01", "2026-11-24"), id_variable))