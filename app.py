import streamlit as st
import pandas as pd
import plotly.express as px

# ----- تاغات منع الكاش -----
st.markdown("""
    <!-- منع المتصفح من تخزين الكاش -->
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />
""", unsafe_allow_html=True)

st.set_page_config(page_title="لوحة التحكم المتقدمة", layout="wide")

# ----- شريط علوي -----
st.markdown("""
    <div style='background-color:#000000;padding:10px 20px;border-radius:12px;margin-bottom:25px;'>
        <h2 style='color:white;margin:0;'>📅 الأحد 5 ذي الحجة 4:30 عصراً</h2>
    </div>
""", unsafe_allow_html=True)

# ----- تحميل البيانات -----
def load_data():
    return pd.read_csv("data.csv")

df = load_data()

# ----- القائمة الجانبية -----
st.sidebar.title("القائمة")

if st.sidebar.button("🔄 تحديث البيانات"):
    st.experimental_rerun()

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
        fig = px.pie(df, names="الجنس", title="نسبة الجنس", color_discrete_sequence=px.colors.sequential.OrRd)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        top_nationalities = df["الجنسية"].value_counts().nlargest(10).reset_index()
        top_nationalities.columns = ["الجنسية", "العدد"]
        fig2 = px.bar(top_nationalities, x="الجنسية", y="العدد", title="أكثر 10 جنسيات", color_discrete_sequence=px.colors.sequential.OrRd)
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        if "العمر" in df.columns:
            fig3 = px.histogram(df, x="العمر", nbins=20, title="توزيع الأعمار", color_discrete_sequence=px.colors.sequential.Reds)
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
        background-image: linear-gradient(to bottom, rgba(11, 61, 11, 0.7), rgba(28, 28, 28, 0.7));
        background-size: cover;
    }
    </style>
""", unsafe_allow_html=True)
