"""
This module is a part of Muse2pokecrystal.

This module contains the text for muse2pokecrystal.

Copyright (C) 2020  nephitejnf and hyperdriveguy

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Full plain text license https://www.gnu.org/licenses/agpl-3.0.txt
"""


from xml.etree.ElementTree import parse
from src import text, notes


class ProcessScore():
    """Processes the xml prior to the notes and inline commands."""

    def __init__(self, options):
        self.output_file_store = []
        self.options = options
        self.term_text = text.TerminalText(self.options.colored_output)
        self.score_tree = parse(self.options.musicxml)
        self.xml_root = self.score_tree.getroot()
        self.song_pointer = self.generate_pointer_title()
        self.output_text = text.OutputText(self.song_pointer)
        self.populate_part_list()
        self.check_part_list_length()

    def process_to_file_store(self):
        self.add_headers()
        # Channel 1
        print(self.term_text.converting_channel(1, self.part_list))
        parser_1 = ParseChannel1(self.options, self.song_pointer)

        channel_1_part = self.xml_root.find(
                        text.XmlText.format_part(
                            self.part_list[0][0]))

        self.output_file_store.append(parser_1.channel_label())

        bpm = int(channel_1_part.find(
            './measure/direction/sound').get('tempo'))

        divisions = int(channel_1_part.find(
            './measure/attributes/divisions').text)

        tempo = notes.calc_score_tempo(bpm, divisions)
        channel_1_commands = parser_1.get_initial_channel_commands(tempo)
        self.output_file_store.extend(channel_1_commands)
        parse_staff_1 = notes.ParseStaff(channel_1_part,
                                         1,
                                         self.song_pointer,
                                         self.options)
        parse_staff_1.output_notes(divisions)
        if parse_staff_1.found_user_loops is False:
            self.output_file_store.append('Music_{}_Ch{}_Loop:\n'.format(
                self.song_pointer, 1))
        self.output_file_store.extend(parse_staff_1.staff_output)
        self.output_file_store.append(
            '\tjumpchannel Music_{}_Ch{}_Loop\n\n\n'.format(
                self.song_pointer, 1))
        # Channel 2
        print(self.term_text.converting_channel(2, self.part_list))
        parser_2 = ParseChannel2(self.options, self.song_pointer)

        channel_2_part = self.xml_root.find(
                        text.XmlText.format_part(
                            self.part_list[1][0]))

        self.output_file_store.append(parser_2.channel_label())
        channel_2_commands = parser_2.get_initial_channel_commands()
        self.output_file_store.extend(channel_2_commands)
        parse_staff_2 = notes.ParseStaff(channel_2_part,
                                         2,
                                         self.song_pointer,
                                         self.options)
        parse_staff_2.output_notes(divisions)
        if parse_staff_2.found_user_loops is False:
            self.output_file_store.append('Music_{}_Ch{}_Loop:\n'.format(
                self.song_pointer, 2))
        self.output_file_store.extend(parse_staff_2.staff_output)
        self.output_file_store.append(
            '\tjumpchannel Music_{}_Ch{}_Loop\n\n\n'.format(
                self.song_pointer, 2))
        # Channel 3
        print(self.term_text.converting_channel(3, self.part_list))
        parser_3 = ParseChannel3(self.options, self.song_pointer)

        channel_3_part = self.xml_root.find(
                        text.XmlText.format_part(
                            self.part_list[2][0]))

        self.output_file_store.append(parser_3.channel_label())
        channel_3_commands = parser_3.get_initial_channel_commands()
        self.output_file_store.extend(channel_3_commands)
        parse_staff_3 = notes.ParseStaff(channel_3_part,
                                         3,
                                         self.song_pointer,
                                         self.options)
        parse_staff_3.output_notes(divisions)
        if parse_staff_3.found_user_loops is False:
            self.output_file_store.append('Music_{}_Ch{}_Loop:\n'.format(
                self.song_pointer, 3))
        self.output_file_store.extend(parse_staff_3.staff_output)
        self.output_file_store.append(
            '\tjumpchannel Music_{}_Ch{}_Loop\n\n\n'.format(
                self.song_pointer, 3))
        # Channel 4
        print(self.term_text.converting_channel(4, self.part_list))
        parser_4 = ParseChannel4(self.options, self.song_pointer)

        channel_4_part = self.xml_root.find(
                        text.XmlText.format_part(
                            self.part_list[3][0]))

        self.output_file_store.append(parser_4.channel_label())
        channel_4_commands = parser_4.get_initial_channel_commands()
        self.output_file_store.extend(channel_4_commands)
        parse_staff_4 = notes.ParseStaff(channel_4_part,
                                         4,
                                         self.song_pointer,
                                         self.options)
        parse_staff_4.output_notes(divisions)
        if parse_staff_4.found_user_loops is False:
            self.output_file_store.append('Music_{}_Ch{}_Loop:\n'.format(
                self.song_pointer, 4))
        self.output_file_store.extend(parse_staff_4.staff_output)
        self.output_file_store.append(
            '\tjumpchannel Music_{}_Ch{}_Loop\n'.format(
                self.song_pointer, 4))

        for line in self.output_file_store:
            print(line, end='')

    def populate_part_list(self):
        self.part_list = []
        xml_part_list = self.xml_root.find('part-list')
        for part in xml_part_list.findall('score-part'):

            self.part_list.append((part.get('id'),
                                   part.find('part-name').text))

    def generate_pointer_title(self):
        if self.options.name is None:
            try:
                song_title = self.xml_root.find('./work/work-title').text
            except AttributeError:
                print(self.term_text.generic_name)
                song_title = 'Song'
        else:
            song_title = self.options.name
        return song_title.replace(':', '').replace(' ', '')

    def check_part_list_length(self):
        """
        Todo.

        Throw a warning if there are more than 4 parts.
        Throw an error if there are less than 3 parts.
        """
        if len(self.part_list) < 4:
            self.options.noiseless = True

    def add_headers(self):
        print(self.term_text.adding_header)
        self.output_file_store.append(self.output_text.music_label())
        self.output_file_store.append(
            self.output_text.music_header_1(
                self.options.noiseless
                ))
        self.output_file_store.append(self.output_text.music_header_234(2))
        self.output_file_store.append(self.output_text.music_header_234(3))
        if not self.options.noiseless:
            self.output_file_store.append(self.output_text.music_header_234(4))
        self.output_file_store.append('\n\n')


