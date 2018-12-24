"""
Name: Jawad Ahmed
Student number: 822654
Date started: June 1, 2018
Description: This program emulates running an MMS (Music Management System) and
can perform various actions typical of an MMS program/software.
Major milestones:
# June 1, 2018: Created main library and created library stats and listings 
modules.
# June 4, 2018: Created album info module.
# June 5, 2018: Created track search module.
# June 6, 2018: Created track info module.
# June 7, 2018: Created track play module.
# June 11, 2018: Started work on meta data update and playlist module.
# June 13, 2018: Completed meta data update and playlist module.
# June 14, 2018: Started work on extensions.
# June 22, 2018: Completed extensions.
# June 23, 2018: 'Polished' entire program.
"""

import gtunes # please comment out all print lines in the loadLibrary and validateTrack functions as it can get quite messy otherwise
import random

# Main  library stored as a list of lists
Lib = gtunes.loadLibrary()
playlists = []

# converts all track names and album names into lower case letters
for libTrack in Lib:
    libTrack[5] = libTrack[5].lower()
for libTrack in Lib:
    libTrack[2] = libTrack[2].lower()

# creates a list of unique artist names
albums = []    
for libTrack in Lib:
    if not(libTrack[2] in albums):
        albums.append(libTrack[2])

# creates a list of unique artist names
artists = []
for libTrack in Lib:
    if not(libTrack[1] in artists):
        artists.append(libTrack[1])

# creates a list of unique genre names
genres = []
for libTrack in Lib:
    if not(libTrack[4] in genres):
        genres.append(libTrack[4])

# creates a list of track names
tracks = []
#index = 0
for libTrack in Lib:
    """
    # This part was supposed to be used to differentiate between similarly
    # named tracks but ended up causing too many problems.
    
    if libTrack[5] in tracks:
        pos = tracks.index(libTrack[5])
        Lib[index][5] += ' by '
        Lib[index][5] += libTrack[2]
        Lib[pos][5] += ' by '
        Lib[pos][5] += Lib[pos][2]
    """
    tracks.append(libTrack[5])
    #index+=1

# this function finds the filename for a given track name and returns the 
# filename, function does not handle cases with incorrect arguments
def fileName(trackName):
    fileName = ''
    for libTrack in Lib:
        if trackName in libTrack:
            fileName = libTrack[0]
            return fileName

# this function calculates the track time, given a track name, and returns a 
# list with the time in two different formats: MM:SS format, #seconds format
def trackLength(trackName):
    metadata, songData = gtunes.loadTrack(fileName(trackName))
    trackLength = len(songData)/10 # convert song data into seconds
    trackLengthRem = trackLength % 60 # SS
    trackLength //= 60 # MM
    
    trackLength = [(str(int(trackLength)) + ':' + str(int(trackLengthRem))), len(songData)/10]
    return trackLength

# displays # of unique artists, albums, genres and tracks, longest and sortest
# tracks and the range of years 
# called when option is 1
def libStats():
    # calculates longest and shortest tracks and stores both name and 
    # time (in seconds) in two lists 
    trackLengths = [0, 10000000000]
    tracksLongShort = ['-', '-']
    for libTrack in Lib:
        if trackLength(libTrack[5])[1] > trackLengths[0]:
            trackLengths[0] = trackLength(libTrack[5])[1]
            tracksLongShort[0] = libTrack[5].capitalize()
        elif trackLength(libTrack[5])[1] < trackLengths[1]:
            trackLengths[1] = trackLength(libTrack[5])[1]
            tracksLongShort[1] = libTrack[5].capitalize()
    
    # stores the earliest and latest years in a list
    # (latest converted to a negative value at the end)
    yearRange = [0, 2100]
    for libTrack in Lib:
        if int(libTrack[3]) > yearRange[0]:
            yearRange[0] = int(libTrack[3])
        elif int(libTrack[3]) < yearRange[1]:
            yearRange[1] = int(libTrack[3])
    yearRange[1]*=-1
    
    
    print('Unique artists:', len(artists))
    print('Unique albums:', len(albums))
    print('Unique genres:', len(genres))
    print('Tracks:', len(Lib))
    print('Longest track:', tracksLongShort[0])
    print('Shortest track:', tracksLongShort[1])
    print('Year range:', sum(yearRange))

# displays unique artists, albums and genres
# called when option is 2
def listings():
    print('Artists:')
    for artistNames in artists:
        print('-', artistNames.capitalize())
    
    print('\nAlbums:')
    check = ''
    for albumNames in albums:
        if albumNames not in check:
            print('-', albumNames.capitalize())
            check+=albumNames
    
    print('\nGenres:')
    for genreNames in genres:
        print('-', genreNames.capitalize())

