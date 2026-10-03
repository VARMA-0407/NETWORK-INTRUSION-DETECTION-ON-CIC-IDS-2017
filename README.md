# 🔒 Network Intrusion Detection System (CICIDS2017)

> A comprehensive Machine Learning and Deep Learning project for classifying network traffic as benign or malicious using the CICIDS2017 dataset. Includes both binary and multiclass classification pipelines, and a live Streamlit web application.

---

## 📌 Overview

This project presents an end-to-end **Network Intrusion Detection System (IDS)** designed to identify and classify malicious network traffic. Using the **CICIDS2017** dataset — a modern, realistic benchmark for intrusion detection — the system supports:

- **Binary Classification**: Distinguishing benign vs. attack traffic
- **Multiclass Classification**: Identifying 15 traffic classes (1 benign + 14 attack types)

The project emphasises real-world generalization — models trained on balanced (SMOTE-augmented) data are evaluated on naturally imbalanced test sets, reflecting actual network conditions.

---

## 🎯 Problem Statement

Network intrusion detection is a critical component of modern cybersecurity. Traditional rule-based IDS systems struggle to keep up with evolving attack vectors. Machine learning offers an opportunity to learn complex patterns from labelled traffic data, enabling automated and adaptive threat detection.

---

## 🏆 Objectives

- Preprocess and clean the CICIDS2017 dataset for ML compatibility
- Apply a rigorous multi-stage feature selection pipeline to reduce dimensionality
- Handle severe class imbalance using SMOTE
- Train, evaluate, and compare multiple ML and DL models
- Deploy the best-performing models in a real-time Streamlit web application

---

## 📊 Dataset

**CICIDS2017** — Canadian Institute for Cybersecurity Intrusion Detection Dataset 2017

Developed by the **Canadian Institute for Cybersecurity**, this dataset contains realistic benign and attack traffic captured over a 5-day period.

| Property           | Detail                              |
|--------------------|-------------------------------------|
| Total samples      | ~2,522,362 records                  |
| Features (raw)     | 78+ network flow features           |
| Selected features  | 12 (after feature selection)        |
| Binary classes     | 2 (Benign, Attack)                  |
| Multiclass classes | 15 (Benign + 14 attack types)       |
| Class imbalance    | Severe (Benign: ~83%, Attacks: ~17%)|

