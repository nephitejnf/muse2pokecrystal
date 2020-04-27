#!/usr/bin/python3
import argparse
from os.path import isfile as filehere
from src import text
import muse2pokecrystal as legacy

TERM_TEXT = text.TerminalText(False)
TERM_TEXT_COLORED = text.TerminalText(True)


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
    parser.add_argument('-v', '--version', action='version',
                        version=TERM_TEXT.version)
    args = parser.parse_args()
    if args.tempo is None:
        speed = False
    else:
        speed = True
    if args.name is None:
        nameoverride = False
    else:
        nameoverride = True
    if args.config is None:
        args.config = ''
    if filehere(args.asm) and args.overwrite is False:
        confirm = input(args.asm + TERM_TEXT.overwrite_prompt)
        if confirm in ['y', 'Y']:
            legacy.process_score(args.musicxml,
                                 args.asm,
                                 args.config,
                                 args.noiseless,
                                 args.tempo,
                                 speed,
                                 args.name,
                                 nameoverride,
                                 args.custom_loop)
    else:
        legacy.process_score(args.musicxml,
                             args.asm,
                             args.config,
                             args.noiseless,
                             args.tempo,
                             speed,
                             args.name,
                             nameoverride,
                             args.custom_loop)

if __name__ == "__main__":
    main()
