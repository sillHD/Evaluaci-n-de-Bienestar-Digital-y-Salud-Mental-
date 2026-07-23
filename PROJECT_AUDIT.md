# PROJECT AUDIT - Mental Health Digital Behavior Prediction

Fecha de auditoria: 2026-07-22
Estado: Fase 1 completada (solo lectura)
Repositorio auditado: carpeta raiz actual

## 1) Alcance y criterio de auditoria

Se realizo una auditoria tecnica del proyecto existente sin modificar la logica cientifica ni los archivos originales.

Objetivo de esta fase:
- Inventariar activos actuales (notebook, flujo Orange, datos, artefactos de salida).
- Identificar flujo funcional real: carga de datos, preprocesamiento, entrenamiento, evaluacion, prediccion y app.
- Detectar riesgos de reproducibilidad y portabilidad (codigo Colab, rutas absolutas, dependencias ocultas, secretos, etc.).
- Proponer un plan de reorganizacion seguro por fases, manteniendo identidad y proposito original.

Restricciones respetadas en esta auditoria:
- No se altero la pregunta de investigacion ni los objetivos de prediccion.
- No se reemplazaron datasets ni se inventaron resultados.
- No se eliminaron archivos originales.
- No se desplego nada ni se ejecuto refactor de comportamiento.

## 2) Inventario actual de archivos relevantes

Archivos detectados en la raiz del proyecto:
- `Entrenamiento_y_Prediccion_(Python).ipynb` (notebook principal, incluye entrenamiento, prediccion y generacion de app Streamlit).
- `Entrenamiento y Prediccion (Orange).ows` (workflow Orange completo para clasificacion y regresion).
- `mental_health_digital_behavior_data.csv` (dataset principal de entrenamiento; separador coma).
- `Copia de Evaluación de Bienestar Digital y Salud Mental (respuestas) - Respuestas de formulario 1 (1).csv` (respuestas de formulario para aplicacion de modelos; contiene columna de correo electronico).
- `Resultados Finales(Orange).xlsx` (salida generada por flujo Orange).

Observacion clave:
- No existe actualmente un `app.py` persistente en el repositorio. La app Streamlit se construye dinamicamente dentro del notebook (se escribe con `with open("app.py", "w")`).

## 3) Flujo funcional identificado

### 3.1 Carga de datos
- Entrenamiento (notebook): lectura de archivo llamado `mental_health_digital_behavior_data (1).csv` con `delimiter=';'`.
- Formulario (notebook): lectura desde ruta Colab absoluta `/content/Copia de Evaluación de Bienestar Digital y Salud Mental (respuestas) - Respuestas de formulario 1 (1).csv`.
- Orange: carga CSV desde widgets `CSV File Import` con rutas absolutas locales historicas.

### 3.2 Preprocesamiento
- Conversión de valores con coma decimal a formato numerico (`str.replace(',', '.')` + `pd.to_numeric`).
- Creacion de variable de riesgo:
  - `at_risk = (anxiety_level >= 8) OR (mood_score <= 6)`
- One-hot encoding con `pd.get_dummies` para clasificacion.
- Reindexado de columnas usando `feature_names_in_` para alinear inferencia con entrenamiento.

### 3.3 Entrenamiento de modelos
- Clasificacion:
  - `LogisticRegression` sobre `X` (todas las columnas salvo `at_risk`).
  - Validacion cruzada con `cross_val_predict(..., cv=10)`.
  - Matriz de confusion.
- Regresion:
  - Seleccion automatica de top 3 features por correlacion con `digital_wellbeing_score`.
  - `LinearRegression` con `train_test_split(test_size=0.2, random_state=42)`.
  - Metricas: R2, MSE, RMSE, MAE, MAPE.

### 3.4 Evaluacion y resultados
- Clasificacion: matriz de confusion en tabla y grafica.
- Regresion: tabla de coeficientes + tabla de metricas.

### 3.5 Exportacion de modelos y resultados
- Guardado de modelos con `joblib.dump` en Google Drive:
  - `/content/drive/MyDrive/Proyecto_Analitica/modelos/logistic_model_mental_health.pkl`
  - `/content/drive/MyDrive/Proyecto_Analitica/modelos/modelo_regresion_lineal_digital_wellbeing.pkl`
- Guardado de resultados finales del notebook en:
  - `/content/drive/MyDrive/Proyecto_Analitica/Bases de Datos/Resultados Finales(Python).xlsx`

### 3.6 Integracion Streamlit
- En el notebook se define un string multi-linea (`app_code`) y luego se escribe `app.py`.
- La app carga modelos desde Google Drive en ruta Colab absoluta.
- Se ejecuta Streamlit en segundo plano y se expone via `pyngrok`.

## 4) Hallazgos de auditoria (riesgos y deuda tecnica)

### 4.1 Codigo especifico de Colab
- Uso de `from google.colab import drive` y `drive.mount('/content/drive')`.
- Rutas absolutas `/content/...` para datos, modelos y logs.
- Comando shell notebook `!streamlit run app.py &> /content/logs.txt &`.

Impacto:
- Baja portabilidad local/reproducibilidad fuera de Colab.

### 4.2 Rutas absolutas y dependencias de entorno
- Notebook depende de estructura de carpetas en `MyDrive/Proyecto_Analitica/...`.
- Orange `.ows` contiene rutas absolutas de maquina local y referencias historicas.

Impacto:
- Fallos al ejecutar en otro equipo sin ajuste manual.

### 4.3 Secreto expuesto
- Se detecto token de ngrok incrustado en el notebook (`ngrok.set_auth_token("...")`).

Impacto:
- Riesgo de seguridad y mal uso de credenciales.

