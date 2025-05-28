
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="لوحة التحكم المتقدمة", layout="wide")

# الشريط الجانبي للملاحة
st.sidebar.title("القائمة")
page = st.sidebar.radio("اذهب إلى:", ["الإحصائيات", "التفاصيل", "التقارير"])

# تحميل البيانات ووضع التخزين المؤقت
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    if "جوال" in df.columns:
        df.drop(columns=["جوال"], inplace=True)
    return df

df = load_data()

# صفحة الإحصائيات
if page == "الإحصائيات":
    st.title("📈 الإحصائيات العامة")
    col1, col2, col3 = st.columns(3)
    col1.metric("👥 العدد الكلي", len(df))
    col2.metric("🌍 عدد الجنسيات", df["الجنسية"].nunique())
    if "الجنس" in df.columns:
        col3.metric("🧑‍🤝‍🧑 عدد الذكور", (df["الجنس"] == "ذكر").sum())

    st.markdown("### 🎨 توزيع الجنسيات")
    fig1 = px.pie(df, names="الجنسية", hole=0.4, title="نسبة توزيع الجنسيات",
                  color_discrete_sequence=px.colors.qualitative.Vivid)
    st.plotly_chart(fig1, use_container_width=True)

    if "الجنس" in df.columns:
        st.markdown("### 📊 توزيع حسب الجنس")
        gender_counts = df["الجنس"].value_counts().reset_index()
        gender_counts.columns = ["الجنس", "العدد"]
        fig2 = px.bar(gender_counts, x="الجنس", y="العدد", color="الجنس",
                      title="عدد الذكور والإناث",
                      color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig2, use_container_width=True)

    if "تاريخ الميلاد" in df.columns:
        st.markdown("### 📈 توزيع حسب سنة الميلاد")
        df_birth = df.copy()
        df_birth["سنة الميلاد"] = pd.to_datetime(df_birth["تاريخ الميلاد"], errors="coerce").dt.year
        birth_counts = df_birth["سنة الميلاد"].value_counts().sort_index().reset_index()
        birth_counts.columns = ["سنة الميلاد", "العدد"]
        fig3 = px.line(birth_counts, x="سنة الميلاد", y="العدد", markers=True, title="عدد الأفراد حسب سنة الميلاد")
        st.plotly_chart(fig3, use_container_width=True)

# صفحة التفاصيل
elif page == "التفاصيل":
    st.title("📋 البيانات التفصيلية")
    search = st.text_input("🔎 ابحث بالاسم أو الجنسية:")
    if search:
        mask = df["الاسم"].str.contains(search, case=False, na=False) | df["الجنسية"].str.contains(search, case=False, na=False)
        df_filtered = df[mask]
        st.info(f"تم العثور على {len(df_filtered)} نتيجة للبحث '{search}'")
    else:
        df_filtered = df
    st.dataframe(df_filtered.reset_index(drop=True), use_container_width=True)

# صفحة التقارير
elif page == "التقارير":
    st.title("📑 تنزيل التقارير")
    st.markdown("يمكنك تنزيل البيانات الحالية بصيغة CSV أو Excel:")
    # تنزيل CSV
    csv_data = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(label="⬇️ تنزيل CSV", data=csv_data, file_name="report.csv", mime="text/csv")
    # تنزيل Excel
    try:
        import io
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='البيانات')
        excel_buffer.seek(0)
        st.download_button(label="⬇️ تنزيل Excel", data=excel_buffer, file_name="report.xlsx")
    except Exception as e:
        st.error("خطأ في إنشاء ملف Excel: " + str(e))
