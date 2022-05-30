import tkinter as tk
from tkinter.ttk import *
from PIL import Image
from io import BytesIO
from io import StringIO

# creating main tkinter window/toplevel
master = tk.Tk()

import urllib.request

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"


from bs4 import BeautifulSoup

import requests
import sqlite3
html_text= requests.get('https://www.ticketbooth.com.au/').text
conn = sqlite3.connect("events.db")
cur = conn.cursor()
soup = BeautifulSoup(html_text, 'lxml')
cont = soup.find("div", class_="container-fluid")
def trending():
    content = soup.find("main",class_="home-main")
    events = content.find_all('div',class_="card")
    trending_titles = []
    trending_locations =[]
    trending_dates = []
    trending_images=[]
    for e in events:
        trending_titles.append(e.find("h5",class_="card-text").text)
        trending_locations.append(e.find_all("h4")[0].text)
        trending_dates.append(e.find_all("h4")[1].text)
        trending_images.append(str(e.find("div",class_="card-header")).split("(")[1][:-10])

    
    return trending_images,trending_dates,trending_titles,trending_locations   
    
def music():
    
    events = cont.find_all('div',class_="event-listings")[1]
    
    music_titles = []
    music_locations =[]
    music_dates = []
    music_images=[]
    
    content_area = events.find_all("div",class_="col-md-3 mb-3 content-area")
    for c in content_area:
        data = c.find("a")
        music_titles.append(data.find("h5",class_="card-text").text)
        music_locations.append(data.find("p").text)
        music_dates.append(data.find("em").text)
        music_images.append(str(data.find("div",class_="card-header")).split("(")[1].split(")")[0])
    return music_images,music_dates,music_titles,music_locations

def culture():
    
    events = cont.find_all('div',class_="event-listings")[2]
    
    culture_titles = []
    culture_locations =[]
    culture_dates = []
    culture_images=[]
    
    content_area = events.find_all("div",class_="col-md-3 mb-3 content-area")
    for c in content_area:
        data = c.find("a")
        culture_titles.append(data.find("h5",class_="card-text").text)
        culture_locations.append(data.find("p").text)
        culture_dates.append(data.find("em").text)
        culture_images.append(str(data.find("div",class_="card-header")).split("(")[1].split(")")[0])
    return culture_images,culture_dates,culture_titles,culture_locations  
def sports():
    
    events = cont.find_all('div',class_="event-listings")[3]
    
    sports_titles = []
    sports_locations =[]
    sports_dates = []
    sports_images=[]
    
    content_area = events.find_all("div",class_="col-md-3 mb-3 content-area")
    for c in content_area:
        data = c.find("a")
        sports_titles.append(data.find("h5",class_="card-text").text)
        sports_locations.append(data.find("p").text)
        sports_dates.append(data.find("em").text)
        sports_images.append(str(data.find("div",class_="card-header")).split("(")[1].split(")")[0])
    return sports_images,sports_dates,sports_titles,sports_locations
