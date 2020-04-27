"""This module contains the text for muse2pokecrystal."""


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

    def set_constant_text(self):
        """Set all the constant text."""
        self.custom_loop_error = (Color(self.colored).warning +
                                  'A user defined loop was found; however, ' +
                                  'the --custom-loop parameter' +
                                  ' was not toggled.\n' +
                                  'Try again with the ' +
                                  '--custom-loop parameter.\n' +
                                  Color(self.colored).end)

        self.conversion_incomplete = (Color(self.colored).error +
                                      '\nConversion incomplete!' +
                                      Color(self.colored).end)

        self.no_tempo_error = (Color(self.colored).warning +
                               'No tempo was detected. ' +
                               'Try again with the --tempo parameter.' +
                               Color(self.colored).end)
        self.parity_check_succeeded = (Color(self.colored).success +
                                       '\nParity check succeeded!' +
                                       Color(self.colored).end)

        self.parity_check_failed = (Color(self.colored).error +
                                    '\nParity check failed!\n' +
                                    'Check that there is only ' +
                                    'one note per channel!' +
                                    Color(self.colored).end)

        self.overwrite_prompt = (Color(self.colored).warning +
                                 ' already exists!\n' +
                                 'Do you want to continue ' +
                                 'and overwrite? [y/N]: ' +
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

        self.arg_custom_loop_desc = 'process user defined loops'

        self.arg_colored_output_desc = 'color code terminal output'

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

    def __init__(self, name):
        """Set variables used across methods."""
        self.music_title = name

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


# debugging
if __name__ == "__main__":
    i_list = [[0, 'yeet'], [0, 'yeety'], [0, 'yeeter'], [0, 'yeetest']]
    for yeet in range(1, 5):
        print(TerminalText(True).converting_channel(yeet, i_list))