# displays information on a given album name
# info includes album, artist and genre names, release year and # of tracks
# and lists all tracks in ascending order
# called when option is 3
def albumInfo():
    albumName = input('Album name: ').lower()
    check = 0
    
    # creates a list of albums (the same album name is used for all tracks in the album)
    allAlbums = []
    for libTrack in Lib:
        allAlbums.append(libTrack[2])
    
    # counts how many tracks are in the given album(from user input)
    numTracks = 0
    for albumNames in allAlbums:
        if albumNames == albumName:
            numTracks += 1
    
    # displays album, artist and genre names, release year and # of tracks
    for libTrack in Lib:
        if libTrack[2] == albumName:
            check += 1
            print('Album:', libTrack[2].capitalize())
            print('Artist:', libTrack[1].capitalize())
            print('Year of release:', libTrack[3])
            print('Genre:', libTrack[4].capitalize())
            print('Tracks:', numTracks)
            break
    
    # sorts and prints all tracks in the given album
    trackNums = []
    for libTrack in Lib:
        if libTrack[2] == albumName:
            l = [int(libTrack[6]), ' - ', libTrack[5]]
            trackNums.append(l)
    trackNums.sort()
    for lineNum in trackNums:
        print(lineNum[0], lineNum[1], lineNum[2].capitalize())
    
    # if the album doesn't exist none of the above codes will run
    if check == 0:
        print('No such album exists!')

# searches for a substring in all tracknames. inputting nothing will list all
# tracks
# called when option is 4
def trackSearch():
    search = input('Search: ').lower()
    
    count = 0
    for track in tracks:
        if track.find(search) > -1:
            print('found:', track)
            count+=1
    
    if count == 0:
        print('No tracks found.')

# displays information on a given track
# info includes track name, # and length, album, artist and genre names, and 
# year of release
# called when option is 5
def trackInfo():
    trackName = input('Track name: ').lower()
    check = 0
    
    for libTrack in Lib:
        if libTrack[5] == trackName:
            check += 1
            print('Artist:', libTrack[1].capitalize())
            print('Album:', libTrack[2].capitalize())
            print('Year of release:', libTrack[3])
            print('Genre:', libTrack[4].capitalize())
            print('Track name:', libTrack[5])
            print('Track number:', libTrack[6])
            print('Track length:', trackLength(libTrack[5])[0])
            break
              
    if check == 0:
        print('No such track exists!')

# gives some suggestions based on previously played tracks' genre(does not give
# any suggestions if no tracks were played before)
# displays the given track's length in MM:SS format and plays the given track
# called when option is 6
def playTracks():
    Lib = gtunes.loadLibrary()
    print(interests)
    
    if len(interests) != 0:
        print('Some suggestions:\n')
        count = 0
        for libTrack in Lib:
            if libTrack[4] == random.choice(interests):
                print('-', libTrack[5])
                count+=1
            if count > 5:
                break
    
    trackToPlay = input('\nTrack: ').lower()
    while count == 0:
        for libTrack in Lib:
            if not(trackToPlay in libTrack[5].lower()):
                    trackToPlay = input('Invalid input! Please try again: ').lower()
            else:
                count+=1
    
    for libTrack in Lib:
        if libTrack[5].lower() == trackToPlay:
            interests.append(libTrack[4])
    
    playTrack = fileName(trackToPlay)
    
    if gtunes.validateTrack(playTrack):
        print('Track length:', trackLength(trackToPlay)[0])
        gtunes.playTrack(playTrack)

# updates meta data of a given track
# initially gives out a warning to the user as well as a tip, user can choose
# to call the trackInfo() function for reference
# asks user for the track name of the track they need to change/update and then
# creates a list consisting of all meta data and asks user to update one by one
# called when option is 7
def updateMetadata():
    # a warning and helpful tips given can call for the trackInfo() function
    warning = 0
    print('Warning! This action cannot be reversed.\nPlease look at current Track information before proceeding.')
    warning = input('\nDo you wish to continue or see track info? (enter yes, no or track info) \n').lower()
    while warning != 'yes' and warning != 'no' and warning != 'track info':
        warning = input('Invalid input! Please try again: ').lower()
    
    if warning == 'track info':
        trackInfo()
    
    if warning == 'yes':
        # updates track meta data
        trackNeedingUpdate = input('Enter track name to update: ').lower()
        while not(trackNeedingUpdate in tracks):
            trackNeedingUpdate = input('Track doesnt exist. Enter valid track name to update: ').lower()
        
        updateTrack = fileName(trackNeedingUpdate)
        
        print('New information:\n\n')
        
        metadataToUpdate = []
        
        metadataToUpdate.append(input('Artisit name: ').lower())
        metadataToUpdate.append(input('Album name: ').lower())
        metadataToUpdate.append(input('Year released: '))
        metadataToUpdate.append(input('Genre name: ').lower())
        metadataToUpdate.append(input('Track name: ').lower())
        metadataToUpdate.append(input('Track number: '))
                
        
        if gtunes.validateTrack(updateTrack):
            gtunes.writeNewMetadata(updateTrack, metadataToUpdate)

