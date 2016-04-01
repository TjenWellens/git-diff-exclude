import sys
from code.buffer_filter import BufferFilter

exclude_pattern = "^[+-]import"
buffer_filter = BufferFilter(exclude_pattern)


def print_lines(lines):
    for line in lines:
        sys.stdout.write(line)


def parse_lines_from(file):
    for line in file:
        output = buffer_filter.add_line_to_buffer(line)
        print_lines(output)
        pass


parse_lines_from(sys.stdin)
