# import streamlit as st
# import pandas as pd 
# import numpy as np 
# import pymongo
# import plotly.express as px

# # Fungsi untuk mengambil data dari MongoDB
# def get_data_from_mongodb():
#     client = pymongo.MongoClient('mongodb://localhost:27017/')
#     db = client['db_facemask']
#     collection = db['bigdata']
#     cursor = collection.find({})
#     data = [{'label': doc['label'], 'hari': doc['hari']} for doc in cursor]
#     return pd.DataFrame(data)

# option = st.sidebar.selectbox(
#     'Silakan pilih:',
#     ('Home','Data')
# )

# if option == 'Home' or option == '':
#     st.write("""# Halaman Utama""") 
#     # Mengambil data dari MongoDB
#     df = get_data_from_mongodb()  
#     st.write(df)
    
#     # Melakukan visualisasi berdasarkan hari
#     st.write("Jumlah pengunjung puskesmas berdasarkan hari:")
#     st.bar_chart(df['hari'].value_counts())
    
#     masker_per_hari = df[df['label'] == 'with_mask'].groupby('hari').size()
#     tanpa_masker_per_hari = df[df['label'] == 'without_mask'].groupby('hari').size()
    
#     # Temukan hari dengan jumlah pengguna masker terbanyak
#     hari_terbanyak_with_mask = masker_per_hari.idxmax()
#     jumlah_terbanyak_with_mask = masker_per_hari.max()

#     hari_terbanyak_without_mask = tanpa_masker_per_hari.idxmax()
#     jumlah_terbanyak_without_mask = tanpa_masker_per_hari.max()

    

    
    
#     # Filter data hanya untuk pengguna masker
#     df_masker = df[df['label'] == 'with_mask']
#     df_without_mask = df[df['label'] == 'without_mask']

#     # Grupkan berdasarkan hari dan label, kemudian hitung jumlahnya
#     df_grouped = df_masker.groupby(['hari']).size().reset_index(name='count')

#     # Visualisasi dengan pie chart
#     fig = px.pie(df_grouped, values='count', names='hari', title='Persentase Pengguna Masker Berdasarkan Hari')
#     st.plotly_chart(fig)
    
#     st.write("Keterangan:")
#     if jumlah_terbanyak_with_mask > 0:
#         st.write(f"Pengguna masker paling banyak ditemukan pada hari {hari_terbanyak_with_mask} dengan jumlah {jumlah_terbanyak_with_mask} (dengan masker).")
#     else:
#         st.write("Belum ada data pengguna masker (dengan masker).")
        
#     # Grupkan berdasarkan hari dan label, kemudian hitung jumlahnya
#     df_grouped = df_without_mask.groupby(['hari']).size().reset_index(name='count')

#     # Visualisasi dengan pie chart
#     fig = px.pie(df_grouped, values='count', names='hari', title='Persentase Pengguna Tidak Menggunakan Masker Berdasarkan Hari')
#     st.plotly_chart(fig)
#     st.write("Keterangan:")
#     if jumlah_terbanyak_without_mask > 0:
#         st.write(f"Pengguna tanpa masker paling banyak ditemukan pada hari {hari_terbanyak_without_mask} dengan jumlah {jumlah_terbanyak_without_mask} (tanpa masker).")
#         st.write("Pihak puskesmas menyediakan masker, sehingga dapat diasumsikan bahwa kepatuhan penggunaan masker akan meningkat.Ketersediaan masker diseluruh hari dapat membantu dalam meningkatkan kepatuhan penggunaan masker oleh pengunjung.")
#     else:
#         st.write("Belum ada data pengguna tanpa masker.")
    
# elif option == 'Data':
#     st.write("""## Data""") 
#     # Mengambil data dari MongoDB
#     df = get_data_from_mongodb()  
    
