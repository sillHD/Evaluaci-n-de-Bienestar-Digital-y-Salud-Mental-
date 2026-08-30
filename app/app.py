
import os
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
MODELS_DIR = Path(os.getenv("MODELS_DIR", PROJECT_ROOT / "models")).resolve()
RISK_MODEL_PATH = MODELS_DIR / "logistic_model_mental_health.joblib"
WELLBEING_MODEL_PATH = MODELS_DIR / "linear_regression_digital_wellbeing.joblib"

if not RISK_MODEL_PATH.exists() or not WELLBEING_MODEL_PATH.exists():
    st.error(
        "Missing model files. Please place the trained models in the 'models' directory "
        "or set the MODELS_DIR environment variable."
    )
    st.info(f"Expected files: {RISK_MODEL_PATH} and {WELLBEING_MODEL_PATH}")
    st.stop()

try:
    modelo_riesgo = joblib.load(RISK_MODEL_PATH)
    modelo_bienestar = joblib.load(WELLBEING_MODEL_PATH)
except Exception as e:
    st.error(f"Unexpected error while loading models: {e}")
    st.stop()

st.title("Evaluacion de Bienestar Digital y Riesgo Mental")
st.header("Introduce tus datos:")

daily_screen_time_min = st.number_input(
    "Cuantos minutos al dia usas el celular o computador?", min_value=0, value=240
)
num_app_switches = st.number_input(
    "Cuantas veces cambias entre aplicaciones en un dia?", min_value=0, value=50
)
social_media_time_min = st.number_input(
    "Cuantos minutos usas redes sociales diariamente?", min_value=0, value=100
)
notification_count = st.number_input(
    "Cuantas notificaciones de redes sociales recibes al dia?", min_value=0, value=150
)
sleep_hours = st.number_input(
    "Cuantas horas duermes por noche?", min_value=0.0, max_value=24.0, value=7.0
)
focus_score = st.slider("Que tan enfocado(a) te sentiste esta semana?", 1, 10, value=7)
anxiety_level = st.slider(
    "Que tan ansioso(a) o estresado(a) te sentiste esta semana?", 1, 10, value=6
)
mood_score = st.slider(
    "Como calificarias tu estado de animo general esta semana?", 1, 10, value=8
)

if st.button("Evaluar"):
    input_data_dict = {
        "daily_screen_time_min": daily_screen_time_min,
        "num_app_switches": num_app_switches,
        "sleep_hours": sleep_hours,
        "notification_count": notification_count,
        "social_media_time_min": social_media_time_min,
        "focus_score": focus_score,
        "mood_score": mood_score,
        "anxiety_level": anxiety_level,
    }

    entrada_clasificacion_df = pd.DataFrame([input_data_dict])

    if hasattr(modelo_riesgo, "feature_names_in_"):
        expected_cols_riesgo = list(modelo_riesgo.feature_names_in_)
        entrada_clasificacion_df = entrada_clasificacion_df.reindex(
            columns=expected_cols_riesgo, fill_value=0
        )
    else:
        st.warning("No se puede verificar el orden de columnas para el modelo de riesgo.")
        if entrada_clasificacion_df.shape[1] != 8:
            st.error(
                f"Numero inesperado de columnas: {entrada_clasificacion_df.shape[1]}. Se esperaban 8."
            )
            st.stop()

    entrada_regresion = np.array([[anxiety_level, sleep_hours, focus_score]])

    riesgo_pred = modelo_riesgo.predict(entrada_clasificacion_df)[0]
    probabilidad_riesgo = modelo_riesgo.predict_proba(entrada_clasificacion_df)[:, 1][0]

    if hasattr(modelo_bienestar, "feature_names_in_"):
        entrada_regresion_df = pd.DataFrame(
            [[anxiety_level, sleep_hours, focus_score]],
            columns=["anxiety_level", "sleep_hours", "focus_score"],
        )
        entrada_regresion_df = entrada_regresion_df.reindex(
            columns=modelo_bienestar.feature_names_in_, fill_value=0
        )
        bienestar = modelo_bienestar.predict(entrada_regresion_df)[0]
    else:
        bienestar = modelo_bienestar.predict(entrada_regresion)[0]

    st.subheader("Resultados de la Evaluacion:")
    riesgo_texto = "Si, hay un riesgo potencial" if riesgo_pred == 1 else "No, el riesgo es bajo"
    st.markdown(f"**Riesgo Mental:** {riesgo_texto}")
    st.info(f"*(Probabilidad de Riesgo: {probabilidad_riesgo:.2%})*")

    st.markdown(f"**Puntaje de Bienestar Digital:** {bienestar:.2f}")
    if bienestar >= 70:
        st.success("Excelente. Tu bienestar digital parece muy saludable.")
    elif bienestar >= 50:
        st.info("Buen trabajo, tu bienestar digital es moderado.")
    else:
        st.warning("Considera revisar tus habitos digitales para mejorar tu bienestar.")

    st.markdown("---")
    st.markdown(
        "Estos resultados son una estimacion y no sustituyen la evaluacion de un profesional."
    )
