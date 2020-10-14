"""
This module contains the methods for note and command parsing.

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


from xml.etree.ElementTree import parse
from src import text


class ParseStaff():

    def __init__(self, part, channel, song_pointer, options):
        # Set class variables from parameters
        self.channel = channel
        self.part = part
        self.song_pointer = song_pointer
        # Make text objects
        self.term_text = text.TerminalText(options.colored_output)
        self.output_text = text.OutputText(song_pointer)
        # Return this value to see if we have to insert a loop for the user
        self.found_user_loops = False
        # Toggle this value if an error is found
        # The reason this is done rather than raising an exception is because
        # this way every single error will be shown without having to rerun.
        self.force_failure = False
        # For more precise warnings and errors
        self.measure_iterator = 0
        self.channel_length = 0
        # Note processing variables
        self.tied_note_duration = 0
        self.tied_note = False
        self.rest_length_queue = 0
        self.no_optimizations = options.no_optimizations
        # Set the current octave to -1 so it's always
        # overridden by the first iteration.
        self.cur_octave = -1
        self.pre_loop_octave = -1
        # List to return for file output
        self.staff_output = []
        # Lists to store commands to be released when the next note is found
        self.priority_command_queue = []
        self.trivial_command_queue = []
        # Tempo changes are only parsed when this is > 1
        self.num_tempo_changes = 0

    def output_notes(self, divisions=None):
        for measure in self.part.findall('measure'):
            self.measure_iterator += 1
            for command in measure:
                if command.tag == "direction":
                    self.process_commands(command, divisions)
                if command.tag == 'note':
                    if (len(self.priority_command_queue) > 0 and
                            len(self.trivial_command_queue) > 0):
                        self.release_rest_queue()
                    self.release_command_queue()
                    # Only process voice 1 to avoid desyncs
                    if int(command.find('voice').text) == 1:
                        self.process_notes(command)
        if (self.found_user_loops and
                self.pre_loop_octave is not self.cur_octave):
            octave_index = self.staff_output.index(
                '\n' + self.output_text.channel_loop_label(self.channel)) + 1
            if 'octave' not in self.staff_output[octave_index]:
                try:
                    self.staff_output.insert(
                        octave_index, self.output_text.octave_change(
                            self.pre_loop_octave))
                except ValueError:
                    pass
        # Generate the rests at the end of the score
        self.release_rest_queue()

    def process_notes(self, note):
        full_note = None
        if note.find('chord') is not None:
            print(self.term_text.chord_ignore(self.measure_iterator))
            # Early return so we don't have to deal with attribute errors
            return
        if note.find('grace') is not None:
            print(self.term_text.grace_notes_unsupported)
            # Early return so we don't have to deal with attribute errors
            return
        # WARNING: rests may occasionally mess with the command order!
        if note.find('rest') is not None:
            self.rest_length_queue += int(note.find('duration').text)
            self.channel_length += int(note.find('duration').text)
            if self.no_optimizations:
                self.release_rest_queue()
        else:
            self.release_rest_queue()
            if self.channel == 4:
                pitch = note.find('unpitched')
            else:
                pitch = note.find('pitch')
                self.handle_octave(pitch)
            # Was the last note tied?
            if self.tied_note is False:
                # If not, is this note tied?
                if note.find(text.XmlText().tie_start) is not None:
                    # Start a new tied note
                    self.tied_note = True
                    self.tied_note_duration += int(note.find('duration').text)
                    self.channel_length += int(note.find('duration').text)
                # Yay, it's a normal note!
                else:
                    full_note = self.output_text.full_note_format(
                        self.handle_accidental(pitch),
                        int(note.find('duration').text))
                    self.note_duration_check(int(note.find('duration').text))
                    self.staff_output.append(full_note)
                    self.channel_length += int(note.find('duration').text)
            # Aw heck, it is tied
            else:
                # Does the tie end here?
                # In order for us to know that it's really the end,
                # there should ONLY be a tie stop.
                if (note.find(text.XmlText().tie_stop) is not None and
                        note.find(text.XmlText().tie_start) is None):
                    # Finalize the duration
                    self.tied_note_duration += int(note.find('duration').text)
                    self.channel_length += int(note.find('duration').text)
                    # Write the note
                    full_note = self.output_text.full_note_format(
                        self.handle_accidental(pitch),
                        self.tied_note_duration)
                    self.note_duration_check(self.tied_note_duration)
                    self.staff_output.append(full_note)
                    # Reset note tie variables
                    self.tied_note = False
                    self.tied_note_duration = 0
                # The tie keeps on going, hold on to yer hats
                elif (note.find(text.XmlText().tie_stop) is not None and
                      note.find(text.XmlText().tie_start) is not None):
                    self.tied_note_duration += int(note.find('duration').text)
                    self.channel_length += int(note.find('duration').text)

    def release_rest_queue(self):
        if self.rest_length_queue > 0:
            while self.rest_length_queue > 16:
                self.rest_length_queue -= 16
                self.staff_output.append(self.output_text.rest_note(16))
            self.staff_output.append(self.output_text.rest_note(
                self.rest_length_queue))
            self.rest_length_queue = 0

    def note_duration_check(self, duration):
        if duration > 16:
            print(self.term_text.note_too_long(self.channel,
                                               self.measure_iterator,
                                               duration))
            self.force_failure = True

    def handle_octave(self, pitch):
        if int(pitch.find('octave').text) is not self.cur_octave:
            self.cur_octave = int(pitch.find('octave').text)
            if self.cur_octave < 1:
                print(self.term_text.octave_zero(self.channel))
            if self.cur_octave > 8:
                print(self.term_text.octave_too_high(self.channel))
            self.staff_output.append(
                self.output_text.octave_change(
                    self.cur_octave))

    def handle_accidental(self, pitch):
        bad_notes = {'E#': 'F_',
                     'B#': 'C_',
                     'Ab': 'G#',
                     'Gb': 'F#',
                     'Eb': 'D#',
                     'Db': 'C#',
                     'Bb': 'A#',
                     'Cb': 'B_'}
        altered_pitch = pitch.find('alter')
        if self.channel == 4:
            step = pitch.find('display-step').text
        else:
            step = pitch.find('step').text
        if altered_pitch is not None:
            altered_pitch = altered_pitch.text
        else:
            altered_pitch = 0
        nibble = '_'
        if int(altered_pitch) == -1:
            nibble = 'b'
        elif int(altered_pitch) == 1:
            nibble = '#'
        formatted_note = '{}{}'.format(step, nibble)
        # Handle an out of the ordinary octave change
        if formatted_note == 'Cb':
            if 'octave' in self.staff_output[-1]:
                self.staff_output.pop(-1)
            self.staff_output.append(
                self.output_text.octave_change(
                    self.cur_octave - 1))
        # Respell flat and odd notes
        if formatted_note in bad_notes:
            formatted_note = bad_notes[formatted_note]
        return formatted_note

    def process_commands(self, command, divisions):
        try:
            command_text = command.find('./direction-type/words').text
            if '@' in command_text:
                command_array = command_text[1:].split(' ', 1)
                command_array[1] = self.handle_loop(command_array[1])
                self.priority_command_queue.append(command_array)
            else:
                command_text = self.handle_loop(command_text)
                self.trivial_command_queue.append(command_text)
        except AttributeError:
            # If it throws this error, let's see if it's a bpm change.
            # It only tries this on channel 1 because all other channels give
            # None as a parameter for divisions which causes an Exception.
            try:
                bpm = float(command.find('./sound').get('tempo'))
                tempo = str(calc_score_tempo(bpm, divisions))
                command_text = 'tempo ' + tempo
                self.num_tempo_changes += 1
                if self.num_tempo_changes > 1:
                    self.priority_command_queue.append([0, command_text])
            except (TypeError, AttributeError):
                # Okay, this is a lost cause. Just throw a warning and move on
                print(self.term_text.unknown_element(self.measure_iterator))

    def handle_loop(self, command_text):
        """Handle user defined loops."""
        if command_text == 'loop':
            self.pre_loop_octave = self.cur_octave
            self.found_user_loops = True
            command_text = self.output_text.channel_loop_label(self.channel)
        return command_text

    def release_command_queue(self):
        top_command_queue_length = len(self.priority_command_queue)
        bottom_command_queue_length = len(self.trivial_command_queue)
        if top_command_queue_length == 0 and bottom_command_queue_length == 0:
            return
        # Sort priority
        sorted_queue = []
        sorted_post_queue = []
        output_queue = []
        for command_set in self.priority_command_queue:
            if int(command_set[0]) > -1:
                sorted_queue.insert(int(command_set[0]), command_set[1])
            else:
                sorted_post_queue.insert(int(command_set[0]), command_set[1])
        # join all the lists
        output_queue.extend(sorted_queue)
        output_queue.extend(self.trivial_command_queue)
        output_queue.extend(sorted_post_queue)
        command_quantity = len(output_queue)
        for command in output_queue:
            if '_Loop:' in command:
                formatted_command = "\n{}".format(command)
            else:
                formatted_command = "\t{}\n".format(command)
            if formatted_command is not None:
                self.staff_output.append(formatted_command)
        # clear all the lists
        self.priority_command_queue.clear()
        self.trivial_command_queue.clear()
        sorted_queue.clear()
        sorted_post_queue.clear()
        output_queue.clear()
        return command_quantity


def calc_score_tempo(bpm, divisions):
    """Calculate the songs tempo from the bpm."""
    smallest_note = float(4 / divisions)
    tempo = 19200 / bpm
    tempo = int(round(tempo * smallest_note))
    return tempo
