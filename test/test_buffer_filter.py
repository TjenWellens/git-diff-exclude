import unittest
from code.buffer_filter import BufferFilter, is_chunk_start, has_changed, is_file_start, is_excluded

file_header = [
    'diff --git a/app/src/main/res/values/ids.xml b/app/src/main/res/values/ids.xml',
    'new file mode 100644',
    'index 0000000..5fd0ee8',
    '--- /dev/null',
    '+++ b/app/src/main/res/values/ids.xml',
]

chunk = [
    '@@ -0,0 +1,4 @@',
    '+<?xml version="1.0" encoding="utf-8"?>',
    '+<resources>',
    '+    <item name="view_position" type="id"/>',
    '+</resources>',
    '\ No newline at end of file',
    '',
]

unchanged_chunk = [
    '@@ -0,0 +1,4 @@',
    '<?xml version="1.0" encoding="utf-8"?>',
    '<resources>',
    '    <item name="view_position" type="id"/>',
    '</resources>',
    '\ No newline at end of file',
    '',
]

FILE_CHANGED = file_header + chunk
FILE_UNCHANGED = file_header + unchanged_chunk
changed_chunk_lines = chunk[1:5]
unchanged_end_lines = [chunk[5]]

CHUNK_START = len(file_header) + 0
FIRST = 0
SECOND = 1


class BufferFilterTestWithoutMatchingFilter(unittest.TestCase):
    def setUp(self):
        self.buffer_filter = BufferFilter('^\+import')

    def test_is_chunk_start(self):
        self.assertTrue(is_chunk_start(chunk[0]))

    def test_has_changed(self):
        self.assertTrue(has_changed(chunk[1]))

    def test_is_file_start(self):
        self.assertTrue(is_file_start(file_header[0]))

    def test_one_chunk(self):
        self.compare_input_lines(FILE_CHANGED, FILE_CHANGED)

    def test_one_chunk_return_at_line_change(self):
        # no return
        for line in file_header:
            self.buffer_filter.add_line_to_buffer(line)
        self.buffer_filter.add_line_to_buffer(FILE_CHANGED[CHUNK_START])

        # all lines up till now
        output = self.buffer_filter.add_line_to_buffer(changed_chunk_lines[FIRST])
        self.assertListEqual(FILE_CHANGED[:7], output)

        # changed lines one by one
        for line in changed_chunk_lines[SECOND:]:
            output = self.buffer_filter.add_line_to_buffer(line)
            self.assertListEqual([line], output)

        # no return
        for line in unchanged_end_lines:
            self.buffer_filter.add_line_to_buffer(line)

        # all lines when done
        output = self.buffer_filter.add_line_to_buffer(None)
        self.assertListEqual(unchanged_end_lines, output)

    def test_two_chunks(self):
        input_lines = file_header + chunk + chunk
        expected = input_lines
        self.compare_input_lines(expected, input_lines)

    def test_unchanged_chunk(self):
        input_lines = file_header + chunk + unchanged_chunk
        expected = FILE_CHANGED
        self.compare_input_lines(expected, input_lines)

    def test_unchanged_chunk_at_beginning_of_file(self):
        input_lines = file_header + unchanged_chunk + chunk
        expected = FILE_CHANGED
        self.compare_input_lines(expected, input_lines)

    def test_unchanged_chunks_only(self):
        input_lines = file_header + unchanged_chunk + unchanged_chunk
        expected = []
        self.compare_input_lines(expected, input_lines)

    def test_multiple_files(self):
        input_lines = FILE_CHANGED * 2
        expected = input_lines
        self.compare_input_lines(expected, input_lines)

    def test_multiple_files_last_unchanged(self):
        input_lines = FILE_CHANGED + FILE_UNCHANGED
        expected = FILE_CHANGED
        self.compare_input_lines(expected, input_lines)

    def test_multiple_files_first_unchanged(self):
        input_lines = FILE_UNCHANGED + FILE_CHANGED
        expected = FILE_CHANGED
        self.compare_input_lines(expected, input_lines)

    def test_multiple_files_middle_unchanged(self):
        input_lines = FILE_CHANGED + FILE_UNCHANGED + FILE_CHANGED * 2
        expected = FILE_CHANGED * 3
        self.compare_input_lines(expected, input_lines)

    def compare_input_lines(self, expected, input_lines):
        output = []
        for line in input_lines:
            output += self.buffer_filter.add_line_to_buffer(line)
        output += self.buffer_filter.add_line_to_buffer(None)
        self.assertListEqual(expected, output)


# filtered_chunk = chunk[:1] + chunk[5:]
# FILE_CHANGED_FILTERED = file_header + filtered_chunk
filtered_line = chunk[3]

unfiltered_chunk = [
    '@@ -0,0 +1,4 @@',
    '+foo1',
    '+foo2',
    '+    foo3',
    '+foo4',
    '\ No newline at end of file',
    '',
]


class BufferFilterTestFilter(unittest.TestCase):
    def setUp(self):
        self.buffer_filter = BufferFilter('^\+ *<')

    def compare_input_lines(self, expected, input_lines):
        output = []
        for line in input_lines:
            output += self.buffer_filter.add_line_to_buffer(line)
        output += self.buffer_filter.add_line_to_buffer(None)
        self.assertListEqual(expected, output)

    def test_is_excluded(self):
        self.assertTrue(is_excluded(self.buffer_filter.exclude_pattern, filtered_line))

    def test_filtered_chunk_returns_empty(self):
        input_lines = FILE_CHANGED
        expected = []
        self.compare_input_lines(expected, input_lines)

    def test_filtered_chunk_unfiltered_chunk_returns_unfiltered_chunk(self):
        input_lines = file_header + chunk + unfiltered_chunk
        expected = file_header + unfiltered_chunk
        self.compare_input_lines(expected, input_lines)
