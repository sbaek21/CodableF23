import tkinter
import customtkinter
import pygame
from threading import *
import time 
import math
import os
from tkinter import filedialog
# from customtkinter import CTkImage
# from PIL import Image, ImageTk

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

root = customtkinter.CTk()

root.title("Music Player")
root.geometry("400x500")


pygame.mixer.init()

n = 0
is_paused = False
inactive_ticks = 0
playlist = []


def update_song_listbox():
    song_listbox.delete(0, tkinter.END)  
    for song in list_of_songs:
        song_title = os.path.basename(song)
        song_listbox.insert(tkinter.END, song_title)

def select_folder():
    global list_of_songs, n
    folder_path = filedialog.askdirectory()
    if folder_path:
        list_of_songs = [os.path.join(folder_path, song) for song in os.listdir(folder_path)
                         if song.endswith(('.wav', '.mp3'))]
        n = 0
        update_song_listbox()



# def progress():
#     a = pygame.mixer.Sound(f"{list_of_songs[n]}")
#     song_len = a.get_length() * 3
#     if pygame.mixer.music.get_busy():
#         progressbar.set(pygame.mixer.music.get_pos() / 100000)
#         root.after(100, progress)
#     else:
#         global inactive_ticks
#         inactive_ticks += 1
#         if inactive_ticks == 10:
#             play_music()
#             inactive_ticks = 0
#         else:
#             root.after(100, progress)

def progress():
    if pygame.mixer.music.get_busy():
        progressbar.set(pygame.mixer.music.get_pos() / 100000)
        root.after(100, progress)
    else:
        global inactive_ticks
        inactive_ticks += 1
        if inactive_ticks == 10:
            play_music()
            inactive_ticks = 0
        else:
            root.after(100, progress)

def threading():
    t1 = Thread(target=progress)
    t1.start()
# def play_music():
#     # threading()
#     global n, is_paused, inactive_ticks
#     if n >= len(list_of_songs):
#         n = 0
#     if is_paused:
#         pygame.mixer.music.unpause()
#         is_paused = False
#     else:
#         try:
#             song_name = list_of_songs[n]
#             pygame.mixer.music.load(song_name)
#             pygame.mixer.music.play(loops=0)
#             pygame.mixer.music.set_volume(0.5)
#         except:
#             print("Error playing music")
#     song_listbox.select_clear(0, tkinter.END)  
#     song_listbox.select_set(n)  
#     song_listbox.see(n)  
#     n += 1

def play_music():
    global n, is_paused, inactive_ticks
    if n >= len(list_of_songs):
        n = 0
    if is_paused:
        pygame.mixer.music.unpause()
        is_paused = False
    else:
        try:
            song_name = list_of_songs[n]
            pygame.mixer.music.load(song_name)
            pygame.mixer.music.play(loops=0)
            pygame.mixer.music.set_volume(0.5)

            # Call progress to handle the progress of the current song
            progress()
        except:
            print("Error playing music")

    song_listbox.select_clear(0, tkinter.END)
    song_listbox.select_set(n)
    song_listbox.see(n)
    n += 1


def pause_music():
    global is_paused
    is_paused = True
    pygame.mixer.music.pause()

def rewind_music():
    # pygame.mixer.music.rewind()
    pygame.mixer.music.stop()
    pygame.mixer.music.play(start=0)
    progressbar.set(0)
    progress()
    # threading()
def skip_forward():
    play_music()
def skip_backward():
    global n
    if n > 0:
        n -= 1
    play_music()

def volume(value):
    #print(value)
    pygame.mixer.music.set_volume(value)

def play_selected_song(event):
    global n
    n = song_listbox.curselection()[0]
    play_music()



#Image

play_image = tkinter.PhotoImage(file="icons/play.png")
pause_image = tkinter.PhotoImage(file="icons/pause.png")
skipfwd_image = tkinter.PhotoImage(file="icons/skipFwd.png")
skipback_image = tkinter.PhotoImage(file="icons/skipBack.png")
rewind_image = tkinter.PhotoImage(file="icons/repeat.png")



#Buttons
play_button = customtkinter.CTkButton(master=root, image=play_image, text="", command = play_music, width = 1)
play_button.place(relx=0.5,rely=0.7,anchor=tkinter.CENTER)

pause_button = customtkinter.CTkButton(master=root, image=pause_image, text="", command = pause_music, width = 1)
pause_button.place(relx=0.6,rely=0.7,anchor=tkinter.CENTER)
#root.bind("<KeyPress-Space>", lambda event: pause_music())

rewind_button = customtkinter.CTkButton(master=root, image=rewind_image, text="", command = rewind_music, width =1)
rewind_button.place(relx=0.4,rely=0.7,anchor=tkinter.CENTER)


skip_f = customtkinter.CTkButton(master=root, image=skipfwd_image, text="", command = skip_forward, width=2)
skip_f.place(relx=0.8,rely=0.7,anchor=tkinter.CENTER)

skip_b = customtkinter.CTkButton(master=root, image=skipback_image, text="", command = skip_backward, width=2)
skip_b.place(relx=0.2,rely=0.7,anchor=tkinter.CENTER)

volume = customtkinter.CTkSlider(master=root, from_=0, to=1, command=volume, width=15, height = 130, orientation=tkinter.VERTICAL)
volume.place(relx=0.05,rely=0.78,anchor=tkinter.CENTER)

progressbar = customtkinter.CTkProgressBar(master=root, progress_color="#9df593", width=250)
progressbar.place(relx=0.5,rely=0.85,anchor=tkinter.CENTER)

select_folder_button = customtkinter.CTkButton(master=root, text="Select Folder", command=select_folder)
select_folder_button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

song_listbox = tkinter.Listbox(root, bg="#333333", fg="white", font=("Helvetica", 20))
song_listbox.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER, height=200, width=330)

scrollbar = tkinter.Scrollbar(root)
scrollbar.place(relx=0.9, rely=0.3, anchor=tkinter.CENTER, height=200)

song_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=song_listbox.yview)

song_listbox.bind("<Double-Button-1>", play_selected_song)
song_listbox.bind("<Return>", play_selected_song)
root.mainloop()
