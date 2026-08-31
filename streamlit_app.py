# # import streamlit as st
# # import pandas as pd
# # import gspread
# # from google.oauth2.service_account import Credentials
# # from streamlit_autorefresh import st_autorefresh

# # # ============================================================
# # # PAGE CONFIG
# # # ============================================================

# # st.set_page_config(
# #     page_title="NIFTY Model Dashboard",
# #     page_icon="📈",
# #     layout="wide"
# # )

# # st_autorefresh(
# #     interval=5000,
# #     key="data_refresh"
# # )



# # SCOPES = [
# #     "https://www.googleapis.com/auth/spreadsheets",
# #     "https://www.googleapis.com/auth/drive"
# # ]

# # credentials = Credentials.from_service_account_info(
# #     dict(st.secrets["gcp_service_account"]),
# #     scopes=SCOPES
# # )

# # gc = gspread.authorize(credentials)



# # GOOGLE_SHEET_ID = "1EP2UEufBvnUtf8LxDpmjuT4lDQFVEGp2apLwFdtfod4"
# # GOOGLE_SHEET_TAB = "Predictions"


# # spreadsheet = gc.open_by_key(
# #     GOOGLE_SHEET_ID
# # )

# # sheet = spreadsheet.worksheet(
# #     GOOGLE_SHEET_TAB
# # )

# # records = sheet.get_all_records()

# # df = pd.DataFrame(records)


# # if df.empty:
# #     st.warning("No prediction data available.")
# #     st.stop()


# # df["datetime"] = pd.to_datetime(
# #     df["datetime"],
# #     errors="coerce"
# # )


# # df = df.dropna(
# #     subset=["datetime"]
# # )


# # df = df.sort_values(
# #     "datetime",
# #     ascending=False
# # )


# # # Convert probabilities to numeric

# # df["up_prob"] = pd.to_numeric(
# #     df["up_prob"],
# #     errors="coerce"
# # )

# # df["down_prob"] = pd.to_numeric(
# #     df["down_prob"],
# #     errors="coerce"
# # )




# # st.title(
# #     "📈 NIFTY Intraday Model Dashboard"
# # )

# # st.caption(
# #     "Morning & Afternoon Model Predictions"
# # )


# # latest = df.iloc[0]




# # col1, col2, col3 = st.columns(3)


# # with col1:

# #     st.metric(
# #         "Symbol",
# #         latest["symbol"]
# #     )


# # with col2:

# #     st.metric(
# #         "Session",
# #         latest["session"]
# #     )


# # with col3:

# #     st.metric(
# #         "Datetime",
# #         latest["datetime"].strftime(
# #             "%d %b %Y %H:%M"
# #         )
# #     )


# # # ============================================================
# # # LATEST PREDICTION
# # # ============================================================

# # st.subheader(
# #     "Latest Prediction"
# # )


# # c1, c2 = st.columns(2)


# # with c1:

# #     if pd.isna(latest["up_prob"]):

# #         up_value = "N/A"

# #     else:

# #         up_value = f"{latest['up_prob']:.2%}"


# #     st.metric(
# #         "UP Probability",
# #         up_value
# #     )


# # with c2:

# #     if pd.isna(latest["down_prob"]):

# #         down_value = "N/A"

# #     else:

# #         down_value = f"{latest['down_prob']:.2%}"


# #     st.metric(
# #         "DOWN Probability",
# #         down_value
# #     )


# # # ============================================================
# # # PREDICTIONS
# # # ============================================================

# # p1, p2 = st.columns(2)


# # with p1:

# #     up_pred = latest["up_pred"]

# #     if pd.isna(up_pred) or up_pred == "":
# #         up_prediction = "N/A"

# #     elif int(float(up_pred)) == 1:
# #         up_prediction = "UP"

# #     else:
# #         up_prediction = "NO"


# #     st.metric(
# #         "UP Prediction",
# #         up_prediction
# #     )


# # with p2:

# #     down_pred = latest["down_pred"]

