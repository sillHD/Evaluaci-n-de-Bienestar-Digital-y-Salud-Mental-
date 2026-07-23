# VALIDATION REPORT (Phase 2)

Fecha: 2026-07-22
Alcance: Reorganizacion segura de estructura (sin extraccion a `src/` y sin rediseno de logica de modelos).

## 1) Dataset consistency check

### Canonical training dataset (nuevo estandar)
- Archivo: `data/mental_health_digital_behavior_data.csv`
- Shape: `(500, 9)`
- Columnas:
  - `daily_screen_time_min`
  - `num_app_switches`
  - `sleep_hours`
  - `notification_count`
  - `social_media_time_min`
  - `focus_score`
  - `mood_score`
  - `anxiety_level`
  - `digital_wellbeing_score`

### Configuracion de carga original observada en notebook
- Archivo esperado: `mental_health_digital_behavior_data (1).csv`
- Lectura usada: `pd.read_csv(..., delimiter=';')`

### Comparacion solicitada (shape, columnas, valores representativos)
- Si se lee el archivo canonico con separador correcto (`,`):
  - Shape: `(500, 9)`
  - Columnas: 9 columnas esperadas.
- Si se lee el archivo canonico con separador `;` (como en la celda original):
  - Shape: `(500, 1)`
  - Columna unica: encabezado completo concatenado.
- Valores representativos (lectura correcta del canonico):
  - Fila 1: `daily_screen_time_min=389.8`, `anxiety_level=10.0`, `digital_wellbeing_score=44.8`
  - Fila 2: `daily_screen_time_min=351.7`, `anxiety_level=10.0`, `digital_wellbeing_score=43.6`
- Valores mostrados en salidas historicas del notebook coinciden semanticamente con esas filas, pero con formato decimal de coma en la visualizacion.

Resultado:
- Se resolvio el desajuste de nombre y delimitador en el notebook de trabajo (`notebooks/mental_health_model.ipynb`) usando `../data/mental_health_digital_behavior_data.csv` con parseo por defecto.

## 2) Target definitions

Definicion mantenida:
- `at_risk = ((anxiety_level >= 8) OR (mood_score <= 6)).astype(int)`

No se modifico la definicion de target durante Fase 2.

## 3) Model types and parameters

### Clasificacion
- Modelo: `LogisticRegression()` (scikit-learn, parametros por defecto en el notebook auditado).
- Evaluacion declarada en notebook: `cross_val_predict(..., cv=10)` + matriz de confusion.

### Regresion
- Modelo: `LinearRegression()` (scikit-learn, parametros por defecto).
- Split reportado: `train_test_split(test_size=0.2, random_state=42)`.
- Features usadas en notebook: top 3 por correlacion con `digital_wellbeing_score`.

## 4) Regression metrics

Estado en Fase 2:
- No se recalcularon metricas en ejecucion completa end-to-end dentro de esta fase.
- El notebook contiene celdas para `R2`, `MSE`, `RMSE`, `MAE`, `MAPE`, pero no se reclama equivalencia numerica aun.

## 5) Classification confusion matrix

Estado en Fase 2:
- No se recalculo la matriz de confusion en una corrida de validacion formal en esta fase.
- El notebook conserva la celda de calculo y visualizacion de la matriz, pero no se certifica equivalencia aun.

## 6) Prediction equivalence (before vs after)

Conclusiones de verificacion en esta fase:
- `No verificado aun` para equivalencia numerica completa de predicciones.
- Se aplicaron cambios de organizacion/rutas y saneamiento de secretos.
- No se introdujo extraccion de logica a `src/` ni rediseno de modelos.

## 7) Security and privacy checks relevant to validation

- Token expuesto de ngrok eliminado de notebooks en esta rama y sustituido por variable de entorno (`NGROK_AUTH_TOKEN`).
- El flujo por defecto de app no depende de ngrok.
- Archivo de respuestas con correo movido a `private-data/form_responses.csv` y excluido de git por `.gitignore`.

## 8) Pending for Phase 6 formal validation

Pendiente para declarar equivalencia completa:
- Ejecutar notebook limpio de inicio a fin en entorno local reproducible.
- Ejecutar `streamlit run app/app.py` con modelos presentes en `models/`.
- Comparar salida de prediccion y metricas contra baseline reproducible y registrar diferencias, si existen.