Nota de tratamiento en Fase 2+:
- No se cambiara comportamiento sin justificar. Se propondra externalizar secretos a variables de entorno o entrada interactiva segura.

### 4.4 Posible dato sensible en dataset de formulario
- El CSV de formulario incluye columna `Dirección de correo electrónico`.

Impacto:
- Riesgo de privacidad si el archivo se publica sin controles.

Nota:
- Se preservara archivo original. Se documentara manejo recomendado y politica de no publicacion de PII sin consentimiento.

### 4.5 Inconsistencia de nombre/formato de dataset de entrenamiento
- El notebook intenta leer `mental_health_digital_behavior_data (1).csv` con separador `;`.
- El archivo presente en repo es `mental_health_digital_behavior_data.csv` y usa separador `,`.

Impacto:
- Riesgo de fallo inmediato o parseo incorrecto segun entorno.

### 4.6 Celdas o bloques duplicados
- Hay bloque de guardado de resultados repetido (guardado de XLSX aparece al menos dos veces con variaciones menores).
- Montajes de Drive repetidos en secciones separadas.

Impacto:
- Mayor complejidad operativa y posible confusion de orden de ejecucion.

### 4.7 Imports no utilizados o parcialmente utilizados
- `make_scorer`, `accuracy_score`, `precision_score`, `recall_score`, `f1_score`, `roc_auc_score`, `cross_val_score`, `cross_validate`, `StratifiedKFold` aparecen importados pero no usados en el flujo visible.
- `from google.colab import auth` aparece sin uso funcional visible.

Impacto:
- Ruido tecnico y dependencia innecesaria.

### 4.8 Dependencias ocultas
- `to_excel` puede requerir engine como `openpyxl`.
- La app depende de que existan los `.pkl` en Drive (no versionados en repo).
- Dependencia de `pyngrok` para exponer app en Colab.

## 5) Mapeo solicitado (Fase 1)

Resumen de componentes requeridos:
- Data loading: identificado en notebook y Orange.
- Preprocessing: conversion numerica por comas, `at_risk`, dummies, alineacion de features.
- Exploratory analysis: correlaciones y visualizaciones (incluye tablas y graficas).
- Model training: `LogisticRegression` y `LinearRegression`.
- Evaluation: confusion matrix + metricas de regresion.
- Prediction logic: aplicacion a base de formulario y prediccion individual en Streamlit.
- Model export: `joblib.dump` a rutas Drive.
- Streamlit integration: app generada desde notebook y lanzada via ngrok.

## 6) Plan propuesto de ejecucion (sin aplicar aun)

## Fase 2 - Reorganizacion segura (sin cambiar comportamiento)
- Crear rama de trabajo: `refactor/project-structure`.
- Crear estructura objetivo de repositorio.
- Mover (no borrar) activos originales:
  - notebook -> `notebooks/mental_health_model.ipynb`
  - orange -> `orange/mental_health_workflow.ows`
  - app -> `app/app.py` (extraida fielmente del bloque actual si no existe archivo persistente)
- Preservar copia intacta del notebook original en ruta de backup dentro del repo.
- Reemplazar rutas absolutas por relativas solo donde sea seguro y documentado.
- Mantener ejecucion top-to-bottom del notebook.

## Fase 3 - Extraccion reutilizable minima
- Extraer solo utilidades claramente reutilizables a `src/`:
  - `src/preprocessing.py`
  - `src/prediction.py`
  - `src/utils.py`
- Mantener analisis exploratorio y narrativo en notebook.
- Validar equivalencia de salidas antes/despues (sin cambiar metricas objetivo).

## Fase 4 - Reproducibilidad
- Generar `requirements.txt` solo con paquetes usados realmente.
- Crear `.gitignore` para Python/Jupyter/Streamlit/modelos/entornos/temporales.
- Quitar dependencia de Colab cuando sea posible sin alterar logica.
- Documentar acceso a datos:
  - si hay PII o restriccion legal, no publicar dataset sensible.
  - incluir `data/README.md` y opcional `data/sample_data.csv` seguro.

## Fase 5 - Documentacion
- Crear `README.md` profesional y sobrio, con:
  - contexto, metodologia, variables, targets, resultados existentes verificados
  - instrucciones de notebook, Streamlit y Orange
  - limitaciones, etica y descargo explicito de no diagnostico medico
  - estructura final del repo

## Fase 6 - Validacion final
- Ejecutar notebook completo.
- Ejecutar Streamlit localmente.
- Verificar que preprocesamiento/predicciones no cambian respecto a baseline.
- Emitir reporte de diferencias (si existen), sin ocultar cambios.

## 7) Politica de cambios para proteger la identidad del proyecto

Durante la ejecucion se aplicaran estas reglas:
- No cambiar pregunta de investigacion, targets ni framing etico.
- No inventar resultados ni claims medicos.
- No eliminar Orange workflow ni archivos originales.
- No incorporar despliegue productivo.
- No commitear secretos ni datos privados sin aprobacion.
- Cualquier cambio de comportamiento se documentara y justificara antes de aplicarlo.

## 8) Entregables previstos

1. `PROJECT_AUDIT.md` (este documento)
2. Reorganizacion de repositorio
3. `README.md`
4. `requirements.txt`
5. `.gitignore`
6. Backup de notebook original preservado
7. Reporte de validacion de equivalencia
8. Resumen de archivos agregados/movidos/modificados

## 9) Estado y siguiente paso

Estado actual:
- Fase 1 completada.
- Ningun cambio estructural ejecutado aun.

Siguiente paso (pendiente de aprobacion explicita):
- Iniciar Fase 2 y crear rama `refactor/project-structure` para comenzar reorganizacion segura.