# #     if pd.isna(down_pred) or down_pred == "":
# #         down_prediction = "N/A"

# #     elif int(float(down_pred)) == 1:
# #         down_prediction = "DOWN"

# #     else:
# #         down_prediction = "NO"


# #     st.metric(
# #         "DOWN Prediction",
# #         down_prediction
# #     )


# # # ============================================================
# # # MODEL VERSION
# # # ============================================================

# # st.caption(
# #     f"Model Version: {latest['model_version']}"
# # )


# # # ============================================================
# # # PREDICTION HISTORY
# # # ============================================================

# # st.subheader(
# #     "Prediction History"
# # )


# # history_df = df.copy()


# # history_df["datetime"] = history_df[
# #     "datetime"
# # ].dt.strftime(
# #     "%d %b %Y %H:%M"
# # )


# # st.dataframe(
# #     history_df,
# #     use_container_width=True,
# #     hide_index=True
# # )


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


# # ============================================================
# # AUTO REFRESH - EVERY 5 SECONDS
# # ============================================================

# st_autorefresh(
#     interval=5000,
#     key="data_refresh"
# )


# # ============================================================
# # GOOGLE SHEETS AUTHENTICATION
# # ============================================================

# SCOPES = [
#     "https://www.googleapis.com/auth/spreadsheets",
#     "https://www.googleapis.com/auth/drive"
# ]


# credentials = Credentials.from_service_account_info(
#     dict(st.secrets["gcp_service_account"]),
#     scopes=SCOPES
# )


# gc = gspread.authorize(credentials)


# # ============================================================
# # GOOGLE SHEET
# # ============================================================

# GOOGLE_SHEET_ID = (
#     "1EP2UEufBvnUtf8LxDpmjuT4lDQFVEGp2apLwFdtfod4"
# )

# GOOGLE_SHEET_TAB = "Predictions"


# spreadsheet = gc.open_by_key(
#     GOOGLE_SHEET_ID
# )

# sheet = spreadsheet.worksheet(
#     GOOGLE_SHEET_TAB
# )


# # ============================================================
# # LOAD DATA
# # ============================================================

# records = sheet.get_all_records()

# df = pd.DataFrame(records)


# if df.empty:

#     st.warning(
#         "No prediction data available."
#     )

#     st.stop()


# # ============================================================
# # CLEAN DATA
# # ============================================================

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
# ).reset_index(drop=True)


# # Convert numeric columns

# for column in [
#     "up_prob",
#     "down_prob",
#     "up_pred",
#     "down_pred"
# ]:

#     if column in df.columns:

#         df[column] = pd.to_numeric(
#             df[column],
#             errors="coerce"
#         )


# # ============================================================
# # TITLE
# # ============================================================

# st.title(
#     "📈 NIFTY Intraday Model Dashboard"
# )

# st.caption(
#     "Morning & Afternoon Model Predictions"
# )

# st.divider()


# # ============================================================
# # LATEST ROW
# # ============================================================

# latest = df.iloc[0]


# # ============================================================
# # TOP INFORMATION
# # ============================================================

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
#         "Latest Datetime",
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


# # ============================================================
# # UP MODEL
# # ============================================================

# with c1:

#     up_prob = latest.get(
#         "up_prob",
#         None
#     )


#     if pd.isna(up_prob):

#         up_value = "N/A"

#     else:

#         up_value = (
#             f"{float(up_prob):.2%}"
#         )


#     up_pred = latest.get(
#         "up_pred",
#         None
#     )


#     if pd.isna(up_pred):

#         up_prediction = "N/A"

#     elif int(float(up_pred)) == 1:

#         up_prediction = "UP"

#     else:

#         up_prediction = "NO UP"


#     st.success(
#         "🟢 UP MODEL"
#     )


#     st.metric(
#         "UP Probability",
#         up_value
#     )


#     st.metric(
#         "UP Prediction",
#         up_prediction
#     )


# # ============================================================
# # DOWN MODEL
# # ============================================================

# with c2:

#     down_prob = latest.get(
#         "down_prob",
#         None
#     )


