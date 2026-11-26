"""Tests de la transformación de tasas PyME."""

from costos_pyme.tasas import COLUMNAS, transformar_tasa

DATOS_DE_PRUEBA = {
    "status": 200,
    "results": [
        {
            "idVariable": 1929,
            "detalle": [
                {"fecha": "2026-10-31", "valor": 36.5},
                {"fecha": "2026-09-30", "valor": 30.74},
            ],
        }
    ],
}


def test_calcula_tasa_efectiva_mensual():
    df = transformar_tasa(DATOS_DE_PRUEBA, 1929)
    fila_octubre = df[df["fecha"].astype(str) == "2026-10-31"].iloc[0]
    assert fila_octubre["tem"] == 3.0  # 36,5 x 30 / 365 = 3,0


def test_ordena_de_la_fecha_mas_vieja_a_la_mas_nueva():
    df = transformar_tasa(DATOS_DE_PRUEBA, 1929)
    assert list(df["fecha"].astype(str)) == ["2026-09-30", "2026-10-31"]


def test_asigna_nombre_de_serie():
    df = transformar_tasa(DATOS_DE_PRUEBA, 1929)
    assert set(df["serie"]) == {"documentos_sola_firma"}


def test_sin_datos_devuelve_tabla_vacia():
    df = transformar_tasa({"status": 200, "results": []}, 1929)
    assert df.empty
    assert list(df.columns) == COLUMNAS