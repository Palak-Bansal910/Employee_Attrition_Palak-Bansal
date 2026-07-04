from pathlib import Path
import pickle

import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "IBM-HR-Employee-Attrition.csv"
MODEL_PATH = BASE_DIR / "model.pkl"
SCALER_PATH = BASE_DIR / "scaler.pkl"
ARTIFACT_PATH = BASE_DIR / "artifacts.pkl"

DROP_COLUMNS = ["EmployeeNumber", "EmployeeCount", "Over18", "StandardHours"]
THRESHOLD = 0.25


def main():
    df = pd.read_csv(DATA_PATH)
    df = df.drop(columns=DROP_COLUMNS)
    df["Attrition"] = df["Attrition"].map({"Yes": 1, "No": 0})

    X = df.drop("Attrition", axis=1)
    y = df["Attrition"]
    categorical_cols = X.select_dtypes(include="object").columns.tolist()
    X_encoded = pd.get_dummies(X, columns=categorical_cols, drop_first=True)

    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    numeric_cols = X_train.select_dtypes(include=["int64", "float64"]).columns.tolist()
    scaler = StandardScaler()
    X_train.loc[:, numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
    X_test.loc[:, numeric_cols] = scaler.transform(X_test[numeric_cols])

    rf_for_selection = RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        min_samples_split=5,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=42,
    )
    rf_for_selection.fit(X_train, y_train)

    rf_importance = pd.DataFrame(
        {"Feature": X_train.columns, "Importance": rf_for_selection.feature_importances_}
    ).sort_values(by="Importance", ascending=False)
    top_features = rf_importance.head(25)["Feature"].tolist()

    X_train_fs = X_train[top_features]
    X_test_fs = X_test[top_features]

    lr = LogisticRegression(
        class_weight="balanced",
        C=2,
        solver="liblinear",
        random_state=42,
        max_iter=2000,
    )
    lr.fit(X_train_fs, y_train)
    lr_pred = lr.predict(X_test_fs)
    lr_prob = lr.predict_proba(X_test_fs)[:, 1]

    rf = RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        min_samples_split=5,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=42,
    )
    rf.fit(X_train_fs, y_train)
    rf_prob = rf.predict_proba(X_test_fs)[:, 1]
    rf_pred = (rf_prob >= THRESHOLD).astype(int)

    gb = GradientBoostingClassifier(
        random_state=42,
        n_estimators=200,
        learning_rate=0.05,
        max_depth=3,
    )
    gb.fit(X_train_fs, y_train)
    gb_prob = gb.predict_proba(X_test_fs)[:, 1]
    gb_pred = (gb_prob >= THRESHOLD).astype(int)

    comparison = pd.DataFrame(
        {
            "Model": ["Logistic Regression", "Random Forest", "Gradient Boosting"],
            "Precision": [
                precision_score(y_test, lr_pred),
                precision_score(y_test, rf_pred),
                precision_score(y_test, gb_pred),
            ],
            "Recall": [
                recall_score(y_test, lr_pred),
                recall_score(y_test, rf_pred),
                recall_score(y_test, gb_pred),
            ],
            "F1 Score": [
                f1_score(y_test, lr_pred),
                f1_score(y_test, rf_pred),
                f1_score(y_test, gb_pred),
            ],
            "ROC-AUC": [
                roc_auc_score(y_test, lr_prob),
                roc_auc_score(y_test, rf_prob),
                roc_auc_score(y_test, gb_prob),
            ],
        }
    )

    metrics = pd.DataFrame(
        {
            "Metric": ["Accuracy", "Precision", "Recall", "F1 Score", "ROC-AUC"],
            "Score": [
                accuracy_score(y_test, gb_pred),
                precision_score(y_test, gb_pred),
                recall_score(y_test, gb_pred),
                f1_score(y_test, gb_pred),
                roc_auc_score(y_test, gb_prob),
            ],
        }
    )

    gb_importance = pd.DataFrame(
        {"Feature": top_features, "Importance": gb.feature_importances_}
    ).sort_values(by="Importance", ascending=False)

    metadata = {
        "threshold": THRESHOLD,
        "drop_columns": DROP_COLUMNS,
        "categorical_cols": categorical_cols,
        "numeric_cols": numeric_cols,
        "encoded_columns": X_encoded.columns.tolist(),
        "top_features": top_features,
        "metrics": metrics,
        "comparison": comparison,
        "feature_importance": gb_importance,
        "raw_feature_columns": X.columns.tolist(),
        "raw_feature_options": {
            col: sorted(X[col].dropna().unique().tolist()) for col in categorical_cols
        },
        "raw_feature_stats": X.select_dtypes(include=["int64", "float64"]).describe().to_dict(),
    }

    with MODEL_PATH.open("wb") as f:
        pickle.dump(gb, f)
    with SCALER_PATH.open("wb") as f:
        pickle.dump(scaler, f)
    with ARTIFACT_PATH.open("wb") as f:
        pickle.dump(metadata, f)

    print(metrics.to_string(index=False))
    print(f"Saved {MODEL_PATH.name}, {SCALER_PATH.name}, and {ARTIFACT_PATH.name}")


if __name__ == "__main__":
    main()