#     if pd.isna(down_prob):

#         down_value = "N/A"

#     else:

#         down_value = (
#             f"{float(down_prob):.2%}"
#         )


#     down_pred = latest.get(
#         "down_pred",
#         None
#     )


#     if pd.isna(down_pred):

#         down_prediction = "N/A"

#     elif int(float(down_pred)) == 1:

#         down_prediction = "DOWN"

#     else:

#         down_prediction = "NO DOWN"


#     st.error(
#         "🔴 DOWN MODEL"
#     )


#     st.metric(
#         "DOWN Probability",
#         down_value
#     )


#     st.metric(
#         "DOWN Prediction",
#         down_prediction
#     )


# st.caption(
#     f"⚙️ Model Version: {latest.get('model_version', 'N/A')}"
# )


# st.divider()


# # ============================================================
# # FILTER
# # ============================================================

# st.subheader(
#     "🔎 Prediction Filter"
# )

# df["date_only"] = df["datetime"].dt.date


# available_dates = sorted(
#     df["date_only"].dropna().unique(),
#     reverse=True
# )


# filter_col1, filter_col2, filter_col3 = st.columns(3)


# # ============================================================
# # DATE DROPDOWN
# # ============================================================

# with filter_col1:

#     selected_date = st.selectbox(
#         "Date",
#         available_dates,
#         index=0,
#         format_func=lambda x:
#             x.strftime("%d %b %Y")
#     )


# # ============================================================
# # FILTER BY DATE
# # ============================================================

# date_df = df[
#     df["date_only"] == selected_date
# ].copy()


# # ============================================================
# # SESSION DROPDOWN
# # ============================================================

# available_sessions = (
#     date_df["session"]
#     .dropna()
#     .astype(str)
#     .unique()
#     .tolist()
# )


# # Sort sessions in logical order

# session_order = {
#     "Morning": 0,
#     "Afternoon": 1
# }


# available_sessions = sorted(
#     available_sessions,
#     key=lambda x: session_order.get(
#         x,
#         99
#     )
# )


# with filter_col2:

#     selected_session = st.selectbox(
#         "Session",
#         available_sessions,
#         index=0
#     )


# # ============================================================
# # FILTER BY DATE + SESSION
# # ============================================================

# session_df = date_df[
#     date_df["session"].astype(str)
#     == selected_session
# ].copy()


# # ============================================================
# # DATETIME DROPDOWN
# # ============================================================

# available_datetimes = sorted(
#     session_df["datetime"].dropna().unique(),
#     reverse=True
# )


# with filter_col3:

#     selected_datetime = st.selectbox(
#         "Datetime",
#         available_datetimes,
#         index=0,
#         format_func=lambda x:
#             x.strftime("%d %b %Y %H:%M")
#     )


# # ============================================================
# # SELECTED ROW
# # ============================================================

# selected_rows = session_df[
#     session_df["datetime"] == selected_datetime
# ]


# if not selected_rows.empty:

#     selected = selected_rows.iloc[0]


#     st.subheader(
#         "Selected Prediction"
#     )


#     # --------------------------------------------------------
#     # BASIC INFORMATION
#     # --------------------------------------------------------

#     s1, s2, s3 = st.columns(3)


#     with s1:

#         st.metric(
#             "Symbol",
#             selected["symbol"]
#         )


#     with s2:

#         st.metric(
#             "Session",
#             selected["session"]
#         )


#     with s3:

#         st.metric(
#             "Datetime",
#             selected["datetime"].strftime(
#                 "%d %b %Y %H:%M"
#             )
#         )


#     # --------------------------------------------------------
#     # PROBABILITIES
#     # --------------------------------------------------------

#     s4, s5 = st.columns(2)


#     with s4:

#         value = selected.get(
#             "up_prob",
#             None
#         )

#         if pd.isna(value):

#             display_value = "N/A"

#         else:

#             display_value = (
#                 f"{float(value):.2%}"
#             )


#         st.metric(
#             "🟢 UP Probability",
#             display_value
#         )


