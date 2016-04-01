from code.buffer_filter import BufferFilter, is_chunk_start, has_changed, is_file_start
    def test_is_chunk_start(self):
        self.assertTrue(is_chunk_start(chunk[0]))

    def test_has_changed(self):
        self.assertTrue(has_changed(chunk[1]))

    def test_is_file_start(self):
        self.assertTrue(is_file_start(file_header[0]))

    def test_unchanged_chunk(self):
    def test_unchanged_chunk_at_beginning_of_file(self):

    def test_unchanged_chunks_only(self):
        output = []
        input_lines = file_header + unchanged_chunk + unchanged_chunk
        expected = file_header + chunk
        for line in input_lines:
            output += self.buffer_filter.add_line_to_buffer(line)
        output += self.buffer_filter.add_line_to_buffer(None)
        self.assertListEqual([], output)

    def test_multiple_files(self):
        output = []
        input_lines = file_header + chunk + file_header + chunk
        expected = input_lines
        for line in input_lines:
            output += self.buffer_filter.add_line_to_buffer(line)
        output += self.buffer_filter.add_line_to_buffer(None)
        self.assertListEqual(expected, output)

    def test_multiple_files_last_unchanged(self):
        output = []
        input_lines = file_header + chunk + file_header + unchanged_chunk
        expected = file_header + chunk
        for line in input_lines:
            output += self.buffer_filter.add_line_to_buffer(line)
        output += self.buffer_filter.add_line_to_buffer(None)
        self.assertListEqual(expected, output)