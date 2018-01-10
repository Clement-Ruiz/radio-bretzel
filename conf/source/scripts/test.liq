#!/usr/bin/liquidsoap

#log dir
set("log.file",false)
set("log.stdout", true)

myPlaylist = playlist("audio/playlist.m3u")

security = single("../fail.mp3")

radio = myPlaylist

output.harbor(%mp3 , security)