#     with s5:

#         value = selected.get(
#             "down_prob",
#             None
#         )

#         if pd.isna(value):

#             display_value = "N/A"

#         else:

#             display_value = (
#                 f"{float(value):.2%}"
#             )


#         st.metric(
#             "🔴 DOWN Probability",
#             display_value
#         )


#     # --------------------------------------------------------
#     # PREDICTIONS
#     # --------------------------------------------------------

#     s6, s7 = st.columns(2)


#     with s6:

#         value = selected.get(
#             "up_pred",
#             None
#         )

#         if pd.isna(value):

#             display_value = "N/A"

#         elif int(float(value)) == 1:

#             display_value = "UP"

#         else:

#             display_value = "NO UP"


#         st.metric(
#             "UP Prediction",
#             display_value
#         )


#     with s7:

#         value = selected.get(
#             "down_pred",
#             None
#         )

#         if pd.isna(value):

#             display_value = "N/A"

#         elif int(float(value)) == 1:

#             display_value = "DOWN"

#         else:

#             display_value = "NO DOWN"


#         st.metric(
#             "DOWN Prediction",
#             display_value
#         )


#     st.caption(
#         f"⚙️ Model Version: "
#         f"{selected.get('model_version', 'N/A')}"
#     )

# st.divider()


# # ============================================================
# # PREDICTION HISTORY
# # ============================================================

# st.subheader(
#     "📊 Prediction History"
# )


# history_df = df.copy()


# # Remove helper column

# history_df = history_df.drop(
#     columns=["date_only"],
#     errors="ignore"
# )


# # Format datetime

# history_df["datetime"] = (
#     history_df["datetime"]
#     .dt.strftime(
#         "%d %b %Y %H:%M"
#     )
# )


# # Format probabilities

# history_df["up_prob"] = (
#     history_df["up_prob"]
#     .apply(
#         lambda x:
#         f"{float(x):.2%}"
#         if pd.notna(x)
#         else "N/A"
#     )
# )


# history_df["down_prob"] = (
#     history_df["down_prob"]
#     .apply(
#         lambda x:
#         f"{float(x):.2%}"
#         if pd.notna(x)
#         else "N/A"
#     )
# )


# # ============================================================
# # RENAME COLUMNS
# # ============================================================

# history_df = history_df.rename(
#     columns={
#         "symbol": "Symbol",
#         "datetime": "Datetime",
#         "session": "Session",
#         "up_pred": "UP Prediction",
#         "down_pred": "DOWN Prediction",
#         "up_prob": "UP Probability",
#         "down_prob": "DOWN Probability",
#         "model_version": "Model Version"
#     }
# )


# # ============================================================
# # SELECT COLUMNS
# # ============================================================

# history_columns = [
#     "Symbol",
#     "Datetime",
#     "Session",
#     "UP Prediction",
#     "DOWN Prediction",
#     "UP Probability",
#     "DOWN Probability",
#     "Model Version"
# ]


# history_df = history_df[
#     [
#         column
#         for column in history_columns
#         if column in history_df.columns
#     ]
# ]


# # ============================================================
# # DISPLAY TABLE
# # ============================================================

# st.dataframe(
#     history_df,
#     use_container_width=True,
#     hide_index=True,
#     height=450
# )


# # ============================================================
# # FOOTER
# # ============================================================

# st.divider()

# st.caption(
#     "🔄 Live Google Sheets Data • "
#     "Dashboard refreshes every 5 seconds"
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
    key="prediction_refresh"
)


# ============================================================
# GOOGLE SHEETS AUTHENTICATION
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

    st.warning("No prediction data available.")

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


