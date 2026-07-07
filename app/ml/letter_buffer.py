"""
letter_buffer.py

Stores and manages recognized letters for SignSpeak.

This module is responsible only for text management.
It does not perform recognition, prediction, or speech.
"""


class LetterBuffer:
    def __init__(self):
        """Initialize an empty letter buffer."""
        self._text = ""

    def add_letter(self, letter: str):
        """
        Add a recognized letter to the buffer.

        Parameters
        ----------
        letter : str
            The letter to append.
        """
        if letter:
            self._text += letter

    def add_space(self):
        """
        Add a space to the buffer.

        Prevents multiple consecutive spaces.
        """
        if self._text and not self._text.endswith(" "):
            self._text += " "

    def backspace(self):
        """
        Remove the last character from the buffer.
        """
        if self._text:
            self._text = self._text[:-1]

    def clear(self):
        """
        Clear the entire buffer.
        """
        self._text = ""

    def get_text(self) -> str:
        """
        Return the current text in the buffer.
        """
        return self._text

    def is_empty(self) -> bool:
        """
        Return True if the buffer is empty.
        """
        return len(self._text) == 0

    def __len__(self):
        """
        Return the number of characters in the buffer.
        """
        return len(self._text)

    def __str__(self):
        """
        Return the buffer as a string.
        """
        return self._text