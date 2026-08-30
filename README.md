# Digital Wellbeing and Mental Health Risk Prediction

A data science portfolio project focused on predicting digital wellbeing and mental health risk based on behavioral and self-reported signals such as sleep duration, social media usage, notification volume, focus level, mood, and anxiety.

This repository was designed to demonstrate a complete ML workflow: data preparation, exploratory analysis, model training, validation, deployment through a Streamlit app, and documentation suitable for a professional portfolio or client-facing presentation.

## Project purpose

The project seeks to estimate two outcomes:

- Mental health risk classification: whether a person is likely to be at risk based on a derived label using anxiety and mood indicators.
- Digital wellbeing score prediction: a regression score representing overall digital wellness.

This is a research and portfolio-oriented project, not a clinical diagnosis tool. It should be used as an analytical dashboard or proof of concept, not as a medical recommendation system.

## Business value

The model can support:

- wellness monitoring in digital behavior studies,
- exploratory analysis for product or UX teams,
- academic and professional demonstration of predictive analytics,
- portfolio storytelling for data science and machine learning work.

## Repository structure

```text
.
├── app/
│   └── app.py                     # Streamlit application
├── data/
│   ├── README.md                  # Data handling and privacy notes
│   └── mental_health_digital_behavior_data.csv
├── docs/
│   └── VALIDATION_REPORT.md       # Baseline validation and reproducibility notes
├── notebooks/
│   ├── mental_health_model.ipynb  # Main analytical notebook
│   └── original/
├── orange/
│   ├── README.md
│   └── mental_health_workflow.ows # Orange analysis workflow
├── validation/
│   ├── baseline_predictions.csv
│   └── validation_metrics.json
├── .env.example                   # Example environment variables
├── .gitignore                     # Ignore rules for secrets and local artifacts
├── PROJECT_AUDIT.md               # Technical audit of the original project state
├── requirements.txt               # Python dependencies
├── README.md                      # Project overview
└── Entrenamiento_y_Prediccion_(Python).ipynb
```

## Data

The primary dataset is located in:

- [data/mental_health_digital_behavior_data.csv](data/mental_health_digital_behavior_data.csv)

The dataset includes variables such as:

- daily screen time
- app switching frequency
- sleep hours
- notification count
- social media activity
- focus score
- mood score
- anxiety level
- digital wellbeing score

The classification target is derived as:

- at_risk = (anxiety_level >= 8) OR (mood_score <= 6)

## Machine learning approach

The project includes two modeling tasks:

### 1. Classification model

A logistic regression model is used to classify whether a user is at risk.

Evaluation is based on:

- confusion matrix
- accuracy
- precision
- recall
- F1 score

### 2. Regression model

A linear regression model predicts the digital wellbeing score based on the most relevant features.

The regression focuses on the top correlated features, especially:

- anxiety level
- sleep hours
- focus score

Metrics include:

- R²
- MSE
- RMSE
- MAE
- MAPE

## Streamlit application

The app is implemented in [app/app.py](app/app.py). It allows users to input behavioral metrics and receive:

- mental health risk estimate,
- risk probability,
- digital wellbeing score,
- wellness interpretation.

It was built for local use and can be launched with:

```bash
streamlit run app/app.py
```

The application checks for trained model artifacts and supports a configurable `MODELS_DIR` environment variable for flexibility across environments.

## Local setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Ensure the trained models exist under the `models/` folder or define `MODELS_DIR`.
4. Launch the app:

```bash
streamlit run app/app.py
```

## Environment configuration

A sample environment file is available at [.env.example](.env.example).

You can copy it to `.env` and adjust the values if needed:

```bash
copy .env.example .env
```

This helps avoid hardcoded secrets and keeps deployment setup cleaner.

## Validation and quality notes

The repository includes validation artifacts under [validation/validation_metrics.json](validation/validation_metrics.json), including:

- model performance metrics,
- feature selection details,
- dataset diagnostics,
- baseline prediction snapshot.

The documents in [PROJECT_AUDIT.md](PROJECT_AUDIT.md) and [docs/VALIDATION_REPORT.md](docs/VALIDATION_REPORT.md) describe the technical audit, baseline verification, and remaining methodological considerations.

## Portfolio and professional positioning

This project is intended to showcase:

- end-to-end data science workflow,
- practical model development and validation,
- production-friendly deployment patterns,
- clear documentation and ethical framing,
- communication quality for client or hiring contexts.

For Upwork or portfolio use, the repository is useful as a visible example of analytical thinking, model evaluation, and implementation quality.

## Important limitations

- This is not a medical diagnostic system.
- The model is a demo and research-oriented artifact.
- There is a known methodological caution around possible target leakage depending on how features are selected and interpreted.
- Sensitive or personal information must not be published without proper anonymization and consent.

## License and usage

This repository is intended for educational, portfolio, and research use.

If you plan to reuse it for client work, make sure to:

- review the data privacy constraints,
- validate the model on your own data,
- document assumptions and limitations,
- avoid presenting the output as medical advice.

## Conclusion

This repository demonstrates an applied machine learning project that combines analytics, modeling, evaluation, and deployment in a single, easy-to-understand structure. It is positioned as a strong example for a portfolio, especially for projects that highlight data-driven decision-making and end-to-end AI application work.