for column in [
    "up_prob",
    "down_prob",
    "up_pred",
    "down_pred"
]:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ================================
       PAGE
       ================================ */

    .stApp {
        background-color: #f4f6f9;
    }


    /* ================================
       MAIN CONTAINER
       ================================ */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }


    /* ================================
       HEADER
       ================================ */

    .dashboard-header {
        background: #111827;
        padding: 26px 30px;
        border-radius: 14px;
        margin-bottom: 22px;
    }


    .dashboard-title {
        color: white;
        font-size: 30px;
        font-weight: 700;
        margin-bottom: 5px;
    }


    .dashboard-subtitle {
        color: #9ca3af;
        font-size: 14px;
    }


    .live {
        color: #22c55e;
        font-weight: 700;
    }


    /* ================================
       INFO CARDS
       ================================ */

    .info-card {
        background: white;
        padding: 18px 20px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.04);
    }


    .info-label {
        color: #6b7280;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 6px;
    }


    .info-value {
        color: #111827;
        font-size: 22px;
        font-weight: 700;
    }


    /* ================================
       PREDICTION CARDS
       ================================ */

    .prediction-card {
        padding: 24px;
        border-radius: 14px;
        min-height: 150px;
    }


    .up-card {
        background: #ecfdf5;
        border: 1px solid #a7f3d0;
    }


    .down-card {
        background: #fef2f2;
        border: 1px solid #fecaca;
    }


    .prediction-title {
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-bottom: 10px;
    }


    .up-title {
        color: #047857;
    }


    .down-title {
        color: #b91c1c;
    }


    .prediction-value {
        font-size: 36px;
        font-weight: 800;
        margin-bottom: 5px;
    }


    .up-value {
        color: #059669;
    }


    .down-value {
        color: #dc2626;
    }


    .prediction-status {
        font-size: 14px;
        font-weight: 600;
    }


    .up-status {
        color: #047857;
    }


    .down-status {
        color: #b91c1c;
    }


    /* ================================
       MODEL VERSION
       ================================ */

    .model-version {
        display: inline-block;
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 20px;
        padding: 6px 12px;
        color: #6b7280;
        font-size: 12px;
        margin-top: 12px;
    }


    /* ================================
       SECTION
       ================================ */

    .section-heading {
        font-size: 20px;
        font-weight: 700;
        color: #111827;
        margin-top: 25px;
        margin-bottom: 12px;
    }


    </style>
    """,
    unsafe_allow_html=True
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
            Morning & Afternoon Model Predictions
            &nbsp; • &nbsp;
            <span class="live">● LIVE</span>
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
    <div class="section-heading">
        Latest Prediction
    </div>
    """,
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


# ============================================================
# UP CARD
# ============================================================

