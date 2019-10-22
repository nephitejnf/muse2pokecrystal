#!/usr/bin/python3

def optimize_callchannel(musicfilein):
    asmfilein = open(musicfilein, "r")
    asmfilearray = asmfilein.readlines()
    # This assumes the name of the song is in the first line of the file
    songname = asmfilearray[0][:-2]
    currentsearch = 0
    searchbeginindex = 0
    # Not inclusive of ending index. To get the "real" end index, this value must be subtracted by 1
    searchendindex = 5
    searcharray = [[]]
    searcharray[currentsearch] = asmfilearray[searchbeginindex:searchendindex]
    asmfilearraybackup = asmfilearray.copy()
    # Contains indexes where matches were found
    blockmatch = []
    for line in range(0, len(asmfilearray) - 1):
        for searchline in range(line, line + len(searcharray[currentsearch]) - 1):
            if not asmfilearray[searchline] == searcharray[currentsearch][searchline - line]:
                print(asmfilearray[searchline][:-1] + " does not match " + searcharray[currentsearch][searchline - line][:-1])
                break


if __name__=="__main__":
#    main(sys.argv[1:])
    optimize_callchannel("/home/carson/Documents/polishedcrystal-stake/audio/music/cherrygrovecity.asm")
