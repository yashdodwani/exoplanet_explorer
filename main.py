from fastapi import FastAPI, APIRouter, UploadFile, File
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
label_classes = ['CANDIDATE', 'CONFIRMED', 'FALSE POSITIVE']

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
    label_classes = ['CANDIDATE', 'CONFIRMED', 'FALSE POSITIVE']
    def decode_label(idx):
        return label_classes[int(idx)]

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
    # Read uploaded CSV file into DataFrame
    df = pd.read_csv(file.file)
    # Fix column name for koi_fittype_LS+MCMC if needed
    if 'koi_fittype_LS_MCMC' in df.columns:
        df = df.rename(columns={'koi_fittype_LS_MCMC': 'koi_fittype_LS+MCMC'})
    # Predict
    preds = model.predict(df)
    # Convert predictions to string labels
    pred_labels = [decode_label(idx) for idx in preds]
    # Add predictions to DataFrame
    df['prediction'] = pred_labels
    # Convert DataFrame to CSV in memory
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=predicted_exoplanets.csv"})

app.include_router(router)
