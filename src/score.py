"""
This module contains methods for constructing the output music script.

This module is a part of Muse2pokecrystal.

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
from src import text, notes, exceptions, config


class ProcessScore():
    """Processes the xml prior to the notes and inline commands."""

    def __init__(self, options):
        self.output_file_store = []
        self.options = options
        self.score_tree = parse(self.options.musicxml)
        self.xml_root = self.score_tree.getroot()
        self.song_pointer = self.generate_pointer_title()
        self.term_text = text.TerminalText(self.options.colored_output)
        self.output_text = text.OutputText(self.song_pointer)
        self.populate_part_list()
        self.check_part_list_length()

    def process_to_file_store(self):
        self.add_headers()
        already_found_user_loop = False
        channel_lengths = []
        for channel in range(1, 5):
            print(self.term_text.converting_channel(channel, self.part_list))
            if channel == 1:
                channel_parser = ParseChannel1(self.options, self.song_pointer)
            if channel == 2:
                channel_parser = ParseChannel2(self.options, self.song_pointer)
            if channel == 3:
                channel_parser = ParseChannel3(self.options, self.song_pointer)
            if channel == 4:
                channel_parser = ParseChannel4(self.options, self.song_pointer)
            channel_part = self.xml_root.find(text.XmlText.format_part(
                self.part_list[channel - 1][0]))
            self.output_file_store.append(
                self.output_text.channel_label(
                    channel))
            if channel == 1:
                # The tempo parameter is fetched because the text isn't always
                # consistent with the actual tempo. This also allows for
                # handling less standard tempo indication.
                bpm = int(channel_part.find(
                    './measure/direction/sound').get('tempo'))
                # We need the divisions so that the bpm can be adjusted.
                divisions = int(channel_part.find(
                    './measure/attributes/divisions').text)
                tempo = notes.calc_score_tempo(bpm, divisions)
                channel_commands = channel_parser.get_initial_channel_commands(
                    tempo)
            else:
                # divisions = None
                channel_commands = \
                    channel_parser.get_initial_channel_commands()
            self.output_file_store.extend(channel_commands)
            parse_staff = notes.ParseStaff(channel_part,
                                           channel,
                                           self.song_pointer,
                                           self.options)
            parse_staff.output_notes(divisions)
            # Check for desync errors
            # Channel length parity check
            channel_lengths.append(parse_staff.channel_length)
            if len(channel_lengths) > 1:
                if (channel_lengths[channel - 1] !=
                        channel_lengths[channel - 2]):
                    for chan in range(0, len(channel_lengths)):
                        print('Channel {} length: '.format(chan + 1) +
                              str(channel_lengths[chan]))
                    raise exceptions.MusicDesyncError(
                        self.term_text.parity_check_failed, channel_lengths)
            # Check to make sure user defined loops are consistent
            if parse_staff.found_user_loops is False:
                if already_found_user_loop is True:
                    raise exceptions.MusicDesyncError(
                        self.term_text.desync_error +
                        self.term_text.conversion_incomplete
                        )
                self.output_file_store.append(
                    self.output_text.channel_loop_label(channel))
            else:
                if channel != 4:
                    already_found_user_loop = True
                else:
                    if already_found_user_loop is False:
                        raise exceptions.MusicDesyncError(
                            self.term_text.desync_error +
                            self.term_text.conversion_incomplete
                            )
            self.output_file_store.extend(parse_staff.staff_output)
            self.output_file_store.append(
                self.output_text.channel_loop_end(channel))
        return self.output_file_store

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
        if self.options.config is not None:
            self.song_config = config.SongConfig(options)
        else:
            self.song_config = None
        self.song_pointer = song_pointer
        self.channel = channel

    def get_initial_channel_commands(self):
        """Use configuration if specified, if not use fallback."""
        if self.song_config is None:
            self.get_fallback_channel_commands()
        else:
            return self.song_config.read_channel_conf(self.channel)

    def get_fallback_channel_commands(self):
        """Meant to be overwritten by inheritance."""


class ParseChannel1(ChannelParse):
    """Parse channel 1."""

    def __init__(self, options, song_pointer):
        super().__init__(options, song_pointer, 1)

    def get_initial_channel_commands(self, tempo):
        """Use configuration if specified, if not use fallback."""
        if self.song_config is None:
            self.get_fallback_channel_commands(tempo)
        else:
            commands = []
            commands.append(self.output_text.format_tempo_command(tempo))
            commands.extend(self.song_config.read_channel_conf(self.channel))
            return commands

    def get_fallback_channel_commands(self, tempo):
        commands = []
        commands.append(self.output_text.format_tempo_command(tempo))
        commands.append(self.output_text.volume)
        commands.append(self.output_text.notetype_12)
        commands.append(self.output_text.dutycycle)
        return commands


class ParseChannel2(ChannelParse):
    """Parse channel 2."""

    def __init__(self, options, song_pointer):
        super().__init__(options, song_pointer, 2)

    def get_fallback_channel_commands(self):
        commands = []
        commands.append(self.output_text.notetype_12)
        commands.append(self.output_text.dutycycle)
        return commands


class ParseChannel3(ChannelParse):
    """Parse channel 3."""

    def __init__(self, options, song_pointer):
        super().__init__(options, song_pointer, 3)

    def get_fallback_channel_commands(self):
        commands = []
        commands.append(self.output_text.notetype_3)
        return commands


class ParseChannel4(ChannelParse):
    """Parse channel 4."""

    def __init__(self, options, song_pointer):
        super().__init__(options, song_pointer, 4)

    def get_fallback_channel_commands(self):
        commands = []
        commands.append(self.output_text.notetype_4)
        commands.append(self.output_text.togglenoise)
        return commands
