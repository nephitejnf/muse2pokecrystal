from xml.etree.ElementTree import parse
from src import text


class ProcessScore():
    """Processes the xml prior to the notes and inline commands."""

    def __init__(self, options):
        self.output_file_store = []
        self.options = options
        self.term_text = text.TerminalText(self.options.colored_output)
        self.score_tree = parse(self.options.musicxml)
        self.xml_root = self.score_tree.getroot()
        self.song_pointer = self.generate_pointer_title()
        self.output_text = text.OutputText(self.song_pointer)
        self.populate_part_list()
        self.check_part_list_length()

    def populate_part_list(self):
        self.part_list = []
        xml_part_list = self.xml_root.find('part-list')
        for part in xml_part_list.findall('score-part'):
            self.part_list.append((part.get('id'),
                                   part.find('part-name').text))

    def generate_pointer_title(self):
        if self.options.name is None:
            try:
                song_title = self.xml_root.find('./work/work-title').text
            except AttributeError:
                print(self.term_text.generic_name)
                song_title = 'Song'
        else:
            song_title = self.options.name
        return song_title.replace(':', '').replace(' ', '')

    def check_part_list_length(self):
        """
        Todo.

        Throw a warning if there are more than 4 parts.
        Throw an error if there are less than 3 parts.
        """
        if len(self.part_list) < 4:
            self.options.noiseless = True


    def add_headers(self):
        print(self.term_text.adding_header)
        self.output_file_store.append(self.output_text.music_label())
        self.output_file_store.append(
            self.output_text.music_header_1(
                self.options.noiseless
                ))
        self.output_file_store.append(self.output_text.music_header_234(2))
        self.output_file_store.append(self.output_text.music_header_234(3))
        if not self.options.noiseless:
            self.output_file_store.append(self.output_text.music_header_234(4))
        self.output_file_store.append('\n\n')

    def
