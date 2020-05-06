"""
This module contains the text for Muse2pokecrystal.

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


class Color():
    r"""
    Constants for formatting terminal output.

    Unused color codes that may be useful for future reference:
    self.blue = '\033[94m'
    cyan = '\033[96m'

    """

    def __init__(self, colored):
        """Set all the variables and aliases."""
        if colored:
            self.set_colors()
        else:
            self.null_colors()
        self.bold = '\033[1m'
        self.underline = '\033[4m'
        self.end = '\033[0m'

        # aliases for quick and uniform formatting changes
        self.error = self.red + self.bold
        self.complete = self.green + self.bold
        self.success = self.dark_cyan + self.bold
        self.warning = self.yellow + self.bold
        self.info = self.yellow
        self.standout = self.purple

    def null_colors(self):
        """Set color variables to dummy strings so no color is output."""
        self.purple = ''
        self.dark_cyan = ''
        self.green = ''
        self.yellow = ''
        self.red = ''

    def set_colors(self):
        """Set color variables."""
        self.purple = '\033[95m'
        self.dark_cyan = '\033[36m'
        self.green = '\033[92m'
        self.yellow = '\033[93m'
        self.red = '\033[91m'


class TerminalText():
    """
    Text that gets output to the terminal.

    All the text that stays constant are in one method.
    The more reusable pieces of text are methods.
    The text methods should always return strings, not print them.

    """

    def __init__(self, colored_output):
        """Toggle colored terminal text."""
        self.colored = colored_output
        self.set_constant_text()
        self.set_legacy_constant_text()

    def converting_channel(self, channel, instrument_list):
        """Format and return channel conversion text."""
        instrument = instrument_list[channel - 1][1]
        text_piece_1 = 'Converting Channel {}: '.format(channel)
        text_piece_2 = (Color(self.colored).standout +
                        instrument +
                        Color(self.colored).end)
        return text_piece_1 + text_piece_2

    def unknown_element(self, measure):
        return (Color(self.colored).warning +
                'Unknown element at measure ' +
                str(measure) +
                Color(self.colored).end)

    def octave_zero(self, channel):
        return (Color(self.colored).warning +
                'Octave 0 detected on channel ' +
                str(channel) +
                '! This may cause unintended behavior.' +
                Color(self.colored).end)

    def octave_too_high(self, channel):
        return (Color(self.colored).warning +
                'Octave greater than 8 detected on channel ' +
                str(channel) +
                '! This may cause unintended behavior.' +
                Color(self.colored).end)

    def note_too_long(self, channel, measure, duration):
        return (Color(self.colored).error +
                'Note too long in Channel ' +
                str(channel) +
                '! Note ends at measure ' +
                str(measure) +
                '. Note length is ' +
                str(duration) +
                '.' +
                Color(self.colored).end)

    def set_constant_text(self):
        """Set all the constant text."""
        self.custom_loop_error = (Color(self.colored).error +
                                  'A user defined loop was found; however, ' +
                                  'the --custom-loop parameter' +
                                  ' was not toggled.\n' +
                                  'Try again with the ' +
                                  '--custom-loop parameter.\n' +
                                  Color(self.colored).end)

        self.conversion_incomplete = (Color(self.colored).error +
                                      '\nConversion incomplete!' +
                                      Color(self.colored).end)

        self.no_tempo_error = (Color(self.colored).error +
                               'No tempo was detected. ' +
                               'Try again with the --tempo parameter.' +
                               Color(self.colored).end)

        self.desync_error = (Color(self.colored).error +
                             'User defined loops are inconsistent ' +
                             'across channels. ' +
                             'Make sure that all channels have a ' +
                             '"loop" element.' +
                             Color(self.colored).end)

        self.invalid_configuration = (Color(self.colored).error +
                                      'Provided configuration has an ' +
                                      'invalid required value.' +
                                      Color(self.colored).end)

        self.hex_value_too_large = (Color(self.colored).warning +
                                    'Hex value in configuration ' +
                                    'is too large.' +
                                    Color(self.colored).end)

        self.invalid_steropanning = (Color(self.colored).warning +
                                     'Invalid stereopanning command in ' +
                                     'in configuration.' +
                                     Color(self.colored).end)

        self.parity_check_succeeded = (Color(self.colored).success +
                                       '\nParity check succeeded!' +
                                       Color(self.colored).end)

        self.parity_check_failed = (Color(self.colored).error +
                                    '\nParity check failed!\n' +
                                    'Check that there are no ' +
                                    'chords in any channel!' +
                                    Color(self.colored).end)

        self.overwrite_prompt = (Color(self.colored).warning +
                                 ' already exists!\n' +
                                 'Do you want to continue ' +
                                 'and overwrite? [y/N]: ' +
                                 Color(self.colored).end)

        self.high_volume_warning = (Color(self.colored).warning +
                                    'Volume setting exceeds $77. ' +
                                    'This may cause unintended behavior.' +
                                    Color(self.colored).end)

        self.generic_name = (Color(self.colored).info +
                             'Could not guess song name. Using generic name.' +
                             Color(self.colored).end)

        self.no_noise_channel = (Color(self.colored).info +
                                 'No noise channel. ' +
                                 'Reprocessing without noise channel...' +
                                 Color(self.colored).end)

        self.conversion_success = (Color(self.colored).complete +
                                   'Conversion success!' +
                                   Color(self.colored).end)

        self.adding_header = (Color(self.colored).info +
                              'Adding Header Info' +
                              Color(self.colored).end)

        self.prog_description = ('Convert MusicXML sheet music'
                                 ' into a script that\'s'
                                 ' compatible with Pokémon Crystal\'s'
                                 ' audio engine.\n')

        self.arg_musicxml_desc = 'input MusicXML file'

        self.arg_asm_desc = 'output music script'

        self.arg_config_desc = 'read commands from a configuration file'

        self.arg_tempo_desc = 'override song with specified tempo in BPM'

        self.arg_name_desc = 'specify the song name'

        self.arg_noiseless_desc = 'don\'t process the noise channel, if any'

        self.arg_overwrite_desc = 'overwrite output file without prompting'

        self.arg_custom_loop_desc = ('process user defined loops'
                                     '(to be depreciated)')

        self.arg_colored_output_desc = 'color code terminal output'

        self.arg_no_optimizations_desc = 'disable optimizations'

        self.version = 'Muse2pokecrystal Git Development Version'

    def set_legacy_constant_text(self):
        """Depreciated text."""
        self.help = ('Usage: muse2pokecrystal '
                     '-i [MUSICXML] -o [ASM]... [OPTION]...\n')

        self.more_help = 'Try \'muse2pokecrystal -h\' for more information.'

        self.description_help = ('Convert MusicXML sheet music'
                                 ' into a script that\'s'
                                 ' compatible with Pokémon Crystal\'s'
                                 ' audio engine.\n')

        self.extended_help = ('Example: muse2pokecrystal'
                              ' -i song.musicxml -o song.asm\n\n'
                              'Mandatory options:\n'
                              '  -i, --score=MUSICXML    input MusicXML\n'
                              '  -o, --code=ASM          output asm\n\n'
                              'Additional options:\n'
                              '      --config=CONFIG     '
                              'read commands from a configuration file\n'
                              '      --tempo=TEMPO       '
                              'override the tempo in the score\n'
                              '      --name=NAME         '
                              'specify the song\'s name\n'
                              '      --noiseless         '
                              'don\'t process the noise channel\n'
                              '      --overwrite         '
                              'force overwrite if the output file exists\n'
                              '      --custom-loop       '
                              'detect user defined loops\n\n'
                              'Found a bug? Open an issue on Github!\n'
                              'Repository: '
                              'https://github.com/nephitejnf'
                              '/muse2pokecrystal\n')


class OutputText():
    """
    Contains text that gets written to the output file.

    These methods only return the strings, not write them.

    """

    def __init__(self, pointer_name):
        """Set variables used across methods."""
        self.music_title = pointer_name
        self.set_default_header_commands()

    def music_label(self):
        """Return the music label."""
        return 'Music_{}:\n'.format(self.music_title)

    def music_header_1(self, noiseless):
        """Return music header based on if there are 4 channels."""
        if noiseless:
            header = '\tmusicheader 3, 1, Music_{}_Ch1\n'.format(
                                self.music_title)
        else:
            header = '\tmusicheader 4, 1, Music_{}_Ch1\n'.format(
                                self.music_title)
        return header

    def music_header_234(self, channel):
        """Return music header based on channel."""
        return '\tmusicheader 1, {0}, Music_{1}_Ch{0}\n'.format(
            channel,
            self.music_title
        )

    def channel_label(self, channel):
        return 'Music_{}_Ch{}:\n'.format(self.music_title, channel)

    def channel_loop_label(self, channel):
        return 'Music_{}_Ch{}_Loop:\n'.format(self.music_title, channel)

    def channel_loop_end(self, channel):
        return '\tjumpchannel Music_{}_Ch{}_Loop\n\n\n'.format(
            self.music_title, channel)

    @staticmethod
    def rest_note(duration):
        """
        Handle rests.

        Todo: Handle new rest macro.
        """
        return '\tnote __, {}\n'.format(duration)

    @staticmethod
    def octave_change(octave):
        return '\toctave {}\n'.format(octave)

    @staticmethod
    def full_note_format(note, length):
        return '\tnote {}, {}\n'.format(note, length)

    @staticmethod
    def format_tempo_command(tempo):
        return '\ttempo {}\n'.format(tempo)

    @staticmethod
    def format_notetype_command(length, intensity=None):
        if intensity is None:
            return '\tnotetype {}\n'.format(length)
        return '\tnotetype {}, {}\n'.format(length, intensity)

    @staticmethod
    def format_volume_command(volume):
        return '\tvolume {}\n'.format(volume)

    @staticmethod
    def format_togglenoise_command(togglenoise):
        return '\ttogglenoise {}\n'.format(togglenoise)

    @staticmethod
    def format_dutycycle_command(dutycycle):
        return '\tdutycycle {}\n'.format(dutycycle)

    @staticmethod
    def format_tone_command(tone):
        return '\ttone {}\n'.format(tone)

    @staticmethod
    def format_stereopanning_command(stereopanning):
        return '\tstereopanning {}\n'.format(stereopanning)

    @staticmethod
    def format_vibrato_command(vibrato_delay, vibrato_extent):
        return '\tvibrato {}, {}\n'.format(vibrato_delay, vibrato_extent)

    def set_default_header_commands(self):
        """
        Set the default header commands to be fetched.

        Only used if there is no configuration.
        """
        self.volume = self.format_volume_command('$77')
        self.notetype_12 = self.format_notetype_command('$c', '$95')
        self.notetype_3 = self.format_notetype_command('$c', '$15')
        self.notetype_4 = self.format_notetype_command('$c')
        self.dutycycle = self.format_dutycycle_command('$2')
        self.togglenoise = self.format_togglenoise_command('1')


class XmlText():
    """Text for xml parsing."""

    def __init__(self):
        self.tie_start = './tie[@type="start"]'
        self.tie_stop = './tie[@type="stop"]'

    @staticmethod
    def format_part(part):
        """Format the part into xml."""
        return './part[@id="{}"]'.format(part)


# debugging
if __name__ == "__main__":
    i_list = [[0, 'yeet'], [0, 'yeety'], [0, 'yeeter'], [0, 'yeetest']]
    for yeet in range(1, 5):
        print(TerminalText(True).converting_channel(yeet, i_list))
