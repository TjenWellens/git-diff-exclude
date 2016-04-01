import re


class BufferFilter:
    def __init__(self, exclude_pattern):
        self.exclude_pattern = exclude_pattern
        self.buffer = []
        self.is_in_chunk = False
        self.has_chunk_changed = False

    def add_line_to_buffer(self, line):  # -> [line]
        output = []
        if line is None:
            if self.is_in_chunk:
                output += self.end_chunk()
            return output

        if is_chunk_start(line):
            output += self.next_chunk(line)

        self.buffer.append(line)

        if self.is_in_chunk and has_changed(line):
            self.has_chunk_changed = True
            output += self.clear_buffer()

        return output

    def clear_buffer(self):
        buffer = self.buffer
        self.buffer = []
        return buffer

    def next_chunk(self, line):
        output = []
        if self.is_in_chunk:
            output = self.end_chunk()

        self.is_in_chunk = True

        return output

    def end_chunk(self):
        output = []
        if self.has_chunk_changed:
            # print buffer
            output = self.clear_buffer()
        else:
            # clear buffer, return nothing
            self.clear_buffer()

        self.is_in_chunk = False
        self.has_chunk_changed = False

        return output


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
