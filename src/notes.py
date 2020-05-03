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
        # return this value to see if we have to insert a loop for the user
        self.found_user_loops = False
        # Toggle this value if an error is found
        self.force_failure = False
        # For more precise warnings and errors
        self.measure_iterator = 0
        # Note processing variables
        self.tied_note_duration = 0
        self.tied_note = False
        self.rest_length_queue = 0
        self.no_optimizations = options.no_optimizations
        # Set the current octave to -1 so it's always
        # overridden by the first iteration.
        self.cur_octave = -1
        # List to return for file output
        self.staff_output = []
        # Lists to store commands to be released when the next note is found
        self.priority_command_queue = []
        self.trivial_command_queue = []

    def output_notes(self, divisions):
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
                    self.process_notes(command)
        # Generate the rests at the end of the score
        self.release_rest_queue()

        return self.staff_output

    def process_notes(self, note):
        full_note = None
        # WARNING: rests may occasionally mess with the command order!
        if note.find('rest') is not None:
            self.rest_length_queue += int(note.find('duration').text)
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
                # Yay, it's a normal note!
                else:
                    full_note = self.output_text.full_note_format(
                        self.handle_accidental(pitch),
                        int(note.find('duration').text))
                    self.note_duration_check(int(note.find('duration').text))
                    self.staff_output.append(full_note)
            # Aw heck, it is tied
            else:
                # Does the tie end here?
                # In order for us to know that it's really the end,
                # there should ONLY be a tie stop.
                if (note.find(text.XmlText().tie_stop) is not None and
                        note.find(text.XmlText().tie_start) is None):
                    # Finalize the duration
                    self.tied_note_duration += int(note.find('duration').text)
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


    # def handle_tied_note(self, note):

            """
            print(note.find(text.XmlText().tie_start))
            if (note.find(text.XmlText().tie_start) is not None and
                    note.find(text.XmlText().tie_stop) is not None):
                note_duration += int(note.find('duration').text)
            elif note.find(text.XmlText().tie_start) is not None:
                tied_note = True
                step = self.handle_accidental(pitch)
                note_duration = int(note.find('duration').text)
            elif note.find(text.XmlText().tie_stop) is not None:
                if int(note.find('duration').text) + note_duration > 16:
                    temp_dura = (int(note.find('duration').text) +
                                 note_duration)
                    print(self.term_text.note_too_long(self.channel,
                                                       self.measure_iterator,
                                                       temp_dura))
                    self.force_failure = True
                if step == self.handle_accidental(pitch):
                    full_note = self.output_text.full_note_format(
                        self.handle_accidental(pitch),
                        note_duration + int(note.find('duration').text))
                else:
                    # Is this code ever reached?
                    self.staff_output.append(self.output_text.full_note_format(
                        step, note_duration))
                    full_note = self.output_text.full_note_format(
                        self.handle_accidental(pitch),
                        int(note.find('duration').text))
                tied_note = False
                step = ''
                note_duration = 0
            else:
                full_note = self.output_text.full_note_format(
                    self.handle_accidental(pitch), note_duration)
            if full_note is not None:
                self.staff_output.append(full_note)
            """

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
        formated_note = '{}{}'.format(step, nibble)
        # Respell flat and odd notes
        if formated_note in bad_notes:
            formated_note = bad_notes[formated_note]
        return formated_note

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
            try:
                bpm = int(command.find('./sound').get('tempo'))
                tempo = str(calc_score_tempo(bpm, divisions))
                command_text = 'tempo ' + tempo
                self.priority_command_queue.append([0, command_text])
            except (TypeError, AttributeError):
                # Okay, this is a lost cause. Just throw a warning and move on
                print(self.term_text.unknown_element(self.measure_iterator))

    def handle_loop(self, command_text):
        """Handle user defined loops."""
        if command_text == 'loop':
            self.found_user_loops = True
            return "Music_{}_Ch{}_Loop:\n".format(
                self.song_pointer, self.channel)
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
                formated_command = "\n{}".format(command)
            else:
                formated_command = "\t{}\n".format(command)
            if formated_command is not None:
                self.staff_output.append(formated_command)
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
