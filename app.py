# ---------------------------------------------------
# Streamlit App: Next-Order Purchase Prediction
# ---------------------------------------------------

import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# ---------------------------------------------------
# Page configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Next-Basket Predictor", page_icon="🛒", layout="centered"
)

st.title("🛒 Instacart Next-Basket Predictor")
st.write(
    "Predict the **top products a user is most likely to reorder** "
    "in their next purchase using a LightGBM model."
)

# ---------------------------------------------------
# Paths
# ---------------------------------------------------
MODEL_PATH = Path("models/lightgbm_reorder.joblib")
FEATURES_PATH = Path("data/features/inference_features.parquet")


# ---------------------------------------------------
# Cached loaders
# ---------------------------------------------------
@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        st.error("Model file not found.")
        st.stop()
    return joblib.load(MODEL_PATH)


@st.cache_data
def load_features():
    if not FEATURES_PATH.exists():
        st.error("Feature file not found.")
        st.stop()
    return pd.read_parquet(FEATURES_PATH)


# ---------------------------------------------------
# Load resources
# ---------------------------------------------------
model = load_model()
features_all = load_features()

# Ensure correct datatype
features_all["user_id"] = features_all["user_id"].astype(int)

# ---------------------------------------------------
# User input
# ---------------------------------------------------
user_id = st.number_input("Enter User ID", min_value=1, step=1)

# st.write("Model expects features:")
# st.write(model.feature_name())


# ---------------------------------------------------
# Prediction logic
# ---------------------------------------------------
if st.button("Predict Next Order"):
    user_features = features_all[features_all["user_id"] == user_id]

    if user_features.empty:
        st.warning(
            "No historical data found for this user. This is a **cold-start user**."
        )
        st.stop()

    # Separate model features
    X = user_features.drop(
        columns=["user_id", "product_id", "product_name"], errors="ignore"
    )

    # Validate feature count
    expected_features = model.num_feature()

    if X.shape[1] != expected_features:
        st.error(
            f"Feature mismatch: model expects {expected_features} features, "
            f"but received {X.shape[1]}."
        )
        st.stop()

    # Predict probabilities (Booster returns probabilities directly)
    probs = model.predict(X)

    results = (
        user_features.assign(reorder_probability=probs)
        .sort_values("reorder_probability", ascending=False)
        .head(10)
    )

    # ---------------------------------------------------
    # Display results
    # ---------------------------------------------------
    st.subheader("🧠 Top Recommended Products")

    st.dataframe(
        results[["product_name", "reorder_probability"]], use_container_width=True
    )

    st.caption(
        "Probabilities represent the likelihood of a product being reordered "
        "in the user’s next basket."
    )

# ---------------------------------------------------
# Footer
# ---------------------------------------------------
st.markdown("---")
st.caption("Built with LightGBM · Parquet features · Streamlit inference pipeline")
