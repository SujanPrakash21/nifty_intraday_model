# import streamlit as st
# import pandas as pd
# import gspread
# from google.oauth2.service_account import Credentials
# from streamlit_autorefresh import st_autorefresh

# # ============================================================
# # PAGE CONFIG
# # ============================================================

# st.set_page_config(
#     page_title="NIFTY Model Dashboard",
#     page_icon="📈",
#     layout="wide"
# )

# st_autorefresh(
#     interval=5000,
#     key="data_refresh"
# )



# SCOPES = [
#     "https://www.googleapis.com/auth/spreadsheets",
#     "https://www.googleapis.com/auth/drive"
# ]

# credentials = Credentials.from_service_account_info(
#     dict(st.secrets["gcp_service_account"]),
#     scopes=SCOPES
# )

# gc = gspread.authorize(credentials)



# GOOGLE_SHEET_ID = "1EP2UEufBvnUtf8LxDpmjuT4lDQFVEGp2apLwFdtfod4"
# GOOGLE_SHEET_TAB = "Predictions"


# spreadsheet = gc.open_by_key(
#     GOOGLE_SHEET_ID
# )

# sheet = spreadsheet.worksheet(
#     GOOGLE_SHEET_TAB
# )

# records = sheet.get_all_records()

# df = pd.DataFrame(records)


# if df.empty:
#     st.warning("No prediction data available.")
#     st.stop()


# df["datetime"] = pd.to_datetime(
#     df["datetime"],
#     errors="coerce"
# )


# df = df.dropna(
#     subset=["datetime"]
# )


# df = df.sort_values(
#     "datetime",
#     ascending=False
# )


# # Convert probabilities to numeric

# df["up_prob"] = pd.to_numeric(
#     df["up_prob"],
#     errors="coerce"
# )

# df["down_prob"] = pd.to_numeric(
#     df["down_prob"],
#     errors="coerce"
# )




# st.title(
#     "📈 NIFTY Intraday Model Dashboard"
# )

# st.caption(
#     "Morning & Afternoon Model Predictions"
# )


# latest = df.iloc[0]




# col1, col2, col3 = st.columns(3)


# with col1:

#     st.metric(
#         "Symbol",
#         latest["symbol"]
#     )


# with col2:

#     st.metric(
#         "Session",
#         latest["session"]
#     )


# with col3:

#     st.metric(
#         "Datetime",
#         latest["datetime"].strftime(
#             "%d %b %Y %H:%M"
#         )
#     )


# # ============================================================
# # LATEST PREDICTION
# # ============================================================

# st.subheader(
#     "Latest Prediction"
# )


# c1, c2 = st.columns(2)


# with c1:

#     if pd.isna(latest["up_prob"]):

#         up_value = "N/A"

#     else:

#         up_value = f"{latest['up_prob']:.2%}"


#     st.metric(
#         "UP Probability",
#         up_value
#     )


# with c2:

#     if pd.isna(latest["down_prob"]):

#         down_value = "N/A"

#     else:

#         down_value = f"{latest['down_prob']:.2%}"


#     st.metric(
#         "DOWN Probability",
#         down_value
#     )


# # ============================================================
# # PREDICTIONS
# # ============================================================

# p1, p2 = st.columns(2)


# with p1:

#     up_pred = latest["up_pred"]

#     if pd.isna(up_pred) or up_pred == "":
#         up_prediction = "N/A"

#     elif int(float(up_pred)) == 1:
#         up_prediction = "UP"

#     else:
#         up_prediction = "NO"


#     st.metric(
#         "UP Prediction",
#         up_prediction
#     )


# with p2:

#     down_pred = latest["down_pred"]

#     if pd.isna(down_pred) or down_pred == "":
#         down_prediction = "N/A"

#     elif int(float(down_pred)) == 1:
#         down_prediction = "DOWN"

#     else:
#         down_prediction = "NO"


#     st.metric(
#         "DOWN Prediction",
#         down_prediction
#     )


# # ============================================================
# # MODEL VERSION
# # ============================================================

# st.caption(
#     f"Model Version: {latest['model_version']}"
# )


# # ============================================================
# # PREDICTION HISTORY
# # ============================================================

# st.subheader(
#     "Prediction History"
# )


