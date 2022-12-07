from sys import stdin
from src.TuningBufferReader import TuningBufferReader, TuningBufferReaderNoStartPacketError


if __name__ == '__main__':
    message_count = 1
    for line in stdin:
        tuning_buffer_reader = TuningBufferReader(line)
        try:
            start_of_packet_position = tuning_buffer_reader.find_start_of_packet_marker()
            print(f'The start-of-packet marker for message {message_count} was found after processing {start_of_packet_position} characters.')
        except TuningBufferReaderNoStartPacketError:
            print(f'No start-of-packet marker found for message {message_count}')
        try:
            start_of_message_position = tuning_buffer_reader.find_start_of_message_marker()
            print(f'The start-of-message marker for message {message_count} was found after processing {start_of_message_position} characters.')
        except TuningBufferReaderNoStartPacketError:
            print(f'No start-of-message marker found for message {message_count}')
        message_count += 1
