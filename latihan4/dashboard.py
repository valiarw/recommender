import streamlit as st
import pandas as pd

# Data contoh soal dan materi (Anda bisa mengganti dengan data sebenarnya)
data = pd.read_csv('data\data soal\questions.csv')
data = data[['question_id','material']]

# Judul aplikasi
st.title("Python Learning Material Recommendation System")
st.write("Material recommendations based on user interaction data with questions.")

# Input data interaksi pengguna
st.subheader("Enter User Interaction Data:")
user_id = st.number_input("User ID", min_value=1, step=1)
question_ids = st.text_input("Question IDs (separated by commas, example: 99,14,8,12)")
attempts = st.text_input("Number of Attempts (according to the order of Question IDs, example: 1,1,1,1)")
corrects = st.text_input("True or False (0 for false, 1 for true, example: 0,1,1,1)")
durations = st.text_input("Duration of answering (in seconds, in order, example: 59,30,35,20)")

# Tombol untuk memproses data
if st.button("Process and Recommend"):
    try:
        # Konversi input pengguna ke dalam DataFrame
        user_interaction = {
            'user_id': [user_id] * len(question_ids.split(',')),
            'question_id': list(map(int, question_ids.split(','))),
            'attempts': list(map(int, attempts.split(','))),
            'correct': list(map(int, corrects.split(','))),
            'duration': list(map(int, durations.split(',')))
        }
        
        user_interaction_df = pd.DataFrame(user_interaction)

        # Gabungkan data interaksi pengguna dengan data materi berdasarkan question_id
        user_interaction_df = user_interaction_df.merge(data, on='question_id', how='left')

        # Hitung rata-rata kesalahan per materi
        user_error_data = user_interaction_df.groupby('material').agg({
            'attempts': 'mean',
            'correct': 'mean',
            'duration': 'mean'
        }).reset_index()

        # Tambahkan kolom tingkat kesalahan
        user_error_data['avg_error_rate'] = 1 - user_error_data['correct']

        # Rekomendasikan materi dengan tingkat kesalahan tertinggi
        user_recommended_materials = user_error_data.sort_values(by='avg_error_rate', ascending=False).head(1)

        # Tampilkan hasil rekomendasi
        st.subheader("Recommendation Results:")
        if not user_recommended_materials.empty:
            st.write("**Material that needs to be studied by students:**")
            st.dataframe(user_recommended_materials)
        else:
            st.write("Data is insufficient to provide recommendations.")
    except Exception as e:
        st.error(f"An error occurred while processing the data: {e}")
