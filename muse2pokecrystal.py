#!/usr/bin/python3

#    muse2pokecrystal : a program to convert MusicXML to pokecrystal music code
#    Copyright (C) 2020  nephitejnf and hyperdriveguy
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#    Full plain text license https://www.gnu.org/licenses/agpl-3.0.txt


from xml.etree.ElementTree import parse
import configparser
import sys
import getopt
from os.path import isfile as filehere
from src import text

customheader = configparser.ConfigParser()
asmfile = None
TERM_TEXT = text.TerminalText(True)

# <part-list><score-part id=""><part-name>Name</partname></score-part></part-list>
# <part id=""><measure number="1"><notes /></measure></part>
def process_score(xmlfile, musicfile, conf, nonoise, manualtempo, tempo, song_title, provided_name, specialloop):
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
            print(TERM_TEXT.generic_name)
    global pointer_title
    pointer_title = song_title.replace(':', '').replace(' ','')
    parts = xmlroot.find('part-list')
    for part in parts.findall('score-part'):
        parts_list.append((part.get('id'), part.find('part-name').text))
    try:
        write_parts(xmlroot, pointer_title, manualtempo, tempo, conf, parts_list, nonoise, specialloop)
    except IndexError:
        print(TERM_TEXT.no_noise_channel)
        nonoise = True
        asmfile.seek(0)
        asmfile.truncate(0)
        write_parts(xmlroot, pointer_title, manualtempo, tempo, conf, parts_list, nonoise, specialloop)

    # close
    asmfile.close()
    parity_check(musicfile, nonoise)
    print(TERM_TEXT.conversion_success)

def write_parts(xmlroot, pointer_title, manualtempo, tempo, conf, parts_list, nonoise, specialloop):

    # the --noiseless parameter tells us whether we should ignore channel 4
    file_text = text.OutputText(pointer_title)
    print(TERM_TEXT.adding_header)
    asmfile.write(file_text.music_label())
    asmfile.write(file_text.music_header_1(nonoise))
    asmfile.write(file_text.music_header_234(2))
    asmfile.write(file_text.music_header_234(3))
    if not nonoise:
        asmfile.write(file_text.music_header_234(4))
    asmfile.write("\n\n")

    if conf != "":
        customheader.read(conf)
    print(TERM_TEXT.converting_channel(1, parts_list))
    parse_channel1(xmlroot.find("./part[@id='{}']".format(parts_list[0][0])), pointer_title, manualtempo, tempo, conf, specialloop)
    print(TERM_TEXT.converting_channel(2, parts_list))
    parse_channel2(xmlroot.find("./part[@id='{}']".format(parts_list[1][0])), pointer_title, conf, specialloop)
    print(TERM_TEXT.converting_channel(3, parts_list))
    parse_channel3(xmlroot.find("./part[@id='{}']".format(parts_list[2][0])), pointer_title, conf, specialloop)

    if not nonoise:
        print(TERM_TEXT.converting_channel(4, parts_list))
        parse_channel4(xmlroot.find("./part[@id='{}']".format(parts_list[3][0])), pointer_title, conf, specialloop)

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
        elif "note" in line and "type" not in line:
            channelcntarray[curchannel - 1] += int(line[9:])
    curchannel = 0
    if nonoise:
        for channelcnt in channelcntarray[:3]:
            if channelcnt != channelcntarray[0]:
                print(TERM_TEXT.parity_check_failed)
                for item in channelcntarray[:3]:
                    if channelcnt == item:
                        print("\033[91m\033[1m" + str(item) + "\033[0m")
                    else:
                        print("\033[93m" + str(item) + "\033[0m")
                sys.exit(1)
    else:
        for channelcnt in channelcntarray:
            if channelcnt != channelcntarray[0]:
                print(TERM_TEXT.parity_check_failed)
                for item in channelcntarray:
                    if channelcnt == item:
                        print("\033[91m\033[1m" + str(item) + "\033[0m")
                    else:
                        print("\033[93m" + str(item) + "\033[0m")
                sys.exit(1)
    print(TERM_TEXT.parity_check_succeeded)