# Inserting the booked events into the database
def ticket_list(email):
    top = tk.Toplevel()
    top.geometry("800x800")
    cur.execute("SELECT title,venue,date,dt FROM events WHERE email =?",(email,))
    row = cur.fetchall()
    # define columns
    columns = ('Title', 'Venue', 'Date', 'Booked')
    tree = Treeview(top, columns=columns, show='headings')

    # define headings
    tree.heading('Title', text='Events Title')
    tree.heading('Venue', text='Event Venue')
    tree.heading('Date', text='Event Date')
    tree.heading('Booked', text='Date Booked/Bought Ticket')
                         
    
    for event in row:
        tree.insert('', tk.END, values=event)
    tree.grid(row=0, column=0, sticky='nsew')

    # add a scrollbar
    scrollbar = Scrollbar(top, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')
    top.mainloop()

def ticket(title,venue,date,email):
    top = tk.Toplevel()
    top.geometry("800x800")
    cur.execute("INSERT INTO events(title,venue,date,email) VALUES (?, ?, ?, ?)",
                         (title, venue, date, email))
    conn.commit()
    conn.close()
    top.mainloop()

def filter_by_email():
    top = tk.Toplevel()
    top.geometry("800x800")
    
    #Email label and text entry box
    emailLabel = Label(top, text="Enter Your Email").place(x=40,y=50)
    email = tk.StringVar()
    emailEntry = Entry(top, textvariable=email).place(x=230,y=50) 
    loginButton = tk.Button(top, text="Filter By Email", bg="green",fg="white",width=20,height=2, command=lambda:ticket_list(email.get())).place(x=70,y=170)  
    top.mainloop()


# Getting email to help filtering the list of events
def get_email(title,venue,date):
    top = tk.Toplevel()
    top.geometry("800x800")
    
    #Email label and text entry box
    emailLabel = Label(top, text="Enter Your Email").place(x=40,y=50)
    email = tk.StringVar()
    emailEntry = Entry(top, textvariable=email).place(x=130,y=50) 
    loginButton = tk.Button(top, text="Book This Event", bg="green",fg="white",width=20,height=2, command=lambda:ticket(title,venue,date,email.get())).place(x=70,y=170)  
    top.mainloop()

# Array variables to hold the events from the site
trending_images,trending_dates,trending_titles,trending_locations = trending()
music_images,music_dates,music_titles,music_locations = music()
culture_images,culture_dates,culture_titles,culture_locations = culture()
sports_images,sports_dates,sports_titles,sports_locations = sports()

master.geometry("1400x800")
master.title("Events")
master.configure(bg="purple")
master.resizable(False,False)



wmain = tk.Frame(master,bg="purple")

wmain.pack(fill="both", expand="yes")
wTrending = tk.LabelFrame(master,text="Trending Events")
wTrending.grid_columnconfigure(0, weight=3, uniform="fred")
wTrending.pack(fill="both", expand="yes")
wCategories = tk.LabelFrame(master,text="Categories Events")
wCategories.pack(fill="both", expand="yes")



imags=[]
for x in range(len(trending_titles)):
    title = tk.StringVar()
    place=tk.StringVar()
    date=tk.StringVar()
    
    place.set(trending_locations[x])
    date.set(trending_dates[x])
    title.set(trending_titles[x])
    
    frame = tk.Frame(wTrending,width=300, height=300, bg="bisque")
    wTrending.grid_columnconfigure(2, minsize=300) 

    import urllib.request
    from PIL import Image,ImageTk
    image=trending_images[x]
    opener = AppURLopener()
    response = opener.open(
    image)
    
    img = Image.open(response)
    imag = ImageTk.PhotoImage(img)
    imags.append(imag)

    
    canvas = tk.Canvas(frame, width = 300, height = 250, bg="skyblue")      
         
        
      
    if x<2:
        
        frame.grid(column=x, row=0, sticky=tk.W,columnspan=3, padx=10, pady=10,ipadx=20, ipady=20)
       
        canvas.create_image(0,0, anchor=tk.W, image=imags[x])
        
         
        canvas.create_text( 140, 160, text=title.get())
        canvas.create_text( 140, 185, text=place.get())
        canvas.create_text( 140, 210, text=date.get())
        
        canvas.pack(fill = "both", expand = True)
        button3 = tk.Button( frame,bg="blue", text = "Booking ticket",width=20,height=2,command=lambda:get_email(trending_titles[x],trending_locations[x],trending_dates[x]))
        
        button1_canvas = canvas.create_window( 20, 70, 
                                       anchor = "sw",
                                       window = button3)
  
        
    if x>=2 and x<4:
        
        frame.grid(column=x-2, row=2, sticky=tk.W, padx=10, pady=10,ipadx=20, ipady=20)
        canvas.create_image(0,0, anchor=tk.W, image=imags[x])
        
         
        canvas.create_text( 140, 160, text=title.get())
        canvas.create_text( 140, 185, text=place.get())
        canvas.create_text( 140, 210, text=date.get())
        
        canvas.pack(fill = "both", expand = True)
        button3 = tk.Button( frame,bg="blue", text = "Booking ticket",width=20,height=2,command=lambda:get_email(trending_titles[x],trending_locations[x],trending_dates[x]))
        
        button1_canvas = canvas.create_window( 20, 70, 
                                       anchor = "sw",
                                       window = button3)



def musicTop():
    top = tk.Toplevel(master)
    top.geometry("1000x800")
    wMusic = tk.LabelFrame(top,text="Music Events")
    wMusic.pack(fill="both", expand="yes")
    imgmusic=[]

    for x in range(len(music_titles)):
        title = tk.StringVar()
        place=tk.StringVar()
        date=tk.StringVar()
        place.set(music_locations[x])
        date.set(music_dates[x])
        title.set(music_titles[x])
        frame = tk.Frame(wMusic,width=200, height=150, bg="bisque")
        image=music_images[x]
        opener = AppURLopener()
        response = opener.open(
        image)
        print(music_images[x])
        img = Image.open(response)
        imag = ImageTk.PhotoImage(img)
        imgmusic.append(imag)
        canvasMusic = tk.Canvas(frame, width = 300, height = 250, bg="skyblue")
        
        if x<2:
        
            frame.grid(column=x, row=0, sticky=tk.W,columnspan=3, padx=10, pady=10,ipadx=20, ipady=20)
        
            canvasMusic.create_image(0,0, anchor=tk.W, image=imgmusic[x])
            
            
            canvasMusic.create_text( 140, 160, text=title.get())
            canvasMusic.create_text( 140, 185, text=place.get())
            canvasMusic.create_text( 140, 210, text=date.get())
            
            canvasMusic.pack(fill = "both", expand = True)
            button3 = tk.Button( frame,bg="blue", text = "Booking ticket",width=20,height=2,command=lambda:get_email(music_titles[x],music_locations[x],music_dates[x]))
            
            button1_canvas = canvasMusic.create_window( 20, 250, 
                                        anchor = "sw",
                                        window = button3)
  
        
        if x>=2 and x<4:
            
            
            frame.grid(column=x-2, row=2, sticky=tk.W, padx=10, pady=10,ipadx=20, ipady=20)
            canvasMusic.create_image(0,0, anchor=tk.W, image=imgmusic[x])
            
            
            canvasMusic.create_text( 140, 160, text=title.get())
            canvasMusic.create_text( 140, 185, text=place.get())
            canvasMusic.create_text( 140, 210, text=date.get())
            
            canvasMusic.pack(fill = "both", expand = True)
            button3 = tk.Button( frame,bg="blue", text = "Booking ticket",width=20,height=2,command=lambda:get_email(music_titles[x],music_locations[x],music_dates[x]))
            
            button1_canvas = canvasMusic.create_window( 20, 250, 
                                        anchor = "sw",
                                        window = button3)
            
    top.mainloop()

def cultureTop():
    top = tk.Toplevel(master)
    top.geometry("1000x800")
    wCulture = tk.LabelFrame(top,text="Culture Events")
    wCulture.pack(fill="both", expand="yes")
    imgculture=[]

    for x in range(len(culture_titles)):
        title = tk.StringVar()
        place=tk.StringVar()
        date=tk.StringVar()
        place.set(culture_locations[x])
        date.set(culture_dates[x])
        title.set(culture_titles[x])
        frame = tk.Frame(wCulture,width=200, height=150, bg="bisque")
        
        image=culture_images[x]
        opener = AppURLopener()
        response = opener.open(
        image)
        print(culture_images[x])
        img = Image.open(response)
        imag = ImageTk.PhotoImage(img)
        imgculture.append(imag)
        canvasCulture = tk.Canvas(frame, width = 300, height = 250, bg="skyblue")
        
        if x<2:
        
            frame.grid(column=x, row=0, sticky=tk.W,columnspan=3, padx=10, pady=10,ipadx=20, ipady=20)
        
            canvasCulture.create_image(0,0, anchor=tk.W, image=imgculture[x])
            
            
            canvasCulture.create_text( 140, 160, text=title.get())
            canvasCulture.create_text( 140, 185, text=place.get())
            canvasCulture.create_text( 140, 210, text=date.get())
            
            canvasCulture.pack(fill = "both", expand = True)
            button3 = tk.Button( frame,bg="blue", text = "Booking ticket",width=20,height=2,command=lambda:get_email(culture_titles[x],culture_locations[x],culture_dates[x]))
            
            button1_canvas = canvasCulture.create_window( 20, 250, 
                                        anchor = "sw",
                                        window = button3)
  
        
        if x>=2 and x<4:
            
            
            frame.grid(column=x-2, row=2, sticky=tk.W, padx=10, pady=10,ipadx=20, ipady=20)
            canvasCulture.create_image(0,0, anchor=tk.W, image=imgculture[x])
            
            
            canvasCulture.create_text( 140, 160, text=title.get())
            canvasCulture.create_text( 140, 185, text=place.get())
            canvasCulture.create_text( 140, 210, text=date.get())
            
            canvasCulture.pack(fill = "both", expand = True)
            button3 = tk.Button( frame,bg="blue", text = "Booking ticket",width=20,height=2,command=lambda:get_email(culture_titles[x],culture_locations[x],culture_dates[x]))
            
            button1_canvas = canvasCulture.create_window( 20, 250, 
                                        anchor = "sw",
                                        window = button3)
        
    top.mainloop()

def sportsTop():
    top = tk.Toplevel(master)
    top.geometry("1000x800")
    wSports = tk.LabelFrame(top,text="Sports Events")
    wSports.pack(fill="both", expand="yes")
    imgsports=[]
    for x in range(len(sports_titles)):
        title = tk.StringVar()
        place=tk.StringVar()
        date=tk.StringVar()
        place.set(sports_locations[x-1])
        date.set(sports_dates[x-1])
        title.set(sports_titles[x-1])
        frame = tk.Frame(wSports,width=400, height=200, bg="bisque")
        
        
        image=culture_images[x]
        opener = AppURLopener()
        response = opener.open(
        image)
        print(sports_images[x])
        img = Image.open(response)
        imag = ImageTk.PhotoImage(img)
        imgsports.append(imag)
        canvasSports = tk.Canvas(frame, width = 300, height = 250, bg="skyblue")
        
        if x<2:
        
            frame.grid(column=x, row=0, sticky=tk.W,columnspan=3, padx=10, pady=10,ipadx=20, ipady=20)
        
            canvasSports.create_image(0,0, anchor=tk.W, image=imgsports[x])
            
            
            canvasSports.create_text( 140, 160, text=title.get())
            canvasSports.create_text( 140, 185, text=place.get())
            canvasSports.create_text( 140, 210, text=date.get())
            
            canvasSports.pack(fill = "both", expand = True)
            button3 = tk.Button( frame,bg="blue", text = "Booking ticket",width=20,height=2,command=lambda:get_email(sports_titles[x],sports_locations[x],sports_dates[x]))
            
            button1_canvas = canvasSports.create_window( 20, 250, 
                                        anchor = "sw",
                                        window = button3)
  
        
        if x>=2 and x<4:
            
            
            frame.grid(column=x-2, row=2, sticky=tk.W, padx=10, pady=10,ipadx=20, ipady=20)
            canvasSports.create_image(0,0, anchor=tk.W, image=imgsports[x])
            
            
            canvasSports.create_text( 140, 160, text=title.get())
            canvasSports.create_text( 140, 185, text=place.get())
            canvasSports.create_text( 140, 210, text=date.get())
            
            canvasSports.pack(fill = "both", expand = True)
            button3 = tk.Button( frame,bg="blue", text = "Booking ticket",width=20,height=2,command=lambda:get_email(sports_titles[x],sports_locations[x],sports_dates[x]))
            
            button1_canvas = canvasSports.create_window( 20, 250, 
                                        anchor = "sw",
                                        window = button3)
        
        
    top.mainloop()
 



# Tickets bookings and listing of booked events
title = tk.Label(wmain,text="Welcome to our Events",bg="purple",fg="white",font=("Arial",15,'bold'))

title.place(x=0,y=10)
btnM = tk.Button(wmain,width=40,height=2,text = "Music Events",bg="blue", command = musicTop)  
  
btnM.place(x=250,y=5)
btnC = tk.Button(wmain,width=40,height=2, text = "Culture and Heritage Events",bg="blue", command = cultureTop)  
  
btnC.place(x=550,y=5)
btnS = tk.Button(wmain,width=40,height=2, text = "Sports Events",bg="blue", command = sportsTop)  
  
btnS.place(x=850,y=5)
btnS = tk.Button(wmain,width=20,height=2, text = "Tickets",bg="blue", command = filter_by_email)  
  
btnS.place(x=1200,y=5)
    








master.mainloop()
