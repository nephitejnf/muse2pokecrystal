"""
This module contains the methods for post-conversion optimizations.

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

from random import random


def callchannel_optimize(output_array):
    backup_array = output_array
    search_array = []
    search_match = True
    match_index_array = [[]]
    found_ideal_optimization = False
    #cur_file_index = 0
    # minimum search length is 4
    for cur_file_index in range(0, len(output_array)):
        search_size = 4
        while not found_ideal_optimization:
            for index in range(cur_file_index, search_size):
                search_array.append(output_array[index])
            print(search_array)
            # check matches
            for file_index in range(0, len(output_array)):
                if search_array[0] == output_array[file_index]:
                    # we may have a match bois
                    search_match = True
                    for check_match_index in range(0, search_size):
                        if(search_array[check_match_index] !=
                           output_array[file_index + check_match_index]):
                            search_match = False
                            break
                    if search_match:
                        match_index_array.append(file_index)
                        print(match_index_array)


if __name__ == "__main__":
    rand_list = []
    for l in range(0, int(random() * 1000)):
        rand_list.append(str(round(random() * 10)) + '\n')
    print(rand_list)
    callchannel_optimize(rand_list)
