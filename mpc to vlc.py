'''
if we want vlc to mpc-hc
from xml.etree.ElementTree import ElementTree
import sys

xmldoc = ElementTree()
try:
  xmldoc.parse(sys.argv[1])
except IndexError:
  sys.exit("you must pass the playlist file as a command line argument")
except:
  sys.exit("that file probably isn't a .xspf playlist file...")

root = xmldoc.getroot()
tracklist = root[1]

total = 0

for track in tracklist:
  for element in track:
    if element.tag.split('}')[1] == 'duration':
      total += int(element.text)
'''

from Tkinter import *
import tkMessageBox, tkFileDialog

class PlaylistConvert:
    mpcPlaylist = ''

    def __init__(self):
        self.createWindow()
        self.createButtons()
        
    def createWindow(self):
        self.root = Tk()
        self.root.config(cursor = 'plus')
        self.root.option_add('*Font', 'Courier 16')
        self.root.option_add('*Background', 'grey30')
        self.root.configure(bg = 'grey30')

        w, h = 550, 200
        x = (self.root.winfo_screenwidth() / 2) - (w / 2)
        y = (self.root.winfo_screenheight() / 2) - (h / 2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def createButtons(self):
        getMpcBtn = Button(self.root, width = 20, fg = 'orange', text = 'Choose MPC playlist', anchor = CENTER, command = self.getMpcFile)
        getMpcBtn.place(x = 95, y = 50)

        toVlcBtn = Button(self.root, width = 20, fg = 'orange', text = 'Convert to VLC', anchor = CENTER, command = self.toVlc)
        toVlcBtn.place(x = 95, y = 100)
        
    def getMpcFile(self):
        PlaylistConvert.mpcPlaylist = tkFileDialog.askopenfilename(title = 'Select MPC-HC Playlist',
                                                                   filetypes = [("Mp3 Files", "*.mpcpl")])

        if PlaylistConvert.mpcPlaylist != '':
            self.gotBtn = Label(self.root, width = 10, fg = 'light green', text = 'Got it', anchor = 'w')
            self.gotBtn.place(x = 370, y = 55)

    def getLocations(self):
        count = 1
        locations = []
        
        with open(PlaylistConvert.mpcPlaylist) as mpc:
            for line in mpc:
                if count % 2 != 0:
                    locations.append(line.strip().split(',')[-1])
                count += 1

        return locations[1:]

    def clean(self, loc):
        subs = {'!': '%21', '#': '%23', '"': '%22',
                '%': '%25', '$': '%24', "'": '%27',
                '&': '%26', ')': '%29', '(': '%28',
                '+': '%2B', '*': '%2A', '-': '%2D',
                ',': '%2C', '/': '%2F', '.': '%2E',
                ';': '%3B', ':': '%3A', '=': '%3D',
                '<': '%3C', '?': '%3F', '>': '%3E',
                '@': '%40', '[': '%5B', ']': '%5D',
                '\\': '%5C', '_': '%5F', '^': '%5E',
                '`': '%60', '{': '%7B', '}': '%7D',
                '|': '%7C', '~': '%7E', ' ': '%20'}

        for char in loc:
            if char in subs:
                loc = loc.replace(char, subs[char])
        return loc

    def writeLocations(self, locations):
        vlcName = PlaylistConvert.mpcPlaylist.split('/')[-1][:-6] + '.xspf'
        vlc = open(vlcName, 'w')

        vlc.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        vlc.write('<playlist xmlns="http://xspf.org/ns/0/" xmlns:vlc="http://www.videolan.org/vlc/playlist/ns/0/" version="1">\n')
        vlc.write('\t<title>Playlist</title>\n')
        vlc.write('\t<trackList>\n')

        count = 0
        for location in locations:
            vlc.write('\t\t<track>\n')
            vlc.write('\t\t\t<location>file:///%s</location>\n' % self.clean(location))
            vlc.write('\t\t\t<extension application="http://www.videolan.org/vlc/playlist/0">\n')
            vlc.write('\t\t\t\t<vlc:id>%d</vlc:id>\n' % count)
            vlc.write('\t\t\t</extension>\n\t\t</track>\n')
            count += 1

        vlc.write('\t</trackList>\n')
        vlc.write('\t<extension application="http://www.videolan.org/vlc/playlist/0">\n')

        count = 0
        for loc in locations:
            vlc.write('\t\t\t<vlc:item tid="%d"/>\n' % count)
            count += 1

        vlc.write('\t</extension>\n')
        vlc.write('</playlist>\n')

        self.doneBtn = Label(self.root, width = 10, fg = 'light green', text = 'Converted', anchor = 'w')
        self.doneBtn.place(x = 370, y = 105)

    def toVlc(self):
        if PlaylistConvert.mpcPlaylist != '':
            locations = self.getLocations()
            print locations
            self.writeLocations(locations)
                
        else:
            tkMessageBox.showinfo('Error', 'playlist not provided')

    def runGui(self):        
        self.root.title('MPC-HC to VLC')
        self.root.resizable(0, 0)
        self.root.mainloop()

if __name__ == "__main__":
    PlaylistConvert().runGui()
