import unittest
import tempfile

import newick

from .lento import Split, Lento, splits_from_tree
from .cli import parse_args
from .plot import plot_lento


EXPECTED = [
    Split(['A'], support=2, conflict=0),
    Split(['C'], support=1, conflict=0),
    Split(['A', 'B'], support=2, conflict=1),
    Split(['A', 'B', 'C'], support=1, conflict=2),
    Split(['A', 'B', 'C', 'D'], support=1, conflict=0),
    Split(['C', 'D'], support=1, conflict=2),
    Split(['A', 'D'], support=1, conflict=4),
]

TEST_DATA = {
    'A': ['1', '1', '1', '1', '0', '1', '0', '1', '1'],
    'B': ['1', '1', '1', '0', '0', '0', '0', '1', '0'],
    'C': ['1', '1', '0', '0', '1', '0', '1', '0', '0'],
    'D': ['1', '0', '0', '0', '0', '0', '1', '0', '1']
}



class Test_Split(unittest.TestCase):
    def test_repr(self):
        assert repr(Split(["a", "b"])) == 'a:b'
        assert repr(Split(["b", "a"])) == 'a:b'
    
    def test_ntaxa(self):
        assert Split(['a', 'b', 'c']).ntaxa == 3
    
    def test_eq(self):
        assert Split(["a", "b"]) == Split(["a", "b"])
        assert Split(["a", "b"], support=1) != Split(["a", "b"], support=2)
        assert Split(["a", "b"], conflict=1) != Split(["a", "b"], conflict=2)
        assert Split(["a", "b"]) != Split(["a", "c"])
    
    def test_weight(self):
        assert Split(["a", "b"], support=5).support == 5
        assert Split(["a", "b"], conflict=5).conflict == 5
    
    def test_is_conflicting(self):
        s = Split(["a", "b"])
        # no conflict -- singletons
        assert s.is_conflicting(Split(["a"])) is False
        assert s.is_conflicting(Split(["b"])) is False
        # no conflict -- another clade
        assert s.is_conflicting(Split(["c", "d"])) is False
        # no conflict -- nested
        assert s.is_conflicting(Split(["a", "b", "c", "d"])) is False
        # conflict -- small
        assert s.is_conflicting(Split(["a", "c"])) is True
        # conflict -- large
        assert s.is_conflicting(Split(["a", "c", "d", "e", "f", "g"])) is True
    
    def test_sort(self):
        s1 = Split(["a", "b"], support=1)
        s2 = Split(["a", "c"], support=2)
        s3 = Split(["c", "d"], support=4)
        assert s1 < s2
        assert s2 >= s1
        assert s3 > s2 > s1
        assert sorted([s2, s1, s3]) == [s1, s2, s3]
        assert sorted([s2, s1, s3], reverse=True) == [s3, s2, s1]


class Test_Lento(unittest.TestCase):
    def setUp(self):
        self.lento = Lento(TEST_DATA)
    
    def test_nchar(self):
        self.assertEqual(self.lento.ntaxa, 4)

    def test_ntaxa(self):
        self.assertEqual(self.lento.nchar, 9)

    def test_taxa(self):
        self.assertEqual(self.lento.taxa, ['A', 'B', 'C', 'D'])

    def test_total_splits(self):
        self.assertEqual(self.lento.total_splits, 8)

    def test__get_total_splits(self):
        self.assertEqual(Lento()._get_total_splits(17), 65536)

    def test_iter_splits(self):
        for s in self.lento.iter_splits():
            s

    def test_get_splits(self):
        splits = self.lento.get_splits()
        for e in EXPECTED:
            assert repr(e) in splits, "Missing split %s" % e

    def test_get_splits_support(self):
        splits = self.lento.get_splits()
        for e in EXPECTED:
            assert repr(e) in splits, "Missing split %s" % e
            self.assertEqual(e.support, splits[repr(e)].support)

    def test_get_splits_conflict(self):
        splits = self.lento.get_splits()
        for e in EXPECTED:
            assert repr(e) in splits, "Missing split %s" % e
            self.assertEqual(e.conflict, splits[repr(e)].conflict)
    
    def test_summary(self):
        s = self.lento.summary()
        self.assertEqual(s['observed'], 7)  # 7 splits
        self.assertEqual(s['supported'], 9)
        self.assertEqual(s['conflicted'], 9)
        self.assertEqual(s['total'], self.lento.total_splits)
    
    def test_write(self):
        assert self.lento.write()
        with tempfile.NamedTemporaryFile() as f:
            self.lento.write(f.name)


