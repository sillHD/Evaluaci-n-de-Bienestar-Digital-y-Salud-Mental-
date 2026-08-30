# VALIDATION REPORT (Formal baseline)

Fecha: 2026-07-23
Estado general: PARTIALLY VERIFIED
Alcance: validacion formal de reproducibilidad y baseline en Fase 2, sin iniciar Fase 3.

## 1) Entorno reproducible

- Python: 3.11.9
- pandas: 3.0.5
- numpy: 2.4.6
- scikit-learn: 1.9.0
- joblib: 1.5.3
- matplotlib: 3.11.1
- streamlit: 1.60.0
- openpyxl: 3.1.5

Archivo de dependencias fijadas:
- requirements.txt

## 2) Consistencia de dataset canonico

Dataset de entrenamiento canonico:
- Ruta: data/mental_health_digital_behavior_data.csv
- Shape: (500, 9)
- Duplicados: 0
- Missing por columna: 0 en todas las columnas
- SHA-256: 009ff9498455dcd780f858ab1a0c650ef1be45b8b18b5d174dc011331e7eb310

Columnas:
- daily_screen_time_min
- num_app_switches
- sleep_hours
- notification_count
- social_media_time_min
- focus_score
- mood_score
- anxiety_level
- digital_wellbeing_score

Distribucion de target derivado at_risk:
- clase 1: 352
- clase 0: 148

## 3) Definiciones y parametros de baseline

Target clasificacion:
- at_risk = (anxiety_level >= 8) OR (mood_score <= 6)

Modelo de clasificacion:
- Clase: LogisticRegression
- Evaluacion: cross_val_predict, cv=10 (out-of-fold)
- Parametros:
  - C: 1.0
  - class_weight: null
  - dual: false
  - fit_intercept: true
  - intercept_scaling: 1
  - l1_ratio: 0.0
  - max_iter: 100
  - n_jobs: null
  - penalty: deprecated
  - random_state: null
  - solver: lbfgs
  - tol: 0.0001
  - verbose: 0
  - warm_start: false

Modelo de regresion:
- Clase: LinearRegression
- Split: test_size=0.2, random_state=42
- Seleccion de variables: top 3 por correlacion absoluta con digital_wellbeing_score
- Top 3:
  - anxiety_level: -0.836475911642246
  - sleep_hours: 0.4404256331292677
  - focus_score: 0.4112660629904365
- Parametros:
  - copy_X: true
  - fit_intercept: true
  - n_jobs: null
  - positive: false
  - tol: 1e-06

## 4) Resultados de baseline (medidos)

Clasificacion:
- confusion matrix: [[143, 5], [4, 348]]
- accuracy: 0.982
- precision: 0.9858356940509915
- recall: 0.9886363636363636
- f1: 0.9872340425531915
- roc_auc: no calculado en la logica baseline actual

Regresion:
- r2: 0.9994721320755598
- mse: 0.030885816192956543
- rmse: 0.17574360925210494
- mae: 0.14327795363199924
- mape: 0.28436100226599204
- train_rows: 400
- test_rows: 100

Coeficientes regresion:
- anxiety_level: -2.9990773623297167
- sleep_hours: 2.995290692628936
- focus_score: 3.9826463673451187
- intercept: 30.151384821767873

## 5) Artefactos y huellas

Modelo clasificacion:
- Ruta: models/logistic_model_mental_health.joblib
- Size: 1359 bytes
- SHA-256: 52ff2bfb048164eb93d03741a93c115a71ec084524bfebcef2ad04290dc99c4b

Modelo regresion:
- Ruta: models/linear_regression_digital_wellbeing.joblib
- Size: 897 bytes
- SHA-256: c3a501c2da24fb173840c004a1b0e83e85cb2ee0d2f56ec336a56533a25b3461

Snapshot de predicciones baseline:
- Archivo: validation/baseline_predictions.csv
- Filas: 10
- Columnas:
  - row_index
  - classification_prediction
  - regression_prediction
  - true_at_risk
  - true_digital_wellbeing_score

## 6) Estado de notebooks (fuente vs ejecutado)

Notebook fuente:
- Ruta: notebooks/mental_health_model.ipynb
- Estado esperado: limpio para control de cambios (execution_count null)

Notebook ejecutado:
- Ruta: notebooks/executed/mental_health_model_executed.ipynb
- Estado esperado: ejecutado con outputs para evidencia reproducible

## 7) Validacion de app Streamlit

Aplicacion:
- Ruta: app/app.py
- Arranque local validado: streamlit run app/app.py
- Resultado funcional: la app carga modelos, acepta inputs y devuelve prediccion
- Mensaje de seguridad funcional: disclaimer de no diagnostico visible

## 8) Seguridad y privacidad

- No se detectan private-data ni .env en git index actual.
- Uso de token de ngrok reemplazado por variable de entorno, sin secreto hardcodeado en flujo activo.
- Flujo principal no depende de ngrok para validacion local.

## 9) Diferencias frente a implementacion original

- Se estandarizo carga de dataset canonico desde data, con rutas robustas por pathlib.
- Se desacoplo infraestructura Colab/Drive/ngrok del flujo analitico principal.
- Se mantuvo la logica de modelos y targets sin rediseno.

## 10) Limitaciones y riesgos residuales

- Riesgo metodologico conocido: posible data leakage en clasificacion porque X incluye digital_wellbeing_score, variable relacionada con el target derivado.
- Se mantienen warnings de convergencia de LogisticRegression con max_iter=100 en algunas ejecuciones.
- No se realizo, por restriccion de alcance, rediseno metodologico ni mitigacion de leakage en esta fase.

## 11) Veredicto de equivalencia

Veredicto: PARTIALLY VERIFIED

Razon:
- La reproducibilidad tecnica y la ejecucion funcional fueron verificadas.
- Las metricas baseline y artefactos quedan documentados y trazables.
- No se declara equivalencia metodologica plena con una version historica externa debido al riesgo de leakage ya conocido y a que no se altero esa decision en Fase 2.