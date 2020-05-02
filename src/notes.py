from xml.etree.ElementTree import parse
from src import text


class ParseStaff():

    def __init__(self, part, channel, song_pointer, colored):
        self.channel = channel
        self.part = part
        self.song_pointer = song_pointer
        self.term_text = text.TerminalText(colored)
        self.found_user_loops = False
        self.measure_iterator = 0
        self.staff_output = []
        self.priority_command_queue = []
        self.trivial_command_queue = []

    def output_notes(self, divisions):
        # Set the current octave to -1 so it's always
        # overridden by the first iteration.
        cur_octave = -1
        tied_note = False
        step = ''
        note_duration = 0
        for measure in self.part.findall('measure'):
            self.measure_iterator += 1
            for command in measure:
                if command.tag == "direction":
                    self.process_commands(command, divisions)
                if command.tag == 'note':
                    self.release_command_queue()
        return self.staff_output

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

    def handle_loop(self, command_text):
        """Handle user defined loops."""
        if command_text == 'loop':
            self.found_user_loops = True
            return "Music_{}_Ch{}_Loop:\n".format(
                self.song_pointer, self.channel)
        return command_text


def calc_score_tempo(bpm, divisions):
    """Calculate the songs tempo from the bpm."""
    smallest_note = float(4 / divisions)
    tempo = 19200 / bpm
    tempo = int(round(tempo * smallest_note))
    return tempo
