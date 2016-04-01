import sys
from code.buffer_filter import BufferFilter

if len(sys.argv) < 2:
    sys.stderr.write("Syntax error: " + sys.argv[0] + " <exclude-pattern>")
    exit(1)

exclude_pattern = sys.argv[1]
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
