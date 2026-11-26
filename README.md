# Costo financiero pyme

Monitor de liquidez y costo financiero real para pymes argentinas: tasas, inflación, dólar y riesgo país.

## El problema

Una de las decisiones más difíciles para una pyme argentina es cómo financiar su capital de trabajo:

> **¿Conviene financiar la mercadería con crédito bancario o descuento de cheques, o usar fondos propios dolarizados?**

La respuesta depende de variables que cambian todos los días: la tasa a la que prestan los bancos, la inflación, el tipo de cambio y la volatilidad del país. Están dispersas en distintas fuentes, y la pyme rara vez tiene un analista que las cruce.

## Qué resuelve

Un pipeline diario que:

1. **Calcula la tasa real de financiamiento:** compara el costo del crédito (adelantos en cuenta corriente, descuento de documentos) contra la inflación y la devaluación.
2. **Cruza esa información con la operación de una pyme** (un dataset simulado de compras y facturación).
3. **Dispara alertas de "Ventana de Financiamiento":**
   - 🟢 **Ventana abierta:** la tasa real es negativa; conviene tomar deuda para stockear.
   - 🔴 **Alerta de margen:** la tasa real es alta y la inflación baja; financiarse caro destruye margen.
   - 🟡 **Cobertura cambiaria:** la devaluación supera a la tasa en pesos; conviene conservar los dólares y endeudarse en pesos.

## Variables

| Variable | Fuente | Frecuencia | Estado |
|---|---|---|---|
| Tipo de cambio oficial y mayorista (Com. A 3500) | API de Estadísticas Cambiarias del BCRA | Diaria | ✅ |
| Tasas activas (adelantos en cta. cte., documentos) | API de Estadísticas Monetarias del BCRA | Diaria | 🔜 |
| Inflación (IPC) | ArgentinaDatos | Mensual | 🔜 |
| Riesgo país | ArgentinaDatos | Diaria | 🔜 |
| Dólar MEP | ArgentinaDatos | Diaria | 🔜 |
| Compras y facturación de una pyme | Dataset simulado en PostgreSQL | — | 🔜 |

## Estado del proyecto

| Etapa | Estado |
|---|---|
| Extracción incremental del tipo de cambio (BCRA) | ✅ |
| Tests unitarios y CI con GitHub Actions | ✅ |
| Extracción de tasas activas, inflación y riesgo país | 🔜 |
| Orquestación diaria con Airflow y Docker Compose | 🔜 |
| Staging en Parquet y carga en Redshift | 🔜 |
| Dataset simulado de la pyme con historial de cambios (SCD2) | 🔜 |
| Data mart de tasa real y alertas de "Ventana de Financiamiento" | 🔜 |

## Estructura del repositorio

```
costo-financiero-pyme/
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
git clone https://github.com/mefaraldo/costo-financiero-pyme.git
cd costo-financiero-pyme

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
- **Solo series del dólar:** el oficial y el mayorista de referencia (Com. A 3500) son los que usa una pyme para valuar importaciones y comparar contra la tasa en pesos.
- **Inflación observada como primera aproximación:** el MVP compara la tasa contra la última inflación publicada. Usar la inflación esperada (REM del BCRA) queda como mejora futura.

## Tests y CI

Los tests verifican la transformación de los datos:

- `test_filtra_solo_el_dolar`: solo quedan las series del dólar.
- `test_columnas_y_fecha_correctas`: el esquema de salida y la fecha de cada fila son correctos.
- `test_dia_sin_datos_devuelve_tabla_vacia`: un día sin cotizaciones devuelve una tabla vacía con las columnas esperadas.

GitHub Actions corre los tests automáticamente en cada Pull Request y en cada push a `main`.

## Video de defensa

🔜 Link al video (se agrega en la entrega final).