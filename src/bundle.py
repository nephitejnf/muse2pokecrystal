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


import tarfile
import hashlib
from src import text, exceptions


def gen_hash(path):
    """Generate hash for archive verification."""
    with open(path, 'rb') as file:
        file_hash = hashlib.blake2b()
        while chunk := file.read(8192):
            file_hash.update(chunk)
        return file_hash.digest()


def create_pack(path, files, colors):
    """Create an LZMA archive with a checksum appended to the end."""
    with tarfile.open(path, 'w:xz') as bundle:
        for file in files:
            bundle.add(file, file[27:])
    hash = gen_hash(path)
    with open(path, 'ab') as file:
        file.write(hash)


def unpack(path, size, colors):
    with open(path, 'r+b') as file:
        file.seek(-64, 2)
        hash_in_file = file.read(64)
        file.truncate(size - 64)
    if gen_hash(path) == hash_in_file:
        print(text.TerminalText(colors).verified_checksum(hash_in_file))
    else:
        sums = (gen_hash(path), hash_in_file)
        raise exceptions.HashFailureError(
            text.TerminalText(colors).checksum_wrong(sums))
    with tarfile.open(path, 'r:xz') as archive:
        archive.extractall('/tmp/muse2pokecrystal/unpack/')
