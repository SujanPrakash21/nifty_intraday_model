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
#     interval=30000,
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
    interval=30000,
    key="data_refresh"
)


# ============================================================
# THRESHOLD CONFIGURATION
#
# IMPORTANT:
# These are DISPLAY thresholds only.
#
# Streamlit DOES NOT calculate predictions using these values.
# Predictions are taken directly from Google Sheets:
#
# up_pred
# down_pred
#
# Keep these values exactly the same as the thresholds
# used inside your respective model codes.
# ============================================================

THRESHOLDS = {
    "Morning": {
        "up": 0.60,
        "down": 0.50
    },

    "Afternoon": {
        "up": 0.55,
        "down": 0.50
    }
}


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


# ============================================================
# CONVERT NUMERIC COLUMNS
# ============================================================

numeric_columns = [
    "up_prob",
    "down_prob",
    "up_pred",
    "down_pred",
    "up_prob_change_15m",
    "up_prob_change_cumulative",
    "down_prob_change_15m",
    "down_prob_change_cumulative",
    "anchor_call_premium_0915",
    "anchor_call_premium_current",
    "anchor_call_change_15m",
    "anchor_call_change_cumulative",
    "anchor_put_premium_0915",
    "anchor_put_premium_current",
    "anchor_put_change_15m",
    "anchor_put_change_cumulative"
]


for column in numeric_columns:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# ============================================================
# SORT DATA
#
# IMPORTANT:
#
# If Morning and Afternoon have the same datetime,
# Afternoon is treated as the latest session.
#
# Example:
#
# 31 Aug 15:15 Morning
# 31 Aug 15:15 Afternoon
#
# Afternoon will be displayed as the latest row.
# ============================================================

session_order = {
    "Afternoon": 0,
    "Morning": 1
}


df["_session_order"] = (
    df["session"]
    .astype(str)
    .map(session_order)
    .fillna(99)
)


df = df.sort_values(
    [
        "datetime",
        "_session_order"
    ],
    ascending=[
        False,
        True
    ]
).reset_index(
    drop=True
)


# ============================================================
# LATEST ROW
# ============================================================

latest = df.iloc[0]


latest_session = str(
    latest.get(
        "session",
        ""
    )
).strip()


# ============================================================
# GET THRESHOLDS
# ============================================================

session_thresholds = THRESHOLDS.get(
    latest_session,
    {
        "up": 0.60,
        "down": 0.50
    }
)


up_threshold = session_thresholds["up"]

down_threshold = session_thresholds["down"]


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
# TOP INFORMATION
# ============================================================

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Symbol",
        latest.get(
            "symbol",
            "N/A"
        )
    )


with col2:

    st.metric(
        "Session",
        latest_session
    )


with col3:

    st.metric(
        "Latest Datetime",
        latest["datetime"].strftime(
            "%d %b %Y %H:%M"
        )
    )


st.divider()


# ============================================================
# LATEST PREDICTION
# ============================================================

st.subheader(
    "Latest Prediction"
)


# ============================================================
# GET PREDICTIONS FROM GOOGLE SHEETS
#
# IMPORTANT:
#
# We DO NOT calculate predictions here.
#
# The model already calculated:
#
# up_pred
# down_pred
#
# Streamlit only displays them.
# ============================================================

up_pred = latest.get(
    "up_pred",
    None
)


down_pred = latest.get(
    "down_pred",
    None
)


if pd.isna(up_pred):

    up_pred_value = 0

else:

    up_pred_value = int(
        float(up_pred)
    )


if pd.isna(down_pred):

    down_pred_value = 0

else:

    down_pred_value = int(
        float(down_pred)
    )


# ============================================================
# PROBABILITIES
# ============================================================

up_prob = latest.get(
    "up_prob",
    None
)


down_prob = latest.get(
    "down_prob",
    None
)


if pd.isna(up_prob):

    up_probability_display = "N/A"

else:

    up_probability_display = (
        f"{float(up_prob):.2%}"
    )


if pd.isna(down_prob):

    down_probability_display = "N/A"

else:

    down_probability_display = (
        f"{float(down_prob):.2%}"
    )


# ============================================================
# PREDICTION TEXT
# ============================================================

if up_pred_value == 1:

    up_prediction_text = "UP"

else:

    up_prediction_text = "NO UP"


if down_pred_value == 1:

    down_prediction_text = "DOWN"

else:

    down_prediction_text = "NO DOWN"


# ============================================================
# COLOR LOGIC
#
# ONLY ONE ACTIVE:
#
# UP = 1 and DOWN = 0
#     -> UP section GREEN
#
# UP = 0 and DOWN = 1
#     -> DOWN section RED
#
# BOTH 0
#     -> NORMAL
#
# BOTH 1
#     -> NORMAL
# ============================================================

up_is_active = (
    up_pred_value == 1
    and
    down_pred_value == 0
)


down_is_active = (
    down_pred_value == 1
    and
    up_pred_value == 0
)


# ============================================================
# TWO MODEL COLUMNS
# ============================================================

up_column, down_column = st.columns(2)


# ============================================================
# UP MODEL
# ============================================================

