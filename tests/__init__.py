import sys, os, gc
import subprocess

thisdir = os.path.dirname(__file__)
libdir = os.path.abspath(os.path.join(thisdir, '..', 'screed'))
sys.path.insert(0, libdir)
from screed import screedDB
import toFasta
import toFastq
from screed import rfqs as read_fastq_sequences
#from screed import read_fastq_sequences
from screed import read_fasta_sequences
from seqparse import read_hava_sequences
from dbConstants import fileExtension

testfa = os.path.join(thisdir, 'test.fa')
testfq = os.path.join(thisdir, 'test.fastq')
testha = os.path.join(thisdir, 'test.hava')

def setup():
    # index databases
    read_fasta_sequences(testfa)
    read_hava_sequences(testha)
    read_fastq_sequences(testfq)

def teardown():
    os.unlink(testfq + fileExtension)
    os.unlink(testfa + fileExtension)
    os.unlink(testha + fileExtension)

class Test_hava_methods(object):
    """
    Make sure that screed can retrieve even retrieve data from
    imaginary filetypes, like HAVA
    """
    def setup(self):
        self.db = screedDB(testha)

    def test_contains(self):
        assert "test_006" in self.db

    def test_beginning_key_retrieval(self):
        result = self.db['test_000']
        assert result.hava == 'test_000'
        assert result.quarzk == 'ACGGTGACGGTCACCGTCGACGGCCCAAGCCCATCGAACG'\
               'TACCACCCCCACCTATCGTCACGCTGGTGGAGAGCCAATG'
        assert result.muchalo == 'AFPPCLHBCCILGMMOCHKNNDBKCCPNHAMKJOCCDJA'\
               'OEPNMHFHCBAJOKEMMMBHCPHIOAEPFFCAOJPGIMKGK'
        assert result.fakours == '218583165871861127719451483455294521865'\
               '68176931571171542294878855181415261425688'
        assert result.selimizicka == 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'\
               'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'
        assert result.marshoon == 'C7AF246AC7AAEABE5A557FCBC6FD5F5263BCDE'\
               '4E745BEF1GG7DD1AB511GBC63A4GF1F4E1A154B35D'

    def test_middle_key_retrieval(self):
        result = self.db['test_0063']
        assert result.hava == 'test_0063'
        assert result.quarzk == 'CAACACGATCAAGTTTGGTAAGAATTCCGCCTTAAGCTTT'\
               'CTAGAACGATAGTTGCCCCCAATCTGGTTCGAAATCTCTT'
        assert result.muchalo == 'GMDAPLMOOFANDHHMLBPIKGHIAFFFOABFMNNJNIJ'\
               'ILEEFEPOCAJLNDLIFBPMGKOFJIEFAHNJPIOFAJMLM'
        assert result.fakours == '392363971393898522756138876485334274384'\
               '39122136418369146118333919885587613673488'
        assert result.selimizicka == 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'\
               'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'
        assert result.marshoon == 'FC25E2CFC2BAFA7A2AA4757F3GFFFEE37G7752'\
               'FCDBAEADBA1AC7374FB5C15552E6E2GG6GFF62C6GE'

    def test_end_key_retrieval(self):
        result = self.db['test_00124']
        assert result.hava == 'test_00124'
        assert result.quarzk == 'ATCGCAACCGTTTCCCCTATCTGGCAATTGAATCCGCGTC'\
               'CTAAAACGAAAGCTTATCCCTGGCGAGGCACGCTAGGCCT'
        assert result.muchalo == 'CIHNCECANFNLKGCHNOEHJDHADHPAEMMNKGMMMPD'\
               'OBMOCKNBCMCPHEBEOINHMBMMGCHEMOIOAPEFPDDJP'
        assert result.fakours == '327364511483537131695325595876269716778'\
               '14946924334424648676283848861393812686731'
        assert result.selimizicka == 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'\
               'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'
        assert result.marshoon == '4FE5FDD76CC5DE4DC2F25AA2GFBD7BEG326C6D'\
               '7AB5B71GA67BAFD63AE1A562CDC1C2D157G6EF17CD'


