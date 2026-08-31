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
# GOOGLE SHEETS CONFIG
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
).reset_index(drop=True)


# ============================================================
# NUMERIC COLUMNS
# ============================================================

numeric_columns = [
    "up_prob",
    "down_prob",
    "up_pred",
    "down_pred"
]


for column in numeric_columns:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       MAIN PAGE
       ======================================================== */

    .stApp {
        background-color: #f5f7fb;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }


    /* ========================================================
       HEADER
       ======================================================== */

    .dashboard-header {
        background: linear-gradient(
            135deg,
            #111827 0%,
            #1f2937 100%
        );

        border-radius: 16px;

        padding: 28px 32px;

        margin-bottom: 22px;

        box-shadow:
            0 8px 25px rgba(15, 23, 42, 0.12);
    }


    .dashboard-title {
        color: #ffffff;

        font-size: 30px;

        font-weight: 750;

        margin: 0;

        letter-spacing: -0.5px;
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


    /* ========================================================
       INFORMATION CARDS
       ======================================================== */

    .info-card {
        background: #ffffff;

        border: 1px solid #e5e7eb;

        border-radius: 14px;

        padding: 20px 22px;

        min-height: 105px;

        box-shadow:
            0 3px 12px rgba(15, 23, 42, 0.05);
    }


    .info-label {
        color: #64748b;

        font-size: 12px;

        font-weight: 700;

        text-transform: uppercase;

        letter-spacing: 0.6px;
    }


    .info-value {
        color: #111827;

        font-size: 23px;

        font-weight: 750;

        margin-top: 8px;
    }


    /* ========================================================
       SECTION TITLE
       ======================================================== */

    .section-title {
        color: #111827;

        font-size: 20px;

        font-weight: 750;

        margin-top: 28px;

        margin-bottom: 14px;
    }


    /* ========================================================
       PREDICTION CARDS
       ======================================================== */

    .prediction-card-up {

        background: linear-gradient(
            135deg,
            #ecfdf5,
            #f0fdf4
        );

        border: 1px solid #a7f3d0;

        border-radius: 16px;

        padding: 25px;

        box-shadow:
            0 5px 16px rgba(16, 185, 129, 0.08);
    }


    .prediction-card-down {

        background: linear-gradient(
            135deg,
            #fff1f2,
            #fef2f2
        );

        border: 1px solid #fecdd3;

        border-radius: 16px;

        padding: 25px;

        box-shadow:
            0 5px 16px rgba(239, 68, 68, 0.08);
    }


    .prediction-heading {

        font-size: 14px;

        font-weight: 750;

        color: #475569;

        text-transform: uppercase;

        letter-spacing: 0.5px;
    }


    .up-probability {

        color: #059669;

        font-size: 36px;

        font-weight: 800;

        margin-top: 12px;
    }


    .down-probability {

        color: #dc2626;

        font-size: 36px;

        font-weight: 800;

        margin-top: 12px;
    }


    .up-status {

        color: #047857;

        font-size: 15px;

        font-weight: 700;

        margin-top: 4px;
    }


    .down-status {

        color: #b91c1c;

        font-size: 15px;

        font-weight: 700;

        margin-top: 4px;
    }


    /* ========================================================
       MODEL VERSION
       ======================================================== */

    .model-version {

        display: inline-block;

        background: #ffffff;

        border: 1px solid #e2e8f0;

        color: #64748b;

        border-radius: 20px;

        padding: 7px 13px;

        font-size: 12px;

        margin-top: 15px;
    }


    /* ========================================================
       SELECTED PREDICTION
       ======================================================== */

    .selected-box {

        background: #ffffff;

        border: 1px solid #e5e7eb;

        border-radius: 14px;

        padding: 18px;

        box-shadow:
            0 3px 12px rgba(15, 23, 42, 0.04);
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {

        text-align: center;

        color: #94a3b8;

        font-size: 11px;

        margin-top: 35px;

        padding-top: 15px;

        border-top: 1px solid #e2e8f0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LATEST DATA
# ============================================================

latest = df.iloc[0]


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

            Morning & Afternoon Model Predictions

            &nbsp; • &nbsp;

            <span class="live-dot">● LIVE</span>

            &nbsp; • &nbsp;

            Auto-refresh every 5 seconds

        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TOP INFORMATION CARDS
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
    """
    <div class="section-title">
        Latest Prediction
    </div>
    """,
    unsafe_allow_html=True
)


p1, p2 = st.columns(2)


# ============================================================
# UP MODEL
# ============================================================

with p1:

    up_prob = latest.get(
        "up_prob",
        None
    )


    if pd.isna(up_prob):

        up_probability = "N/A"

    else:

        up_probability = (
            f"{float(up_prob):.2%}"
        )


    up_pred = latest.get(
        "up_pred",
        None
    )


    if pd.isna(up_pred):

        up_status = "N/A"

    elif int(float(up_pred)) == 1:

        up_status = "UP"

    else:

        up_status = "NO UP"


    st.markdown(
        f"""
        <div class="prediction-card-up">

            <div class="prediction-heading">
                🟢 UP MODEL
            </div>

            <div class="up-probability">
                {up_probability}
            </div>

            <div class="up-status">
                Prediction: {up_status}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DOWN MODEL
# ============================================================

with p2:

    down_prob = latest.get(
        "down_prob",
        None
    )


    if pd.isna(down_prob):

        down_probability = "N/A"

    else:

        down_probability = (
            f"{float(down_prob):.2%}"
        )


    down_pred = latest.get(
        "down_pred",
        None
    )


    if pd.isna(down_pred):

        down_status = "N/A"

    elif int(float(down_pred)) == 1:

        down_status = "DOWN"

    else:

        down_status = "NO DOWN"


    st.markdown(
        f"""
        <div class="prediction-card-down">

            <div class="prediction-heading">
                🔴 DOWN MODEL
            </div>

            <div class="down-probability">
                {down_probability}
            </div>

            <div class="down-status">
                Prediction: {down_status}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# MODEL VERSION
# ============================================================

model_version = latest.get(
    "model_version",
    "N/A"
)


st.markdown(
    f"""
    <div class="model-version">
        ⚙️ Model Version: <b>{model_version}</b>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FILTER SECTION
# ============================================================

st.markdown(
    """
    <div class="section-title">
        Prediction Filter
    </div>
    """,
    unsafe_allow_html=True
)


filter_col1, filter_col2 = st.columns(2)


# ============================================================
# DATE DROPDOWN
# ============================================================

df["date_only"] = df["datetime"].dt.date


available_dates = sorted(
    df["date_only"].dropna().unique(),
    reverse=True
)


with filter_col1:

    selected_date = st.selectbox(
        "Select Date",
        available_dates,
        index=0,
        format_func=lambda x:
            x.strftime("%d %b %Y")
    )


# ============================================================
# FILTER BY DATE
# ============================================================

date_df = df[
    df["date_only"] == selected_date
].copy()


available_datetimes = sorted(
    date_df["datetime"].dropna().unique(),
    reverse=True
)


# ============================================================
# DATETIME DROPDOWN
# ============================================================

with filter_col2:

    selected_datetime = st.selectbox(
        "Select Datetime",
        available_datetimes,
        index=0,
        format_func=lambda x:
            x.strftime("%d %b %Y %H:%M")
    )


# ============================================================
# SELECTED ROW
# ============================================================

selected_rows = date_df[
    date_df["datetime"] == selected_datetime
]


if not selected_rows.empty:

    selected = selected_rows.iloc[0]


    st.markdown(
        """
        <div class="section-title">
            Selected Prediction
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # Selected top cards
    # --------------------------------------------------------

    s1, s2, s3 = st.columns(3)


    with s1:

        st.metric(
            "Symbol",
            selected["symbol"]
        )


    with s2:

        st.metric(
            "Session",
            selected["session"]
        )


    with s3:

        st.metric(
            "Datetime",
            selected["datetime"].strftime(
                "%d %b %Y %H:%M"
            )
        )


    # --------------------------------------------------------
    # Selected probabilities
    # --------------------------------------------------------

    s4, s5 = st.columns(2)


    with s4:

        selected_up_prob = selected.get(
            "up_prob",
            None
        )


        if pd.isna(selected_up_prob):

            value = "N/A"

        else:

            value = (
                f"{float(selected_up_prob):.2%}"
            )


        st.metric(
            "UP Probability",
            value
        )


    with s5:

        selected_down_prob = selected.get(
            "down_prob",
            None
        )


        if pd.isna(selected_down_prob):

            value = "N/A"

        else:

            value = (
                f"{float(selected_down_prob):.2%}"
            )


        st.metric(
            "DOWN Probability",
            value
        )


    # --------------------------------------------------------
    # Selected predictions
    # --------------------------------------------------------

    s6, s7 = st.columns(2)


    with s6:

        selected_up_pred = selected.get(
            "up_pred",
            None
        )


        if pd.isna(selected_up_pred):

            value = "N/A"

        elif int(float(selected_up_pred)) == 1:

            value = "UP"

        else:

            value = "NO UP"


        st.metric(
            "UP Prediction",
            value
        )


    with s7:

        selected_down_pred = selected.get(
            "down_pred",
            None
        )


        if pd.isna(selected_down_pred):

            value = "N/A"

        elif int(float(selected_down_pred)) == 1:

            value = "DOWN"

        else:

            value = "NO DOWN"


        st.metric(
            "DOWN Prediction",
            value
        )


# ============================================================
# PREDICTION HISTORY
# ============================================================

st.markdown(
    """
    <div class="section-title">
        Prediction History
    </div>
    """,
    unsafe_allow_html=True
)


history_df = df.copy()


# Remove helper column

history_df = history_df.drop(
    columns=["date_only"],
    errors="ignore"
)


# Format datetime

history_df["datetime"] = (
    history_df["datetime"]
    .dt.strftime("%d %b %Y %H:%M")
)


# Format probabilities

history_df["up_prob"] = (
    history_df["up_prob"]
    .apply(
        lambda x:
        f"{float(x):.2%}"
        if pd.notna(x)
        else "N/A"
    )
)


history_df["down_prob"] = (
    history_df["down_prob"]
    .apply(
        lambda x:
        f"{float(x):.2%}"
        if pd.notna(x)
        else "N/A"
    )
)


# ============================================================
# RENAME COLUMNS
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
# ORDER COLUMNS
# ============================================================

history_columns = [
    "Symbol",
    "Datetime",
    "Session",
    "UP Prediction",
    "DOWN Prediction",
    "UP Probability",
    "DOWN Probability",
    "Model Version"
]


history_df = history_df[
    [
        column
        for column in history_columns
        if column in history_df.columns
    ]
]


# ============================================================
# DISPLAY HISTORY
# ============================================================

st.dataframe(
    history_df,
    use_container_width=True,
    hide_index=True,
    height=450
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        NIFTY Intraday Prediction System
        &nbsp; • &nbsp;
        Live Google Sheets Data
        &nbsp; • &nbsp;
        Auto-refresh: 5 seconds
    </div>
    """,
    unsafe_allow_html=True
)