with up_column:

    if up_is_active:

        # Green area only when UP is the sole prediction
        with st.success(
            "🟢 UP MODEL — ACTIVE"
        ):

            st.write(
                f"**UP Probability | "
                f"Threshold: {up_threshold:.0%}**"
            )

            st.metric(
                "UP Probability",
                up_probability_display
            )

            st.write(
                "**UP Prediction**"
            )

            st.write(
                f"### {up_prediction_text}"
            )

    else:

        st.write(
            "🟢 **UP MODEL**"
        )

        st.write(
            f"**UP Probability | "
            f"Threshold: {up_threshold:.0%}**"
        )

        st.metric(
            "UP Probability",
            up_probability_display
        )

        st.write(
            "**UP Prediction**"
        )

        st.write(
            f"### {up_prediction_text}"
        )


# ============================================================
# DOWN MODEL
# ============================================================

with down_column:

    if down_is_active:

        # Red area only when DOWN is the sole prediction
        with st.error(
            "🔴 DOWN MODEL — ACTIVE"
        ):

            st.write(
                f"**DOWN Probability | "
                f"Threshold: {down_threshold:.0%}**"
            )

            st.metric(
                "DOWN Probability",
                down_probability_display
            )

            st.write(
                "**DOWN Prediction**"
            )

            st.write(
                f"### {down_prediction_text}"
            )

    else:

        st.write(
            "🔴 **DOWN MODEL**"
        )

        st.write(
            f"**DOWN Probability | "
            f"Threshold: {down_threshold:.0%}**"
        )

        st.metric(
            "DOWN Probability",
            down_probability_display
        )

        st.write(
            "**DOWN Prediction**"
        )

        st.write(
            f"### {down_prediction_text}"
        )


# ============================================================
# MODEL VERSION
# ============================================================

# st.caption(
#     f"⚙️ Model Version: "
#     f"{latest.get('model_version', 'N/A')}"
# )


st.divider()


# ============================================================
# PREDICTION HISTORY
# ============================================================

st.subheader(
    "📊 Prediction History"
)


# ============================================================
# LATEST 50 ROWS
# ============================================================

history_df = df.copy()


# Remove internal sorting helper

history_df = history_df.drop(
    columns=[
        "_session_order"
    ],
    errors="ignore"
)


# ============================================================
# LIMIT TO 50 ROWS
# ============================================================

history_df = history_df.head(
    50
).copy()


# ============================================================
# FORMAT DATETIME
# ============================================================

history_df["datetime"] = (
    history_df["datetime"]
    .dt.strftime(
        "%d %b %Y %H:%M"
    )
)


# ============================================================
# FORMAT PROBABILITIES
# ============================================================

if "up_prob" in history_df.columns:

    history_df["up_prob"] = (
        history_df["up_prob"]
        .apply(
            lambda x:
            f"{float(x):.2%}"
            if pd.notna(x)
            else ""
        )
    )


if "down_prob" in history_df.columns:

    history_df["down_prob"] = (
        history_df["down_prob"]
        .apply(
            lambda x:
            f"{float(x):.2%}"
            if pd.notna(x)
            else ""
        )
    )


# ============================================================
# ROUND NUMERIC CHANGE / PREMIUM COLUMNS
# ============================================================

display_numeric_columns = [

    "up_prob_change_15m",
    "up_prob_change_cumulative",

    "down_prob_change_15m",
    "down_prob_change_cumulative",

    "anchor_call_premium_0915",
    "anchor_call_premium_current",
    "anchor_call_change_15m",
    "anchor_call_change_cumulative",

    "anchor_put_premium_0915",
    "anchor_put_premium_current",
    "anchor_put_change_15m",
    "anchor_put_change_cumulative"

]


for column in display_numeric_columns:

    if column in history_df.columns:

        history_df[column] = (
            pd.to_numeric(
                history_df[column],
                errors="coerce"
            )
            .round(2)
        )


# ============================================================
# RENAME COLUMNS
# ============================================================

history_df = history_df.rename(
    columns={

        "symbol":
            "Symbol",

        "datetime":
            "Datetime",

        "session":
            "Session",

        "up_pred":
            "UP Prediction",

        "down_pred":
            "DOWN Prediction",

        "up_prob":
            "UP Probability",

        "up_prob_change_15m":
            "UP Prob Change 15m",

        "up_prob_change_cumulative":
            "UP Prob Change Cumulative",

        "down_prob":
            "DOWN Probability",

        "down_prob_change_15m":
            "DOWN Prob Change 15m",

        "down_prob_change_cumulative":
            "DOWN Prob Change Cumulative",

        "anchor_call_premium_0915":
            "Anchor Call Premium 09:15",

        "anchor_call_premium_current":
            "Anchor Call Premium Current",

        "anchor_call_change_15m":
            "Anchor Call Change 15m",

        "anchor_call_change_cumulative":
            "Anchor Call Change Cumulative",

        "anchor_put_premium_0915":
            "Anchor Put Premium 09:15",

        "anchor_put_premium_current":
            "Anchor Put Premium Current",

        "anchor_put_change_15m":
            "Anchor Put Change 15m",

        "anchor_put_change_cumulative":
            "Anchor Put Change Cumulative",

        "model_version":
            "Model Version"

    }
)


# ============================================================
# SHOW ALL COLUMNS
# ============================================================

st.dataframe(
    history_df,
    use_container_width=True,
    hide_index=True,
    height=600
)


# ============================================================
# FOOTER
# ============================================================

st.divider()


st.caption(
    "🔄 Live Google Sheets Data • "
    "Dashboard refreshes every 30 seconds • "
    "Showing latest 50 predictions"
)