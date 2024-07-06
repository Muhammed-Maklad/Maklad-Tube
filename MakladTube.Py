import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from pytube import YouTube, Playlist
import threading
import os
import webbrowser
from PIL import Image, ImageTk


Background_color = "#212121"
Text_color = "#FFFFFF"
Entry_BgColor = "#424242"
Button_BgColor = "#607D8B"
ButtonText_color = "#FFFFFF"
RadioSelect_Color = "#64B5F6"
Checked_Color = "#FFD700"

def select_directory():
    directory_path = filedialog.askdirectory()
    if not directory_path:
        directory_path = os.path.expanduser("~/Downloads") # Make Download The Defualte Directory 
    directory_var.set(directory_path)

def download_video():
    url = url_entry.get().strip()
    save_path = directory_var.get().strip()
    
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL")
        return
    
    if not save_path:
        save_path = os.path.expanduser("~/Downloads")
        directory_var.set(save_path)
    
    try:
        if 'playlist' in url:
            download_playlist(url, save_path)
        else:
            download_single_video(url, save_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download video(s): {e}")

def download_single_video(url, save_path):
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        video_title = yt.title

        if mp4_format_var.get() == "MP4":
            video_quality = quality_var.get()
            available_qualities = [stream.resolution for stream in yt.streams.filter(file_extension='mp4')]
            if video_quality not in available_qualities:
                video_quality = "360p"
            stream = yt.streams.filter(res=video_quality, file_extension='mp4').first()
        elif mp4_format_var.get() == "MP3":
            stream = yt.streams.filter(only_audio=True).first()

        download_thread = threading.Thread(target=download_stream, args=(stream, save_path, video_title))
        download_thread.start()
        
        in_progress_listbox.insert(tk.END, f"⌛ {video_title}: 0.00%")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download video: {e}")

def download_playlist(url, save_path):
    try:
        playlist = Playlist(url)
        download_thread = threading.Thread(target=download_playlist_videos, args=(playlist, save_path))
        download_thread.start()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download playlist: {e}")

def download_playlist_videos(playlist, save_path):
    for video_url in playlist.video_urls:
        download_single_video(video_url, save_path)
    messagebox.showinfo("Download Complete", "All videos in the playlist have been downloaded")

def download_stream(stream, save_path, video_title):
    try:
        stream.download(output_path=save_path)
        update_download_status(video_title)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download stream: {e}")

def update_download_status(video_title):
    completed_listbox.insert(tk.END, f"✅ {video_title}")

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100 # Show the precentage of Doanload 
    
    for i in range(in_progress_listbox.size()):
        item = in_progress_listbox.get(i)
        if stream.title in item:
            in_progress_listbox.delete(i)
            break
    in_progress_listbox.insert(tk.END, f"⌛ {stream.title}: {percentage:.2f}%")

root = tk.Tk()
root.title("Maklad Tube")
root.configure(bg=Background_color)

Youtube_logo = Image.open(r"D:\Project\Youtube.png")
Youtube_logo = Youtube_logo.resize((50, 50))
Youtube_logo = ImageTk.PhotoImage(Youtube_logo)

style = ttk.Style()
style.theme_use("clam")
style.configure("Custom.TRadiobutton", background=Entry_BgColor, foreground=Text_color, selectcolor=RadioSelect_Color, indicatorcolor=Checked_Color)

title_label = tk.Label(root, text="Maklad Tube", font=("Cascadia Code SemiBold", 30, "bold"), bg=Background_color, fg="#a6414d",image=Youtube_logo, compound=tk.LEFT)
title_label.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 10))

# URL Entry
url_label = tk.Label(root, text="Enter YouTube URL:", bg=Background_color, fg=Text_color)
url_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
url_entry = tk.Entry(root, width=50, bg=Entry_BgColor, fg=Text_color)
url_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")

# Select the Suitable Format
format_frame = tk.LabelFrame(root, text="Choose format:", bg=Background_color, fg=Text_color)
format_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")
mp4_format_var = tk.StringVar()
mp4_format_var.set("MP4")
mp4_radio = ttk.Radiobutton(format_frame, text="MP4", variable=mp4_format_var, value="MP4", style="Custom.TRadiobutton")
mp4_radio.pack(side="left", padx=10, pady=5)
mp3_radio = ttk.Radiobutton(format_frame, text="MP3", variable=mp4_format_var, value="MP3", style="Custom.TRadiobutton")
mp3_radio.pack(side="left", padx=10, pady=5)

# Select the Best Quality
quality_frame = tk.LabelFrame(root, text="Choose quality:", bg=Background_color, fg=Text_color)
quality_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w")
quality_var = tk.StringVar()
quality_var.set("360p")
qualities = ["360p", "480p", "720p", "1080p"]
for quality in qualities:
    radio = ttk.Radiobutton(quality_frame, text=quality, variable=quality_var, value=quality, style="Custom.TRadiobutton")
    radio.pack(side="left", padx=10, pady=5)

# Selecte the Directory to save the videos
directory_label = tk.Label(root, text="Select download directory:", bg=Background_color, fg=Text_color)
directory_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
directory_var = tk.StringVar(root)
directory_entry = tk.Entry(root, textvariable=directory_var, width=40, bg=Entry_BgColor, fg=Text_color)
directory_entry.grid(row=4, column=1, padx=10, pady=5, sticky="we")
directory_button = tk.Button(root, text="Browse", command=select_directory, bg=Button_BgColor, fg=ButtonText_color)
directory_button.grid(row=4, column=2, padx=10, pady=5)

# Make a  Download Button
download_button = tk.Button(root, text="Download", command=download_video, bg=Button_BgColor, fg=ButtonText_color)
download_button.grid(row=5, column=0, columnspan=3, padx=10, pady=(20, 10), sticky="we")

# Tha name Of the videos that is In-progress 
in_progress_label = tk.Label(root, text="⌛ In Progress:", bg=Background_color, fg=Text_color)
in_progress_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
in_progress_listbox = tk.Listbox(root, width=60, height=3, bg=Entry_BgColor, fg=Text_color)
in_progress_listbox.grid(row=6, column=1, padx=10, pady=5, sticky="we")

# Tha name Of the videos that is Completed Listbox
completed_label = tk.Label(root, text="✅ Completed:", bg=Background_color, fg=Text_color)
completed_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")
completed_listbox = tk.Listbox(root, width=60, height=3, bg=Entry_BgColor, fg=Text_color)
completed_listbox.grid(row=7, column=1, padx=10, pady=5, sticky="we")

def open_linkedin():
    webbrowser.open_new("https://www.linkedin.com/in/muhammed-gamal-61337b260/")

linkedin_logo = Image.open(r"D:\Project\linkedin.png")
linkedin_logo = linkedin_logo.resize((30, 30))
linkedin_logo = ImageTk.PhotoImage(linkedin_logo)


linkedin_label = tk.Label(root, text="   My LinkedIn profile",background=Background_color, fg="#0a66c2", font=("Kristen Itc", 14), cursor="hand2",image=linkedin_logo, compound=tk.LEFT)
linkedin_label.grid(row=8, column=1, padx=10, pady=20)
linkedin_label.bind("<Button-1>", lambda e: open_linkedin())

root.iconbitmap(r"D:\Project\Youtube.ico")
root.mainloop()

