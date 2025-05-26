
import streamlit as st
import pandas as pd

# تحميل البيانات
df = pd.read_csv("data.csv")

# إخفاء رقم الجوال
if "جوال" in df.columns:
    df = df.drop(columns=["جوال"])

st.set_page_config(page_title="لوحة البيانات", layout="wide")

st.title("📊 لوحة معلومات الأسماء")

# العدد الكلي
st.metric("العدد الكلي", len(df))

# إحصائية حسب الجنسية
st.subheader("توزيع حسب الجنسية")
st.dataframe(df["الجنسية"].value_counts().reset_index().rename(columns={"index": "الجنسية", "الجنسية": "العدد"}))

# جدول البيانات الكامل
st.subheader("تفاصيل الأسماء")
search = st.text_input("🔍 ابحث بالاسم:")
if search:
    filtered_df = df[df["الاسم"].str.contains(search, case=False, na=False)]
else:
    filtered_df = df

st.dataframe(filtered_df.reset_index(drop=True))
