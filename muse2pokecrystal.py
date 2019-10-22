#!/usr/bin/python3

from xml.etree.ElementTree import parse
import xml.etree.ElementTree as et
import configparser
import sys, getopt
from os.path import isfile as filehere

customheader = configparser.ConfigParser()
asmfile = None
# <part-list><score-part id=""><part-name>Name</partname></score-part></part-list>
# <part id=""><measure number="1"><notes /></measure></part>
def process_score(xmlfile, musicfile, conf, nonoise, manualtempo, tempo, song_title, provided_name):
    global asmfile
    asmfile = open(musicfile, "w")
    # (part id, part-name)
    parts_list = []

    ScoreTree = parse(xmlfile)
    xmlroot = ScoreTree.getroot()
    if provided_name is False:
        try:
            song_title = xmlroot.find('./work/work-title').text
        except AttributeError:
            print("\033[93mCould not guess song name. Using generic name.\033[0m")
    pointer_title = song_title.replace(':', '').replace(' ','')
    parts = xmlroot.find('part-list')
    for part in parts.findall('score-part'):
        parts_list.append((part.get('id'), part.find('part-name').text))
    try:
        write_parts(xmlroot, pointer_title, manualtempo, tempo, conf, parts_list, nonoise)
    except IndexError:
        print("\033[93mNo noise channel. Reprocessing without noise channel...")
        nonoise = True
        asmfile.seek(0)
        asmfile.truncate(0)
        write_parts(xmlroot, pointer_title, manualtempo, tempo, conf, parts_list, nonoise)

    # close
    asmfile.close()
    parity_check(musicfile, nonoise)
    print("\033[92m\033[1mConversion success!\033[0m")

def write_parts(xmlroot, pointer_title, manualtempo, tempo, conf, parts_list, nonoise):

    # the --noiseless parameter tells us whether we should ignore channel 4
    print("\033[93mAdding Header Info\033[0m")
    asmfile.write("Music_{}:\n".format(pointer_title))
    if nonoise:
        asmfile.write("\tmusicheader 3, 1, Music_{}_Ch1\n".format(pointer_title))
    else:
        asmfile.write("\tmusicheader 4, 1, Music_{}_Ch1\n".format(pointer_title))
    asmfile.write("\tmusicheader 1, 2, Music_{}_Ch2\n".format(pointer_title))
    asmfile.write("\tmusicheader 1, 3, Music_{}_Ch3\n".format(pointer_title))
    if not nonoise:
        asmfile.write("\tmusicheader 1, 4, Music_{}_Ch4\n".format(pointer_title))
    asmfile.write("\n\n")

    if conf is not "":
        customheader.read(conf)
    print("Converting Channel 1: \033[95m{}\033[0m".format(parts_list[0][1]))
    parse_channel1(xmlroot.find("./part[@id='{}']".format(parts_list[0][0])), pointer_title, manualtempo, tempo, conf)
    print("Converting Channel 2: \033[95m{}\033[0m".format(parts_list[1][1]))
    parse_channel2(xmlroot.find("./part[@id='{}']".format(parts_list[1][0])), pointer_title, conf)
    print("Converting Channel 3: \033[95m{}\033[0m".format(parts_list[2][1]))
    parse_channel3(xmlroot.find("./part[@id='{}']".format(parts_list[2][0])), pointer_title, conf)

    if not nonoise:
        print("Converting Channel 4: \033[95m{}\033[0m".format(parts_list[3][1]))
        parse_channel4(xmlroot.find("./part[@id='{}']".format(parts_list[3][0])), pointer_title, conf)\

# checks the length of each channel to prevent desyncing
def parity_check(musicfile, nonoise):
    curchannel = 0
    channelcntarray = [0, 0, 0, 0]
    asmread = open(musicfile, "r")
    filearray = asmread.readlines()
    for line in filearray:
        if "_Ch1_Loop" in line:
            curchannel = 1
        if "_Ch2_Loop" in line:
            curchannel = 2
        if "_Ch3_Loop" in line:
            curchannel = 3
        if "_Ch4_Loop" in line:
            curchannel = 4
        elif "note" in line and not "type" in line:
            channelcntarray[curchannel - 1] += int(line[9:])
    curchannel = 0
    if nonoise:
        for channelcnt in channelcntarray[:3]:
            if channelcnt != channelcntarray[0]:
                print("\n\033[91m\033[1mParity check failed!")
                print("Check that there is only one note per channel!\033[0m")
                for item in channelcntarray[:3]:
                    if channelcnt == item:
                        print("\033[91m\033[1m" + str(item) + "\033[0m")
                    else:
                        print("\033[93m" + str(item) + "\033[0m")
                sys.exit(1)
    else:
        for channelcnt in channelcntarray:
            if channelcnt != channelcntarray[0]:
                print("\n\033[91m\033[1mParity check failed!")
                print("Check that there is only one note per channel!\033[0m")
                for item in channelcntarray:
                    if channelcnt == item:
                        print("\033[91m\033[1m" + str(item) + "\033[0m")
                    else:
                        print("\033[93m" + str(item) + "\033[0m")
                sys.exit(1)
    print("\n\033[94mParity check succeeded!")