def note_process(pitch, channel):
    bad_notes = {'E#': 'F_',
                 'B#': 'C_',
                 'Ab': 'G#',
                 'Gb': 'F#',
                 'Eb': 'D#',
                 'Db': 'C#',
                 'Bb': 'A#',
                 'Cb': 'B_'}
    altered = pitch.find('alter')
    if channel == 4:
        step = pitch.find('display-step').text
    else:
        step = pitch.find('step').text
    if altered is not None: altered = altered.text
    else: altered = '0'
    nibble = '_'
    if int(altered) < 0: nibble = 'b'
    elif int(altered) > 0: nibble = '#'
    noted = "{}{}".format(step, nibble)
    # fix the troublemaking notes
    if noted in bad_notes:
        noted = bad_notes[noted]

    return noted

def note_print(part, channel):
    # set to -1 so it's always overridden by the first iteration
    curroctave = -1
    tied = False
    step = ''
    dura = 0
    global priority_command_queue
    global async_command_queue
    priority_command_queue = []
    async_command_queue = []
    for measure in part.findall('measure'):
        for command in measure:
        	# read a command from the "Staff Text" element
            if command.tag == "direction":
                try:
                    command_text = command.find('./direction-type/words').text
                    """
                    The "@" is used to indicate a command's priority.
                    For example, to make sure a loop takes precedence over all other commands,
                    you would write "@0 loop" because 0 is the highest priority.
                    Negative values make sure the command the command is run last,
                    including after commands with no priority attached.
                    """
                    if '@' in command_text:
                        command_array = command_text[1:].split(' ', 1)
                        if command_array[1] == 'loop':
                            if customloop == False:
                                print(TERM_TEXT.custom_loop_error,
                                      TERM_TEXT.conversion_incomplete)
                                sys.exit(2)
                            command_array[1] = "Music_{}_Ch{}_Loop:\n".format(pointer_title, channel)
                        priority_command_queue.append(command_array)
                    else:
                        if command_text == 'loop':
                            command_text = "Music_{}_Ch{}_Loop:\n".format(pointer_title, channel)
                        async_command_queue.append(command_text)
                except AttributeError:
                    continue
            if command.tag == 'note':
                release_command_queue()
                note = command
                t = ""
                if note.find('rest') is not None:
                    asmfile.write("\tnote __, {}\n".format(note.find('duration').text))
                elif note.find('pitch') is None and note.find('unpitched') is None:
                    print('None?')
                else:
                    if channel != 4:
                        pitch = note.find('pitch')
                        if int(pitch.find('octave').text) is not curroctave:
                            curroctave = int(pitch.find('octave').text)
                            if curroctave < 1:
                            	print("\033[93mOctave 0 detected on channel {}! This may cause unintended behavior.\033[0m".format(channel))
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

def release_command_queue():
    if len(priority_command_queue) == 0 and len(async_command_queue) == 0:
        return
    # sort priority
    sorted_queue = []
    sorted_post_queue = []
    output_queue = []
    for command_set in priority_command_queue:
        if int(command_set[0]) > -1:
            sorted_queue.insert(int(command_set[0]), command_set[1])
        else:
            sorted_post_queue.insert(int(command_set[0]), command_set[1])
    # join all the lists
    output_queue.extend(sorted_queue)
    output_queue.extend(async_command_queue)
    output_queue.extend(sorted_post_queue)
    for command in output_queue:
        t = "\t{}\n".format(command)
        if ':' in command:
            t = "\n{}".format(command)
        if t != None: asmfile.write(t)
    # clear all the lists
    priority_command_queue.clear()
    async_command_queue.clear()
    sorted_queue.clear()
    sorted_post_queue.clear()
    output_queue.clear()


