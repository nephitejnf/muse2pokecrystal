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


def callchannel_optimize(output_array, song_name):
    backup_array = output_array
    branch = 1
    cur_file_search_index = 0
    while cur_file_search_index < len(output_array):
        cur_file_search_index += 1
        match_index_array = [[]]
        found_ideal_optimization = False
        # minimum search length is 4
        search_size = 4
        while not found_ideal_optimization:
            search_array = []
            for index in range(cur_file_search_index, cur_file_search_index + search_size):
                search_array.append(output_array[index])
            print(search_array)
            # check matches
            for file_index in range(0, len(output_array)):
                if search_array[0] == output_array[file_index]:
                    # we may have a match bois
                    search_match = True
                    for check_match_index in range(0, search_size):
                        try:
                            if(search_array[check_match_index] !=
                               output_array[file_index + check_match_index]):
                                search_match = False
                                break
                        except IndexError:
                            search_match = False
                            break
                    if search_match:
                        try:
                            match_index_array[search_size - 4].append(file_index)
                        except IndexError:
                            match_index_array.append([])
                            match_index_array[search_size - 4].append(file_index)
            if len(match_index_array[-1]) <= 1:
                # there's no other matches, so lets move on
                opt_match = get_optimal_matches(match_index_array)
                # no matches, move on
                if opt_match is None:
                    found_ideal_optimization = True
                else:
                    for matched_index in match_index_array[opt_match]:
                        output_array.insert(matched_index,
                                            'Music_' + song_name + '_Branch' + str(branch))
                        for iteration in range(0, opt_match + 4):
                            print(output_array.pop(matched_index + 1))
                        print(output_array)
                    # restart from the beginning
                    cur_file_search_index = -1
                    found_ideal_optimization = True
                    branch += 1

            else:
                search_size += 1

            #input()


def get_optimal_matches(match_array):
    optimum_index = None
    for index in range(0, len(match_array)):
        if (len(match_array[index]) >
                len(match_array[index - 1])):
            optimum_index = index
    print(match_array)
    print(optimum_index)
    return optimum_index




if __name__ == "__main__":
    rand_list = []
    for l in range(0, int(random() * 1000)):
        rand_list.append(str(round(random() * 10)) + '\n')
    print(rand_list)
    callchannel_optimize(rand_list, 'Yeet_Song')
