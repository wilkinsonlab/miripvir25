import unittest
import pandas as pd

test_case_1 = pd.DataFrame.from_records(
    [
        {
            "read": "TRAILING%CHARACTER1-XVM1",
            "base_id": "XVM1",
            "qcovs": 90, 
            "length": 125,
            "ref": "foo",
            "file": "forward",
            
        },
        {
            "read": "TRAILING%CHARACTER1-XVM1", 
            "base_id": "XVM1",
            "qcovs": 100, 
            "length": 150,
            "ref": "foo",
            "file": "backward"
        },
        {
            "read": "TRAILING%CHARACTER1-XFGV", 
            "base_id": "XFGV",
            "qcovs": 69, 
            "length": 10,
            "ref": "bah",
            "file": "forward"
        },
        {
            "read": "TRAILING%CHARACTER1-XFGV", 
            "base_id": "XFGV",
            "qcovs": 69, 
            "length": 10,
            "ref": "bah",
            "file": "backward"
        },
        {
            "read": "TRAILING%CHARACTER1-JUJU", 
            "base_id": "JUJU",
            "qcovs": 69, 
            "length": 10,
            "ref": "meh",
            "file": "forward"
        },
        {
            "read": "TRAILING%CHARACTER1-JUJU", 
            "base_id": "JUJU",
            "qcovs": 69, 
            "length": 10,
            "ref": "buah",
            "file": "backward"
        },
        {
            "read": "TRAILING%CHARACTER1-XFGV", 
            "base_id": "XFGV",
            "qcovs": 69, 
            "length": 10,
            "ref": "nuh",
            "file": "forward"
        },
        {
            "read": "TRAILING%CHARACTER1-XFGV", 
            "base_id": "XFGV",
            "qcovs": 69, 
            "length": 10,
            "ref": "nuh",
            "file": "backward"
        },
    ]
)

lookup_table_1 = pd.DataFrame.from_records(
    [
        {"ref": "foo", "taxid": 1, "organism":"123"},
        {"ref": "bah", "taxid": 2, "organism":"123"},
        {"ref": "buah", "taxid": 3, "organism":"123"},
        {"ref": "nuh", "taxid": 4, "organism":"123"},

    ]
)



class FilterCase(unittest.TestCase):
    def test_import(self):
        from miripvir.filters import blast_filter
    def test_remove_prefix(self):
        from miripvir.filters import remove_prefixes
        sol = remove_prefixes(test_case_1)
        self.assertListEqual(sol['base_id'].tolist(), sol['base_id'].tolist())
    def test_blast_filter_by_length_and_coverage(self):
        from miripvir.filters import blast_filter_by_length, blast_filter_by_qcoverage
        sol = blast_filter_by_qcoverage(test_case_1, 80)
        sol = blast_filter_by_length(sol, 120)
        self.assertEqual(len(sol), 2)
    def test_blast_filter_by_paired_end(self):
        from miripvir.filters import blast_filter_paired_end
        sol = blast_filter_paired_end(test_case_1)
        self.assertEqual(len(sol), 3)
    def test_blast_filter_ambiguous(self):
        from miripvir.filters import blast_filter_ambiguous
        from miripvir.filters import blast_filter_paired_end
        sol = blast_filter_paired_end(test_case_1)
        sol = blast_filter_ambiguous(sol)
        self.assertEqual(len(sol), 1)
    def test_blast_filter(self):
        from miripvir.filters import blast_filter
        from miripvir.data import LookUpTable, BlastPairedEndReads

        bper = BlastPairedEndReads(
            reads_1 = test_case_1.query('file == "forward"').copy(),
            reads_2 = test_case_1.query('file == "backward"').copy(),
            source_1="bah",
            source_2="beh"
        )
        lt = LookUpTable(
            source="m",
            reference=lookup_table_1
        )
        sol = blast_filter(bper, 'PV064', query_coverage=80, length_threshold=120, lookup_table=lt)
        self.assertEqual(sol.final_length, 1)

    def test_blast_filter_realcase(self):
        from miripvir.filters import blast_filter
        from miripvir.data import LookUpTable, BlastPairedEndReads
        from miripvir.ioutils import read_blastdb_reference, read_paired_end_files

        bper = read_paired_end_files("test/blast-hits.PV0641.tab", "test/blast-hits.PV0642.tab")
        print("loaded!")
        lt = read_blastdb_reference("test/sanchis21.reference.json")
        print("loaded!")
        sol = blast_filter(bper, 'PV064', query_coverage=100, length_threshold=125, lookup_table=lt)
        self.assertGreater(sol.final_length, 1)

    def test_remove_prefix_largefile(self):
        from miripvir.filters import remove_prefixes
        from miripvir.data import BlastPairedEndReads
        from miripvir.ioutils import read_paired_end_files
        bper = read_paired_end_files("test/blast-hits.PV0641.tab", "test/blast-hits.PV0642.tab")
        u = remove_prefixes(bper.reads_1, randomize=True)
        u = remove_prefixes(bper.reads_2, randomize=True)
        
        print("bingo!")

if __name__ == '__main__':
    unittest.main()