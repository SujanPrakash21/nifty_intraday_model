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
# AUTO REFRESH - EVERY 5 SECONDS
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

    /* =========================
       PAGE
       ========================= */

    .stApp {
        background: #f4f6f9;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }


    /* =========================
       HEADER
       ========================= */

    .dashboard-header {
        background: linear-gradient(
            135deg,
            #111827 0%,
            #1f2937 100%
        );

        padding: 24px 28px;

        border-radius: 14px;

        margin-bottom: 22px;

        box-shadow:
            0 6px 20px rgba(0,0,0,0.10);
    }

    .dashboard-title {
        color: #ffffff;
        font-size: 30px;
        font-weight: 750;
        margin: 0;
        line-height: 1.2;
    }

    .dashboard-subtitle {
        color: #cbd5e1;
        font-size: 14px;
        margin-top: 7px;
    }

    .live-dot {
        color: #22c55e;
        font-weight: 700;
    }


    /* =========================
       TOP INFO CARDS
       ========================= */

    .info-card {
        background: #ffffff;

        border: 1px solid #e5e7eb;

        border-radius: 12px;

        padding: 18px 20px;

        box-shadow:
            0 3px 12px rgba(0,0,0,0.04);

        height: 100px;
    }

    .info-label {
        color: #6b7280;

        font-size: 12px;

        font-weight: 700;

        letter-spacing: 0.5px;

        text-transform: uppercase;

        margin-bottom: 9px;
    }

    .info-value {
        color: #111827;

        font-size: 21px;

        font-weight: 750;
    }


    /* =========================
       SECTION TITLE
       ========================= */

    .section-title {
        color: #111827;

        font-size: 20px;

        font-weight: 750;

        margin-top: 28px;

        margin-bottom: 14px;
    }


    /* =========================
       UP / DOWN CARDS
       ========================= */

    .prediction-card {

        border-radius: 14px;

        padding: 22px 24px;

        min-height: 155px;

        box-shadow:
            0 5px 16px rgba(0,0,0,0.05);
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
            #fff1f2,
            #ffe4e6
        );

        border: 1px solid #fecdd3;
    }


    .prediction-header {

        font-size: 13px;

        font-weight: 750;

        color: #4b5563;

        margin-bottom: 12px;
    }


    .prediction-main {

        font-size: 29px;

        font-weight: 800;

        margin-bottom: 8px;
    }


    .up-main {
        color: #059669;
    }


    .down-main {
        color: #dc2626;
    }


    .prediction-probability {

        font-size: 17px;

        font-weight: 700;
    }


    .up-probability {
        color: #047857;
    }


    .down-probability {
        color: #b91c1c;
    }


    /* =========================
       MODEL VERSION
       ========================= */

    .model-version {

        display: inline-block;

        background: #ffffff;

        border: 1px solid #e5e7eb;

        border-radius: 8px;

        padding: 7px 12px;

        margin-top: 12px;

        color: #6b7280;

        font-size: 12px;
    }


    /* =========================
       TABLE
       ========================= */

    .history-container {

        background: #ffffff;

        border-radius: 12px;

        padding: 4px;

        border: 1px solid #e5e7eb;

        box-shadow:
            0 3px 12px rgba(0,0,0,0.04);
    }


    /* =========================
       FOOTER
       ========================= */

    .footer {

        text-align: center;

        color: #9ca3af;

        font-size: 11px;

        margin-top: 24px;

        padding-top: 12px;

        border-top: 1px solid #e5e7eb;
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

GOOGLE_SHEET_ID = (
    "1EP2UEufBvnUtf8LxDpmjuT4lDQFVEGp2apLwFdtfod4"
)

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


# ============================================================
# CLEAN DATA
# ============================================================

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

    <div class="dashboard-title">
        📈 NIFTY Intraday Model Dashboard
    </div>

    <div class="dashboard-subtitle">
        <span class="live-dot">● LIVE</span>
        &nbsp;&nbsp; Morning & Afternoon Model Predictions
        &nbsp; • &nbsp;
        Auto-refresh every 5 seconds
    </div>

</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# LATEST ROW
# ============================================================

latest = df.iloc[0]


# ============================================================
# TOP INFORMATION
# ============================================================

col1, col2, col3 = st.columns(3)


with col1:

    st.markdown(
        f"""
<div class="info-card">

    <div class="info-label">
        Symbol
    </div>

    <div class="info-value">
        {latest["symbol"]}
    </div>

</div>
""",
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
<div class="info-card">

    <div class="info-label">
        Session
    </div>

    <div class="info-value">
        {latest["session"]}
    </div>

</div>
""",
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
<div class="info-card">

    <div class="info-label">
        Latest Datetime
    </div>

    <div class="info-value">
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
# UP MODEL
# ============================================================

with c1:

    up_prob = latest["up_prob"]

    if pd.isna(up_prob):

        up_probability = "N/A"

    else:

        up_probability = (
            f"{up_prob:.2%}"
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

    <div class="prediction-header">
        🟢 &nbsp; UP MODEL
    </div>

    <div class="prediction-main up-main">
        {up_prediction}
    </div>

    <div class="prediction-probability up-probability">
        Probability &nbsp; {up_probability}
    </div>

</div>
""",
        unsafe_allow_html=True
    )


# ============================================================
# DOWN MODEL
# ============================================================

with c2:

    down_prob = latest["down_prob"]


    if pd.isna(down_prob):

        down_probability = "N/A"

    else:

        down_probability = (
            f"{down_prob:.2%}"
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

    <div class="prediction-header">
        🔴 &nbsp; DOWN MODEL
    </div>

    <div class="prediction-main down-main">
        {down_prediction}
    </div>

    <div class="prediction-probability down-probability">
        Probability &nbsp; {down_probability}
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
    ⚙️ &nbsp; Model Version:
    <strong>{latest["model_version"]}</strong>
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


history_df["datetime"] = (
    history_df["datetime"]
    .dt.strftime("%d %b %Y %H:%M")
)


# ============================================================
# DISPLAY COLUMNS
# ============================================================

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


# ============================================================
# FORMAT PROBABILITIES
# ============================================================

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


# ============================================================
# DISPLAY TABLE
# ============================================================

st.markdown(
    '<div class="history-container">',
    unsafe_allow_html=True
)


st.dataframe(
    history_df,
    use_container_width=True,
    hide_index=True,
    height=500
)


st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="footer">
    NIFTY Intraday Prediction System
    &nbsp; • &nbsp;
    Google Sheets Data
    &nbsp; • &nbsp;
    Auto-refresh: 5 seconds
</div>
""",
    unsafe_allow_html=True
)