# Employee Attrition Prediction Dashboard

Professional Streamlit dashboard converted from the completed Employee Attrition Jupyter Notebook.

## What Is Preserved

- Notebook preprocessing: dropped identifier/constant columns, target mapping, one-hot encoding, stratified split, numeric scaling, and top-feature selection.
- Final selected model: Gradient Boosting Classifier.
- Notebook decision threshold: 0.25.
- Notebook metrics and model comparison results.
- Exported notebook EDA and evaluation charts from `assets/charts/`.

The original folder did not include serialized model artifacts, so `scripts/build_artifacts.py` recreates the notebook pipeline once and saves `model.pkl`, `scaler.pkl`, and `artifacts.pkl`. The Streamlit app loads those saved artifacts and does not retrain during normal use.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Pages

- Home: overview, dataset information, technologies, algorithms, workflow.
- Data Analysis: notebook EDA charts.
- Prediction: employee attrition prediction form using the saved pipeline.
- Model Performance: metrics, model comparison, confusion matrix, ROC curve, feature importance.
- About: methodology and preservation notes.

## Project Structure

```text
employee_attrition/
|-- app.py
|-- utils.py
|-- model.pkl
|-- scaler.pkl
|-- artifacts.pkl
|-- assets/charts/
|-- scripts/build_artifacts.py
|-- notebook.ipynb
|-- IBM-HR-Employee-Attrition.csv
|-- requirements.txt
|-- README.md
```
