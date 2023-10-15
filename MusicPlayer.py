import tkinter
import customtkinter
import pygame
from PIL import Image, ImageTk
from threading import *
import time 
import math
import os
from tkinter import filedialog

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

root = customtkinter.CTk()

root.title("Music Player")
root.geometry("400x480")

pygame.mixer.init()


#cover_folder_path = 'img/'
#list_of_covers = [os.path.join(cover_folder_path, cover) for cover in os.listdir(cover_folder_path) if cover.endswith('.jpg')]
n = 0
is_paused = False
playlist = []

def select_folder():
    global list_of_songs, n
    folder_path = filedialog.askdirectory()
    if folder_path:
        list_of_songs = [os.path.join(folder_path, song) for song in os.listdir(folder_path) if song.endswith(('.wav', '.mp3'))]
        n = 0

#def get_album_cover(song_name, n):
#    image1 = Image.open(list_of_covers[n])
#    image2=image1.resize((750, 750))
#    load = ImageTk.PhotoImage(image2)
#    
#    label1 = tkinter.Label(root, image=load)
#    label1.image = load
#    label1.place(relx=.19, rely=.06)
#    
#    stripped_string = song_name[6:-3]
#    song_name_label = tkinter.Label(text= stripped_string,bg="#222222", fg="white")
#    song_name_label.place(relx=0.4,rely=0.6)


def progress():
    a = pygame.mixer.Sound(f"{list_of_songs[n]}")
    song_len = a.get_length()*3
    for i in range(0,math.ceil(song_len)):
        time.sleep(0.3)
        progressbar.set(pygame.mixer.music.get_pos()/100000)

def threading():
    t1 = Thread(target=progress)
    t1.start()
def play_music():
    global n, is_paused
    if is_paused:
        pygame.mixer.music.unpause()
        is_paused = False
    else:
        try:
            song_name = list_of_songs[n]
            pygame.mixer.music.load(song_name)
            pygame.mixer.music.play(loops=0)
            pygame.mixer.music.set_volume(0.5)
#            get_album_cover(song_name, n)
        except:
            print("Error playing music")
    n += 1
    if n >= len(list_of_songs):
        n = 0
""" def play_music():
    global n
    song_name = list_of_songs[n]
    threading()
    try:
        paused
    except NameError:
        try:
            pygame.mixer.music.load(song_name)
            pygame.mixer.music.play(loops=0)
            pygame.mixer.music.set_volume(0.5)
            get_album_cover(song_name, n)
        except:
            print("Error playing music")
    else:
        pygame.mixer.music.unpause()
    n += 1
    if n >= len(list_of_songs):
        n = 0
"""

def pause_music():
    global is_paused
    is_paused = True
    pygame.mixer.music.pause()

def rewind_music():
    pygame.mixer.music.rewind()
    progressbar.set(0)
def skip_forward():
    play_music()
def skip_backward():
    global n
    n -= 2
    play_music()
def volume(value):
    #print(value)
    pygame.mixer.music.set_volume(value)



#Image

play_image = tkinter.PhotoImage(file="icons/play.png")
pause_image = tkinter.PhotoImage(file="icons/pause.png")
skipfwd_image = tkinter.PhotoImage(file="icons/skipFwd.png")
skipback_image = tkinter.PhotoImage(file="icons/skipBack.png")
rewind_image = tkinter.PhotoImage(file="icons/repeat.png")



#Buttons
play_button = customtkinter.CTkButton(master=root, image=play_image, text="", command = play_music, width =1)
play_button.place(relx=0.5,rely=0.7,anchor=tkinter.CENTER)

pause_button = customtkinter.CTkButton(master=root, image=pause_image, text="", command = pause_music, width = 1)
pause_button.place(relx=0.6,rely=0.7,anchor=tkinter.CENTER)

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


root.mainloop()