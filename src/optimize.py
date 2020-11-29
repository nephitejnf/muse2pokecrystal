#!/usr/bin/python
"""
This module contains the methods for optimizing pokecrystal music scripts.

Copyright (C) 2020 hyperdriveguy

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


def optimize(music, name):
    """
    Run optimizations the music.
    
    Call if importing as a module.
    """
    search = MetaSearch(music, name)
    return search.iterate_script()


class MetaSearch():
    """Controls the primary iteration over the file."""

    def __init__(self, music, name):
        self.music = music
        self.song_name = 'Music_' + name + '_Branch_'
        # Start at the beginning of the file
        self.main_file_index = 0

    def iterate_script(self):
        branch = 1
        ditty_append = []
        while self.main_file_index < len(self.music):
            search_at_index = self.search_in_place()
            to_replace = self.pick_optimial_search(search_at_index[0],
                                                   search_at_index[1])
            if to_replace is not None:
                self.replace_matches(to_replace, branch)
                # Build the ditty to append
                ditty_append.append(self.song_name + str(branch) + ':\n')
                ditty_append.extend(to_replace[1])
                ditty_append.append('\tendchannel\n\n')
                branch += 1
                # We messed with the size of the list, so we're restarting
                self.main_file_index = 0
            else:
                self.main_file_index += 1
        self.music.extend(ditty_append)
        print('Created {} different branches for callchannel optimizations'.format(branch - 1))
        return(self.music)


    def replace_matches(self, target, branch):
        target_indexes = target[0]
        replace_length = len(target[1])
        for target_index in range(len(target_indexes) - 1, -1, -1):
            cur_replace_index = int(target_indexes[target_index])
            for x in range(replace_length):
                self.music.pop(cur_replace_index)
            self.music.insert(cur_replace_index,
                              '\tcallchannel ' +
                              self.song_name +
                              str(branch) + '\n')


    def pick_optimial_search(self, results, past_searches):
        if len(results) <= 1:
            return None
        best_search = 0
        for results_index in range(1, len(results) - 1):
            if(self.byte_savings_formula(results,
                                         past_searches,
                                         results_index) >
                self.byte_savings_formula(results,
                                          past_searches,
                                          results_index - 1)):
                best_search = results_index
        return (results[best_search], past_searches[best_search])

    def byte_savings_formula(self, results, search, index):
        return (len(results[index]) - 1) * len(search[index])

    def search_in_place(self):
        # minimum search size to see space savings is 4
        search_size = 4
        # 2D lists for calculating ideal optimizations
        search_results = []
        search_attempts = []
        while not search_is_over(search_results):
            # Set the parameters for a new search
            search_array = []
            for index in range(self.main_file_index,
                               self.main_file_index + search_size):
                try:
                    if not check_unoptimizable(self.music[index]):
                        search_array.append(self.music[index])
                except IndexError:
                    # Can't search past the end of the file
                    pass
            # Only possible when IndexError occurs above
            if len(search_array) < 4:
                break
            if len(self.check_matches(search_array)) == 0:
                break
            search_attempts.append(search_array)
            search_results.append(self.check_matches(search_array))
            # Increment search length to find optimum savings
            search_size += 1
        # Yes, I'm returning a tuple containing two different 2D lists
        # I'm sorry.
        return (search_results, search_attempts)

    def check_matches(self, search):
        """Iterate over the file to check for search matches."""
        match_indexes = []
        for file_index in range(0, len(self.music)):
            # See if the line we're on matches the first line in the search
            if search[0] == self.music[file_index]:
                # Innocent until proven guilty
                search_match = True
                # We need to check the other values
                for search_index in range(0, len(search)):
                    try:
                        if(search[search_index] !=
                                self.music[search_index + file_index]):
                            search_match = False
                            break
                    except IndexError:
                        # Past EOF, so it's not a match
                        search_match = False
                        break
                if search_match:
                    match_indexes.append(file_index)
        # Sort out conflicts
        conflicts = []
        for match in match_indexes:
            try:
                if(match_indexes[match_indexes.index(match) + 1]
                        < match + len(search)):
                    conflicts.append(match_indexes.index(match) + 1)
            except IndexError:
                # We reached the end, nothing to be concerned over
                pass
        # Iterate through the conflicts backwards to avoid messing up indexes
        for conflict_index in range(len(conflicts) - 1, -1, -1):
            match_indexes.pop(conflicts[conflict_index])
        return match_indexes


def check_unoptimizable(line):
    if 'callchannel' in line:
        return True
    if 'loopchannel' in line:
        return True
    if 'musicheader' in line:
        return True
    if 'togglenoise' in line:
        return True
    if ':' in line:
        return True


def search_is_over(results):
    # If the list is empty, don't bother (avoids IndexError)
    if len(results) < 1:
        return False
    if len(results[-1]) == 1:
        return True
    else:
        return False


def main():
    """For running as a standalone script."""
    parser = argparse.ArgumentParser(
        description='A script for optimizing pokecrystal music.')
    parser.add_argument('asm', help='script input file')
    parser.add_argument('output', help='optimized output file')
    parser.add_argument('name', help='name of the song (eg. \"YeetBattle\")')
    args = parser.parse_args()

    with open(args.asm, 'r') as music:
        file_array = music.readlines()
    search = MetaSearch(file_array, args.name)
    with open(args.output, 'w') as test:
        test.writelines(search.iterate_script())


if __name__ == "__main__":
    main()
