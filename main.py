import requests
import os
import vlc
import tkinter as tk
from tqdm import tqdm


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

    if not(songGlobal["loaded"]): 
      lbl_result["text"] = "No Song Loaded"
      return
    
    if songGlobal["isPlaying"] & songGlobal["loaded"]:
      songGlobal["player"].pause()
      lbl_result["text"] = "Paused: " + songGlobal["songData"]['name']
      songGlobal["isPlaying"] = False
      btn_play["text"] = "Play"
    else:
      songGlobal["player"].play()
      lbl_result["text"] = "Now Playing: " + songGlobal["songData"]['name']
      songGlobal["isPlaying"] = True
      btn_play["text"] = "Pause"

#_____________________________________________________

  # loads song into player, sets data
  def loadSong ():

    pullRequest = 'https://monster-siren.hypergryph.com/api/song/' + ent_cid.get()
    song = requests.get(pullRequest, headers={'Accept': 'application/json'}).json()['data']

    try:
     source = song['sourceUrl']
    except: 
     lbl_result["text"] = "Invalid CID"
     return
    
    songGlobal['loaded'] = True
    lbl_result["text"] = "(" + song['name'] +") Loaded!"
    
    songGlobal["player"] = vlc.MediaPlayer(song['sourceUrl'])
    songGlobal["songData"]= song
    songGlobal["isPlaying"] = False
  
#_____________________________________________________

 #play song given cid
  def downloadSong ():

    if not(songGlobal["loaded"]): 
      lbl_result["text"] = "No Song Loaded"
      return
    
    source = requests.get(songGlobal['songData']['sourceUrl'], stream=True)
    filename = './MonsterSiren/' + '/' + make_valid(songGlobal['songData']['name'])

    if source.headers['content-type'] == 'audio/mpeg':
        filename += '.mp3'
    else:
        filename += '.wav'

    # Download song
    total = int(source.headers.get('content-length', 0))
    with open(filename, 'w+b') as f, tqdm(
        desc=songGlobal['songData']['name'],
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in source.iter_content(chunk_size = 1024):
            size = f.write(data)
            bar.update(size)

    lbl_result["text"] = "Downloaded (" +songGlobal['songData']['name']+ ") to [" + filename + "]"


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

  #variables
  songGlobal = {"player" : None, "songData" : [], "loaded" : False, "isPlaying": False}
  
  # play song from cid in entry box
  btn_play = tk.Button(
    master=window,
    text="Play",
    command = playSong
  )
  lbl_result = tk.Label(master=window, text="Now Playing: Nothing!")

  # load song into player
  btn_load = tk.Button(
    master=window,
    text="Load",
    command = loadSong
  )

  # download loaded song
  btn_download = tk.Button(
    master=window,
    text="Download",
    command = downloadSong
  )

  # Set up the layout using the .grid() geometry manager
  frm_entry.grid(row=0, column=0, padx=10)
  btn_play.grid(row=0, column=2, pady=5, padx=10)
  btn_load.grid(row=0, column=1, pady=5, padx=10)
  btn_download.grid(row=0, column=3, pady=5, padx=10)
  lbl_result.grid(row=1, columnspan=4, sticky="w", padx =5, pady=5)

  window.mainloop()

 
def main():
  directory = './MonsterSiren/'
  try:
        os.mkdir(directory)
  except:
        pass

  
  createWindow()
  
main()

