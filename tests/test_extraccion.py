"""Tests de la transformación de cotizaciones."""

from costos_pyme.extraccion import COLUMNAS, transformar_cotizaciones

DATOS_DE_PRUEBA = {
    "status": 200,
    "results": {
        "fecha": "2026-11-24",
        "detalle": [
            {"codigoMoneda": "USD", "descripcion": "DOLAR E.E.U.U.", "tipoPase": 0.0, "tipoCotizacion": 1593.0},
            {"codigoMoneda": "EUR", "descripcion": "EURO", "tipoPase": 1.0974, "tipoCotizacion": 1748.1582},
            {"codigoMoneda": "JPY", "descripcion": "YENS", "tipoPase": 0.006281, "tipoCotizacion": 10.005024},
        ],
    },
}


def test_filtra_solo_el_dolar():
    df = transformar_cotizaciones(DATOS_DE_PRUEBA)
    assert set(df["codigo_moneda"]) == {"USD"}


def test_columnas_y_fecha_correctas():
    df = transformar_cotizaciones(DATOS_DE_PRUEBA)
    assert list(df.columns) == COLUMNAS
    assert str(df.loc[0, "fecha"]) == "2026-11-24"


def test_dia_sin_datos_devuelve_tabla_vacia():
    datos_vacios = {"status": 200, "results": {"fecha": "2026-11-22", "detalle": []}}
    df = transformar_cotizaciones(datos_vacios)
    assert df.empty
    assert list(df.columns) == COLUMNAS