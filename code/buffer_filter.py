import re


class BufferFilter:
    def __init__(self, exclude_pattern):
        self.exclude_pattern = exclude_pattern
        self.buffer = []
        self.is_in_chunk = False

    def add_line_to_buffer(self, line):  # -> [line]
        if line is None:
            return self.clear_buffer()

        self.buffer.append(line)

        if is_chunk_start(line):
            self.is_in_chunk = True

        if self.is_in_chunk and has_changed(line):
            return self.clear_buffer()

        return []

    def clear_buffer(self):
        buffer = self.buffer
        self.buffer = []
        return buffer


def match(regex, line):
    return regex.search(line) is not None


chunk_start = re.compile(r'@@ [^ ]* [^ ]* @@')
line_added = re.compile(r'^\+')
line_removed = re.compile(r'^\-')


def is_chunk_start(line):
    return match(chunk_start, line)


def has_changed(line):
    return match(line_added, line) \
           or match(line_removed, line)
