from fastapi import FastAPI, APIRouter, UploadFile, File, Body
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
import io
from fastapi.responses import StreamingResponse

app = FastAPI()
router = APIRouter()

# Load the model and label encoder
model = joblib.load("LightGBM_exoplanet_model.pkl")

# For now, let's assume the classes are known (update as needed)
label_classes = ['APC', 'CANDIDATE', 'CONFIRMED', 'FALSE POSITIVE']

# List of all features except koi_disposition and the relative error columns
feature_names = [
    'koi_score','koi_period','koi_eccen','koi_impact','koi_duration','koi_depth','koi_ror','koi_srho','koi_incl','koi_teq','koi_insol','koi_dor','koi_model_snr','koi_count','koi_num_transits','koi_steff','koi_slogg','koi_smet','koi_smass','ra','dec','koi_kepmag','koi_gmag','koi_rmag','koi_imag','koi_zmag','koi_jmag','koi_hmag','koi_kmag','loc_rowid','st_pmra','st_pmdec','pl_tranmid','koi_prad','koi_tmag','st_dist','koi_srad','koi_fittype_LS+MCMC','koi_fittype_MCMC','koi_fittype_none'
]

class ExoplanetInput(BaseModel):
    koi_score: float
    koi_period: float
    koi_eccen: float
    koi_impact: float
    koi_duration: float
    koi_depth: float
    koi_ror: float
    koi_srho: float
    koi_incl: float
    koi_teq: float
    koi_insol: float
    koi_dor: float
    koi_model_snr: float
    koi_count: float
    koi_num_transits: float
    koi_steff: float
    koi_slogg: float
    koi_smet: float
    koi_smass: float
    ra: float
    dec: float
    koi_kepmag: float
    koi_gmag: float
    koi_rmag: float
    koi_imag: float
    koi_zmag: float
    koi_jmag: float
    koi_hmag: float
    koi_kmag: float
    loc_rowid: float
    st_pmra: float
    st_pmdec: float
    pl_tranmid: float
    koi_prad: float
    koi_tmag: float
    st_dist: float
    koi_srad: float
    koi_fittype_LS_MCMC: float
    koi_fittype_MCMC: float
    koi_fittype_none: float

# Try to load the label encoder if available
try:
    le = joblib.load("label_encoder.pkl")
    def decode_label(idx):
        return le.inverse_transform([int(idx)])[0]
except Exception:
    label_classes = ['APC', 'CANDIDATE', 'CONFIRMED', 'FALSE POSITIVE']
    def decode_label(idx):
        return label_classes[int(idx)]

# Load the feature list used for training
try:
    training_features = joblib.load("features.pkl")
except Exception:
    training_features = feature_names  # fallback, but may cause errors if not matching

@router.post("/predict")
def predict_exoplanet(data: ExoplanetInput):
    # Convert input to DataFrame
    input_df = pd.DataFrame([data.dict()])
    # Fix column name for koi_fittype_LS+MCMC
    if 'koi_fittype_LS_MCMC' in input_df.columns:
        input_df = input_df.rename(columns={'koi_fittype_LS_MCMC': 'koi_fittype_LS+MCMC'})
    # Predict
    pred = model.predict(input_df)
    # Convert prediction to string label
    pred_label = decode_label(pred[0])
    return {"prediction": pred_label}

@router.post("/predict_csv")
def predict_exoplanet_csv(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    df.columns = df.columns.str.strip()
    print("Received columns ({}):".format(len(df.columns)), list(df.columns))
    print("Expected columns ({}):".format(len(training_features)), list(training_features))
    missing = [col for col in training_features if col not in df.columns]
    extra = [col for col in df.columns if col not in training_features]
    print("Missing columns:", missing)
    print("Extra columns:", extra)
    # Reindex to match training features, fill missing with 0
    df = df.reindex(columns=training_features, fill_value=0)
    print("DataFrame shape after reindex:", df.shape)
    print("DataFrame columns after reindex:", list(df.columns))
    preds = model.predict(df)
    pred_labels = [decode_label(idx) for idx in preds]
    df['prediction'] = pred_labels
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=predicted_exoplanets.csv"})

@router.post("/encode_label")
def encode_label(label: str = Body(..., embed=True)):
    try:
        encoded = int(le.transform([label])[0])
        return {"encoded": encoded}
    except Exception as e:
        return {"error": str(e)}

@router.post("/decode_label")
def decode_label_api(encoded: int = Body(..., embed=True)):
    try:
        decoded = str(le.inverse_transform([encoded])[0])
        return {"label": decoded}
    except Exception as e:
        return {"error": str(e)}

app.include_router(router)
