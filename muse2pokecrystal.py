#!/usr/bin/python3

from xml.etree.ElementTree import parse
import xml.etree.ElementTree as et
import sys, getopt

asmfile = None
# <part-list><score-part id=""><part-name>Name</partname></score-part></part-list>
# <part id=""><measure number="1"><notes /></measure></part>
def process_score(xmlfile, musicfile, nonoise):
    global asmfile
    asmfile = open(musicfile, "w")
    # (part id, part-name)
    parts_list = []

    ScoreTree = parse(xmlfile)
    xmlroot = ScoreTree.getroot()
    song_title = xmlroot.find('./work/work-title').text
    pointer_title = song_title.replace(':', '').replace(' ','')
    parts = xmlroot.find('part-list')
    for part in parts.findall('score-part'):
        parts_list.append((part.get('id'), part.find('part-name').text))

    # the --noiseless parameter tells us whether we should ignore channel 4
    print("adding Header info")
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

    print("Converting Channel 1: {}".format(parts_list[0][1]))
    parse_channel1(xmlroot.find("./part[@id='{}']".format(parts_list[0][0])), pointer_title)
    print("Converting Channel 2: {}".format(parts_list[1][1]))
    parse_channel2(xmlroot.find("./part[@id='{}']".format(parts_list[1][0])), pointer_title)
    print("Converting Channel 3: {}".format(parts_list[2][1]))
    parse_channel3(xmlroot.find("./part[@id='{}']".format(parts_list[2][0])), pointer_title)

    if not nonoise:
        try:
            print("Converting Channel 4: {}".format(parts_list[3][1]))
            parse_channel4(xmlroot.find("./part[@id='{}']".format(parts_list[3][0])), pointer_title)
        except IndexError:
            print("\033[93mNo noise channel. Try running with the --noiseless option.")
            print("\n\033[91m\033[1mConversion incomplete!")
            sys.exit(2)

    # close
    asmfile.close()
    print("\n\033[92m\033[1mConversion success!")


def noise_process(pitch):
    altered = pitch.find('alter')
    step = pitch.find('display-step').text
    if altered is not None: altered = altered.text
    else: altered = '0'
    nibble = '_'
    if int(altered) < 0:
        nibble = '#'
        step = chr(ord(step)-1)
    elif int(altered) > 0: nibble = '#'
    noted = "{}{}".format(step, nibble)
    return noted

def note_process(pitch):
    altered = pitch.find('alter')
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

# tempo, volume, dutycycle, tone, vibrato, notetype, octave, stereopanning
# <tie type="start" (type="stop")/>
def parse_channel1(part, title):
    global asmfile
    # parse channel 1 header stuff
    asmfile.write("Music_{}_Ch1:\n".format(title))
    asmfile.write("\ttempo {}\n".format(int(19200/int(part.find('./measure/direction/sound').get('tempo')))))
    asmfile.write("\tvolume $77\n")
    asmfile.write("\tnotetype $c, $95\n")
    asmfile.write("\tdutycycle $2\n")
    asmfile.write("Music_{}_Ch1_Loop:\n".format(title))
    curroctave = 4
    asmfile.write("\toctave {}\n".format(curroctave))
    tied = False
    step = ''
    dura = 0
    # redundant note parsing code, note very efficient when copypastad
    for measure in part.findall('measure'):
        for note in measure.findall('note'):
            t = ""
            if note.find('rest') is not None:
                asmfile.write("\tnote __, {}\n".format(note.find('duration').text))
            elif note.find('pitch') is None:
                print('None?')
            else:
                pitch = note.find('pitch')
                if int(pitch.find('octave').text) is not curroctave:
                    curroctave = int(pitch.find('octave').text)
                    asmfile.write("\toctave {}\n".format(curroctave))
                if note.find('./tie[@type="start"]') is not None and note.find('./tie[@type="stop"]') is not None:
                    dura += int(note.find('duration').text)
                elif note.find('./tie[@type="start"]') is not None:
                    tied = True
                    step = note_process(pitch)
                    dura = int(note.find('duration').text)
                elif note.find('./tie[@type="stop"]') is not None:
                    if step == note_process(pitch):
                        t = "\tnote {}, {}\n".format(note_process(pitch),int(note.find('duration').text)+dura)
                    else:
                        asmfile.write("\tnote {}, {}\n".format(step,dura))
                        t = "\tnote {}, {}\n".format(note_process(pitch),note.find('duration').text)
                    tied = False
                    step = ''
                    dura = 0
                else:
                    t = "\tnote {}, {}\n".format(note_process(pitch),note.find('duration').text)
                if t != None: asmfile.write(t)
    asmfile.write("\tloopchannel 0, Music_{}_Ch1_Loop\n\n\n".format(title))

