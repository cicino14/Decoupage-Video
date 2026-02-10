
from tkinter import filedialog, messagebox
from moviepy.video.io.VideoFileClip import VideoFileClip
import os


def select_video(video_path):
    path = filedialog.askopenfilename(
        filetypes=[("Video files", "*.mp4 *.avi *.mov")]
    )
    video_path.set(path)


def cut_video(video_path, segments_entry):
    path = video_path.get()
    segments_text = segments_entry.get("1.0", "end").strip()

    if not path or not segments_text:
        messagebox.showerror("Erreur", "Veuillez choisir une vidéo et définir les segments")
        return

    try:
        video = VideoFileClip(path)
        base_name = os.path.splitext(os.path.basename(path))[0]
        output_dir = "clips"
        os.makedirs(output_dir, exist_ok=True)

        for i, line in enumerate(segments_text.split("\n")):
            if "-" not in line: continue # Ignore les lignes mal formatées
            
            # On garde en texte pour supporter le format "00:01:15"
            times = [t.strip() for t in line.split("-")]
            start, end = times[0], times[1]
            
            output_path = os.path.join(output_dir, f"{base_name}_clip_{i+1}.mp4")
            
            # subclip accepte (start, end)
            clip = video.subclip(start, end)
            clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
            clip.close()

        video.close()
        messagebox.showinfo("Succès", "Découpage terminé ✅")

    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")