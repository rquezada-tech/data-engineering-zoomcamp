# Apéndice opcional · Lo que requiere Google Cloud de verdad

[← Proyecto final](proyecto-final.md) · [Índice](../../README.es.md)

> **En una frase:** aquí está todo lo que **no** se puede reproducir fielmente en tu Mac, explicado para que entiendas el concepto aunque no lo ejecutes, y con los pasos para hacerlo si algún día abres una cuenta de GCP.

**Clasificación:** 🔴 requiere GCP. **Nada de este apéndice es obligatorio para completar la ruta.**

> ⚠️ **Antes de usar GCP real:** Google Cloud cobra por uso. Al crear una cuenta te piden una tarjeta. Configura una **alerta de presupuesto** (*Billing → Budgets & alerts*) y borra los recursos al terminar (`terraform destroy`). Esta ruta no ejecutó nada de este apéndice: los comandos se dejan como referencia y están marcados **no probados**.

---

## 1. Terraform: infraestructura como código

### El concepto

En vez de crear un bucket o un dataset haciendo clics en la consola web, **describes** lo que quieres en archivos de texto (`.tf`) y Terraform lo crea por ti. Ventajas: queda versionado en git, se puede repetir idéntico y se puede destruir con un comando.

```hcl
resource "google_storage_bucket" "lago" {
  name          = "mi-lago-de-datos-unico"
  location      = "US"
  force_destroy = true
}
```

El ciclo de trabajo, que la tarea del módulo 1 pregunta en Q7:

| Comando | Qué hace |
|---|---|
| `terraform init` | Descarga los *providers*, los plugins para hablar con GCP |
| `terraform plan` | Muestra qué va a crear, cambiar o borrar, **sin hacerlo** |
| `terraform apply` | Lo crea. Con `-auto-approve` no pide confirmación |
| `terraform destroy` | Borra todo lo que creó |

### Cómo hacerlo (no probado en esta ruta)

Sigue el material oficial del módulo 1: [carpeta de Terraform (2026)](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/a66ad5da2598d7ac147b37eec29632c93f4b1d9d/01-docker-terraform/terraform) y los videos [Terraform: primeros pasos](https://youtu.be/s2bOYDCKl_M), [Terraform básico](https://youtu.be/Y2ux7gq3Z0o) y [Terraform con variables](https://youtu.be/PBi0hHjLftk).

```bash
cd 01-docker-terraform/terraform/terraform/terraform_with_variables
terraform init
terraform plan
terraform apply
terraform destroy
```

Requiere crear una *service account* en GCP y descargar su clave JSON. **Nunca** subas esa clave a git.

> **Idea para explorar (no probada):** el provider `hashicorp/google` permite cambiar los endpoints con opciones como `storage_custom_endpoint` y `bigquery_custom_endpoint`. En teoría podría apuntarse a LocalCloud. No se verificó en esta ruta.

## 2. Compute Engine (máquinas virtuales)

El curso muestra cómo crear una VM en GCP para trabajar desde la nube ([introducción a GCP](https://youtu.be/18jIzE41fJ4)). En esta ruta no hace falta: tu Mac cumple ese rol. LocalCloud incluye un emulador de Compute Engine, pero requiere dar acceso al socket de Docker y no se usa aquí.

## 3. Comparar bytes reales en BigQuery

Es lo más importante que el emulador **no** reproduce. En el [módulo 3](modulo-03-data-warehouse-bigquery.md) aprendiste a pedir un *dry run*. En BigQuery real:

- La consola muestra "This query will process X MB" **antes** de ejecutar.
- Una **tabla externa** suele estimar **0 B**, porque BigQuery no conoce de antemano el tamaño de los archivos. Una tabla **materializada** muestra la cifra real.
- Una consulta con filtro sobre la columna de partición estima **muchos menos** bytes en la tabla particionada.
- `SELECT COUNT(*)` sobre una tabla materializada puede estimar **0 B**, porque se responde con metadatos.

Esas son las preguntas Q2, Q6 y Q9 de la [tarea del módulo 3](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/a66ad5da2598d7ac147b37eec29632c93f4b1d9d/cohorts/2026/03-data-warehouse/homework.md).

### Cómo hacerlo (no probado en esta ruta)

1. Crea un proyecto en GCP, un bucket y un dataset (con Terraform o en la consola).
2. Sube los Parquet del laboratorio. Los scripts de `laboratorios/03-bigquery-parquet/lab/` están pensados **solo** para LocalCloud y bloquean Google a propósito, así que para GCP usa las herramientas oficiales:

```bash
gcloud storage cp laboratorios/03-bigquery-parquet/datos/*.parquet gs://TU-BUCKET/viajes/
```

```bash
bq query --use_legacy_sql=false --dry_run 'SELECT SUM(tarifa) FROM `TU-PROYECTO.lab_m3.viajes_particionada` WHERE DATE(inicio) BETWEEN "2024-02-01" AND "2024-02-07"'
```

3. Compara la estimación de la tabla particionada con la de la no particionada, y con el porcentaje de particiones que calculaste localmente en el paso 6 del laboratorio.

> Con 6000 filas, BigQuery cobra un **mínimo de 10 MB por consulta**, así que las diferencias de costo serán invisibles aunque la estimación cambie. Para ver diferencias de verdad, usa los datos de taxis de la tarea oficial (millones de filas).

## 4. BigQuery ML

BigQuery permite entrenar modelos de machine learning con SQL (`CREATE MODEL ...`). El emulador solo lo ofrece en su imagen "full", que no se probó en esta ruta. Material: [ML en BigQuery](https://youtu.be/B-WtpB0PuG4), [desplegar el modelo](https://youtu.be/BjARzEWaznU) y [SQL de ejemplo](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/a66ad5da2598d7ac147b37eec29632c93f4b1d9d/03-data-warehouse/big_query_ml.sql).

## 5. Kestra con GCP, Spark en Dataproc y dbt Cloud con BigQuery

| Tema | Material oficial |
|---|---|
| Kestra + GCS + BigQuery (flujos 06–09) | [Flujos del módulo 2](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/a66ad5da2598d7ac147b37eec29632c93f4b1d9d/02-workflow-orchestration/flows) |
| Spark con GCS, Dataproc y Spark → BigQuery | [Material del módulo 6](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/a66ad5da2598d7ac147b37eec29632c93f4b1d9d/06-batch) |
| dbt Cloud + BigQuery | [Configuración en la nube](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/a66ad5da2598d7ac147b37eec29632c93f4b1d9d/04-analytics-engineering/setup/cloud_setup.md) |

## 6. Resumen

| Tema | Por qué requiere GCP | Qué puedes hacer en local |
|---|---|---|
| Terraform sobre GCP | Crea recursos reales con costos | Entender el ciclo `init/plan/apply/destroy` |
| Compute Engine | Máquinas virtuales reales | Tu Mac cumple ese rol |
| Bytes reales y costos | El emulador no reproduce la facturación ni la poda de particiones al estimar | Calcular el % de particiones con `INFORMATION_SCHEMA.PARTITIONS` |
| BigQuery ML | No disponible en la imagen estándar del emulador | — |
| Kestra, Spark y dbt Cloud con GCP | Usan servicios reales | Las versiones locales de los módulos 2, 4 y 6 |

[← Proyecto final](proyecto-final.md) · [Índice](../../README.es.md)
