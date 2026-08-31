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
    interval=30000,
    key="data_refresh"
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


# Convert numeric columns

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
# TITLE
# ============================================================

st.title(
    "📈 NIFTY Intraday Model Dashboard"
)

st.caption(
    "Morning & Afternoon Model Predictions"
)

st.divider()


# ============================================================
# LATEST ROW
# ============================================================

latest = df.iloc[0]


# ============================================================
# TOP INFORMATION
# ============================================================

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Symbol",
        latest["symbol"]
    )


with col2:

    st.metric(
        "Session",
        latest["session"]
    )


with col3:

    st.metric(
        "Latest Datetime",
        latest["datetime"].strftime(
            "%d %b %Y %H:%M"
        )
    )


# ============================================================
# LATEST PREDICTION
# ============================================================

st.subheader(
    "Latest Prediction"
)


c1, c2 = st.columns(2)


# ============================================================
# UP MODEL
# ============================================================

with c1:

    up_prob = latest.get(
        "up_prob",
        None
    )


    if pd.isna(up_prob):

        up_value = "N/A"

    else:

        up_value = (
            f"{float(up_prob):.2%}"
        )


    up_pred = latest.get(
        "up_pred",
        None
    )


    if pd.isna(up_pred):

        up_prediction = "N/A"

    elif int(float(up_pred)) == 1:

        up_prediction = "UP"

    else:

        up_prediction = "NO UP"


    st.success(
        "🟢 UP MODEL"
    )


    st.metric(
        "UP Probability",
        up_value
    )


    st.metric(
        "UP Prediction",
        up_prediction
    )


# ============================================================
# DOWN MODEL
# ============================================================

with c2:

    down_prob = latest.get(
        "down_prob",
        None
    )


    if pd.isna(down_prob):

        down_value = "N/A"

    else:

        down_value = (
            f"{float(down_prob):.2%}"
        )


    down_pred = latest.get(
        "down_pred",
        None
    )


    if pd.isna(down_pred):

        down_prediction = "N/A"

    elif int(float(down_pred)) == 1:

        down_prediction = "DOWN"

    else:

        down_prediction = "NO DOWN"


    st.error(
        "🔴 DOWN MODEL"
    )


    st.metric(
        "DOWN Probability",
        down_value
    )


    st.metric(
        "DOWN Prediction",
        down_prediction
    )


st.caption(
    f"⚙️ Model Version: {latest.get('model_version', 'N/A')}"
)


st.divider()


# ============================================================
# FILTER
# ============================================================

st.subheader(
    "🔎 Prediction Filter"
)

df["date_only"] = df["datetime"].dt.date


available_dates = sorted(
    df["date_only"].dropna().unique(),
    reverse=True
)


filter_col1, filter_col2, filter_col3 = st.columns(3)


# ============================================================
# DATE DROPDOWN
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
# FILTER BY DATE
# ============================================================

date_df = df[
    df["date_only"] == selected_date
].copy()


# ============================================================
# SESSION DROPDOWN
# ============================================================

available_sessions = (
    date_df["session"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)


# Sort sessions in logical order

session_order = {
    "Morning": 0,
    "Afternoon": 1
}


available_sessions = sorted(
    available_sessions,
    key=lambda x: session_order.get(
        x,
        99
    )
)


with filter_col2:

    selected_session = st.selectbox(
        "Session",
        available_sessions,
        index=0
    )


# ============================================================
# FILTER BY DATE + SESSION
# ============================================================

session_df = date_df[
    date_df["session"].astype(str)
    == selected_session
].copy()


# ============================================================
# DATETIME DROPDOWN
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
# SELECTED ROW
# ============================================================

selected_rows = session_df[
    session_df["datetime"] == selected_datetime
]


if not selected_rows.empty:

    selected = selected_rows.iloc[0]


    st.subheader(
        "Selected Prediction"
    )


    # --------------------------------------------------------
    # BASIC INFORMATION
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
    # PROBABILITIES
    # --------------------------------------------------------

    s4, s5 = st.columns(2)


    with s4:

        value = selected.get(
            "up_prob",
            None
        )

        if pd.isna(value):

            display_value = "N/A"

        else:

            display_value = (
                f"{float(value):.2%}"
            )


        st.metric(
            "🟢 UP Probability",
            display_value
        )


    with s5:

        value = selected.get(
            "down_prob",
            None
        )

        if pd.isna(value):

            display_value = "N/A"

        else:

            display_value = (
                f"{float(value):.2%}"
            )


        st.metric(
            "🔴 DOWN Probability",
            display_value
        )


    # --------------------------------------------------------
    # PREDICTIONS
    # --------------------------------------------------------

    s6, s7 = st.columns(2)


    with s6:

        value = selected.get(
            "up_pred",
            None
        )

        if pd.isna(value):

            display_value = "N/A"

        elif int(float(value)) == 1:

            display_value = "UP"

        else:

            display_value = "NO UP"


        st.metric(
            "UP Prediction",
            display_value
        )


    with s7:

        value = selected.get(
            "down_pred",
            None
        )

        if pd.isna(value):

            display_value = "N/A"

        elif int(float(value)) == 1:

            display_value = "DOWN"

        else:

            display_value = "NO DOWN"


        st.metric(
            "DOWN Prediction",
            display_value
        )


    st.caption(
        f"⚙️ Model Version: "
        f"{selected.get('model_version', 'N/A')}"
    )

st.divider()


# ============================================================
# PREDICTION HISTORY
# ============================================================

st.subheader(
    "📊 Prediction History"
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
    .dt.strftime(
        "%d %b %Y %H:%M"
    )
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
        "model_version": "Model Version",
        "up_prob_change": "up_prob_change"
    }
)


# ============================================================
# SELECT COLUMNS
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
# DISPLAY TABLE
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
    "Dashboard refreshes every 5 seconds"
)