import streamlit as st
import pandas as pd
from sqlalchemy import create_engine


engine = create_engine(
    "mysql+pymysql://admin:Liquide123@localhost:3306/fno"
)


st.set_page_config(
    page_title="NIFTY Model Dashboard",
    layout="wide"
)


st.title("📈 NIFTY Intraday Model Dashboard")


query = """
SELECT *
FROM nifty_model_predictions
ORDER BY datetime DESC
LIMIT 50
"""


df = pd.read_sql(query, engine)


latest = df.iloc[0]


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
        "Datetime",
        str(latest["datetime"])
    )



st.subheader("Latest Prediction")


c1,c2 = st.columns(2)


with c1:
    st.metric(
        "UP Probability",
        f"{latest['up_prob']:.2%}"
    )

with c2:
    st.metric(
        "DOWN Probability",
        f"{latest['down_prob']:.2%}"
    )


st.subheader("Prediction History")

st.dataframe(
    df,
    use_container_width=True
)