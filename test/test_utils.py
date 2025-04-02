import unittest

class TestUtils(unittest.TestCase):

    def test_imports(self):
        from miripvir.ioutils import read_blastdb_reference, read_paired_end_files

    def test_paired_end_reads(self):
        from miripvir.ioutils import read_paired_end_files
        from miripvir.data import BlastPairedEndReads
        u = read_paired_end_files(file_forward='test/BLAST1.test.tab', file_backward='test/BLAST2.test.tab')
        self.assertIsInstance(u, BlastPairedEndReads)

    def test_look_up(self):
        from miripvir.ioutils import read_blastdb_reference
        from miripvir.data import LookUpTable
        u = read_blastdb_reference(reference='test/sanchis21.reference.json')
        self.assertIsInstance(u, LookUpTable)