class ChannelParse():
    """Superclass for parsing each channel."""

    def __init__(self, options, song_pointer, channel):
        self.output_text = text.OutputText(song_pointer)
        self.options = options
        self.song_pointer = song_pointer
        self.channel = channel

    def channel_label(self):
        label = 'Music_{}_Ch{}:\n'.format(self.song_pointer, self.channel)
        return label

    def channel_loop_label(self):
        loop = 'Music_{}_Ch{}_Loop:\n'.format(self.song_pointer, self.channel)
        return loop

    def channel_loop(self):
        loop_channel = '\tloopchannel 0, Music_{}_Ch{}_Loop\n\n\n'.format(
            self.song_pointer,
            self.channel
        )
        return loop_channel


class ParseChannel1(ChannelParse):
    """Parse channel 1."""

    def __init__(self, options, song_pointer):
        super().__init__(options, song_pointer, 1)

    def get_initial_channel_commands(self, tempo):
        commands = []
        commands.append('\ttempo {}\n'.format(tempo))
        commands.append(self.output_text.volume)
        commands.append(self.output_text.notetype_12)
        commands.append(self.output_text.dutycycle)
        return commands


class ParseChannel2(ChannelParse):
    """Parse channel 2."""

    def __init__(self, options, song_pointer):
        super().__init__(options, song_pointer, 2)

    def get_initial_channel_commands(self):
        commands = []
        commands.append(self.output_text.notetype_12)
        commands.append(self.output_text.dutycycle)
        return commands


class ParseChannel3(ChannelParse):
    """Parse channel 3."""

    def __init__(self, options, song_pointer):
        super().__init__(options, song_pointer, 3)

    def get_initial_channel_commands(self):
        commands = []
        commands.append(self.output_text.notetype_3)
        return commands


class ParseChannel4(ChannelParse):
    """Parse channel 4."""

    def __init__(self, options, song_pointer):
        super().__init__(options, song_pointer, 4)

    def get_initial_channel_commands(self):
        commands = []
        commands.append(self.output_text.notetype_4)
        commands.append(self.output_text.togglenoise)
        return commands
