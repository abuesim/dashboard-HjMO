
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="لوحة البيانات التفاعلية", layout="wide")

# تحميل البيانات
df = pd.read_csv("data.csv")

# حذف رقم الجوال إن وجد
if "جوال" in df.columns:
    df = df.drop(columns=["جوال"])

st.title("📊 الخميس 29 مايو 3:30 عصرا	")

# ===== بطاقات الإحصائيات =====
col1, col2, col3 = st.columns(3)
col1.metric("👥 العدد الكلي", len(df))
col2.metric("🌍 عدد الجنسيات", df["الجنسية"].nunique())
if "الجنس" in df.columns:
    col3.metric("🧑‍🤝‍🧑 عدد الذكور", (df["الجنس"] == "ذكر").sum())

st.markdown("---")

# ===== الرسم الدائري لتوزيع الجنسيات =====
st.subheader("🎯 توزيع الأشخاص حسب الجنسية (اضغط على أي جزء لرؤية التفاصيل)")

fig = px.pie(df, names="الجنسية", title="نسبة توزيع الجنسيات", hole=0.4,
             color_discrete_sequence=px.colors.qualitative.Set3)
selected = st.plotly_chart(fig, use_container_width=True)

# ===== فلترة حسب الجنسية =====
selected_nationality = st.selectbox("اختر الجنسية لعرض التفاصيل:", options=[""] + sorted(df["الجنسية"].unique()))
if selected_nationality:
    filtered_df = df[df["الجنسية"] == selected_nationality]
    st.info(f"تم العثور على {len(filtered_df)} شخص من الجنسية: {selected_nationality}")
    st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)
else:
    st.dataframe(df, use_container_width=True)

# ===== رسم بياني بالأعمدة حسب الجنس =====
if "الجنس" in df.columns:
    st.subheader("📈 توزيع حسب الجنس")
    gender_counts = df["الجنس"].value_counts().reset_index()
    gender_counts.columns = ["الجنس", "العدد"]
    fig2 = px.bar(gender_counts, x="الجنس", y="العدد", color="الجنس",
                  color_discrete_sequence=px.colors.sequential.Tealgrn)
    st.plotly_chart(fig2, use_container_width=True)