def note_process(pitch, channel):
    altered = pitch.find('alter')
    if channel is 4:
        step = pitch.find('display-step').text
    else:
        step = pitch.find('step').text
    if altered is not None: altered = altered.text
    else: altered = '0'
    nibble = '_'
    if int(altered) < 0:
        nibble = '#'
        step = chr(ord(step)-1)
    elif int(altered) > 0: nibble = '#'
    noted = "{}{}".format(step, nibble)
    return noted

def note_print(part, channel):
    # set to -1 so it's always overridden by the first iteration
    curroctave = -1
    tied = False
    step = ''
    dura = 0
    for measure in part.findall('measure'):
        for command in measure:
            if command.tag == "direction":
                try:
                    t = "\t{}\n".format(command.find('./direction-type/words').text)
                    if t != None: asmfile.write(t)
                except AttributeError:
                    continue
            if command.tag == "note":
                note = command
                t = ""
                if note.find('rest') is not None:
                    asmfile.write("\tnote __, {}\n".format(note.find('duration').text))
                elif note.find('pitch') is None and note.find('unpitched') is None:
                    print('None?')
                else:
                    if channel is not 4:
                        pitch = note.find('pitch')
                        if int(pitch.find('octave').text) is not curroctave:
                            curroctave = int(pitch.find('octave').text)
                            asmfile.write("\toctave {}\n".format(curroctave))
                    else:
                        pitch = note.find('unpitched')
                    if note.find('./tie[@type="start"]') is not None and note.find('./tie[@type="stop"]') is not None:
                        dura += int(note.find('duration').text)
                    elif note.find('./tie[@type="start"]') is not None:
                        tied = True
                        step = note_process(pitch, channel)
                        dura = int(note.find('duration').text)
                    elif note.find('./tie[@type="stop"]') is not None:
                        if int(note.find('duration').text) + dura > 16:
                            print("\n\033[91m\033[1mLength check failed!")
                            print("Note too long in Channel {}! Note length {}.\033[0m".format(channel, dura + int(note.find('duration').text)))
                            sys.exit(2)
                        if step == note_process(pitch, channel):
                            t = "\tnote {}, {}\n".format(note_process(pitch, channel),int(note.find('duration').text)+dura)
                        else:
                            asmfile.write("\tnote {}, {}\n".format(step,dura))
                            t = "\tnote {}, {}\n".format(note_process(pitch, channel),note.find('duration').text)
                        tied = False
                        step = ''
                        dura = 0
                    else:
                        t = "\tnote {}, {}\n".format(note_process(pitch, channel),note.find('duration').text)
                    if t != None: asmfile.write(t)

# tempo, volume, dutycycle, tone, vibrato, notetype, octave, stereopanning
# <tie type="start" (type="stop")/>
def parse_channel1(part, title, manualtempo, tempo, conf):
    global asmfile
    # write channel header including tempo
    asmfile.write("Music_{}_Ch1:\n".format(title))
    # Try to auto detect tempo, or get it from the user
    if not manualtempo:
        try:
        	asmfile.write("\ttempo {}\n".format(int(19200/int(part.find('./measure/direction/sound').get('tempo')))))
        except TypeError:
            print("\033[93mNo tempo was detected. Use try again with the --tempo parameter.")
            print("\n\033[91m\033[1mConversion incomplete!\033[0m")
            sys.exit(2)
    else:
        asmfile.write("\ttempo {}\n".format(int(19200/int(tempo))))
    if conf is "":
        asmfile.write("\tvolume $77\n")
        asmfile.write("\tnotetype $c, $95\n")
        asmfile.write("\tdutycycle $2\n")
    else:
        read_custom_header(1)
    asmfile.write("Music_{}_Ch1_Loop:\n".format(title))
    note_print(part, 1)
    asmfile.write("\tloopchannel 0, Music_{}_Ch1_Loop\n\n\n".format(title))

