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
#        for line in self.output_file_store:
#            print(line, end='')

from src import score


def write_music_file(options):
    """Write music file."""
    with open(options.asm, 'w') as asm_file:
        commands_list = score.ProcessScore(options).process_to_file_store()
        for line in commands_list:
            asm_file.write(line)