# tempo, volume, dutycycle, tone, vibrato, notetype, octave, stereopanning
# <tie type="start" (type="stop")/>
def parse_channel1(part, title, manualtempo, tempo, conf, loop):
    global asmfile
    # write channel header including tempo
    asmfile.write("Music_{}_Ch1:\n".format(title))
    # Try to auto detect tempo, or get it from the user
    if not manualtempo:
        try:
            asmfile.write("\ttempo {}\n".format(int(19200/int(round(float(part.find('./measure/direction/sound').get('tempo')))))))
        except TypeError or AttributeError:
            print(TERM_TEXT.no_tempo_error,
                  TERM_TEXT.conversion_incomplete)
            sys.exit(2)
    else:
        asmfile.write("\ttempo {}\n".format(int(19200/int(tempo))))
    if conf == "":
        asmfile.write("\tvolume $77\n")
        asmfile.write("\tnotetype $c, $95\n")
        asmfile.write("\tdutycycle $2\n")
    else:
        read_custom_header(1)
    if loop == False:
        asmfile.write("Music_{}_Ch1_Loop:\n".format(title))
    # custom loops are determined when the score is parsed
    # custom loops must be defined in *each channel*
    note_print(part, 1)
    asmfile.write("\tloopchannel 0, Music_{}_Ch1_Loop\n\n\n".format(title))

# dutycycle, tone, vibrato, notetype, octave, stereopanning
def parse_channel2(part, title, conf, loop):
    global asmfile
    # write channel header
    asmfile.write("Music_{}_Ch2:\n".format(title))
    if conf == "":
        asmfile.write("\tnotetype $c, $95\n")
        asmfile.write("\tdutycycle $2\n")
    else:
        read_custom_header(2)
    if loop == False:
        asmfile.write("Music_{}_Ch2_Loop:\n".format(title))
    # custom loops are determined when the score is parsed
    # custom loops must be defined in *each channel*
    note_print(part, 2)
    asmfile.write("\tloopchannel 0, Music_{}_Ch2_Loop\n\n\n".format(title))

# stereopanning, vibrato, notetype, tone, octave
def parse_channel3(part, title, conf, loop):
    global asmfile
    # write channel header
    asmfile.write("Music_{}_Ch3:\n".format(title))
    if conf == "":
        asmfile.write("\tnotetype $c, $15\n")
    else:
        read_custom_header(3)
    if loop == False:
        asmfile.write("Music_{}_Ch3_Loop:\n".format(title))
    # custom loops are determined when the score is parsed
    # custom loops must be defined in *each channel*
    note_print(part, 3)
    asmfile.write("\tloopchannel 0, Music_{}_Ch3_Loop\n\n\n".format(title))

# notetype, togglenoise
def parse_channel4(part, title, conf, loop):
    global asmfile
    # write channel header
    asmfile.write("Music_{}_Ch4:\n".format(title))
    if conf == "":
        asmfile.write("\tnotetype $c\n")
        asmfile.write("\ttogglenoise 1\n")
    else:
        read_custom_header(4)
    if loop == False:
        asmfile.write("Music_{}_Ch4_Loop:\n".format(title))
    # custom loops are determined when the score is parsed
    # custom loops must be defined in *each channel*
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
    global customloop
    infile = ""
    outfile = ""
    configfile = ""
    speed = 120
    speedoverride = False
    songname = "Music Song"
    nameoverride = False
    noiseless = False
    forceoverwrite = False
    customloop = False
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["score=", "code=", "config=", "tempo=", "name=", "noiseless", "overwrite", "custom-loop"])
    except getopt.GetoptError:
        print(TERM_TEXT.help,
              TERM_TEXT.description_help,
              TERM_TEXT.more_help)
        sys.exit(2)
    if len(argv) == 0:
        print(TERM_TEXT.help,
              TERM_TEXT.description_help,
              TERM_TEXT.more_help)
        sys.exit(2)
    for opt, arg in opts:
        if opt =='-h' or opt == '--help':
            print(TERM_TEXT.help,
                  TERM_TEXT.extended_help)
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
        elif opt in ("--custom-loop"):
            customloop = True
    if filehere(outfile) and forceoverwrite is False:
        confirm = input(outfile + TERM_TEXT.overwrite_prompt)
        if confirm in ['y', 'Y']:
            process_score(infile, outfile, configfile, noiseless, speedoverride, speed, songname, nameoverride, customloop)
    else:
        process_score(infile, outfile, configfile, noiseless, speedoverride, speed, songname, nameoverride, customloop)

if __name__== "__main__":
    main(sys.argv[1:])
