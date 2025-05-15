import streamlit as st
import pandas as pd

st.set_page_config(page_title="Rekap Order Source", layout="wide")
st.title("📊 Rekapitulasi Data Berdasarkan Order Source")

# Upload file Excel
uploaded_file = st.file_uploader("📁 Upload file Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        # Baca file
        df = pd.read_excel(uploaded_file)

        # Bersihkan kolom kosong & kolom duplikat
        df = df.dropna(axis=1, how='all')
        df = df.loc[:, ~df.columns.duplicated()]

        st.subheader("✅ Data Awal yang Diunggah:")
        st.dataframe(df)

        # Cek apakah kolom 'Order Source' ada
        if 'Order Source' not in df.columns:
            st.error("❌ Kolom 'Order Source' tidak ditemukan dalam file Excel.")
        else:
            # Pilih order source yang ingin difilter (opsional)
            unique_sources = df['Order Source'].dropna().unique().tolist()
            selected_sources = st.multiselect("🔍 Pilih Order Source yang ingin ditampilkan:", unique_sources, default=unique_sources)

            # Filter data jika ada pilihan
            df_filtered = df[df['Order Source'].isin(selected_sources)]

            # Ambil kolom numerik
            numeric_cols = df_filtered.select_dtypes(include='number').columns.tolist()

            # Grouping dan agregasi
            summary = df_filtered.groupby('Order Source')[numeric_cols].sum().reset_index()

            st.subheader("📈 Hasil Penjumlahan per Order Source:")
            st.dataframe(summary)

            # Download tombol
            csv = summary.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Download hasil (.csv)", csv, file_name="rekap_order_source.csv", mime="text/csv")

    except Exception as e:
        st.error(f"❌ Terjadi kesalahan saat membaca file: {e}")
