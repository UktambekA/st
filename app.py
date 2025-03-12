import streamlit as st
import pandas as pd
import datetime
from io import BytesIO

# Streamlit sarlavha
st.title("Mahsulotlar ro‘yxatini yaratish")

# Mahsulotlar uchun bo‘sh DataFrame
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Mahsulot", "Narx", "Sana"])

# Foydalanuvchidan mahsulot nomi va narxini qabul qilish
mahsulot_nomi = st.text_input("Mahsulot nomini kiriting:")
mahsulot_narxi = st.number_input("Mahsulot narxini kiriting:", min_value=0.0, step=0.01)

if st.button("Qo‘shish"):
    if mahsulot_nomi and mahsulot_narxi:
        yangi_mahsulot = pd.DataFrame({
            "Mahsulot": [mahsulot_nomi],
            "Narx": [mahsulot_narxi],
            "Sana": [datetime.datetime.today().strftime("%Y-%m-%d")]
        })
        st.session_state.data = pd.concat([st.session_state.data, yangi_mahsulot], ignore_index=True)
        st.success(f"✅ {mahsulot_nomi} mahsuloti qo‘shildi!")

# Joriy jadvalni ko‘rsatish
st.subheader("Kiritilgan mahsulotlar:")
st.write(st.session_state.data)

# Excel faylni yaratish va yuklab olish uchun funksiya
def create_excel_download_link(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Mahsulotlar")
    output.seek(0)
    return output

# Excel faylni yuklab olish tugmasi
if not st.session_state.data.empty:
    excel_file = create_excel_download_link(st.session_state.data)
    st.download_button(
        label="📥 Excel faylni yuklab olish",
        data=excel_file,
        file_name="mahsulotlar.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