# manages playlists
# starts off with a choice to either save to a playlist, or to load a playlist
# if user decides to save, an option to search tracks is given
# if user decides to search, the function trackSearch() is called
# if the user decides against it, the user is asked for a playlist name and 
# track names (can be multiple) that the user wants to add 
# if playlist exists, tracks are added, if not then the playlist is created
# if user decides to load, user is asked to give the playlist name and then
# displays the length of the playlist and the tracks in the playlist
# called when option is 8
def managePlaylists():
    # save or load choice
    choice = input('Enter -save- to save to playlist/create playlist,\nEnter -load- to load playlists:\n').lower()
    while choice!='save' and choice!='load':
        choice = input('Invalid input! Please try again: ').lower()
    
    if choice == 'save':
        # option to search for tracks before continuing
        choice = input('Do you want to search for tracks before continuing? (enter yes or no)\n').lower()
        while 1:
            if choice != 'yes' and choice != 'no':
                choice = input('Invalid input! Please try again: ').lower()
            
            # calls for trackSearch() to search for tracks
            while choice == 'yes':
                trackSearch()
                choice = input('Do you want to search for more tracks before continuing? (enter yes or no)\n').lower()
            
            if choice == 'no':
                break
        
        fileName = input('Enter playlist name (without the .pl, case sensitive): ')+'.pl'
        playlist = input('Enter all track names you would like to add seperated with a comma:\n').lower().split(', ')
        
        # scanning for any tracks that do not exist and asking for replacement
        for playlistIndex in range(len(playlist)):
            while not(playlist[playlistIndex] in tracks):
                print('The track ', playlist[playlistIndex], 'does not exist in the library.')
                playlist[playlistIndex] = input('Please enter a valid track name: ').lower()
        
        # removes repeating tracks
        for trackInPlaylist in playlist:
            if playlist.count(trackInPlaylist)>1:
                for count in range(playlist.count(trackInPlaylist)-1):
                    playlist.remove(trackInPlaylist)
        
        # converts track names into their respective filenames
        for libTrack in Lib:
            for playlistIndex in range(len(playlist)):
                if playlist[playlistIndex] == libTrack[5]:
                    playlist[playlistIndex] = libTrack[0]
        
        # saves playlist
        gtunes.savePlaylist(fileName, playlist)
        
    if choice == 'load':
        playlist = input('Playlist name: ')+'.pl'
        while not(gtunes.validatePlaylist(playlist)):
            playlist = input('This playlist does not exist! \nPlease enter an existing playlist or enter nothing to cancel: ')+'.pl'
            
            if playlist == '.pl':
                break
        
        if playlist != '.pl':
            playlist = gtunes.loadPlaylist(playlist)
        
        # converts filename into track name
        for libTrack in Lib:
            for playlistIndex in range(len(playlist)):
                if playlist[playlistIndex] == libTrack[0]:
                    playlist[playlistIndex] = libTrack[5]
        
        # prints all track names onto screen
        print('This playlist contains', len(playlist), 'track(s):')
        for track in playlist:
            print('\n - ', track)

# the main menu that calls all other functions and refreshes information 
# between each call
interests = []
def menu():

    while 1:
        # these small pieces of codes are the same as the ones in the beginning
        Lib = gtunes.loadLibrary()
        
        # converts all track names and album names into lower case letters
        for libTrack in Lib:
            libTrack[5] = libTrack[5].lower()
        for libTrack in Lib:
            libTrack[2] = libTrack[2].lower()
        
        # creates a list of unique artist names
        albums = []    
        for libTrack in Lib:
            if not(libTrack[2] in albums):
                albums.append(libTrack[2])
        
        # creates a list of unique artist names
        artists = []
        for libTrack in Lib:
            if not(libTrack[1] in artists):
                artists.append(libTrack[1])
        
        # creates a list of unique genre names
        genres = []
        for libTrack in Lib:
            if not(libTrack[4] in genres):
                genres.append(libTrack[4])
        
        # creates a list of track names
        tracks = []
        #index = 0
        for libTrack in Lib:
            """
            # This part was supposed to be used to differentiate between similarly
            # named tracks but ended up causing too many problems.
            
            if libTrack[5] in tracks:
                pos = tracks.index(libTrack[5])
                Lib[index][5] += ' by '
                Lib[index][5] += libTrack[2]
                Lib[pos][5] += ' by '
                Lib[pos][5] += Lib[pos][2]
            """
            tracks.append(libTrack[5])
            #index+=1
                
        print('_'*50)
        option = input(
                        '\n(1) Library Stats'
                        '\n(2) Listings'
                        '\n(3) Album Information'
                        '\n(4) Search For Tracks'
                        '\n(5) Track Information'
                        '\n(6) Play a Track'
                        '\n(7) Edit Track Information'
                        '\n(8) Manage Playlists'
                        '\n(9) Quit\n'
                        )
        while 1:
            if option.isnumeric():
                if int(option) > 0 and int(option) < 10:
                    break
                else:
                    option = input('Invalid input! Please try again!\n')
            else:
                option = input('Invalid input! Please try again!\n')
        option = int(option)
        print()
        
        if option == 1:
            libStats()
        if option == 2:
            listings()
        if option == 3:
            albumInfo()
        if option == 4:
            trackSearch()        
        if option == 5:
            trackInfo()        
        if option == 6:
            playTracks()        
        if option == 7:
            updateMetadata()
        if option == 8:
            managePlaylists()
        if option == 9:
            print('Goodbye!')
            break

# the hardest and longest piece of code that starts the whole program! :P
menu()




