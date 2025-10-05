import streamlit as st
import pandas as pd
import requests
import io
st.cache_data.clear()
st.set_page_config(page_title="Exoplanet Explorer", layout="centered", page_icon="🪐", initial_sidebar_state="auto")

st.markdown(
    """
    <style>
    body {
        background-color: #181825;
        color: #e0e0e0;
    }
    .stApp {
        background-color: #181825;
    }
    .css-1d391kg, .css-1v0mbdj, .css-1cpxqw2, .css-1offfwp, .css-1q8dd3e, .css-1lcbmhc {
        background-color: #232136 !important;
        color: #e0e0e0 !important;
    }
    .stButton>button {
        color: #fff;
        background: linear-gradient(90deg, #7f5af0 0%, #232136 100%);
        border: none;
        border-radius: 8px;
        padding: 0.5em 2em;
        font-weight: bold;
    }
    .stFileUploader>div>div {
        background: #232136;
        color: #e0e0e0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🪐 Exoplanet Explorer")

st.markdown("""
Upload a CSV file or enter the features for a single exoplanet candidate below to predict its disposition (CONFIRMED, CANDIDATE, FALSE POSITIVE).
""")

API_URL = "/api"

with st.expander("🔢 Predict for a single exoplanet candidate"):
    with st.form("single_form"):
        # All features except koi_disposition and relative error columns
        koi_score = st.number_input("koi_score", value=0.0, format="%f")
        koi_period = st.number_input("koi_period", value=0.0, format="%f")
        koi_eccen = st.number_input("koi_eccen", value=0.0, format="%f")
        koi_impact = st.number_input("koi_impact", value=0.0, format="%f")
        koi_duration = st.number_input("koi_duration", value=0.0, format="%f")
        koi_depth = st.number_input("koi_depth", value=0.0, format="%f")
        koi_ror = st.number_input("koi_ror", value=0.0, format="%f")
        koi_srho = st.number_input("koi_srho", value=0.0, format="%f")
        koi_incl = st.number_input("koi_incl", value=0.0, format="%f")
        koi_teq = st.number_input("koi_teq", value=0.0, format="%f")
        koi_insol = st.number_input("koi_insol", value=0.0, format="%f")
        koi_dor = st.number_input("koi_dor", value=0.0, format="%f")
        koi_model_snr = st.number_input("koi_model_snr", value=0.0, format="%f")
        koi_count = st.number_input("koi_count", value=0.0, format="%f")
        koi_num_transits = st.number_input("koi_num_transits", value=0.0, format="%f")
        koi_steff = st.number_input("koi_steff", value=0.0, format="%f")
        koi_slogg = st.number_input("koi_slogg", value=0.0, format="%f")
        koi_smet = st.number_input("koi_smet", value=0.0, format="%f")
        koi_smass = st.number_input("koi_smass", value=0.0, format="%f")
        ra = st.number_input("ra", value=0.0, format="%f")
        dec = st.number_input("dec", value=0.0, format="%f")
        koi_kepmag = st.number_input("koi_kepmag", value=0.0, format="%f")
        koi_gmag = st.number_input("koi_gmag", value=0.0, format="%f")
        koi_rmag = st.number_input("koi_rmag", value=0.0, format="%f")
        koi_imag = st.number_input("koi_imag", value=0.0, format="%f")
        koi_zmag = st.number_input("koi_zmag", value=0.0, format="%f")
        koi_jmag = st.number_input("koi_jmag", value=0.0, format="%f")
        koi_hmag = st.number_input("koi_hmag", value=0.0, format="%f")
        koi_kmag = st.number_input("koi_kmag", value=0.0, format="%f")
        loc_rowid = st.number_input("loc_rowid", value=0.0, format="%f")
        st_pmra = st.number_input("st_pmra", value=0.0, format="%f")
        st_pmdec = st.number_input("st_pmdec", value=0.0, format="%f")
        pl_tranmid = st.number_input("pl_tranmid", value=0.0, format="%f")
        koi_prad = st.number_input("koi_prad", value=0.0, format="%f")
        koi_tmag = st.number_input("koi_tmag", value=0.0, format="%f")
        st_dist = st.number_input("st_dist", value=0.0, format="%f")
        koi_srad = st.number_input("koi_srad", value=0.0, format="%f")
        koi_fittype_LS_MCMC = st.number_input("koi_fittype_LS_MCMC", value=0.0, format="%f")
        koi_fittype_MCMC = st.number_input("koi_fittype_MCMC", value=0.0, format="%f")
        koi_fittype_none = st.number_input("koi_fittype_none", value=0.0, format="%f")
        submitted = st.form_submit_button("Predict")
        if submitted:
            payload = {
                "koi_score": koi_score,
                "koi_period": koi_period,
                "koi_eccen": koi_eccen,
                "koi_impact": koi_impact,
                "koi_duration": koi_duration,
                "koi_depth": koi_depth,
                "koi_ror": koi_ror,
                "koi_srho": koi_srho,
                "koi_incl": koi_incl,
                "koi_teq": koi_teq,
                "koi_insol": koi_insol,
                "koi_dor": koi_dor,
                "koi_model_snr": koi_model_snr,
                "koi_count": koi_count,
                "koi_num_transits": koi_num_transits,
                "koi_steff": koi_steff,
                "koi_slogg": koi_slogg,
                "koi_smet": koi_smet,
                "koi_smass": koi_smass,
                "ra": ra,
                "dec": dec,
                "koi_kepmag": koi_kepmag,
                "koi_gmag": koi_gmag,
                "koi_rmag": koi_rmag,
                "koi_imag": koi_imag,
                "koi_zmag": koi_zmag,
                "koi_jmag": koi_jmag,
                "koi_hmag": koi_hmag,
                "koi_kmag": koi_kmag,
                "loc_rowid": loc_rowid,
                "st_pmra": st_pmra,
                "st_pmdec": st_pmdec,
                "pl_tranmid": pl_tranmid,
                "koi_prad": koi_prad,
                "koi_tmag": koi_tmag,
                "st_dist": st_dist,
                "koi_srad": koi_srad,
                "koi_fittype_LS_MCMC": koi_fittype_LS_MCMC,
                "koi_fittype_MCMC": koi_fittype_MCMC,
                "koi_fittype_none": koi_fittype_none
            }
            try:
                response = requests.post(f"{API_URL}/predict", json=payload)
                if response.status_code == 200:
                    st.success(f"Prediction: {response.json()['prediction']}")
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Request failed: {e}")

st.markdown("---")

with st.expander("📁 Predict for a batch (CSV upload)"):
    uploaded_file = st.file_uploader("Upload CSV file with the required columns", type=["csv"])
    if uploaded_file is not None:
        if st.button("Predict for CSV"):
            try:
                files = {"file": uploaded_file.getvalue()}
                response = requests.post(f"{API_URL}/predict_csv", files={"file": (uploaded_file.name, uploaded_file, "text/csv")})
                if response.status_code == 200:
                    st.success("Prediction complete! Download your results below.")
                    st.download_button(
                        label="Download Predicted CSV",
                        data=response.content,
                        file_name="predicted_exoplanets.csv",
                        mime="text/csv"
                    )
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Request failed: {e}")

st.markdown("""
<style>
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