# history_df = df.copy()


# history_df["datetime"] = history_df[
#     "datetime"
# ].dt.strftime(
#     "%d %b %Y %H:%M"
# )


# st.dataframe(
#     history_df,
#     use_container_width=True,
#     hide_index=True
# )


import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from streamlit_autorefresh import st_autorefresh


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="NIFTY Model Dashboard",
    page_icon="📈",
    layout="wide"
)


# ============================================================
# AUTO REFRESH
# ============================================================

st_autorefresh(
    interval=5000,
    key="data_refresh"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #f5f7fb;
    }

    /* Remove excessive top padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Main title */
    .main-title {
        font-size: 32px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 2px;
    }

    .subtitle {
        font-size: 14px;
        color: #6b7280;
        margin-bottom: 20px;
    }

    /* Header */
    .dashboard-header {
        background: linear-gradient(
            135deg,
            #111827,
            #1f2937
        );
        padding: 24px 28px;
        border-radius: 16px;
        margin-bottom: 24px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    }

    .dashboard-header-title {
        color: white;
        font-size: 28px;
        font-weight: 700;
        margin: 0;
    }

    .dashboard-header-subtitle {
        color: #cbd5e1;
        font-size: 14px;
        margin-top: 5px;
    }

    /* Metric cards */
    .metric-card {
        background: white;
        padding: 18px 20px;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 3px 12px rgba(0,0,0,0.04);
        min-height: 95px;
    }

    .metric-label {
        color: #6b7280;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 7px;
    }

    .metric-value {
        color: #111827;
        font-size: 21px;
        font-weight: 700;
    }

    /* Prediction cards */
    .prediction-card {
        padding: 22px;
        border-radius: 16px;
        min-height: 145px;
        box-shadow: 0 5px 16px rgba(0,0,0,0.06);
    }

    .up-card {
        background: linear-gradient(
            135deg,
            #ecfdf5,
            #d1fae5
        );
        border: 1px solid #a7f3d0;
    }

    .down-card {
        background: linear-gradient(
            135deg,
            #fef2f2,
            #fee2e2
        );
        border: 1px solid #fecaca;
    }

    .prediction-title {
        font-size: 14px;
        font-weight: 600;
        color: #6b7280;
        margin-bottom: 8px;
    }

    .prediction-value {
        font-size: 30px;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .up-value {
        color: #059669;
    }

    .down-value {
        color: #dc2626;
    }

    .probability {
        font-size: 18px;
        font-weight: 700;
    }

    /* Section titles */
    .section-title {
        font-size: 20px;
        font-weight: 700;
        color: #111827;
        margin-top: 28px;
        margin-bottom: 14px;
    }

    /* Status badge */
    .status-badge {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
    }

    .live-badge {
        background: #dcfce7;
        color: #15803d;
    }

    /* Model version */
    .model-version {
        background: white;
        border: 1px solid #e5e7eb;
        padding: 10px 14px;
        border-radius: 10px;
        color: #6b7280;
        font-size: 13px;
        display: inline-block;
        margin-top: 10px;
    }

    /* Table */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# GOOGLE AUTHENTICATION
# ============================================================

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_info(
    dict(st.secrets["gcp_service_account"]),
    scopes=SCOPES
)

gc = gspread.authorize(credentials)


# ============================================================
# GOOGLE SHEET
# ============================================================

GOOGLE_SHEET_ID = "1EP2UEufBvnUtf8LxDpmjuT4lDQFVEGp2apLwFdtfod4"
GOOGLE_SHEET_TAB = "Predictions"


spreadsheet = gc.open_by_key(
    GOOGLE_SHEET_ID
)

sheet = spreadsheet.worksheet(
    GOOGLE_SHEET_TAB
)


# ============================================================
# LOAD DATA
# ============================================================

records = sheet.get_all_records()

df = pd.DataFrame(records)


if df.empty:

    st.warning(
        "No prediction data available."
    )

    st.stop()


df["datetime"] = pd.to_datetime(
    df["datetime"],
    errors="coerce"
)


df = df.dropna(
    subset=["datetime"]
)


df = df.sort_values(
    "datetime",
    ascending=False
)


# ============================================================
# NUMERIC CONVERSION
# ============================================================

for col in [
    "up_prob",
    "down_prob",
    "up_pred",
    "down_pred"
]:

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="dashboard-header">

        <div class="dashboard-header-title">
            📈 NIFTY Intraday Model Dashboard
        </div>

        <div class="dashboard-header-subtitle">
            Morning & Afternoon Model Predictions
            &nbsp; • &nbsp;
            Live Data
            &nbsp; • &nbsp;
            Auto-refresh: 5 seconds
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LATEST DATA
# ============================================================

latest = df.iloc[0]


# ============================================================
# TOP METRICS
# ============================================================

col1, col2, col3 = st.columns(3)


with col1:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                SYMBOL
            </div>

            <div class="metric-value">
                {latest["symbol"]}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                SESSION
            </div>

            <div class="metric-value">
                {latest["session"]}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                LATEST DATETIME
            </div>

            <div class="metric-value">
                {latest["datetime"].strftime("%d %b %Y %H:%M")}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# LATEST PREDICTION
# ============================================================

st.markdown(
    '<div class="section-title">Latest Prediction</div>',
    unsafe_allow_html=True
)


c1, c2 = st.columns(2)


# ============================================================
# UP CARD
# ============================================================

with c1:

    if pd.isna(latest["up_prob"]):

        up_probability = "N/A"

    else:

        up_probability = (
            f"{latest['up_prob']:.2%}"
        )


    up_pred = latest["up_pred"]


    if pd.isna(up_pred):

        up_prediction = "N/A"

    elif int(float(up_pred)) == 1:

        up_prediction = "UP"

    else:

        up_prediction = "NO UP"


    st.markdown(
        f"""
        <div class="prediction-card up-card">

            <div class="prediction-title">
                🟢 UP MODEL
            </div>

            <div class="prediction-value up-value">
                {up_prediction}
            </div>

            <div class="probability up-value">
                Probability: {up_probability}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DOWN CARD
# ============================================================

with c2:

    if pd.isna(latest["down_prob"]):

        down_probability = "N/A"

    else:

        down_probability = (
            f"{latest['down_prob']:.2%}"
        )


    down_pred = latest["down_pred"]


    if pd.isna(down_pred):

        down_prediction = "N/A"

    elif int(float(down_pred)) == 1:

        down_prediction = "DOWN"

    else:

        down_prediction = "NO DOWN"


    st.markdown(
        f"""
        <div class="prediction-card down-card">

            <div class="prediction-title">
                🔴 DOWN MODEL
            </div>

            <div class="prediction-value down-value">
                {down_prediction}
            </div>

            <div class="probability down-value">
                Probability: {down_probability}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# MODEL VERSION
# ============================================================

st.markdown(
    f"""
    <div class="model-version">
        ⚙️ Model Version: <strong>{latest["model_version"]}</strong>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PREDICTION HISTORY
# ============================================================

st.markdown(
    '<div class="section-title">Prediction History</div>',
    unsafe_allow_html=True
)


history_df = df.copy()


history_df["datetime"] = history_df[
    "datetime"
].dt.strftime(
    "%d %b %Y %H:%M"
)


# Rename columns for display

history_df = history_df.rename(
    columns={
        "symbol": "Symbol",
        "datetime": "Datetime",
        "session": "Session",
        "up_pred": "UP Prediction",
        "down_pred": "DOWN Prediction",
        "up_prob": "UP Probability",
        "down_prob": "DOWN Probability",
        "model_version": "Model Version"
    }
)


# Format probabilities

history_df["UP Probability"] = (
    history_df["UP Probability"]
    .apply(
        lambda x:
        f"{x:.2%}"
        if pd.notna(x)
        else "N/A"
    )
)


history_df["DOWN Probability"] = (
    history_df["DOWN Probability"]
    .apply(
        lambda x:
        f"{x:.2%}"
        if pd.notna(x)
        else "N/A"
    )
)


st.dataframe(
    history_df,
    use_container_width=True,
    hide_index=True,
    height=500
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#9ca3af;
        font-size:12px;
        margin-top:25px;
    ">
        NIFTY Intraday Prediction System
        &nbsp; • &nbsp;
        Data refreshes automatically every 5 seconds
    </div>
    """,
    unsafe_allow_html=True
)