# dutycycle, tone, vibrato, notetype, octave, stereopanning
def parse_channel2(part, title):
    global asmfile
    # default header stuff
    asmfile.write("Music_{}_Ch2:\n".format(title))
    asmfile.write("\tvolume $77\n")
    asmfile.write("\tnotetype $c, $95\n")
    asmfile.write("\tdutycycle $2\n")
    asmfile.write("Music_{}_Ch2_Loop:\n".format(title))
    curroctave = 4
    asmfile.write("\toctave {}\n".format(curroctave))
    tied = False
    step = ''
    dura = 0
    # redundant note parsing code, note very efficient when copypastad
    for measure in part.findall('measure'):
        for note in measure.findall('note'):
            t = ""
            if note.find('rest') is not None:
                asmfile.write("\tnote __, {}\n".format(note.find('duration').text))
            elif note.find('pitch') is None:
                print('None?')
            else:
                pitch = note.find('pitch')
                if int(pitch.find('octave').text) is not curroctave:
                    curroctave = int(pitch.find('octave').text)
                    asmfile.write("\toctave {}\n".format(curroctave))
                if note.find('./tie[@type="start"]') is not None and note.find('./tie[@type="stop"]') is not None:
                    dura += int(note.find('duration').text)
                elif note.find('./tie[@type="start"]') is not None:
                    tied = True
                    step = note_process(pitch)
                    dura = int(note.find('duration').text)
                elif note.find('./tie[@type="stop"]') is not None:
                    if step == note_process(pitch):
                        t = "\tnote {}, {}\n".format(note_process(pitch),int(note.find('duration').text)+dura)
                    else:
                        asmfile.write("\tnote {}, {}\n".format(step,dura))
                        t = "\tnote {}, {}\n".format(note_process(pitch),note.find('duration').text)
                    tied = False
                    step = ''
                    dura = 0
                else:
                    t = "\tnote {}, {}\n".format(note_process(pitch),note.find('duration').text)
                if t != None: asmfile.write(t)
    asmfile.write("\tloopchannel 0, Music_{}_Ch2_Loop\n\n\n".format(title))

# stereopanning, vibrato, notetype, tone, octave
def parse_channel3(part, title):
    global asmfile
    asmfile.write("Music_{}_Ch3:\n".format(title))
    asmfile.write("\tnotetype $c, $15\n")
    asmfile.write("Music_{}_Ch3_Loop:\n".format(title))
    # redundant note parsing code, note very efficient when copypastad
    curroctave = 4
    asmfile.write("\toctave {}\n".format(curroctave))
    tied = False
    step = ''
    dura = 0
    for measure in part.findall('measure'):
        for note in measure.findall('note'):
            t = ""
            if note.find('rest') is not None:
                asmfile.write("\tnote __, {}\n".format(note.find('duration').text))
            elif note.find('pitch') is None:
                print('None?')
            else:
                pitch = note.find('pitch')
                if int(pitch.find('octave').text) is not curroctave:
                    curroctave = int(pitch.find('octave').text)
                    asmfile.write("\toctave {}\n".format(curroctave))
                if note.find('./tie[@type="start"]') is not None and note.find('./tie[@type="stop"]') is not None:
                    dura += int(note.find('duration').text)
                elif note.find('./tie[@type="start"]') is not None:
                    tied = True
                    step = note_process(pitch)
                    dura = int(note.find('duration').text)
                elif note.find('./tie[@type="stop"]') is not None:
                    if step == note_process(pitch):
                        t = "\tnote {}, {}\n".format(note_process(pitch),int(note.find('duration').text)+dura)
                    else:
                        asmfile.write("\tnote {}, {}\n".format(step,dura))
                        t = "\tnote {}, {}\n".format(note_process(pitch),note.find('duration').text)
                    tied = False
                    step = ''
                    dura = 0
                else:
                    t = "\tnote {}, {}\n".format(note_process(pitch),note.find('duration').text)
                if t != None: asmfile.write(t)
    asmfile.write("\tloopchannel 0, Music_{}_Ch3_Loop\n\n\n".format(title))

# notetype, togglenoise
def parse_channel4(part, title):
    global asmfile
    asmfile.write("Music_{}_Ch4:\n".format(title))
    asmfile.write("\tnotetype $c\n")
    asmfile.write("\ttogglenoise 1\n")
    asmfile.write("Music_{}_Ch4_Loop:\n".format(title))
    # redundant note parsing code, note very efficient when copypastad
    for measure in part.findall('measure'):
        for note in measure.findall('note'):
            if note.find('rest') is not None:
                asmfile.write("\tnote __, {}\n".format(note.find('duration').text))
            elif note.find('pitch') is not None:
                pitch = note.find('pitch')
                t = "\tnote {}, {}\n".format(note_process(pitch),note.find('duration').text)
                asmfile.write(t)
            elif note.find('unpitched') is not None:
                pitch = note.find('unpitched')
                t = "\tnote {}, {}\n".format(noise_process(pitch),note.find('duration').text)
                asmfile.write(t)
    asmfile.write("\tloopchannel 0, Music_{}_Ch4_Loop\n\n\n".format(title))

def main(argv):
    infile = ""
    outfile = ""
    noiseless = False
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["score=","code=", "noiseless"])
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
        elif opt in (s"--noiseless"):
            noiseless = True
    process_score(infile, outfile, noiseless)

if __name__=="__main__":
    main(sys.argv[1:])
