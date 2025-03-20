import streamlit as st
import pandas as pd
import datetime
import os
from io import BytesIO

# CSV fayl nomi
CSV_FILE = "mahsulotlar.csv"

# CSV faylni yuklash yoki yaratish
def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["Mahsulot", "Narx", "Sana"])

# Ma'lumotlarni CSV faylga saqlash
def save_data(df):
    df.to_csv(CSV_FILE, index=False)

# Mahsulotlarni yuklash
df = load_data()

# Streamlit UI
st.title("📊 Mahsulotlar ro‘yxati")

# Foydalanuvchidan mahsulot nomi va narxini kiritish
mahsulot_nomi = st.text_input("Mahsulot nomini kiriting:")
mahsulot_narxi = st.number_input("Mahsulot narxini kiriting:", min_value=0.0, step=0)

# Mahsulot qo‘shish tugmasi
if st.button("➕ Qo‘shish"):
    if mahsulot_nomi and mahsulot_narxi:
        yangi_mahsulot = pd.DataFrame({
            "Mahsulot": [mahsulot_nomi],
            "Narx": [mahsulot_narxi],
            "Sana": [datetime.datetime.today().strftime("%Y-%m-%d")]
        })
        df = pd.concat([df, yangi_mahsulot], ignore_index=True)
        save_data(df)
        st.success(f"✅ {mahsulot_nomi} qo‘shildi!")

# Tozalash tugmasi (tarixni o‘chirish)
if st.button("🗑️ Tozalash"):
    df = pd.DataFrame(columns=["Mahsulot", "Narx", "Sana"])
    save_data(df)
    st.success("🔄 Ma'lumotlar tozalandi!")

# Joriy mahsulotlar ro‘yxatini ko‘rsatish
st.subheader("📋 Kiritilgan mahsulotlar:")
st.write(df)

# Excel fayl yaratish va yuklab olish
def create_excel_download_link(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Mahsulotlar")
    output.seek(0)
    return output

# Excel yuklab olish tugmasi
if not df.empty:
    excel_file = create_excel_download_link(df)
    st.download_button(
        label="📥 Excel faylni yuklab olish",
        data=excel_file,
        file_name="mahsulotlar.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
