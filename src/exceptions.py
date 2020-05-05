"""
This module contains the custom exceptions for Muse2pokecrystal.

Why use custom exceptions at all?
1) So we can distinguish actual bugs from user error a little better.
2) Allow for more graceful exits.

Exceptions are only used for showstopper errors that output garbage.
Warnings are printed using print().

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


class MusicDesyncError(RuntimeError):
    """Music desync exception."""

    def __init__(self, message, errors=None):
        """Inherit exception."""
        super().__init__(message)
        self.errors = errors


class MusicConfigError(ValueError):
    """Invalid music configuration exception."""

    def __init__(self, message=None, errors=None):
        """Inherit exception."""
        super().__init__(message)
        self.errors = errors