class Test_fastq(object):
    def setup(self):
        self.db = screedDB(testfq)

    def test_length(self):
        assert len(self.db) == 125

    def test_keys(self):
        for key in self.db:
            assert key == self.db[key].name

    def test_id_retrieval(self):
        for key in self.db:
            record = self.db[key]
            intRcrd = self.db.loadRecordByIndex(record.id)
            assert record == intRcrd

    def test_contains_front(self):
        first = self.db[self.db.keys()[0]]
        assert first.id == 0
        assert first.name == 'HWI-EAS_4_PE-FC20GCB:2:1:492:573/2'
        assert first.sequence == 'ACAGCAAAATTGTGATTGAGGATGAAGAACTGCTGT'
        assert first.accuracy == 'AA7AAA3+AAAAAA.AAA.;7;AA;;;;*;<1;<<<'

    def test_contains_middle(self):
        middle = self.db[self.db.keys()[62]]
        assert middle.id == 62
        assert middle.name == 'HWI-EAS_4_PE-FC20GCB:2:1:245:483/2'
        assert middle.sequence == 'TGTCGAGCAAAGCAAAACAGGCGTAAAAATTGCCAT'
        assert middle.accuracy == 'AAAAAAAAAAAAAAAAAAAAA>AAAAAAAA?9>6><'

    def test_contains_end(self):
        end = self.db[self.db.keys()[124]]
        assert end.id == 124
        assert end.name == 'HWI-EAS_4_PE-FC20GCB:2:1:350:588/2'
        assert end.sequence == 'GGTACAAAATAGATGCTGGACTCTCCGAATCCTATA'
        assert end.accuracy == ';?5AAAAAAAAAA?A??;?AA;AAA>AAAA?4?844'

    def test_contains(self):
        for k in self.db:
            assert self.db.has_key(k)

        assert self.db.get('FOO') == None

        assert not 'FOO' in self.db

    def test_iterv(self):
        entries = []
        for entry in self.db:
            entries.append(self.db[entry])

        ivalues = list(self.db.itervalues())
        assert sorted(entries) == sorted(ivalues)

    def test_iteri(self):
        for id, entry in self.db.iteritems():
            assert id == self.db[entry.name].id
            assert entry == self.db[entry.name]

class Test_fasta(object):
    def setup(self):
        self.db = screedDB(testfa)

    def test_length(self):
        assert len(self.db) == 22

    def test_keys(self):
        for key in self.db:
            assert key == self.db[key].name

    def test_id_retrieval(self):
        for key in self.db:
            record = self.db[key]
            intRcrd = self.db.loadRecordByIndex(record.id)
            assert record == intRcrd

    def test_contains_front(self):
        first = self.db[self.db.keys()[0]]
        assert first.id == 0
        assert first.name == 'ENSMICT00000012722'
        assert first.description == 'cdna:pseudogene scaffold:micMur1:'\
               'scaffold_185008:9:424:1 gene:ENSMICG00000012730'
        assert str(first.sequence).startswith('TGCAGAAAATATCAAGAGTCAGC'\
                                              'AGAAAAACTATACAAGGGCTGGT'\
                                              'ATTTTGATTATTCT')

    def test_contains_middle(self):
        middle = self.db[self.db.keys()[10]]
        assert middle.id == 10
        assert middle.name == 'ENSMICT00000012078'
        assert middle.description == 'cdna:pseudogene scaffold:micMur1'\
               ':scaffold_180699:3:774:-1 gene:ENSMICG00000012085'
        assert str(middle.sequence).startswith('GCGCACTCCCAGTGGCTACCCA'\
                                               'CGGCAGGAGGCGGCGGCAGTGA'\
                                               'CTGGGCCGGCGGCCCG')

    def test_contains_end(self):
        end = self.db[self.db.keys()[21]]
        assert end.id == 21
        assert end.name == 'ENSMICT00000003880'
        assert end.description == 'cdna:novel scaffold:micMur1:scaffol'\
               'd_175819:130:631:1 gene:ENSMICG00000003884'
        assert str(end.sequence).startswith('ATGCTGCCTAAGTTTGACCCCAACG'\
                                            'CGATCAAAGTCATGTACCTGAGGTG'\
                                            'CACGGGTGGC')

    def test_contains(self):
        for k in self.db:
            assert self.db.has_key(k)

        assert self.db.get('FOO') == None

        assert not 'FOO' in self.db

    def test_iterv(self):
        entries = []
        for entry in self.db:
            entries.append(self.db[entry])

        ivalues = list(self.db.itervalues())
        assert sorted(entries) == sorted(ivalues)

    def test_iteri(self):
        for id, entry in self.db.iteritems():
            assert id == self.db[entry.name].id
            assert entry == self.db[entry.name]

