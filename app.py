import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="لوحة التحكم المتقدمة", layout="wide")

# ----- شريط علوي -----
st.markdown("""
    <div style='background-color:#0d3b66;padding:10px 20px;border-radius:12px;margin-bottom:25px;'>
        <h2 style='color:white;margin:0;'>📅 الجمعة 30 مايو 1:30 ظهراً</h2>
    </div>
""", unsafe_allow_html=True)

# ----- تحميل البيانات -----
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

df = load_data()

# ----- القائمة الجانبية -----
st.sidebar.title("القائمة")
page = st.sidebar.radio("اذهب إلى:", ["الإحصائيات", "التفاصيل"])

if page == "الإحصائيات":
    st.title("📊 الإحصائيات العامة")

    # بطاقات رقمية
    total = len(df)
    male_count = int((df.get("الجنس") == "ذكر").sum())
    female_count = int((df.get("الجنس") == "أنثى").sum())
    nationalities = df["الجنسية"].nunique()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👥 العدد الكلي", total)
    col2.metric("🧑 عدد الذكور", male_count)
    col3.metric("👩 عدد الإناث", female_count)
    col4.metric("🌍 عدد الجنسيات", nationalities)

    # تبويبات بيانية
    tab1, tab2, tab3 = st.tabs(["الجنس", "الجنسيات", "العمر"])

    with tab1:
        fig = px.pie(df, names="الجنس", title="نسبة الجنس")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        top_nationalities = df["الجنسية"].value_counts().nlargest(10).reset_index()
        top_nationalities.columns = ["الجنسية", "العدد"]
        fig2 = px.bar(top_nationalities, x="الجنسية", y="العدد", title="أكثر 10 جنسيات")
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        if "العمر" in df.columns:
            fig3 = px.histogram(df, x="العمر", nbins=20, title="توزيع الأعمار")
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("📌 لا يوجد عمود باسم 'العمر' في البيانات")

elif page == "التفاصيل":
    st.title("📋 التفاصيل الكاملة")
    st.dataframe(df, use_container_width=True)

# ----- خلفية -----
st.markdown("""
    <style>
    body {
        background-color: #f4f4f4;
    }
    .stApp {
        background-image: linear-gradient(to bottom right, #e0f7fa, #ffffff);
        background-size: cover;
    }
    </style>
""", unsafe_allow_html=True)
