import unittest
from code.buffer_filter import BufferFilter

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

input_lines = file_header + chunk
changed_chunk_lines = chunk[1:5]
unchanged_end_lines = [chunk[5]]

CHUNK_START = len(file_header) + 0
FIRST = 0
SECOND = 1


class BufferFilterTest(unittest.TestCase):
    def setUp(self):
        self.buffer_filter = BufferFilter('^\+import')

    def test_one_buffer(self):
        output = []
        for line in input_lines:
            output += self.buffer_filter.add_line_to_buffer(line)
        output += self.buffer_filter.add_line_to_buffer(None)
        self.assertListEqual(input_lines, output)

    def test_one_buffer_return_at_line_change(self):
        # no return
        for line in file_header:
            self.buffer_filter.add_line_to_buffer(line)
        self.buffer_filter.add_line_to_buffer(input_lines[CHUNK_START])

        # all lines up till now
        output = self.buffer_filter.add_line_to_buffer(changed_chunk_lines[FIRST])
        self.assertListEqual(input_lines[:7], output)

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

    def test_two_buffers(self):
        output = []
        input_lines = file_header + chunk + chunk
        for line in input_lines:
            output += self.buffer_filter.add_line_to_buffer(line)
        output += self.buffer_filter.add_line_to_buffer(None)
        self.assertListEqual(input_lines, output)

    def test_unchanged_chunk(self):
        output = []
        input_lines = file_header + chunk + unchanged_chunk
        expected = file_header + chunk
        for line in input_lines:
            output += self.buffer_filter.add_line_to_buffer(line)
        output += self.buffer_filter.add_line_to_buffer(None)
        self.assertListEqual(expected, output)

    def test_unchanged_chunk_at_beginning_of_file(self):
        output = []
        input_lines = file_header + unchanged_chunk + chunk
        expected = file_header + chunk
        for line in input_lines:
            output += self.buffer_filter.add_line_to_buffer(line)
        output += self.buffer_filter.add_line_to_buffer(None)
        self.assertListEqual(expected, output)

    def test_unchanged_chunks_only(self):
        output = []
        input_lines = file_header + unchanged_chunk + unchanged_chunk
        expected = file_header + chunk
        for line in input_lines:
            output += self.buffer_filter.add_line_to_buffer(line)
        output += self.buffer_filter.add_line_to_buffer(None)
        self.assertListEqual([], output)