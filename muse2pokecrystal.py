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
from src import text, fileio, bundle, exceptions

TERM_TEXT = text.TerminalText(False)


def main():
    parser = argparse.ArgumentParser(description=TERM_TEXT.prog_description)
    parser.add_argument('musicxml',
                        help=TERM_TEXT.arg_musicxml_desc)
    parser.add_argument('asm',
                        metavar='output',
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
    parser.add_argument('-C', '--colored-output',
                        action='store_true',
                        help=TERM_TEXT.arg_colored_output_desc)
    parser.add_argument('-x', '--no-optimizations',
                        action='store_true',
                        help=TERM_TEXT.arg_no_optimizations_desc)
    parser.add_argument('-p', '--pack',
                        metavar='FILE',
                        help=TERM_TEXT.arg_pack_desc)
    parser.add_argument('-P', '--pack-only',
                        action='store_true',
                        help=TERM_TEXT.arg_pack_only_desc)
    parser.add_argument('-u', '--unpack',
                        action='store_true',
                        help=TERM_TEXT.arg_unpack_desc)
    parser.add_argument('-v', '--version', action='version',
                        version=TERM_TEXT.version)
    args = parser.parse_args()

    # pack creation
    if args.pack is not None:
        if args.config is None:
            raise exceptions.MusicConfigError(
                text.TerminalText(args.colored_output).conf_required)
        if fileio.check_overwrite(args.pack,
                                  args.overwrite,
                                  args.colored_output):
            try:
                files = fileio.make_temp_copy_pack(args.musicxml, args.config)
            except FileExistsError:
                fileio.delete_temp_dir()
                files = fileio.make_temp_copy_pack(args.musicxml, args.config)
            bundle.create_pack(args.pack, files, args.colored_output)

    if args.pack_only:
        # args.asm is the output for the pack in this case
        if fileio.check_overwrite(args.asm,
                                  args.overwrite,
                                  args.colored_output):
            try:
                files = fileio.make_temp_copy_pack(args.musicxml, args.config)
            except FileExistsError:
                fileio.delete_temp_dir()
                files = fileio.make_temp_copy_pack(args.musicxml, args.config)
            bundle.create_pack(args.asm,
                               files,
                               args.colored_output)

    else:
        # unpacking
        if args.unpack:
            try:
                size = fileio.make_temp_copy_unpack(args.musicxml)
            except FileExistsError:
                fileio.delete_temp_dir()
                size = fileio.make_temp_copy_unpack(args.musicxml)
            # unpack from temporary copy
            bundle.unpack('/tmp/muse2pokecrystal/pack.tar.xz',
                          size,
                          args.colored_output)
            overwrite_args = fileio.guess_files()
            args.musicxml = overwrite_args['musicxml']
            args.config = overwrite_args['config']

        # conversion
        if fileio.check_overwrite(args.asm,
                                  args.overwrite,
                                  args.colored_output):
            fileio.write_music_file(args)


if __name__ == "__main__":
    main()
