"""This module contains the text for muse2pokecrystal."""


class Color:
    """Constants for formatting terminal output"""

    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARK_CYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    # aliases for quick and uniform formatting changes
    ERROR = RED + BOLD
    COMPLETE = GREEN + BOLD
    SUCCESS = DARK_CYAN + BOLD
    WARNING = YELLOW + BOLD
    INFO = YELLOW


class TerminalText():
    """Text that gets output to the terminal."""

    def __init__(self):
        pass

    help = ('Usage: muse2pokecrystal '
            '-i [MUSICXML] -o [ASM]... [OPTION]...\n')

    more_help = 'Try \'muse2pokecrystal -h\' for more information.'

    extended_help = ('Convert MusicXML sheet music into a script that\'s'
                     ' compatible with Pokémon Crystal\'s audio engine.\n'
                     'Example: '
                     'muse2pokecrystal -i song.musicxml -o song.asm\n\n'
                     'Mandatory options:\n'
                     '  -i, --score=MUSICXML    input MusicXML\n'
                     '  -o, --code=ASM          output asm\n\n'
                     'Additional options:\n'
                     '      --config=CONFIG     '
                     'read commands from a configuration file\n'
                     '      --tempo=TEMPO       '
                     'override the tempo in the score\n'
                     '      --name=NAME         specify the song\'s name\n'
                     '      --noiseless         '
                     'don\'t process the noise channel\n'
                     '      --overwrite         '
                     'force overwrite if the output file exists\n'
                     '      --custom-loop       detect user defined loops\n\n'
                     'Found a bug? Open an issue on Github!\n'
                     'Repository: '
                     'https://github.com/nephitejnf/muse2pokecrystal\n')

    custom_loop_error = (Color.WARNING +
                         'A user defined loop was found; however, ' +
                         'the --custom-loop parameter was not toggled.\n' +
                         'Try again with the --custom-loop parameter.\n' +
                         Color.END)

    conversion_incomplete = (Color.ERROR +
                             '\nConversion incomplete!' +
                             Color.END)

    no_tempo_error = (Color.WARNING +
                      'No tempo was detected. ' +
                      'Try again with the --tempo parameter.' +
                      Color.END)

    parity_check_failed = (Color.ERROR +
                           '\nParity check failed!\n' +
                           'Check that there is only one note per channel!' +
                           Color.END)

    overwrite_prompt = (Color.WARNING +
                        ' already exists!\n' +
                        'Do you want to continue and overwrite? [Y/n]: ' +
                        Color.END)

    generic_name = (Color.WARNING +
                    'Could not guess song name. Using generic name.' +
                    Color.END)


# debugging
if __name__ == "__main__":
    print(TerminalText.help)
