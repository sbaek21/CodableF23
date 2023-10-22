import tkinter as tk
from tkinter import ttk
from ttkthemes import themed_tk
import pygame
from PIL import Image, ImageTk
import os
from tkinter import filedialog
import time
from threading import Thread


# Define song_thread as a global variable
song_thread = None

root = themed_tk.ThemedTk()
root.set_theme("black")

root.title("Music Player")
root.geometry("400x500")

pygame.mixer.init()

n = 0
is_playing = False
list_of_songs = []

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

# Function to play music
def play_music():
    global n, is_playing
    if is_playing:
        pygame.mixer.music.unpause()
    else:
        try:
            song_name = list_of_songs[n]
            pygame.mixer.music.load(song_name)
            pygame.mixer.music.play(loops=0)
            pygame.mixer.music.set_volume(0.5)
            is_playing = True
            threading()
        except Exception as e:
            print(f"Error playing music: {e}")
    
    song_listbox.select_clear(0, tk.END)
    song_listbox.select_set(n)
    song_listbox.see(n)
    n += 1
    if n >= len(list_of_songs):
        n = 0

# Function to pause music
def pause_music():
    global is_playing
    if is_playing:
        pygame.mixer.music.pause()
        is_playing = False

# Function to rewind music
def rewind_music():
    pygame.mixer.music.rewind()
    progressbar["value"] = 0

# Function to skip forward
def skip_forward():
    global n
    n += 1
    if n >= len(list_of_songs):
        n = 0
    play_music()

# Function to skip backward
def skip_backward():
    global n
    n -= 1
    if n < 0:
        n = len(list_of_songs) - 1
    play_music()

# Function to set the volume
def set_volume(value):
    volume_level = float(value)
    pygame.mixer.music.set_volume(volume_level)

# Function to update the progress bar
def update_progress():
    if is_playing:
        pos = pygame.mixer.music.get_pos()
        if pos >= 0:
            progressbar["value"] = pos
        root.after(100, update_progress)

# Function to update the song list
def update_song_listbox():
    song_listbox.delete(0, tk.END)
    for song in list_of_songs:
        song_title = os.path.basename(song)
        song_listbox.insert(tk.END, song_title)

# Function to create a separate thread for progress
def threading():
    global song_thread
    if song_thread and song_thread.is_alive():
        song_thread.join()
    song_thread = Thread(target=update_progress)
    song_thread.daemon = True
    song_thread.start()

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

volume = ttk.Scale(master=root, from_=1, to=0, command=set_volume, orient=tk.VERTICAL)
volume.place(relx=0.05, rely=0.78, anchor=tk.CENTER)

progressbar = ttk.Progressbar(master=root, mode="determinate", length=250)
progressbar.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

select_folder_button = ttk.Button(master=root, text="Select Folder", command=select_folder)
select_folder_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

song_listbox = tk.Listbox(root, bg="#333333", fg="white", font=("Helvetica", 20), selectbackground="blue", selectmode=tk.SINGLE)
song_listbox.place(relx=0.5, rely=0.3, anchor=tk.CENTER, height=200, width=330)

scrollbar = tk.Scrollbar(root)
scrollbar.place(relx=0.9, rely=0.3, anchor=tk.CENTER, height=200)

song_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=song_listbox.yview)

song_listbox.bind("<Double-1>", play_music)
song_listbox.bind("<Return>", play_music)

def on_closing():
    global song_thread
    # Stop the background thread when the program is closed
    if song_thread and song_thread.is_alive():
        song_thread.join()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
