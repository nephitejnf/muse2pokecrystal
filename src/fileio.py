"""
This module contains the file writing functions for Muse2pokecrystal.

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


from src import score, text
from os.path import isfile as filehere
from os.path import getsize as getfilesize
from os import remove, mkdir, listdir
from shutil import rmtree, copy


def write_music_file(options):
    """Write music file."""
    with open(options.asm, 'w') as asm_file:
        commands_list = score.ProcessScore(options).process_to_file_store()
        for line in commands_list:
            asm_file.write(line)


def check_overwrite(path, skip=False, colors=False):
    """
    File overwrite check.

    Deletes the file if it exists beforehand.
    Returns True if the file will be written to.
    """
    if skip is True:
        remove(path)
        return True
    if filehere(path):
        confirm = input(path + text.TerminalText(colors).overwrite_prompt)
        if confirm in ['y', 'Y']:
            remove(path)
            return True
        else:
            return False
    return True


def make_temp_copy_unpack(path):
    mkdir('/tmp/muse2pokecrystal')
    copy(path, '/tmp/muse2pokecrystal/pack.tar.xz')
    return getfilesize(path)


def make_temp_copy_pack(musicxml, config):
    mkdir('/tmp/muse2pokecrystal')
    mkdir('/tmp/muse2pokecrystal/pack')
    copy(musicxml, '/tmp/muse2pokecrystal/pack')
    copy(config, '/tmp/muse2pokecrystal/pack')
    full_path = []
    rel_path = listdir('/tmp/muse2pokecrystal/pack')
    for file in rel_path:
        full_path.append('/tmp/muse2pokecrystal/pack/{}'.format(file))
    return full_path


def delete_temp_dir():
    rmtree('/tmp/muse2pokecrystal')


def guess_files():
    arg_dict = {}
    files = listdir('/tmp/muse2pokecrystal/unpack')
    for file in files:
        file_path_full = '/tmp/muse2pokecrystal/unpack/{}'.format(file)
        if '.musicxml' in file:
            arg_dict['musicxml'] = file_path_full
            continue
        elif '.ini' in file or '.cfg' in file:
            arg_dict['config'] = file_path_full
            continue
        # last resort file detection
        with open('/tmp/muse2pokecrystal/unpack/{}'.format(file), 'r') as f:
            determining_chars = f.read(2)
            if determining_chars == '<?' or '<' in determining_chars:
                arg_dict['musicxml'] = file_path_full
                continue
            elif '[' in determining_chars:
                arg_dict['config'] = file_path_full
                continue
    return arg_dict
