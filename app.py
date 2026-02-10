import streamlit as st
from moviepy.video.io.VideoFileClip import VideoFileClip
import os

st.set_page_config(page_title="Découpeur Vidéo Web", page_icon="✂️")
st.title("✂️ Découpeur de Vidéo Professionnel")

# 1. Chargement du fichier
uploaded_file = st.file_uploader("Choisissez une vidéo...", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    # Sauvegarde temporaire du fichier uploadé (utilisation de getbuffer pour plus de stabilité)
    with open("temp_video.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # On charge la vidéo
    video = VideoFileClip("temp_video.mp4")
    duration = video.duration
    st.info(f"Durée totale de la vidéo : {duration:.2f} secondes")

    # 2. Formulaire pour les segments
    st.subheader("Configurer le segment")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Début**")
        start_min = st.number_input("Minutes (Début)", min_value=0, value=0, step=1)
        start_sec = st.number_input("Secondes (Début)", min_value=0.0, max_value=59.9, value=0.0, step=0.1)
        
    with col2:
        st.write("**Fin**")
        end_min = st.number_input("Minutes (Fin)", min_value=0, value=0, step=1)
        end_sec = st.number_input("Secondes (Fin)", min_value=0.0, max_value=59.9, value=min(10.0, duration), step=0.1)

    # Calcul du temps total en secondes
    start_total = (start_min * 60) + start_sec
    end_total = (end_min * 60) + end_sec

    if st.button("Générer l'aperçu du clip"):
        if start_total >= end_total:
            st.error("Le temps de début doit être inférieur au temps de fin !")
        elif end_total > duration:
            st.error(f"Le temps de fin dépasse la durée de la vidéo ({duration:.2f}s)")
        else:
            try:
                with st.spinner("Découpage en cours..."):
                    output_path = "clip_resultat.mp4"
                    # On crée le clip
                    clip = video.subclip(start_total, end_total)
                    clip.write_videofile(output_path, codec="libx264", audio_codec="aac", temp_audiofile="temp-audio.m4a", remove_temp=True)
                    clip.close()
                
                st.success("Clip généré !")
                st.video(output_path)
                
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="⬇️ Télécharger le clip",
                        data=file,
                        file_name="mon_clip.mp4",
                        mime="video/mp4"
                    )
            except Exception as e:
                st.error(f"Une erreur est survenue pendant le découpage : {e}")
    
    # On ferme la vidéo source UNIQUEMENT après tout le reste
    video.close()
