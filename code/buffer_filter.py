import re


class BufferFilter:
    def __init__(self, exclude_pattern=None, exclude_patterns=[]):
        self.exclude_pattern = re.compile(exclude_pattern) if exclude_pattern is not None else None
        self.exclude_patterns = list(map(lambda p: re.compile(p), exclude_patterns))
        self.buffer = []
        self.file_buffer = []
        self.chunk_buffer = []
        self.is_in_chunk = False
        self.has_chunk_changed = False
        self.has_file_changed = False

    def add_line_to_buffer(self, line):  # -> [line]
        output = []
        if line is None:
            if self.is_in_chunk:
                output += self.end_chunk()
            return output

        # finish
        if is_file_start(line):
            output += self.next_file()
        elif is_chunk_start(line):
            output += self.next_chunk()

        # add line to correct buffer
        if self.is_in_chunk:
            self.chunk_buffer.append(line)
        else:
            self.file_buffer.append(line)

        # output if linechanged
        if self.is_in_chunk and has_changed(line) \
                and not is_excluded(self.exclude_pattern, line) \
                and not is_excluded_from_any(self.exclude_patterns, line):
            self.has_chunk_changed = True
            self.has_file_changed = True
            output += self.clear_file_buffer()
            output += self.clear_chunk_buffer()

        return output

    def clear_file_buffer(self):
        file_buffer = self.file_buffer
        self.file_buffer = []
        return file_buffer

    def clear_chunk_buffer(self):
        chunk_buffer = self.chunk_buffer
        self.chunk_buffer = []
        return chunk_buffer

    def next_chunk(self):
        output = []
        if self.is_in_chunk:
            output = self.end_chunk()
        self.is_in_chunk = True
        return output

    def end_chunk(self):
        output = []
        if self.has_chunk_changed:
            # output buffer
            output += self.clear_file_buffer()
            output += self.clear_chunk_buffer()
        else:
            # clear buffer, return nothing
            self.clear_chunk_buffer()

        self.is_in_chunk = False
        self.has_chunk_changed = False

        return output

    def next_file(self):
        output = []
        if not self.has_file_changed:
            self.clear_file_buffer()

        if self.is_in_chunk:
            output = self.end_chunk()

        self.has_file_changed = False

        return output


def match(regex, line):
    return regex.search(strip_color_stuff(line)) is not None

color_stuff = re.compile(r'\u001B[^m]*m')

def strip_color_stuff(line):
    return re.sub(color_stuff, '', line)

chunk_start = re.compile(r'@@ [^ ]* [^ ]* @@')
line_added = re.compile(r'^\+')
line_removed = re.compile(r'^\-')
file_start = re.compile(r'^diff --git [^ ]* [^ ]*')


def is_chunk_start(line):
    return match(chunk_start, line)


def has_changed(line):
    return match(line_added, line) \
           or match(line_removed, line)


def is_file_start(line):
    return match(file_start, line)


def is_excluded(exclude_pattern, line):
    if exclude_pattern is None:
        return False
    return match(exclude_pattern, line)


def is_excluded_from_any(exclude_patterns, line):
    for exclude_pattern in exclude_patterns:
        if match(exclude_pattern, line):
            return True
    return False
