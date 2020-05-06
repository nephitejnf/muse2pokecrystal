#!/usr/bin/python3
"""
The main function and argument parsing for Muse2pokecrystal.

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


import argparse
from os.path import isfile as filehere
from src import text, fileio
import muse2pokecrystal as legacy

TERM_TEXT = text.TerminalText(False)


def main():
    parser = argparse.ArgumentParser(description=TERM_TEXT.prog_description)
    parser.add_argument('musicxml',
                        help=TERM_TEXT.arg_musicxml_desc)
    parser.add_argument('asm',
                        help=TERM_TEXT.arg_asm_desc)
    parser.add_argument('-c', '--config',
                        help=TERM_TEXT.arg_config_desc)
    parser.add_argument('-t', '--tempo',
                        type=int,
                        help=TERM_TEXT.arg_tempo_desc)
    parser.add_argument('-n', '--name',
                        metavar='"SONG NAME"',
                        help=TERM_TEXT.arg_name_desc)
    parser.add_argument('-N', '--noiseless',
                        action='store_true',
                        help=TERM_TEXT.arg_noiseless_desc)
    parser.add_argument('-f', '--overwrite',
                        action='store_true',
                        help=TERM_TEXT.arg_overwrite_desc)
    parser.add_argument('-l', '--custom-loop',
                        action='store_true',
                        help=TERM_TEXT.arg_custom_loop_desc)
    parser.add_argument('-C', '--colored-output',
                        action='store_true',
                        help=TERM_TEXT.arg_colored_output_desc)
    parser.add_argument('-x', '--no-optimizations',
                        action='store_true',
                        help=TERM_TEXT.arg_no_optimizations_desc)
    parser.add_argument('-v', '--version', action='version',
                        version=TERM_TEXT.version)
    args = parser.parse_args()
    if filehere(args.asm) and args.overwrite is False:
        confirm = input(args.asm +
                        text.TerminalText
                        (args.colored_output)
                        .overwrite_prompt)
        if confirm in ['y', 'Y']:
            fileio.write_music_file(args)
    else:
        fileio.write_music_file(args)


if __name__ == "__main__":
    main()