#     # Tambahkan tabel untuk menampilkan jumlah pengguna masker berdasarkan hari
#     st.write("Tabel pengguna masker berdasarkan hari:")
#     masker_per_hari = df[df['label'] == 'with_mask'].groupby('hari').size()
#     tanpa_masker_per_hari = df[df['label'] == 'without_mask'].groupby('hari').size()
#     total = masker_per_hari + tanpa_masker_per_hari
#     masker_table_data = {
#         'Hari': masker_per_hari.index,
#         'with_mask': masker_per_hari.values,
#         'without_mask': tanpa_masker_per_hari.values,
#         'Total' : total.values
#     }
#     masker_table_df = pd.DataFrame(masker_table_data)
    
#     st.write(masker_table_df)
    
#     without_mask = df[df['label'] == 'without_mask'].shape[0]
#     with_mask = df[df['label'] == 'with_mask'].shape[0]
#     label = df.shape[0]
#     total = without_mask + with_mask
#     persentase = with_mask / label * 100
#     data = {
#         'with_mask': [with_mask],
#         'without_mask' : [without_mask],
#         'Total Terdeteksi': [total],
#         # 'Persentase with_mask': [persentase]
#     }
#     table = pd.DataFrame(data, index=['Jumlah'])
#     st.write(table)
    
    
    
        
#     # Tambahkan tabel untuk menampilkan rata-rata pengguna masker berdasarkan hari Senin
#     st.write("Rata-rata pengguna masker berdasarkan hari Senin:")
#     monday_data = df[df['hari'] == 'Monday']

#     rata_rata_with_mask_monday = monday_data[monday_data['label'] == 'with_mask'].shape[0] / monday_data.shape[0]
#     rata_rata_without_mask_monday = monday_data[monday_data['label'] == 'without_mask'].shape[0] / monday_data.shape[0]

#     rata_rata_masker_table_data = {
#         'Label': ['with_mask', 'without_mask'],
#         'Rata-rata per Hari': [rata_rata_with_mask_monday, rata_rata_without_mask_monday]
#     }
#     rata_rata_masker_table_df = pd.DataFrame(rata_rata_masker_table_data)

#     st.write(rata_rata_masker_table_df)
    
#     # Tambahkan tabel untuk menampilkan rata-rata pengguna masker berdasarkan hari Senin
#     st.write("Rata-rata pengguna masker berdasarkan hari Selasa:")
#     monday_data = df[df['hari'] == 'Tuesday']

#     rata_rata_with_mask_monday = monday_data[monday_data['label'] == 'with_mask'].shape[0] / monday_data.shape[0]
#     rata_rata_without_mask_monday = monday_data[monday_data['label'] == 'without_mask'].shape[0] / monday_data.shape[0]

#     rata_rata_masker_table_data = {
#         'Label': ['with_mask', 'without_mask'],
#         'Rata-rata per Hari': [rata_rata_with_mask_monday, rata_rata_without_mask_monday]
#     }
#     rata_rata_masker_table_df = pd.DataFrame(rata_rata_masker_table_data)

#     st.write(rata_rata_masker_table_df)
    
#     # Tambahkan tabel untuk menampilkan rata-rata pengguna masker berdasarkan hari Senin
#     st.write("Rata-rata pengguna masker berdasarkan hari Rabu:")
#     monday_data = df[df['hari'] == 'Wednesday']

#     rata_rata_with_mask_monday = monday_data[monday_data['label'] == 'with_mask'].shape[0] / monday_data.shape[0]
#     rata_rata_without_mask_monday = monday_data[monday_data['label'] == 'without_mask'].shape[0] / monday_data.shape[0]

#     rata_rata_masker_table_data = {
#         'Label': ['with_mask', 'without_mask'],
#         'Rata-rata per Hari': [rata_rata_with_mask_monday, rata_rata_without_mask_monday]
#     }
#     rata_rata_masker_table_df = pd.DataFrame(rata_rata_masker_table_data)

#     st.write(rata_rata_masker_table_df)
    
#     # Tambahkan tabel untuk menampilkan rata-rata pengguna masker berdasarkan hari Senin
#     st.write("Rata-rata pengguna masker berdasarkan hari Kamis:")
#     monday_data = df[df['hari'] == 'Thursday']

#     rata_rata_with_mask_monday = monday_data[monday_data['label'] == 'with_mask'].shape[0] / monday_data.shape[0]
#     rata_rata_without_mask_monday = monday_data[monday_data['label'] == 'without_mask'].shape[0] / monday_data.shape[0]