with col1:

    up_prob = latest.get("up_prob")

    if pd.isna(up_prob):
        up_probability = "N/A"
    else:
        up_probability = f"{float(up_prob):.2%}"


    up_pred = latest.get("up_pred")

    if pd.isna(up_pred):

        up_prediction = "N/A"

    elif int(float(up_pred)) == 1:

        up_prediction = "UP"

    else:

        up_prediction = "NO UP"


    st.markdown(
        f"""
        <div class="prediction-card up-card">

            <div class="prediction-title up-title">
                🟢 UP MODEL
            </div>

            <div class="prediction-value up-value">
                {up_probability}
            </div>

            <div class="prediction-status up-status">
                Prediction: {up_prediction}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DOWN CARD
# ============================================================

with col2:

    down_prob = latest.get("down_prob")

    if pd.isna(down_prob):
        down_probability = "N/A"
    else:
        down_probability = f"{float(down_prob):.2%}"


    down_pred = latest.get("down_pred")

    if pd.isna(down_pred):

        down_prediction = "N/A"

    elif int(float(down_pred)) == 1:

        down_prediction = "DOWN"

    else:

        down_prediction = "NO DOWN"


    st.markdown(
        f"""
        <div class="prediction-card down-card">

            <div class="prediction-title down-title">
                🔴 DOWN MODEL
            </div>

            <div class="prediction-value down-value">
                {down_probability}
            </div>

            <div class="prediction-status down-status">
                Prediction: {down_prediction}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown(
    f"""
    <div class="model-version">
        ⚙️ Model Version: <b>{latest.get("model_version", "N/A")}</b>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FILTER
# ============================================================

st.markdown(
    """
    <div class="section-heading">
        🔎 Prediction Filter
    </div>
    """,
    unsafe_allow_html=True
)


df["date_only"] = df["datetime"].dt.date


available_dates = sorted(
    df["date_only"].dropna().unique(),
    reverse=True
)


filter_col1, filter_col2, filter_col3 = st.columns(3)


# ============================================================
# DATE
# ============================================================

with filter_col1:

    selected_date = st.selectbox(
        "Date",
        available_dates,
        index=0,
        format_func=lambda x:
            x.strftime("%d %b %Y")
    )


# ============================================================
# DATE FILTER
# ============================================================

date_df = df[
    df["date_only"] == selected_date
].copy()


# ============================================================
# SESSION
# ============================================================

available_sessions = (
    date_df["session"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)


session_order = {
    "Morning": 0,
    "Afternoon": 1
}


available_sessions = sorted(
    available_sessions,
    key=lambda x:
        session_order.get(x, 99)
)


with filter_col2:

    selected_session = st.selectbox(
        "Session",
        available_sessions,
        index=0
    )


# ============================================================
# SESSION FILTER
# ============================================================

session_df = date_df[
    date_df["session"].astype(str)
    == selected_session
].copy()


# ============================================================
# DATETIME
# ============================================================

available_datetimes = sorted(
    session_df["datetime"].dropna().unique(),
    reverse=True
)


with filter_col3:

    selected_datetime = st.selectbox(
        "Datetime",
        available_datetimes,
        index=0,
        format_func=lambda x:
            x.strftime("%d %b %Y %H:%M")
    )


# ============================================================
# SELECTED PREDICTION
# ============================================================

selected_rows = session_df[
    session_df["datetime"] == selected_datetime
]


if not selected_rows.empty:

    selected = selected_rows.iloc[0]


    st.markdown(
        """
        <div class="section-heading">
            Selected Prediction
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # BASIC INFO
    # --------------------------------------------------------

    c1, c2, c3 = st.columns(3)


    with c1:

        st.metric(
            "Symbol",
            selected["symbol"]
        )


    with c2:

        st.metric(
            "Session",
            selected["session"]
        )


    with c3:

        st.metric(
            "Datetime",
            selected["datetime"].strftime(
                "%d %b %Y %H:%M"
            )
        )


    # --------------------------------------------------------
    # PROBABILITY
    # --------------------------------------------------------

    c1, c2 = st.columns(2)


    with c1:

        value = selected.get("up_prob")

        if pd.isna(value):
            value = "N/A"
        else:
            value = f"{float(value):.2%}"


        st.metric(
            "🟢 UP Probability",
            value
        )


    with c2:

        value = selected.get("down_prob")

        if pd.isna(value):
            value = "N/A"
        else:
            value = f"{float(value):.2%}"


        st.metric(
            "🔴 DOWN Probability",
            value
        )


    # --------------------------------------------------------
    # PREDICTIONS
    # --------------------------------------------------------

    c1, c2 = st.columns(2)


    with c1:

        value = selected.get("up_pred")

        if pd.isna(value):

            prediction = "N/A"

        elif int(float(value)) == 1:

            prediction = "UP"

        else:

            prediction = "NO UP"


        st.metric(
            "UP Prediction",
            prediction
        )


    with c2:

        value = selected.get("down_pred")

        if pd.isna(value):

            prediction = "N/A"

        elif int(float(value)) == 1:

            prediction = "DOWN"

        else:

            prediction = "NO DOWN"


        st.metric(
            "DOWN Prediction",
            prediction
        )


    st.caption(
        f"⚙️ Model Version: "
        f"{selected.get('model_version', 'N/A')}"
    )


# ============================================================
# HISTORY
# ============================================================

st.markdown(
    """
    <div class="section-heading">
        📊 Prediction History
    </div>
    """,
    unsafe_allow_html=True
)


history_df = df.copy()


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
# RENAME
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
# TABLE
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

st.divider()

st.caption(
    "🔄 Live Google Sheets Data • "
    "Auto-refresh every 5 seconds"
)