from pathlib import Path
import pickle

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "IBM-HR-Employee-Attrition.csv"
MODEL_PATH = BASE_DIR / "model.pkl"
SCALER_PATH = BASE_DIR / "scaler.pkl"
ARTIFACT_PATH = BASE_DIR / "artifacts.pkl"
CHART_DIR = BASE_DIR / "assets" / "charts"


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


@st.cache_resource
def load_model_bundle():
    with MODEL_PATH.open("rb") as f:
        model = pickle.load(f)
    with SCALER_PATH.open("rb") as f:
        scaler = pickle.load(f)
    with ARTIFACT_PATH.open("rb") as f:
        artifacts = pickle.load(f)
    return model, scaler, artifacts


def chart_path(filename):
    return CHART_DIR / filename


def preprocess_employee_input(employee_input, scaler, artifacts):
    row = pd.DataFrame([employee_input])
    encoded = pd.get_dummies(
        row,
        columns=artifacts["categorical_cols"],
        drop_first=True,
    )
    encoded = encoded.reindex(columns=artifacts["encoded_columns"], fill_value=0)
    encoded.loc[:, artifacts["numeric_cols"]] = scaler.transform(
        encoded[artifacts["numeric_cols"]]
    )
    return encoded[artifacts["top_features"]]


def predict_attrition(employee_input, model, scaler, artifacts):
    processed = preprocess_employee_input(employee_input, scaler, artifacts)
    attrition_probability = float(model.predict_proba(processed)[:, 1][0])
    prediction = int(attrition_probability >= artifacts["threshold"])
    confidence = attrition_probability if prediction == 1 else 1 - attrition_probability
    return prediction, attrition_probability, confidence


def default_employee_values(df, artifacts):
    features = artifacts["raw_feature_columns"]
    defaults = {}
    for col in features:
        if col in artifacts["categorical_cols"]:
            defaults[col] = df[col].mode().iloc[0]
        else:
            defaults[col] = int(df[col].median())
    return defaults


def metric_lookup(artifacts):
    metrics = artifacts["metrics"].copy()
    return dict(zip(metrics["Metric"], metrics["Score"]))


def format_percent(value):
    return f"{value * 100:.1f}%"
