import requests
import vlc
import tkinter as tk


def make_valid(filename):
    # Make a filename valid in different OSs
    f = filename.replace(':', '_')
    f = f.replace('/', '_')
    f = f.replace('<', '_')
    f = f.replace('>', '_')
    f = f.replace('\'', '_')
    f = f.replace('\\', '_')
    f = f.replace('|', '_')
    f = f.replace('?', '_')
    f = f.replace('*', '_')
    f = f.replace(' ', '_')
    return f




def createWindow():

  #play song given cid
  def playSong ():
   pullRequest = 'https://monster-siren.hypergryph.com/api/song/' + ent_cid.get()
   song = requests.get(pullRequest, headers={'Accept': 'application/json'}).json()['data']

   try:
     source = song['sourceUrl']
   except: 
     lbl_result["text"] = "Invalid CID"
     return

   p = vlc.MediaPlayer(source)
   p.play()

   lbl_result["text"] = "Now Playing: " + song['name']

#_____________________________________________________
  # declare the window
  window = tk.Tk()
  # set window title
  window.title("MS Download")
  # set window width and height
  # window.configure(width=500, height=300)
  # set window background color
  # window.configure(bg='lightgray')

  window.resizable(width=False, height=False)

  # main window
  frm_entry = tk.Frame(master=window)
  ent_cid = tk.Entry(master=frm_entry, width=10)
  lbl_cid = tk.Label(master=frm_entry, text="ENTER CID OF SONG")

  ent_cid.grid(row=0, column=0, sticky="e")
  lbl_cid.grid(row=0, column=1, sticky="w")

  # play song from cid in entry box
  btn_play = tk.Button(
    master=window,
    text="Play",
    command = playSong
  )
  lbl_result = tk.Label(master=window, text="Now Playing: Nothing!")

  # Set up the layout using the .grid() geometry manager
  frm_entry.grid(row=0, column=0, padx=10)
  btn_play.grid(row=0, column=1, pady=5, padx=10)
  lbl_result.grid(row=1, column=0, sticky="e")

  window.mainloop()

 
def main():
  
  createWindow()
  
main()

