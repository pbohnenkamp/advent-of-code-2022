from collections import deque
from dataclasses import dataclass


class TuningBufferReaderNoStartPacketError(Exception):
    pass


@dataclass
class TuningBufferDuplicate:
    character: str
    stream_index: int


class TuningBufferReader:
    def __init__(self, stream: str) -> None:
        self._distinct_character_count = None
        self._stream: str = stream.strip()
        self._stream_index = 0
        self._stream_sliding_window: deque[str] = deque()
        self._duplicates: deque[TuningBufferDuplicate] = deque()
        self._non_repeating_count = 0

    def find_start_of_packet_marker(self):
        return self._find_first_index_of_distinct_characters(4)

    def find_start_of_message_marker(self):
        return self._find_first_index_of_distinct_characters(14)

    def _find_first_index_of_distinct_characters(self, distinct_character_count):
        self._distinct_character_count = distinct_character_count
        for i, character in enumerate(self._stream):
            self._stream_index = i
            self._advance_sliding_window()
            self._clean_passed_duplicates()
            self._add_character_to_window(character)
            if self._non_repeating_count == self._distinct_character_count:
                # we found the start packet character position
                return self._stream_index + 1

        # Uh oh, no packet marker found
        raise TuningBufferReaderNoStartPacketError("No start-of-packet marker found!")

    def _advance_sliding_window(self):
        if len(self._stream_sliding_window) > self._distinct_character_count - 1:
            self._stream_sliding_window.popleft()

    def _clean_passed_duplicates(self):
        if len(self._duplicates) > 0:
            if (self._stream_index - self._duplicates[0].stream_index) > self._distinct_character_count - 1:
                self._duplicates.popleft()

    def _add_character_to_window(self, character):
        duplicate = self._determine_and_build_duplicate(character)
        if duplicate is not None:
            self._duplicates.append(duplicate)
            self._non_repeating_count = self._stream_index - max(self._duplicates,
                                                                 key=lambda dup: dup.stream_index).stream_index
        else:
            self._non_repeating_count += 1
        self._stream_sliding_window.append(character)

    def _determine_and_build_duplicate(self, character):
        try:
            window_index = self._search_window_from_left(character)
            duplicate_index = self._stream_index - len(self._stream_sliding_window) + window_index
            return TuningBufferDuplicate(character, duplicate_index)
        except ValueError:
            return None

    def _search_window_from_left(self, search_char):
        for i, i_char in reversed(list(enumerate(self._stream_sliding_window))):
            if i_char == search_char:
                return i

        raise ValueError()
