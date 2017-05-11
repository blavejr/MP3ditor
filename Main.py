from mutagen.easyid3 import EasyID3
from mutagen.easymp4 import EasyMP4
import re
import os
from time import sleep
music_dir = "I:\\Music"


def init():
    '''
    This function makes sure everything is in order before the actual songs are edited
    or something like that
    '''

    artists = os.listdir(music_dir)
    print "Here is a list of the library sir"

    num = 0
    for i in artists:
        print str(num) + " : " + i
        num += 1

    ch = input("Pick an artists")
    #ch = 2
    print "\n"
    print "You have chosen " + artists[ch]
    ans = raw_input("Would you like to change the artists name? Y/N")
    # ans = "no"

    if ans.lower() == 'y':
        new_artist_name = raw_input("Enter the new name: ")
        # changes the folder name, which is  what is used as the artist name
        os.renames(music_dir+"\\"+artists[ch], music_dir+"\\"+new_artist_name)
        # list of the albums in the artists folder with the new name
        albums = os.listdir(music_dir+"\\"+new_artist_name)
        for i in albums:
            print i

    elif ans.lower() == 'n':
        print "Using " + artists[ch] + " as artist name"
        # list of albums in the folder using the old name. if name not changed
        albums = os.listdir(music_dir+"\\"+artists[ch])
        num = 0
        for i in albums:
            print str(num) + " : "+i
            num += 1
        album_to_ed = input("Which album would you like to edit?: ")
        # list album contents
        # make necessary changes, name the album and artists same as the folder
        # I will add manual editing later
        album_dir = music_dir+"\\"+artists[ch] + "\\" + albums[album_to_ed]
        album_cont = os.listdir(music_dir+"\\"+artists[ch] + "\\" + albums[album_to_ed])

        # Change the extensions of the files
        ext_ans = raw_input("Would you like to change the extension of the songs?(Y/N): ")
        if ext_ans.lower() == "y":
            ext = raw_input("What would you like to change the extensions to?: ")
            for i in album_cont:
                os.renames(album_dir+"\\"+i, album_dir+"\\"+i[:-3]+ext)
                sleep(.5)
            print "Extension change process complete."

        for i in album_cont:
            try:
                audio = EasyID3(music_dir+"\\"+artists[ch] + "\\" + albums[album_to_ed]+"\\"+i)
                audio['artist'] = artists[ch]
                audio['album'] = albums[album_to_ed]
                audio.save()
                # print audio['album']
                # print audio['artist']
            except Exception, e:
                # print e
                # print "Not an mp3 file"
                try:
                    audio = EasyMP4(music_dir+"\\"+artists[ch] + "\\" + albums[album_to_ed]+"\\"+i)
                    audio['artist'] = artists[ch]
                    audio['album'] = albums[album_to_ed]
                    audio.save()
                    print audio['album']
                    print audio['artist']
                except Exception, e:
                    # print e
                    pass



        # If the artist name is in the title
        # Fix song title
        Q = raw_input("Would you like to edit the title?(Y/N): ")
        if Q.lower() == "y":
            try:
                art_name = raw_input("Enter phrase to be removed from title")
                other = raw_input("Enter char to be replaced with space")
                for i in album_cont:
                    audio = EasyID3(music_dir+"\\"+artists[ch] + "\\" + albums[album_to_ed]+"\\"+i)
                    a = str(i)
                    r = re.findall(art_name, a)
                    print r
                    if r:
                        print "found Reece"
                        a = a.replace(r[0], "")
                        a = a.replace(other, " ")
                        if a[0] == " ":
                            a = a[1:]
                            print a
                        else:
                            print a
                    else:
                        print "No Reece found"

                    audio['title'] = a
                    audio.save()
                    print audio['title']
            except Exception, z:
                # print z
                try:
                    art_name = raw_input("Enter phrase to be removed from title")
                    other = raw_input("Enter char to be replaced with space")
                    for i in album_cont:
                        audio = EasyMP4(music_dir+"\\"+artists[ch] + "\\" + albums[album_to_ed]+"\\"+i)
                        a = str(i)
                        r = re.findall(art_name, a)
                        print r
                        if r and art_name != "" and other != "":
                            print "found " + art_name
                            a = a.replace(r[0], "")
                            a = a.replace(other, " ")
                            if a[0] == " ":
                                a = a[1:]
                                # print a
                            else:
                                pass
                                # print a
                        else:
                            audio['title'] = a[3:-4]
                            print audio['title']
                            audio['tracknumber'] = a[:2]
                            audio.save()
                            print audio['tracknumber']
                except Exception, z:
                    print z
                    pass
        else:
            print "Titles will not be edited"

        # add song track numbers
        # Track numbers will be added manually
        Q2 = raw_input("Would you like to edit the track numbers?(Y/N): ")
        if Q2.lower() == 'y':
            for i in album_cont:
                audio = EasyID3(music_dir+"\\"+artists[ch] + "\\" + albums[album_to_ed]+"\\"+i)
                trck = input("What is the track number for " + str(audio['title']) + ": ")
                audio['tracknumber'] = str(trck)
                audio.save()

                print audio['title'], audio['tracknumber']
        else:
            print "track numbers will not be edited."

init()