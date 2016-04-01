from code.buffer_filter import BufferFilter, is_chunk_start, has_changed, is_file_start, is_excluded
FILE_CHANGED = file_header + chunk
FILE_UNCHANGED = file_header + unchanged_chunk
class BufferFilterTestWithoutMatchingFilter(unittest.TestCase):
    def test_one_chunk(self):
        self.compare_input_lines(FILE_CHANGED, FILE_CHANGED)
    def test_one_chunk_return_at_line_change(self):
        self.buffer_filter.add_line_to_buffer(FILE_CHANGED[CHUNK_START])
        self.assertListEqual(FILE_CHANGED[:7], output)
    def test_two_chunks(self):
        expected = input_lines
        self.compare_input_lines(expected, input_lines)
        expected = FILE_CHANGED
        self.compare_input_lines(expected, input_lines)
        expected = FILE_CHANGED
        self.compare_input_lines(expected, input_lines)
        expected = []
        self.compare_input_lines(expected, input_lines)
        input_lines = FILE_CHANGED * 2
        self.compare_input_lines(expected, input_lines)
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