
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="لوحة التحكم المتقدمة", layout="wide")

# الشريط الجانبي للملاحة
st.sidebar.title("القائمة")
page = st.sidebar.radio("اذهب إلى:", ["الإحصائيات", "التفاصيل"])

# تحميل البيانات ووضع التخزين المؤقت
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    return df

df = load_data()

# صفحة الإحصائيات
if page == "الإحصائيات":
    # عبارة آخر تحديث
    st.markdown("**آخر تحديث العاملين 28 مايو الساعة 5:30 عصراً**")
    st.title("📈 الإحصائيات العامة")
    total = len(df)
    male_count = int((df.get("الجنس") == "ذكر").sum())
    female_count = int((df.get("الجنس") == "أنثى").sum())
    nationalities = df["الجنسية"].unique().tolist()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👥 العدد الكلي", total)
    col2.metric("🧑‍🤝‍🧑 عدد الذكور", male_count)
    col3.metric("👩‍🤝‍👩 عدد الإناث", female_count)
    col4.metric("🌍 عدد الجنسيات", len(nationalities))

    st.markdown("---")
    st.subheader("🎯 توزيع الأشخاص حسب الجنسية")
    fig1 = px.pie(df, names="الجنسية", hole=0.4, title="نسبة توزيع الجنسيات",
                  color_discrete_sequence=px.colors.qualitative.Vivid)
    st.plotly_chart(fig1, use_container_width=True)

    selected_nationality = st.selectbox("أو اختر جنسية لعرض التفاصيل:", options=["كل الجنسيات"] + sorted(nationalities))
    if selected_nationality != "كل الجنسيات":
        filtered_df = df[df["الجنسية"] == selected_nationality]
        st.info(f"تم العثور على {len(filtered_df)} شخص من الجنسية: {selected_nationality}")
        st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)
    else:
        st.dataframe(df, use_container_width=True)

# صفحة التفاصيل
elif page == "التفاصيل":
    st.title("📋 البيانات التفصيلية")
    search = st.text_input("🔎 ابحث بالمعرف أو الاسم أو الجنسية:")
    if search:
        mask = (
            df["المعرف"].astype(str).str.contains(search, case=False, na=False) |
            df["الاسم"].str.contains(search, case=False, na=False) |
            df["الجنسية"].str.contains(search, case=False, na=False)
        )
        df_filtered = df[mask]
        st.info(f"تم العثور على {len(df_filtered)} نتيجة للبحث '{search}'")
    else:
        df_filtered = df
    st.dataframe(df_filtered.reset_index(drop=True), use_container_width=True)