> ⚠️ **Note:** The original raw dataset is not included in this repository due to its large size. The preprocessed CSV files (`CICIDS_Binary_processed.csv`, `CICIDS_multiclass_processed.csv`) were generated during the feature engineering pipeline and are also not included in the repo. Please download the CICIDS2017 dataset from the [Canadian Institute for Cybersecurity](https://www.unb.ca/cic/datasets/ids-2017.html) and run the preprocessing notebooks to generate them.

### Attack Types (Multiclass)

| Class ID | Attack Type          |
|----------|----------------------|
| 0        | BENIGN               |
| 1        | Bot                  |
| 2        | DoS Hulk             |
| 3        | DoS GoldenEye        |
| 4        | PortScan             |
| 5        | FTP-Patator          |
| 6        | SSH-Patator          |
| 7        | DDoS                 |
| 8        | Heartbleed           |
| 9        | Infiltration         |
| 10       | DoS Slowloris        |
| 11       | DoS Slowhttptest     |
| 12       | Web Attack – Brute Force |
| 13       | Web Attack – XSS     |
| 14       | Web Attack – SQL Injection |

---

## 🔁 Project Architecture / Pipeline

```
Raw CICIDS2017 Data
        │
        ▼
  Data Cleaning
  (Remove NaN, Inf, duplicates, non-numeric cols)
        │
        ▼
  Feature Selection (3-stage)
  ANOVA F-Test → Pearson Correlation → ExtraTrees
        │
        ▼
  Train / Test Split (80/20, stratified)
        │
        ▼
  Class Balancing (SMOTE on training set only)
        │
        ▼
  Model-Specific Preprocessing
  (Yeo-Johnson + MinMax for linear/KNN models)
        │
        ▼
  Model Training & Evaluation
  (Accuracy, Precision, Recall, F1, Confusion Matrix)
        │
        ▼
  Streamlit Web App (Real-time prediction)
```

---

## 🧹 Data Preprocessing

The following preprocessing steps were applied (documented in `index1.ipynb` and the `*_processed.ipynb` notebooks):

| Step                     | Description                                              |
|--------------------------|----------------------------------------------------------|
| **Missing value removal**| Dropped rows with NaN values                             |
| **Duplicate removal**    | Removed duplicate records from the raw dataset           |
| **Inf/invalid values**   | Replaced infinite values and dropped non-numeric columns |
| **Yeo-Johnson transform**| Applied to normalise skewed feature distributions        |
| **Min-Max scaling**      | Applied after transformation for distance-based models   |
| **SMOTE**                | Synthetic Minority Oversampling on the training set only |

> Model-specific preprocessing: Yeo-Johnson + Min-Max scaling applied selectively for **Logistic Regression**, **KNN**, and **SVM** models. Tree-based models trained on raw (unscaled) features.

---

## ⚙️ Feature Selection / Engineering

A **3-stage hybrid feature selection pipeline** was applied to reduce from 78 raw features to **12 highly discriminative features**:

1. **ANOVA F-Test** — Univariate statistical test to rank features by their correlation with the target label
2. **Pearson Correlation** — Removed redundant highly-correlated features
3. **ExtraTrees (Embedded Method)** — Tree-based feature importance to retain only the most predictive features

### Final 12 Selected Features

| Feature               |
|-----------------------|
| Flow Duration         |
| Bwd Packet Length Max |
| Bwd Packet Length Min |
| Flow IAT Mean         |
| Flow IAT Std          |
| Flow IAT Min          |
| Bwd IAT Std           |
| Bwd IAT Max           |
| FIN Flag Count        |
| PSH Flag Count        |
| ACK Flag Count        |
| Active Mean           |

---

## 🤖 Machine Learning Models

The following models were implemented and evaluated across both **binary** and **multiclass** tasks:

| Model                         | Type           | Notes                                           |
|-------------------------------|----------------|-------------------------------------------------|
| **Decision Tree**             | Tree-based     | Baseline tree model; evaluated with no scaling  |
| **Random Forest**             | Ensemble       | Deployed in Streamlit app                       |
| **XGBoost**                   | Gradient Boost | Fast and scalable gradient boosting framework   |
| **Logistic Regression**       | Linear         | Requires Yeo-Johnson + MinMax preprocessing     |
| **K-Nearest Neighbours (KNN)**| Distance-based | Best performing model; deployed in Streamlit app|
| **Linear SVM**                | Linear         | Requires Yeo-Johnson + MinMax preprocessing     |
| **RBF SVM**                   | Kernel-based   | Trained on a subset due to computational cost   |
| **LSTM**                      | Deep Learning  | Sequential model; input reshaped to (samples, 1, 12) |

---

## 📈 Evaluation

The following metrics were calculated for all models:

- **Accuracy** (overall and per class)
- **Precision, Recall, F1-score** (per class and macro/weighted averages)
- **Confusion Matrix** (visualised as heatmaps)
- **Balanced Accuracy**
- **Macro F1-score**

### Results (Multiclass — from executed notebook outputs)

| Model              | Test Accuracy | Macro Avg F1 | Notes                          |
|--------------------|---------------|--------------|--------------------------------|
| Decision Tree      | 0.97          | 0.67         | Evaluated on original test set |
| Random Forest      | —             | —            | See notebook for full report   |
| XGBoost            | —             | —            | See notebook for full report   |
| Logistic Regression| —             | —            | See notebook for full report   |
| KNN                | —             | —            | See notebook for full report   |
| Linear SVM         | —             | —            | See notebook for full report   |
| RBF SVM            | —             | —            | Trained on 200k-sample subset  |
| LSTM               | ~0.58         | —            | Tested; lower than tree models |

### Results (Binary — from executed notebook outputs)

| Model         | Test Accuracy | Macro Avg F1 |
|---------------|---------------|--------------|
| Decision Tree | 1.00          | 0.99         |

> 📌 Full per-class reports and confusion matrix visualisations are available in the executed notebooks.

---

## 🚀 Deployment (Streamlit App)

A **Streamlit web application** is included for real-time intrusion prediction.

**Features:**
- Select between **KNN** or **Random Forest** model
- Manually input 12 network flow feature values via sidebar
- Get instant attack type classification
- View **top-5 class probabilities** as a table

**Saved Artifacts:**
- `yeo_johnson.pkl` — Fitted Yeo-Johnson PowerTransformer
- `minmax_scaler.pkl` — Fitted Min-Max scaler

> The trained model files (`knn_model.pkl`, `random_forest_model.pkl`) are not included in the repository. Run the training notebooks to generate them.

---

## 📁 Project Structure

```
NETWORK-INTRUSION-DETECTION-ON-CIC-IDS-2017/
│
├── .devcontainer/
│   └── devcontainer.json          # GitHub Codespaces configuration
│
├── Report/                        # Research papers and project synopsis
│   ├── Research Paper_CIC.docx
│   ├── Research Paper_CIC_f.docx
│   ├── Rethinking Model Complexity...docx
│   └── Synopsis.group_23.docx
│
├── images/                        # Architecture and attack overview images
│   ├── ATTACKS.png
│   ├── MODEL_OVERVIEW.png
│   └── flowchart-modified.png
│
├── index1.ipynb                   # Main preprocessing + feature selection notebook
├── merge.ipynb                    # Dataset merging/preparation notebook
│
├── Binary_IDS.ipynb               # Binary classification (raw data exploration)
├── Binary_IDS_processed.ipynb     # Binary classification with preprocessed data
│
├── Multiclass_IDS.ipynb           # Multiclass classification (raw data)
├── Multiclass_IDS_processed.ipynb # Multiclass classification with all models
│
├── streamlit.py                   # Streamlit web application
│
├── yeo_johnson.pkl                # Saved Yeo-Johnson transformer
├── minmax_scaler.pkl              # Saved MinMax scaler
│
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation
```

---

## 🛠️ Installation

### Prerequisites

- Python 3.9+
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/VARMA-0407/NETWORK-INTRUSION-DETECTION-ON-CIC-IDS-2017.git
cd NETWORK-INTRUSION-DETECTION-ON-CIC-IDS-2017

# 2. Create and activate a virtual environment (recommended)
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Install additional notebook dependencies
pip install lightgbm tensorflow
```

---

## ▶️ Usage

### Run the Notebooks

Run in the following recommended order:

1. **`merge.ipynb`** — Merge/prepare raw CICIDS2017 data files
2. **`index1.ipynb`** — Full preprocessing + feature selection pipeline
3. **`Binary_IDS_processed.ipynb`** — Train and evaluate binary classification models
4. **`Multiclass_IDS_processed.ipynb`** — Train and evaluate all multiclass models

> Open with Jupyter Notebook or JupyterLab:
> ```bash
> jupyter notebook
> ```

### Run the Streamlit App

```bash
streamlit run streamlit.py
```

> Make sure `knn_model.pkl` (or `random_forest_model.pkl`), `yeo_johnson.pkl`, and `minmax_scaler.pkl` are present in the same directory. These are generated by the training notebooks.

---

## 🔮 Future Improvements

The following enhancements could further improve this system:

- [ ] **Hyperparameter tuning** — Apply GridSearchCV or Optuna for optimised model parameters
- [ ] **Ensemble stacking** — Combine predictions from multiple models
- [ ] **Real-time packet capture** — Integrate with tools like Scapy or CICFlowMeter for live traffic analysis
- [ ] **Explainability (XAI)** — Integrate SHAP or LIME for interpretable predictions
- [ ] **Model versioning** — Use MLflow or DVC to track experiments and model versions
- [ ] **REST API** — Expose the model as a FastAPI or Flask endpoint

---

## 🧰 Technologies Used

| Technology          | Purpose                                  |
|---------------------|------------------------------------------|
| Python 3.9+         | Primary programming language             |
| Pandas              | Data manipulation and analysis           |
| NumPy               | Numerical computing                      |
| Scikit-learn        | ML models, preprocessing, evaluation    |
| Imbalanced-learn    | SMOTE oversampling                       |
| XGBoost             | Gradient boosting classifier             |
| TensorFlow / Keras  | LSTM deep learning model                 |
| Streamlit           | Interactive web application              |
| Matplotlib / Seaborn| Data visualisation                       |
| Joblib              | Model serialisation                      |

---

## 👤 Author

**GitHub:** [@VARMA-0407](https://github.com/VARMA-0407)

---

## 📄 License

This project is for educational and research purposes.
