"""
This module contains the configuration parsing functions for Muse2pokecrystal.

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


import configparser
from src import text, exceptions


class SongConfig():
    """Song configuration class."""

    def __init__(self, options):
        """Read configuration file."""
        self.config_file = options.config
        self.term_text = text.TerminalText(options.colored_output)
        self.config_parse = configparser.ConfigParser()
        self.config_parse.read(self.config_file)
        self.channel_config = None
        self.formatted_command_list = []

    def read_channel_conf(self, channel):
        """Read the configuration for a specified channel."""
        self.channel_config = self.config_parse['Channel {}'.format(channel)]
        if channel == 1:
            self.add_volume()
        # The notetype validity check is the same across channels.
        self.check_valid_hex_value(
            self.channel_config['notetype'][1:],
            True,
            'f')
        if channel != 4:
            self.add_notetype_1()
            if channel != 3:
                self.add_dutycycle()
            self.add_tone()
            self.add_vibrato()
        else:
            self.add_notetype_2()
            self.add_togglenoise()
        self.add_stereopanning()
        return self.formatted_command_list

    def add_volume(self):
        # volume (Channel 1)
        self.check_valid_hex_value(
            self.channel_config['volume'][1:],
            True)
        # Another check to see if the value is in warning threshold.
        if not self.check_valid_hex_value(
                self.channel_config['volume'][1:],
                False,
                '77'):
            print(self.term_text.high_volume_warning)
        self.add_to_output(text.OutputText.format_volume_command, 'volume')

    def add_notetype_1(self):
        # notetype (Channels 1 - 3)
        self.check_valid_hex_value(
            self.channel_config['intensity'][1:],
            True)
        self.formatted_command_list.append(
            text.OutputText.format_notetype_command(
                self.channel_config['notetype'],
                self.channel_config['intensity']))

    def add_notetype_2(self):
        # notetype (Channel 4)
        self.add_to_output(
            text.OutputText.format_notetype_command,
            'notetype')

    def add_togglenoise(self):
        # togglenoise (Channel 4)
        if (int(self.channel_config['togglenoise']) < 0 or
                self.channel_config['togglenoise'] is None):
            raise ValueError(self.term_text.invalid_configuration)
        self.add_to_output(
            text.OutputText.format_togglenoise_command,
            'togglenoise')

    def add_dutycycle(self):
        # dutycycle (Channels 1 - 2)
        self.check_valid_hex_value(
            self.channel_config['dutycycle'][1:],
            True,
            '3')
        self.add_to_output(
            text.OutputText.format_dutycycle_command,
            'dutycycle')

    def add_tone(self):
        # tone (Channels 1 - 3)
        if self.check_valid_hex_value(self.channel_config['tone'][1:]):
            self.add_to_output(
                text.OutputText.format_tone_command,
                'tone')

    def add_vibrato(self):
        # vibrato (Channels 1 - 3)
        vibrato_on = ['true', 'on', 'yes', '1']
        if self.channel_config['vibrato'] in vibrato_on:
            self.check_valid_hex_value(
                self.channel_config['vibrato_delay'][1:],
                False)
            self.check_valid_hex_value(
                self.channel_config['vibrato_extent'][1:],
                False)
            self.formatted_command_list.append(
                text.OutputText.format_vibrato_command(
                    self.channel_config['vibrato_delay'],
                    self.channel_config['vibrato_extent']))

    def add_stereopanning(self):
        # stereopanning (Channel 1 - 4)
        self.check_valid_stereopanning()
        full_sound = ['$ff', '$FF']
        if self.channel_config['stereopanning'] not in full_sound:
            self.add_to_output(
                text.OutputText.format_stereopanning_command,
                'stereopanning')

    def add_to_output(self, format_command, config_value):
        self.formatted_command_list.append(
            format_command(self.channel_config[config_value]))

    def check_valid_hex_value(self, value, required=False, max_hex='ff'):
        try:
            if int(value, 16) > int(max_hex, 16):
                if required is True:
                    raise ValueError(self.term_text.hex_value_too_large)
                return False
            return True
        except ValueError:
            if required is True:
                raise exceptions.MusicConfigError(
                    self.term_text.invalid_configuration)
            return False

    def check_valid_stereopanning(self):
        valid_values = ['$ff', '$FF', '$f0', '$F0', '$0f', '$0F']
        if self.channel_config['stereopanning'] in valid_values:
            return True
        raise exceptions.MusicConfigError(self.term_text.invalid_steropanning)