class Test_fasta_recover(Test_fasta):
    """
    Test the functionality of the recovery script to take a screedDB to a
    fasta file and back again
    """
    def setup(self):
        self._fileName = os.path.join(thisdir, 'fastaRecovery')
        toFasta.toFasta(testfa, self._fileName)
        read_fasta_sequences(self._fileName)
        self.db = screedDB(self._fileName)

    def teardown(self):
        os.unlink(self._fileName)
        os.unlink(self._fileName + fileExtension)

class Test_fastq_recover(Test_fastq):
    """
    Test the functionality of the recovery script to take a screedDB to a
    fastq file and back again
    """
    def setup(self):
        self._fileName = os.path.join(thisdir, 'fastqRecovery')
        toFastq.toFastq(testfq, self._fileName)
        read_fastq_sequences(self._fileName)
        self.db = screedDB(self._fileName)

    def teardown(self):
        os.unlink(self._fileName)
        os.unlink(self._fileName + fileExtension)

class Test_fasta_shell(Test_fasta):
    """
    Tests the functionality of the script 'fadbm' in creating a
    screed database correctly from the shell
    """
    def setup(self):
        os.unlink(testfa + fileExtension)
        fadbm = os.path.join(libdir, 'fadbm.py')
        subprocess.check_call([fadbm, testfa], stdout=subprocess.PIPE)
        self.db = screedDB(testfa)

    def teardown(self):
        read_fasta_sequences(testfa)    

class Test_fastq_shell(Test_fastq):
    """
    Tests the functionality of the script 'fqdbm' in creating a
    screed database correctly from the shell
    """
    def setup(self):
        os.unlink(testfq + fileExtension)
        fqdbm = os.path.join(libdir, 'fqdbm.py')
        subprocess.check_call([fqdbm, testfq], stdout=subprocess.PIPE)
        self.db = screedDB(testfq)

    def teardown(self):
        read_fastq_sequences(testfq)

class Test_dict_methods(object):
    """
    Make sure that screed returns sensible results for standard dictionary
    queries.
    """
    def setup(self):
        self.db = screedDB(testfa)

    def test_iter_stuff(self):
        db = self.db
        keys = db.keys()
        ikeys = list(db.iterkeys())
        assert sorted(keys) == sorted(ikeys)

        values = db.values()
        ivalues = list(db.itervalues())
        assert sorted(values) == sorted(ivalues)

        items = db.items()
        iitems = list(db.iteritems())
        assert sorted(items) == sorted(iitems)

    def test_contains(self):
        for k in self.db:
            assert self.db.has_key(k)

        assert db.get('FOO') == None

        assert not self.db.has_key('FOO')
            
    def test_contains(self):
        for k in self.db:
            assert k in self.db

        assert not 'FOO' in self.db

    def test_get(self):
        for k in self.db:
            record = self.db.get(k)
            assert record.name == k

            record = self.db[k]
            assert record.name == k

        try:
            self.db['FOO']
            assert False, "the previous line should raise a KeyError"
        except KeyError:
            pass

    def test_missing(self):
        """
        Make sure that unsupported dict attributes are actually missing.
        """
        db = self.db

        try:
            db.clear()
            assert 0
        except AttributeError:
            pass

        try:
            db.update({})
            assert 0
        except AttributeError:
            pass

        try:
            db.setdefault(None)
            assert 0
        except AttributeError:
            pass

        try:
            db.pop()
            assert 0
        except AttributeError:
            pass

        try:
            db.popitem()
            assert 0
        except AttributeError:
            pass