class Test_ParseArgs(unittest.TestCase):
    def test_IOError_on_no_file(self):
        with self.assertRaises(IOError):
            parse_args(['a'])
    
    def test_parse_filename_only(self):
        args = parse_args(['%s' % __file__])
        assert args.input == __file__
        assert args.plot is None  # No output file
        assert args.label is False
    
    def test_parse_filename_and_output(self):
        args = parse_args(['%s' % __file__, '-p', 'test.pdf'])
        assert args.input == __file__
        assert args.plot == 'test.pdf'
        assert args.label is False

    def test_parse_filename_and_output_and_label(self):
        args = parse_args(['%s' % __file__, '-p', 'test.pdf', '--label'])
        assert args.input == __file__
        assert args.plot == 'test.pdf'
        assert args.label is True


class Test_Plot(unittest.TestCase):
    def setUp(self):
        self.lento = Lento(TEST_DATA)
    
    def test(self):
        plot_lento(self.lento)
    
    def test_save(self):
        with tempfile.NamedTemporaryFile() as f:
            plot_lento(self.lento, filename=f.name)
    
    def test_singles(self):
        p = plot_lento(self.lento, singles=False, showlabels=True)
        for o in p.gca().get_xticklabels():
            assert ':' in o.get_text()

    def test_showlabels(self):
        p = plot_lento(self.lento, showlabels=True)
        expected = [repr(s) for s in EXPECTED]
        for o in p.gca().get_xticklabels():
            assert o.get_text() in expected, o.get_text()

        p = plot_lento(self.lento, showlabels=False)
        expected = [str(i) for i in range(0, 8)]
        for o in p.gca().get_xticklabels():
            assert o.get_text() in expected


class Test_SplitsFromTree(unittest.TestCase):
    
    expected = [
        Split(['A'], support=1, conflict=0),
        Split(['B'], support=1, conflict=0),
        Split(['C'], support=1, conflict=0),
        Split(['D'], support=1, conflict=0),
        Split(['E'], support=1, conflict=0),
        Split(['F'], support=1, conflict=0),
        Split(['B', 'C'], support=1, conflict=0),
        Split(['D', 'E', 'F'], support=1, conflict=0),
        Split(['E', 'F'], support=1, conflict=0),
        Split(['B', 'C', 'D', 'E', 'F'], support=1, conflict=0),
        Split(['A', 'B', 'C', 'D', 'E', 'F'], support=1, conflict=0),
    ]
    
    def setUp(self):
        self.tree = newick.loads("(A,((B,C),(D,(E,F))))")[0]
        self.splits = list(splits_from_tree(self.tree))
    
    def test_type(self):
        with self.assertRaises(TypeError):
            list(splits_from_tree("(1,2,3)"))
    
    def test_count(self):
        assert len(self.splits) == len(self.expected)

    def test_expected(self):
        for e in self.expected:
            assert e in self.splits, 'missing %s' % e
    
    def test_expected_reverse(self):
        for s in self.splits:
            assert s in self.expected, 'missing %s' % s
    
    def test_weights(self):
        for s in self.splits:
            assert s.support == 1
            assert s.conflict == 0
    
    def test_print(self):
        o = Lento()
        o._splits = {repr(s): s for s in self.splits}
        print(o.write())


if __name__ == '__main__':
    unittest.main()