#     rata_rata_masker_table_data = {
#         'Label': ['with_mask', 'without_mask'],
#         'Rata-rata per Hari': [rata_rata_with_mask_monday, rata_rata_without_mask_monday]
#     }
#     rata_rata_masker_table_df = pd.DataFrame(rata_rata_masker_table_data)

#     st.write(rata_rata_masker_table_df)
    
#     # Tambahkan tabel untuk menampilkan rata-rata pengguna masker berdasarkan hari Senin
#     st.write("Rata-rata pengguna masker berdasarkan hari Jumat:")
#     monday_data = df[df['hari'] == 'Friday']

#     rata_rata_with_mask_monday = monday_data[monday_data['label'] == 'with_mask'].shape[0] / monday_data.shape[0]
#     rata_rata_without_mask_monday = monday_data[monday_data['label'] == 'without_mask'].shape[0] / monday_data.shape[0]

#     rata_rata_masker_table_data = {
#         'Label': ['with_mask', 'without_mask'],
#         'Rata-rata per Hari': [rata_rata_with_mask_monday, rata_rata_without_mask_monday]
#     }
#     rata_rata_masker_table_df = pd.DataFrame(rata_rata_masker_table_data)

#     st.write(rata_rata_masker_table_df)
    
#     st.write("Dari data yang diberikan, terlihat bahwa penggunaan masker bervariasi dari hari ke hari.Secara umum, penggunaan masker lebih tinggi pada senin,rabu dan kamis, sedangkan lebih rendah pada hari selasa dan jumat.Hal ini menunjukkan adanya perubahan yang tidak tetap atau tidak teratur dalam kepatuhan penggunaan masker dari hari ke hari. ")
    
#     # # Rata-rata pengguna masker berdasarkan hari Senin
#     # monday_data = df[df['hari'] == 'Monday']
#     # rata_rata_with_mask_monday = monday_data[monday_data['label'] == 'with_mask'].shape[0] / monday_data.shape[0]
#     # rata_rata_without_mask_monday = monday_data[monday_data['label'] == 'without_mask'].shape[0] / monday_data.shape[0]

#     # # Buat DataFrame untuk tabel
#     # rata_rata_masker_table_data = {
#     #         'Label': ['with_mask', 'without_mask'],
#     #         'Rata-rata per Hari': [rata_rata_with_mask_monday, rata_rata_without_mask_monday]
#     #     }
#     # rata_rata_masker_table_df = pd.DataFrame(rata_rata_masker_table_data)

#     # # Tampilkan diagram Pie Plotly
#     # fig = px.pie(rata_rata_masker_table_df, values='Rata-rata per Hari', names='Label',
#     #                 title='Rata-rata Pengguna Masker Berdasarkan Hari Senin')
#     # st.plotly_chart(fig)


import streamlit as st
from pymongo import MongoClient
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# Setup MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['object_counter_db']
collection = db['detections']

# Function to load data from MongoDB
def load_data():
    data = list(collection.find())
    df = pd.DataFrame(data)
    return df

# Load data
df = load_data()

# Streamlit UI
st.title("Object Counter Data Visualization")

# Filters
class_filter = st.selectbox("Select Class", options=df['class'].unique(), index=0)
direction_filter = st.selectbox("Select Direction", options=df['direction'].unique(), index=0)

# Filter data
filtered_df = df[(df['class'] == class_filter) & (df['direction'] == direction_filter)]

# Display filtered data
st.subheader(f"Data for {class_filter} with {direction_filter} direction")
st.dataframe(filtered_df)

# Count of entries by timestamp
st.subheader("Count of Entries by Timestamp")
counts = filtered_df['timestamp'].value_counts().sort_index()
st.line_chart(counts)

# Bar chart of class distribution
st.subheader("Class Distribution")
class_counts = df['class'].value_counts()
st.bar_chart(class_counts)

# Direction distribution
st.subheader("Direction Distribution")
direction_counts = df['direction'].value_counts()
st.bar_chart(direction_counts)

