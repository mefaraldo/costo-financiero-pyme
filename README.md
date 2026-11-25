# Monitor de costos pyme

Comparativo de costos para pymes argentinas: salarios, dólar, inflación y crédito.

## El problema

El dueño de una pyme argentina toma decisiones todos los días (cuánto aumentar precios, si reponer stock, si pedir un crédito) mirando variables que se mueven solas y que están dispersas en distintas fuentes: el BCRA, el INDEC y los convenios colectivos.

Este proyecto junta esas variables en un solo lugar, con un pipeline que se actualiza todos los días, para responder tres preguntas:

1. **¿Cuánto le cuesta un empleado a la pyme, en pesos y en dólares?**
2. **¿Conviene endeudarse?** (tasa de crédito vs. inflación)
3. **¿Cómo viene el contexto?** (tipo de cambio y actividad económica)

## Estado del proyecto

| Etapa | Estado |
|---|---|
| Extracción incremental de cotizaciones del dólar (BCRA) | ✅ |
| Tests unitarios y CI con GitHub Actions | ✅ |
| Orquestación diaria con Airflow y Docker Compose | 🔜 |
| Staging en Parquet y carga en Redshift | 🔜 |
| Salarios (SMVM / convenio de Comercio) con historial de cambios (SCD2) | 🔜 |
| Inflación y tasas de crédito | 🔜 |

## Fuentes de datos

- **API de Estadísticas Cambiarias del BCRA**: cotizaciones diarias. Es pública y no requiere token. Se consulta una fecha por corrida.

Series que se usan:
- `USD`: dólar oficial.
- `REF`: dólar mayorista de referencia (Comunicación A 3500).

## Estructura del repositorio

```
monitor-costos-pyme/
├── .github/workflows/tests.yml   # CI: corre los tests en cada Pull Request
├── costos_pyme/
│   ├── __init__.py
│   └── extraccion.py             # Extracción (API) y transformación de cotizaciones
├── tests/
│   └── test_extraccion.py        # Tests unitarios de la transformación
├── .env.example                  # Variables de entorno a completar
├── requirements.txt              # Dependencias de Python
└── README.md
```

## Cómo correrlo

Requisitos: Python 3.13 y Git.

```bash
# 1. Clonar el repositorio
git clone https://github.com/mefaraldo/monitor-costos-pyme.git
cd monitor-costos-pyme

# 2. Crear y activar un entorno virtual
python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows (PowerShell)
# source .venv/bin/activate       # Linux / Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
copy .env.example .env            # Windows
# cp .env.example .env            # Linux / Mac

# 5. Probar la extracción de un día
python -m costos_pyme.extraccion

# 6. Correr los tests
python -m pytest -v
```

## Decisiones de diseño

- **Extracción incremental:** cada corrida pide a la API una sola fecha, en lugar de traer toda la historia. Esto prepara el pipeline para que Airflow ejecute un día por corrida.
- **Extracción separada de la transformación:** `extraer_cotizaciones` solo habla con la API; `transformar_cotizaciones` solo limpia los datos. Así la transformación se puede testear sin depender de internet.
- **Días sin datos:** los fines de semana y feriados el BCRA no publica cotizaciones. En ese caso la transformación devuelve una tabla vacía con el esquema correcto, en lugar de fallar.
- **Solo series del dólar:** el foco del proyecto son los costos de una pyme argentina, que se miden contra el dólar oficial y el mayorista.

## Tests y CI

Los tests verifican la transformación de los datos:

- `test_filtra_solo_el_dolar`: solo quedan las series del dólar.
- `test_columnas_y_fecha_correctas`: el esquema de salida y la fecha de cada fila son correctos.
- `test_dia_sin_datos_devuelve_tabla_vacia`: un día sin cotizaciones devuelve una tabla vacía con las columnas esperadas.

GitHub Actions corre los tests automáticamente en cada Pull Request y en cada push a `main`.

## Video de defensa

🔜 Link al video (se agrega en la entrega final).
