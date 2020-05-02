#!/usr/bin/python3
import argparse
from os.path import isfile as filehere
from src import text, score
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
    parser.add_argument('-d', '--depreciated', action='store_true')
    parser.add_argument('-v', '--version', action='version',
                        version=TERM_TEXT.version)
    args = parser.parse_args()
    # Legacy compat, DELETE ASAP!
    if args.depreciated:
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
    # Legacy compat, DELETE ASAP!
    if filehere(args.asm) and args.overwrite is False:
        confirm = input(args.asm +
                        text.TerminalText
                        (args.colored_output)
                        .overwrite_prompt)
        if confirm in ['y', 'Y']:
            if args.depreciated:
                legacy.process_score(args.musicxml,
                                     args.asm,
                                     args.config,
                                     args.noiseless,
                                     speed,
                                     args.tempo,
                                     args.name,
                                     nameoverride,
                                     args.custom_loop)
            else:
                score.ProcessScore(args).process_to_file_store()
    else:
        if args.depreciated:
            legacy.process_score(args.musicxml,
                                 args.asm,
                                 args.config,
                                 args.noiseless,
                                 speed,
                                 args.tempo,
                                 args.name,
                                 nameoverride,
                                 args.custom_loop)
        else:
            score.ProcessScore(args).process_to_file_store()


if __name__ == "__main__":
    main()
