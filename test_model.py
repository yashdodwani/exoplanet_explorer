import pytest
import joblib
import numpy as np
import pandas as pd

# Load model and label encoder
model = joblib.load("LightGBM_exoplanet_model.pkl")
le = joblib.load("label_encoder.pkl")
features = joblib.load("features.pkl")

def test_model_on_custom_input():
    # Example custom input (fill with realistic values or zeros for demo)
    custom_input = {
        'koi_score': 0.5,
        'koi_period': 1.0,
        'koi_eccen': 0.0,
        'koi_impact': 0.1,
        'koi_duration': 2.0,
        'koi_depth': 0.01,
        'koi_ror': 0.2,
        'koi_srho': 1.0,
        'koi_incl': 89.0,
        'koi_teq': 500.0,
        'koi_insol': 1.0,
        'koi_dor': 10.0,
        'koi_model_snr': 20.0,
        'koi_count': 1.0,
        'koi_num_transits': 3.0,
        'koi_steff': 5700.0,
        'koi_slogg': 4.4,
        'koi_smet': 0.0,
        'koi_smass': 1.0,
        'ra': 290.0,
        'dec': 44.0,
        'koi_kepmag': 12.0,
        'koi_gmag': 13.0,
        'koi_rmag': 13.0,
        'koi_imag': 13.0,
        'koi_zmag': 13.0,
        'koi_jmag': 12.0,
        'koi_hmag': 12.0,
        'koi_kmag': 12.0,
        'loc_rowid': 1.0,
        'st_pmra': 0.0,
        'st_pmdec': 0.0,
        'pl_tranmid': 0.0,
        'koi_prad': 1.0,
        'koi_tmag': 12.0,
        'st_dist': 100.0,
        'koi_srad': 1.0,
        'Relative_Error_PLANET_ORBPER': 0.0,
        'Relative_Error_PLANET_RADE': 0.0,
        'Relative_Error_PLANET_TRANDEP': 0.0,
        'Relative_Error_PLANET_TRANDURH': 0.0,
        'Relative_Error_PLANET_TRANMID': 0.0,
        'Relative_Error_STAR_DIST': 0.0,
        'Relative_Error_STAR_LOGG': 0.0,
        'Relative_Error_STAR_PMDEC': 0.0,
        'Relative_Error_STAR_PMRA': 0.0,
        'Relative_Error_STAR_RAD': 0.0,
        'Relative_Error_STAR_TEFF': 0.0,
        'Relative_Error_STAR_TMAG': 0.0,
        'koi_fittype_LS+MCMC': 1.0,
        'koi_fittype_MCMC': 0.0,
        'koi_fittype_none': 0.0
    }
    # Ensure all features are present and in correct order
    input_df = pd.DataFrame([custom_input])[features]
    pred = model.predict(input_df)
    pred_label = le.inverse_transform([int(pred[0])])[0]
    print(f"Predicted label: {pred_label}")
    assert pred_label in le.classes_