# dutycycle, tone, vibrato, notetype, octave, stereopanning
def parse_channel2(part, title, conf):
    global asmfile
    # write channel header
    asmfile.write("Music_{}_Ch2:\n".format(title))
    if conf is "":
        asmfile.write("\tnotetype $c, $95\n")
        asmfile.write("\tdutycycle $2\n")
    else:
        read_custom_header(2)
    asmfile.write("Music_{}_Ch2_Loop:\n".format(title))
    note_print(part, 2)
    asmfile.write("\tloopchannel 0, Music_{}_Ch2_Loop\n\n\n".format(title))

# stereopanning, vibrato, notetype, tone, octave
def parse_channel3(part, title, conf):
    global asmfile
    # write channel header
    asmfile.write("Music_{}_Ch3:\n".format(title))
    if conf is "":
        asmfile.write("\tnotetype $c, $15\n")
    else:
        read_custom_header(3)
    asmfile.write("Music_{}_Ch3_Loop:\n".format(title))
    note_print(part, 3)
    asmfile.write("\tloopchannel 0, Music_{}_Ch3_Loop\n\n\n".format(title))

# notetype, togglenoise
def parse_channel4(part, title, conf):
    global asmfile
    # write channel header
    asmfile.write("Music_{}_Ch4:\n".format(title))
    if conf is "":
        asmfile.write("\tnotetype $c\n")
        asmfile.write("\ttogglenoise 1\n")
    else:
        read_custom_header(4)
    asmfile.write("Music_{}_Ch4_Loop:\n".format(title))
    note_print(part, 4)
    asmfile.write("\tloopchannel 0, Music_{}_Ch4_Loop\n\n\n".format(title))

def read_custom_header(channel):
    chan = customheader['Channel{}'.format(channel)]
    if channel != 4:
        if channel == 1:
            asmfile.write("\tvolume {}\n".format(chan['volume']))
        asmfile.write("\tnotetype {}, {}\n".format(chan['notetype'], chan['intensity']))
        if channel != 3:
            asmfile.write("\tdutycycle {}\n".format(chan['dutycycle']))
        if chan['tone'] != "no":
            asmfile.write("\ttone {}\n".format(chan['tone']))
        if chan['vibrato'] != "no":
            asmfile.write("\tvibrato {}, {}\n".format(chan['vibrato_delay'], chan['vibrato_extent']))
    if channel == 4:
        asmfile.write("\tnotetype {}\n".format(chan['notetype']))
        asmfile.write("\ttogglenoise {}\n".format(chan['togglenoise']))
    if chan['stereopanning'] != "$ff":
        asmfile.write("\tstereopanning {}\n".format(chan['stereopanning']))

def main(argv):
    infile = ""
    outfile = ""
    configfile = ""
    speed = 120
    speedoverride = False
    songname = "Music Song"
    nameoverride = False
    noiseless = False
    forceoverwrite = False
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["score=","code=", "config=", "tempo=", "name=", "noiseless", "overwrite"])
    except getopt.GetoptError:
        print('muse2pokecrystal -i <musicxml> -o <music code>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('muse2pokecrystal -i <musicxml> -o <music code>')
            sys.exit()
        elif opt in ("-i", "--score"):
            infile = arg
        elif opt in ("-o", "--code"):
            outfile = arg
        elif opt in ("--config"):
            configfile = arg
        elif opt in ("--tempo"):
            speed = arg
            speedoverride = True
        elif opt in ("--name"):
            songname = arg
            nameoverride = True
        elif opt in ("--noiseless"):
            noiseless = True
        elif opt in ("--overwrite"):
            forceoverwrite = True
    if filehere(outfile) and forceoverwrite is False:
        confirm = input("{} already exists!\nDo you want to continue and overwrite? [Y/n]: ".format(outfile))
        if confirm in ["", 'y', 'Y']:
            process_score(infile, outfile, configfile, noiseless, speedoverride, speed, songname, nameoverride)
    else:
        process_score(infile, outfile, configfile, noiseless, speedoverride, speed, songname, nameoverride)

if __name__=="__main__":
    main(sys.argv[1:])
