import tkinter as tk
from tkinter import ttk
from ttkthemes import themed_tk
import pygame
from PIL import Image, ImageTk
import time
import os
from tkinter import filedialog

root = themed_tk.ThemedTk()
root.set_theme("black")

root.title("Music Player")
root.geometry("400x500")

pygame.mixer.init()

n = 0
is_paused = False
list_of_songs = []
current_song = None
progress_interval = 1000  # Progress update interval in milliseconds

def update_song_listbox():
    song_listbox.delete(0, tk.END)
    for song in list_of_songs:
        song_title = os.path.basename(song)
        song_listbox.insert(tk.END, song_title)

def select_folder():
    global list_of_songs, n
    folder_path = filedialog.askdirectory()
    if folder_path:
        list_of_songs = [os.path.join(folder_path, song) for song in os.listdir(folder_path) if song.endswith(('.wav', '.mp3'))]
        n = 0
        update_song_listbox()

def play_music():
    global n, is_paused, current_song
    if is_paused:
        pygame.mixer.music.unpause()
        is_paused = False
    else:
        try:
            song_name = list_of_songs[n]
            current_song = pygame.mixer.Sound(song_name)
            pygame.mixer.music.load(song_name)
            pygame.mixer.music.play()
            pygame.mixer.music.set_endevent(pygame.USEREVENT)
            pygame.mixer.music.set_volume(0.5)
            update_progress()
        except:
            print("Error playing music")

    song_listbox.select_clear(0, tk.END)
    song_listbox.select_set(n)
    song_listbox.see(n)

def pause_music():
    global is_paused, current_song
    is_paused = True
    pygame.mixer.music.pause()
    current_song = None

def rewind_music():
    pygame.mixer.music.rewind()
    progressbar["value"] = 0
    update_progress()

def skip_forward():
    global n, current_song
    n += 1
    if n >= len(list_of_songs):
        n = 0
    if current_song is not None:
        current_song.stop()
    play_music()

def skip_backward():
    global n, current_song
    n -= 1
    if n < 0:
        n = len(list_of_songs) - 1
    if current_song is not None:
        current_song.stop()
    play_music()

def volume(value):
    volume_level = float(value)
    pygame.mixer.music.set_volume(volume_level)

def update_progress():
    global current_song
    if pygame.mixer.get_busy():
        elapsed_time = pygame.mixer.music.get_pos() / 1000  # in seconds
        progressbar["value"] = elapsed_time / current_song.get_length() * 100
        root.after(progress_interval, update_progress)
    else:
        progressbar["value"] = 0
        skip_forward()

def play_selected_song(event):
    selected_song_index = song_listbox.curselection()
    if selected_song_index:
        global n, current_song
        n = selected_song_index[0]
        if current_song is not None:
            current_song.stop()
        play_music()

# Image
play_image = Image.open("icons/play.png")
play_image = ImageTk.PhotoImage(play_image)
pause_image = Image.open("icons/pause.png")
pause_image = ImageTk.PhotoImage(pause_image)
skipfwd_image = Image.open("icons/skipFwd.png")
skipfwd_image = ImageTk.PhotoImage(skipfwd_image)
skipback_image = Image.open("icons/skipBack.png")
skipback_image = ImageTk.PhotoImage(skipback_image)
rewind_image = Image.open("icons/repeat.png")
rewind_image = ImageTk.PhotoImage(rewind_image)

# Buttons
play_button = ttk.Button(master=root, image=play_image, text="", command=play_music)
play_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

pause_button = ttk.Button(master=root, image=pause_image, text="", command=pause_music)
pause_button.place(relx=0.6, rely=0.7, anchor=tk.CENTER)

rewind_button = ttk.Button(master=root, image=rewind_image, text="", command=rewind_music)
rewind_button.place(relx=0.4, rely=0.7, anchor=tk.CENTER)

skip_f = ttk.Button(master=root, image=skipfwd_image, text="", command=skip_forward)
skip_f.place(relx=0.8, rely=0.7, anchor=tk.CENTER)

skip_b = ttk.Button(master=root, image=skipback_image, text="", command=skip_backward)
skip_b.place(relx=0.2, rely=0.7, anchor=tk.CENTER)

volume = ttk.Scale(master=root, from_=1, to=0, command=volume, orient=tk.VERTICAL)
volume.place(relx=0.05, rely=0.78, anchor=tk.CENTER)

progressbar = ttk.Progressbar(master=root, mode="determinate", length=250)
progressbar.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

select_folder_button = ttk.Button(master=root, text="Select Folder", command=select_folder)
select_folder_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

song_listbox = tk.Listbox(root, bg="#333333", fg="white", font=("Helvetica", 20),
    selectbackground="blue", selectmode=tk.SINGLE)
song_listbox.place(relx=0.5, rely=0.3, anchor=tk.CENTER, height=200, width=330)

scrollbar = tk.Scrollbar(root)
scrollbar.place(relx=0.9, rely=0.3, anchor=tk.CENTER, height=200)

song_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=song_listbox.yview)

song_listbox.bind("<Double-1>", play_selected_song)
song_listbox.bind("<Return>", play_selected_song)

root.mainloop()
