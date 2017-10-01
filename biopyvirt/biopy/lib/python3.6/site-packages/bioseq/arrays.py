from .basetypes import *
import os
import numpy as np
import re
from collections.abc import MutableMapping
from collections import OrderedDict, Counter
import collections
from copy import deepcopy

__all__ = ['SEQTYPES', 'validate_sequence_chars',
           'SequenceArray', 'NucleotideArray', 'ProteinArray', 'CodonArray',
           'SequenceAlignment', 'NucleotideAlignment', 'ProteinAlignment', 'CodonAlignment']

SEQTYPES = ('nucl', 'prot', 'cod')


def validate_sequence_chars(seq, seqtype='nucl'):
    assert isinstance(seq, str), TypeError('seq should be str or string-like.')
    assert seqtype in SEQTYPES, ValueError('seqtype must be "nucl" for nucleotide, "prot" for protein, '
                                           'or "cod" for codon.')
    pattern = '[^{}]'.format(AMINO_ACIDS if seqtype == 'prot' else BASES)
    invalid_chars = set(re.findall(pattern, seq))
    if len(invalid_chars) > 0:
        raise ValueError('Sequence contains invalid characters: {}. Check sequence type or individual sequences.'
                         .format(repr(invalid_chars)))
    return seq


class SequenceArray(MutableMapping):
    """
    Multiple sequence array object constructor

    Stores one or more biological sequences as a set of id (key) - sequence string (value) pair based on its original
    input order by using an OrderedDict container.

    SequenceArray can be instantiated by passing a dictionary-like object whose keys are names or descriptions of their
    corresponding sequence string value. The string value can be a nucleotide sequence (nucl), codon sequence (cod),
    or protein sequence (prot). Note that the string value type, whether 'nucl', 'prot', or 'cod,  must be the same
    for all items in the SequenceArray.

    """

    def __init__(self, input_obj, seqtype='nucl', name='', description='', validate=False):
        """Create a new SequenceArray object from a dictionary, file or FASTA-formatted string.

        Parameters
        ----------
        input_obj : dict or str
            Object used to populate a SequenceArray object. This may be one of the following:
            - Dictionary-like object whose id are sequence record names and values are the corresponding sequences
            - Path to a FASTA file
            - FASTA-formatted string
        seqtype : str
            'nucl' (Nucleotide), 'prot' (Protein), 'cod' (Codon-based)
        name : str
            Name of the set of sequence records
        description : str
            Short description

        """
        assert seqtype in SEQTYPES, ValueError('seqtype must be "nucl" for nucleotide, "prot" for protein, '
                                               'or "cod" for codon.')
        self.seqtype = seqtype
        self.name = name
        self.description = description

        # Key-value pairs where id is the sequence record name and the value is the sequence
        if isinstance(input_obj, dict):
            records = input_obj
            self._ids = list(records.keys())
            self._sequences = list(records.values())
        # String, assumed to be path to FASTA file or contents of FASTA file as a long string
        elif isinstance(input_obj, str):
            # Test if file path
            if os.path.exists(input_obj):
                records = SequenceArray.parse_fasta(input_obj)
                # self._ids = [key.split(' ')[0] for key in records.keys()]
                self._ids = list(records.keys())  # preprocessing already done by parse_fasta method
                self._sequences = list(records.values())
            else:
                raise NotImplementedError('Passing FASTA-formatted strings are not yet supported. '
                                          'Instantiate using an OrderedDict or passing a valid filepath instead.')
        if validate:
            # Check if sequences contain invalid characters
            if seqtype in ('nucl', 'prot'):
                self._sequences = [validate_sequence_chars(_, seqtype=seqtype) for _ in self._sequences]
            else:  # codon seqtype
                pass

    @property
    def ids(self):
        return self._ids

    @ids.setter
    def ids(self, value):
        raise AttributeError('Setting ids using this method is not permitted.')

    @ids.deleter
    def ids(self):
        raise AttributeError('Deleting ids using this method is not permitted.')

    @property
    def sequences(self):
        return self._sequences

    @sequences.setter
    def sequences(self, value):
        raise AttributeError('Setting sequences using this method is not permitted.')

    @sequences.deleter
    def sequences(self):
        raise AttributeError('Deleting sequences using this method is not permitted.')

    def __setitem__(self, key, sequence):
        self.ids.append(key)
        self.sequences.append(sequence)

    def __getitem__(self, keys):
        if isinstance(keys, collections.Iterable) and not isinstance(keys, str):
            return_list = []
            for key in keys:
                if key in self.ids:
                    return_list.append(self.sequences[self.ids.index(key)])
                else:
                    raise KeyError('Key "{0}" does not exist'.format(key))
            return return_list
        else:
            key = keys
            if key in self.ids:
                return self.sequences[self.ids.index(key)]
            else:
                raise KeyError('Key "{0}" does not exist'.format(key))

    def __delitem__(self, key):
        if key in self.ids:
            index = self.ids.index(key)
            self.ids.remove(key)
            self.sequences.pop(index)
        else:
            raise KeyError('Key "{0}" does not exist'.format(key))

    def __iter__(self):
        for key, sequence in zip(self.ids, self.sequences):
            yield (key, sequence)

    def __len__(self):
        return len(self.ids)

    def __repr__(self):
        return 'SequenceArray({0})'.format([(k, v) for k, v in zip(self.ids, self.sequences)])

    def __contains__(self, key):
        return True if key in self.ids else False

    def keys(self):
        for _ in self.ids:
            yield _

    def values(self):
        for _ in self.sequences:
            yield _

    def items(self):
        for x in range(len(self.ids)):
            yield (self.ids[x], self.sequences[x])

    def to_fasta(self, path, linewidth=60):
        """Save sequence array as a FASTA file

        Parameters
        ----------
        path : str
            Filename/path of FASTA file
        linewidth : int
            Line width of FASTA file

        """
        with open(path, 'w') as f:
            print(SequenceArray.array_to_fasta(self.ids, self.sequences, linewidth=linewidth), file=f)

    def align(self, aln_file='out.aln', program='muscle', program_args=None):
        """Calls an external alignment program to align the sequences in the sequence array.

        Parameters
        ----------
        aln_file : str
            Filename/path of resulting multiple sequence alignment
        program : str
            External program to be called for multiple sequence alignment. Currently supported programs are
            'muscle' (Muscle), 'mafft' (MAFFT), 'clustalw' (ClustalW), 'clustalo' (Clustal Omega), 'prank' (PRANK).
            To ensure that this method works properly, make sure that these programs are installed and
            accessible from the system's PATH.
        program_args : str
            Additional user-specified arguments

        Returns
        -------
        SequenceAlignment

        """
        # check if program is in choices or not. if not return an error
        choices = ['muscle', 'mafft', 'clustalo']
        assert program in choices, Exception('Program not supported. Choose from the following: \
        "muscle", "mafft", "clustalw", "clustalo", "prank"')

        # Write the SequenceArray object to file
        seqfile = '{0}.{1}'.format(self.name, 'fna' if self.seqtype == 'nucl' else 'faa')
        self.to_fasta(seqfile)

        # TODO : extract program paths into variables so that users can alter at runtime
        # Default to MUSCLE
        if program == 'mafft':
            cmd_str = 'mafft {args} {i} > {o}'.format(args='--auto' if not program_args else program_args,
                                                      i=seqfile, o=aln_file)
        elif program == 'clustalw':  # TODO : ClustalW hook
            raise Exception('ClustalW support is in development.')
        elif program == 'clustalo':
            cmd_str = 'clustalo -i {i} -o {o} '.format(i=seqfile, o=aln_file)
        elif program == 'prank':  # TODO : PRANK hook
            raise Exception('PRANK support is in development.')
        else:
            # Default to MUSCLE
            cmd_str = 'muscle {args}-in {i} -out {o}'.format(args='' if not program_args else program_args+' ',
                                                             i=seqfile, o=aln_file)
        # TODO : change to subprocess
        os.system(cmd_str)
        if self.seqtype == 'nucl':
            return NucleotideAlignment(aln_file)
        elif self.seqtype == 'prot':
            return ProteinAlignment(aln_file)

    @staticmethod
    def parse_fasta(path, seqtype='nucl'):
        """Read FASTA format entirely using only built-ins.

        Parameters
        ----------
        path : str
            File path (absolute or relative) where the FASTA file is located.
        seqtype : str
            'nucl' (Nucleotide), 'prot' (Protein), 'cod' (Codon-based)

        Returns
        -------
        OrderedDict
            FASTA headers are stored as dictionary keys and its corresponding sequence is stored as its value.

        """
        keys = []
        sequence = ''
        sequences = []
        line_id_re = re.compile('^>(.+)[\s\n]')
        with open(path, 'r') as f:
            for i, line in enumerate(f.readlines()):
                if line.startswith('>'):
                    # TODO : remove when validated to work
                    # line_id = line[1:-1]  # uses the entire description line
                    _match = line_id_re.search(line)  # uses only the string before space
                    try:
                        line_id = _match.group(1)
                    except:
                        raise ValueError('Malformed description line <line {} of {}>'.format(i, path))
                    keys.append(line_id)
                    if sequence:
                        sequences.append(sequence)
                        sequence = ''
                else:
                    sequence += re.sub('\s', '', line.upper())
            if sequence:
                sequences.append(sequence)
        return SequenceArray(OrderedDict(zip(keys, sequences)), seqtype=seqtype)

    @staticmethod
    def array_to_fasta(keys, sequences, linewidth=60):
        """Converts a sequence array to a FASTA-formatted string

        Parameters
        ----------
        keys : list
            List of record names
        sequences : list
            List of sequences (list of lists or 2d ndarray)
        linewidth : int
            Number of characters per line

        Returns
        -------
        str
            FASTA-formatted string

        """
        fasta_str = ''
        for key, sequence in zip(keys, sequences):
            sequence = ''.join(sequence)
            header = '>{0}'.format(key)
            fasta_str += header + '\n'
            for i in range(0, len(sequence), linewidth):
                curr_line = sequence[i:i+linewidth]
                fasta_str += curr_line + '\n'
        return fasta_str

    @staticmethod
    def composition(sequence_obj, seqtype='nucl'):
        """Return the per sequence composition of a sequence array

        Parameters
        ----------
        sequence_obj : SequenceArray
        seqtype : str


        Returns
        -------
        OrderedDict
            Keys are sequence ids and values are OrderedDict of the corresponding percent makeup for each character
            except gaps

        Notes
        -----
        The return value is an OrderedDict of OrderedDicts. First level is indexed by sequence while second level is
        indexed by character.
        >>> seq_array = OrderedDict([('key1', 'AAA'), ('key2', 'TTT')])
        >>> composition_of_seq_array = OrderedDict([ \
            ('key1', OrderedDict([('T', 0), ('C', 0), ('A', 3/float(3)), ('G', 0)])), \
            ('key2', OrderedDict([('T', 3/float(3)), ('C', 0), ('A', 0), ('G', 0)])), ])
        >>> seq_array['key1']
        'AAA'
        >>> composition_of_seq_array['key1']
        OrderedDict([('T', 0), ('C', 0), ('A', 1.0), ('G', 0)])
        >>> composition_of_seq_array['key1']['A']
        1.0

        """
        # assert re.search('^[ATCG\-]+$', sequence), 'Input sequence contains characters other than A,T,C,G,-'
        composition_of = OrderedDict()
        characters = BASES if seqtype in ['nucl', 'cod'] else AMINO_ACIDS
        for seqid, sequence in zip(sequence_obj.ids, sequence_obj.sequences):
            char_counts = Counter(sequence.upper())
            total = sum([v for k, v in char_counts.items() if k != '-'])
            composition_of[seqid] = OrderedDict([(k, char_counts[k]/float(total)) for k in characters])
        # return pd.DataFrame(composition_of)
        return composition_of


class NucleotideArray(SequenceArray):
    """
    Nucleotide sequence array object constructor

    This is a special type of SequenceArray for nucleotide sequences containing additional methods specific for
    handling nucleotide sequence data. On instantiation, it constructs a SequenceArray object whose seqtype is set to
    'nucl'.

    NucleotideArray is suitable for both protein-coding and non-protein coding nucleotide sequences. However,
    if sequences are protein-coding, it is better to use the CodonArray object as this contains methods useful
    for protein-coding sequences such as the ability count by nucleotide triplets and to translate to amino acid
    sequences.

    If the array contains in-frame protein-coding sequence, NucleotideArray can construct a CodonArray using the method
    `to_codonarray`. However, NucleotideArray cannot differentiate by itself whether a sequence is coding or
    non-coding, and if coding, whether it is in-frame or not, therefore it is up to the user to judge
    whether it is appropriate to represent the sequences as plain nucleotides through NucleotideArray or as
    protein-coding sequences through CodonArray.

    """
    def __init__(self, input_obj, name='', description='', validate=False):
        """Create a new NucleotideArray from a dictionary, file or FASTA-formatted string.

        Parameters
        ----------
        input_obj : dict, str
            Object used to populate a SequenceArray object. This may be one of the following:
            - Dictionary-like object whose id are sequence record names and values are the corresponding sequences
            - Path to a FASTA file
            - FASTA-formatted string
        name : str
            Name of the set of sequence records
        description : str
            Short description

        """
        super().__init__(input_obj, name=name, seqtype='nucl', description=description, validate=validate)

    def to_codonarray(self):
        """Create a CodonArray from the current NucleotideArray

        Returns
        -------
        CodonArray

        """
        return CodonArray(deepcopy(self), name=self.name, description=self.description)

    def basecomp(self):
        """Return base composition of each sequence

        Returns
        -------
        OrderedDict
            Keys are sequence ids and values are OrderedDict of the corresponding percent makeup for each character
            except gaps. For example, 'T', 'C', 'A', 'G' for nucleotides.

        Sea also
        --------
        SequenceArray.composition : Character composition of a sequence
        """
        basecomp_of = super().composition(self, seqtype=self.seqtype)
        for key, comp in basecomp_of.items():
            basecomp_of[key]['AT'] = comp['A'] + comp['T']
            basecomp_of[key]['GC'] = comp['G'] + comp['C']
        return basecomp_of

    @staticmethod
    def nucleotide_to_codon(nucleotide_str):
        """Converts a nucleotide triplet into its corresponding codon

        Parameters
        ----------
        nucleotide_str : str or sequence
            Nucleotide sequence (str or list)

        Yields
        ------
        str
            3-character string codon

        """
        if len(nucleotide_str) % 3 != 0:
            raise ValueError('SequenceArray length is not a multiple of three ({0}).'.format(len(nucleotide_str)))
        for j in range(0, len(nucleotide_str), 3):
            if j+3 <= len(nucleotide_str):
                yield nucleotide_str[j:j+3]


class CodonArray(SequenceArray):
    """
    Protein-coding nucleotide sequence array object constructor

    This is a special type of SequenceArray for protein-coding sequences. If the array contains
    in-frame protein-coding sequence, NucleotideArray contains methods to represent data as codons (nculeotide triplets)
    and translate to protein sequence. Note that NucleotideArray cannot differentiate by itself whether a sequence
    is coding or non-coding, therefore it is up to the user to judge whether it is appropriate to use these methods on
    the data.

    """
    def __init__(self, input_obj, name='', description='', validate=False):
        """Create a new CodonArray from a dictionary, file or FASTA-formatted string.

        Parameters
        ----------
        input_obj : dict or str
            Object used to populate a SequenceArray object. This may be one of the following:
            - Dictionary-like object whose id are sequence record names and values are the corresponding sequences
            - Path to a FASTA file
            - FASTA-formatted string
        name : str
            Name of the set of sequence records
        description : str
            Short description

        """
        super().__init__(input_obj, name=name, seqtype='cod', description=description, validate=validate)
        self.pos = OrderedDict()
        self.pos[1] = NucleotideArray(
            OrderedDict([(seqid, ''.join(sequence_as_list))
                         for seqid, sequence_as_list in zip(self.ids,
                                                            map(lambda x: x[0::3], self.sequences))]))
        self.pos[2] = NucleotideArray(
            OrderedDict([(seqid, ''.join(sequence_as_list))
                         for seqid, sequence_as_list in zip(self.ids,
                                                            map(lambda x: x[1::3], self.sequences))]))
        self.pos[3] = NucleotideArray(
            OrderedDict([(seqid, ''.join(sequence_as_list))
                         for seqid, sequence_as_list in zip(self.ids,
                                                            map(lambda x: x[2::3], self.sequences))]))

    @property
    def translated(self):
        """Translates nucleotide sequences into amino acid sequences

        Assumes that the nucleotide sequence is protein-coding, in-frame, and the start of the ORF corresponds
        to the beginning of the nucleotide sequence.

        Returns
        -------
        ProteinArray

        """
        translated_seqarray = OrderedDict()
        for key, nt_seq in zip(self.ids, self.sequences):
            translated_seqarray[key] = ''.join([GENETIC_CODE[cod.upper()]
                                                for cod in NucleotideArray.nucleotide_to_codon(nt_seq)])
        return ProteinArray(translated_seqarray)

    def codonalign(self, codon_aln_file='out.ffn.aln', program='muscle'):
        """Aligns by codons using a protein alignment generated by an external program

        Assumes the sequence is in-frame and is a coding sequences. First, the sequences are translated into proteins,
        which are aligned by an external program. The resulting protein alignment is used as an anchor to align
        nucleotide sequences.

        Parameters
        ----------
        codon_aln_file : str
            File path of resulting codon-aligned multiple sequence alignment
        program : str or path
            External program to be called to align translated protein sequences. Currently supported
            programs are 'muscle' (Muscle), 'mafft' (MAFFT), 'clustalw' (ClustalW), 'clustalo' (Clustal Omega),
            'prank' (PRANK)

        Returns
        -------
        CodonAlignment
            codon-based multiple sequence alignment.

        """
        if self.seqtype != 'nucl':
            raise Exception('Seqtype must be "nucl" (nucleotide) to perform codon alignment.')
        for i, sequence in enumerate(self.sequences):
            if len(sequence) % 3 != 0:
                raise ValueError('"{0}" sequence length is not a multiple of three ({1}).'
                                 .format(self.ids[i], len(sequence)))

        # check if program is in choices or not. if not return an error
        choices = ['muscle', 'mafft', 'clustalo']
        assert program in choices, 'Program not supported. Choose from the following: \
        "muscle", "mafft", "clustalw", "clustalo", "prank"'

        # Write translated SequenceArray object to file
        transl_seqfile = '{0}.transl.{1}'.format(self.name, 'faa')
        self.translated.to_fasta(transl_seqfile)

        # Align protein sequences
        aa_aln = self.translated.align(aln_file=codon_aln_file, program=program)

        # Adjust codons based on amino acid alignment
        codon_aln = OrderedDict()
        i = 0
        for nt_seq, aa_aln_seq in zip(self.sequences, aa_aln.sequences):
            codon = NucleotideArray.nucleotide_to_codon(nt_seq)
            codon_aln[self.ids[i]] = ''.join([next(codon) if aa != '-' else '---' for aa in list(aa_aln_seq)])
            i += 1
        codon_aln = CodonAlignment(codon_aln)
        codon_aln.to_fasta(codon_aln_file)
        return codon_aln

    def basecomp(self):
        """Return base composition of each sequence

        Returns
        -------
        OrderedDict
            Keys are sequence ids and values are OrderedDict of the corresponding percent makeup for each character
            except gaps. For example, 'T', 'C', 'A', 'G' for nucleotides.

        Sea also
        --------
        SequenceArray.composition : Character composition of a sequence
        """
        all_basecomp_of = super().composition(self, seqtype=self.seqtype)
        for key, comp in all_basecomp_of.items():
            all_basecomp_of[key]['AT'] = comp['A'] + comp['T']
            all_basecomp_of[key]['GC'] = comp['G'] + comp['C']

        pos_basecomp_of = {1: super().composition(self.pos[1], seqtype=self.seqtype),
                           2: super().composition(self.pos[2], seqtype=self.seqtype),
                           3: super().composition(self.pos[3], seqtype=self.seqtype),
                           }
        for pos, basecomp_of in pos_basecomp_of.items():
            for key, comp in basecomp_of.items():
                for base in BASES:
                    all_basecomp_of[key][base + str(pos)] = basecomp_of[key][base]
                all_basecomp_of[key]['AT' + str(pos)] = comp['A'] + comp['T']
                all_basecomp_of[key]['GC' + str(pos)] = comp['G'] + comp['C']
        return all_basecomp_of

    # TODO : Subclass string and tuple to create nucl, prot, cod datatypes
    @staticmethod
    def icod(nucl_seq, pos):
        """Retrieves the codon at the specified codon position from a nucleotide sequence

        Parameters
        ----------
        nucl_seq : str
        pos : int

        Returns
        -------
        str
            codon string of length 3

        """
        assert len(nucl_seq) % 3 == 0, ValueError('Sequence is not in multiples of three.')
        assert isinstance(pos, int), ValueError('Position should be an integer value.')
        return nucl_seq[3*pos:(3*pos)+3]


class ProteinArray(SequenceArray):
    def __init__(self, input_obj, name='', description='', validate=False):
        """Create a new ProteinArray from a dictionary, file or FASTA-formatted string.

        Parameters
        ----------
        input_obj : tuple or dict or str
            Object used to populate a SequenceArray object. This may be one of the following:
            - Dictionary-like object whose id are sequence record names and values are the corresponding sequences
            - Path to a FASTA file
            - FASTA-formatted string
        name : str
            Name of the set of sequence records
        description : str
            Short description

        """
        super().__init__(input_obj, name=name, seqtype='prot', description=description, validate=validate)

    def aacomp(self):
        return super().composition(self, seqtype=self.seqtype)


class SequenceAlignment(MutableMapping):
    """
    Multiple sequence alignment base class

    The object specified by this class is a combination of a list of sequence names and a 2d numpy ndarray that
    represents the alignment. Thus, each sequence record is a key-value pairing of a sequence name and its corresponding
    sequence in the ndarray.

    Records can be accessed by its key like a dictionary. In addition, multiple records can be accessed simultaneously
    by passing a list. Record values are returned as a numpy ndarray based on the order of keys passed.

    Methods that permutate the alignment other than adding or deleting records will return a new instance of the
    alignment. No in-place changes take place when using these methods.

    This is the base class for NucleotideAlignment, ProteinAlignment and CodonAlignment.

    """
    def __init__(self, input_obj, seqtype, charsize=1, name='', description=''):
        # TODO : accept FASTA-formatted string
        """Create a new SequenceAlignment from a tuple, dictionary, file or FASTA-formatted string.

        Parameters
        ----------
        input_obj : dict or str
            Alignment objects can be instantiated by passing one of the following:
            - Tuple of list of record names and ndarray of sequences
            - Dictionary-like object
            - File path (absolute or relative)
        seqtype : str
            'nucl' (Nucleotide), 'prot' (Protein), 'cod' (Codon-based)
        charsize : int
            Number of characters that define a column of the alignment.
        name : str
            Name of the set of sequence records
        description : str
            Short description

        """
        # Description
        self.seqtype = seqtype
        self.name = name
        self.description = description
        self.charsize = charsize

        # Tuple containing an ordered list of ids and a numpy array of the sequence
        if isinstance(input_obj, tuple):
            if len(input_obj) == 2:
                if isinstance(input_obj[0], list):
                    self._ids = input_obj[0]
                else:
                    raise TypeError('First item of tuple is not a list.')
                # TODO : obviate the need for importing numpy, possibly by forking tinynumpy to enable character arrays
                if isinstance(input_obj[1], np.ndarray):
                    self._sequences = input_obj[1]
                else:
                    raise TypeError('Second item in tuple is not a numpy ndarray.')
        else:
            list_of_sequences = []

            # dictionary of id as index and sequence stored as str as the value
            if isinstance(input_obj, dict) or isinstance(input_obj, MutableMapping):
                self._ids = []
                for k, v in input_obj.items():
                    if not isinstance(v, str):
                        raise TypeError('SequenceArray "{0}" is not a string.'.format(k))
                    self._ids.append(k)
                    list_of_sequences.append(v)
                # Check if sequences are of equal length
                list_of_sequence_lengths = set([len(s) for s in list_of_sequences])
                if len(list_of_sequence_lengths) > 1:
                    raise ValueError('Unequal sequence lengths.')
            # String path to FASTA file
            elif isinstance(input_obj, str):
                # Check if it is a valid path, and the file exists
                if os.path.exists(input_obj):
                    # Parse FASTA file
                    # fasta_dct = self.parse_fasta(input_obj)
                    fasta_dct = SequenceArray.parse_fasta(input_obj)
                    # Store record ID as list
                    self._ids = list(fasta_dct.keys())
                    list_of_sequences = list(fasta_dct.values())
                # TODO : Test if the string is in FASTA format
                else:
                    raise Exception('Passing FASTA-formatted strings are not yet supported. \
                    Instantiate using an OrderedDict or passing a valid filepath instead.')
            # Store sequences as a numpy array. Order of array rows should correspond to the order of IDs
            # in the record list

            # Check if length is divisible by charsize
            assert len(list_of_sequences[0]) % self.charsize == 0, \
                ValueError('Alignment length is not divisible by 3 ({} nt)'.format(len(list_of_sequences[0])))
            self._sequences = np.array(
                [[seq[j:j+self.charsize] for j in range(0, len(seq), self.charsize) if j+self.charsize <= len(seq)]
                 for seq in list_of_sequences], dtype='U1' if charsize == 1 else 'U3')

        # Size of alignment
        self.count = len(self)
        self.shape = self.sequences.shape  # number of sample, number of units (bases/aa/codons), char per unit
        self.length = self.sequences.shape[1]

    # TODO : Make a "restricted" descriptor for any type of attribute that should not be changed outside of __init__
    # Restrict setting "ids" attribute outside of __init__
    @property
    def ids(self):
        return self._ids

    @ids.setter
    def ids(self, value):
        raise AttributeError('Setting ids using this method is not permitted.')

    @ids.deleter
    def ids(self):
        raise AttributeError('Deleting ids using this method is not permitted.')

    # Restrict setting "sequences" attribute outside of __init__
    @property
    def sequences(self):
        return self._sequences

    @sequences.setter
    def sequences(self, value):
        raise AttributeError('Setting sequences using this method is not permitted.')

    @sequences.deleter
    def sequences(self):
        raise AttributeError('Deleting sequences using this method is not permitted.')

    def __setitem__(self, key, value):
        """Add or update a sequence record

        Parameters
        ----------
        key: str
            Record name
        value: np.ndarray
            Numpy array of the sequence. The length of the added array must be the same as the length of the current
            array.

        """
        if key in self.ids:
            raise KeyError('Key name {0} already in use.'.format(key))
        else:
            # Check if has the same length as the number of cols of the current array
            if len(value) == self.length:
                self.ids.append(key)
                self.sequences = np.vstack(
                    [self.sequences, [value[j:j+self.charsize] for j in range(0, len(value), self.charsize)
                                      if j+self.charsize <= len(value)]])
            else:
                raise ValueError('New sequence length {0} does not match alignment length {1}.'
                                 .format(len(value), self.length))

    def __getitem__(self, keys):
        """Given a key or list of keys, retrieve a record or multiple records

        Parameters
        keys : str or list
            Record name or list of record names

        Returns
        -------
        np.ndarray
            Sequence ndarray or multiple sequence alignment ndarray if a list of keys was passed

        """
        if isinstance(keys, collections.Iterable) and not isinstance(keys, str):
            index_list = []
            for key in keys:
                if key in self.ids:
                    index_list.append(self.ids.index(key))
                else:
                    raise Exception('Key "{0}" does not exist'.format(key))
            return self.sequences[index_list]
        else:
            key = keys
            if key in self.ids:
                index = self.ids.index(key)
            else:
                raise KeyError('Key "{0}" does not exist'.format(key))
            return self.sequences[index]

    def __delitem__(self, key):
        if key in self.ids:
            index = self.ids.index(key)
            self.ids.remove(key)
            self.sequences = np.delete(self.sequences, index, axis=0)  # 0 means by row
        else:
            raise KeyError('Key "{0}" does not exist'.format(key))

    def __iter__(self):
        for key, sequence in zip(self.ids, self.sequences):
            yield key, sequence

    def __len__(self):
        # Return the number of samples in the alignment
        return len(self.ids)

    def __repr__(self):
        return 'keys({0})\n{1}'.format(repr(self.ids), repr(self.sequences))

    def __add__(self, other):
        # Check if self.ids and other.ids match
        if set(self.ids) != set(other.ids):
            raise KeyError('Keys do not match.')
        if self.seqtype != other.seqtype:
            raise ValueError('Seqtypes do not match.')
        other_order = [other.ids.index(key) for key in self.ids]
        return type(self)(
            MSA(ids=self.ids, alignment=np.concatenate((self.sequences, other.sequences[other_order]), axis=1)),
            self.seqtype)

    def __iadd__(self, other):
        return self + other

    def keys(self):
        for _ in self.ids:
            yield _

    def values(self):
        for _ in self.sequences:
            yield _

    def items(self):
        for x in range(len(self.ids)):
            yield (self.ids[x], self.sequences[x])

    def head(self):
        """Retrieves the first 5 entries of the sequence alignment

        Returns
        -------
        SequenceAlignment
            Creates a subset of the current SequenceAlignment containing only the first five entries.

        """
        return type(self)(MSA(ids=self.ids[:5], alignment=self.sequences[:5]), self.seqtype)

    def tail(self):
        """Retrieves the last 5 entries of the sequence alignment

        Returns
        -------
        SequenceAlignment
            Creates a subset of the current SequenceAlignment containing only the last five entries.

        """
        return type(self)(MSA(ids=self.ids[-5:], alignment=self.sequences[-5:]), self.seqtype)

    # noinspection PyTypeChecker
    def colx(self, *args):
        """Returns a length-wise (column range) subset of the alignment

        Parameters
        ----------
        args: int
            Inclusive start and exclusive end position of the subset. Follows Python slice conventions.

        Returns
        -------
        SequenceAlignment
            Create a subset of the current SequenceAlignment containing only the specified column range.

        """
        if len(args) == 1:
            return type(self)(MSA(ids=self.ids, alignment=self.sequences[:, args[0]]), self.seqtype)
        elif len(args) == 2:
            return type(self)(MSA(ids=self.ids, alignment=self.sequences[:, args[0]:args[1]]), self.seqtype)
        elif len(args) == 3:
            return type(self)(MSA(ids=self.ids, alignment=self.sequences[:, args[0]:args[1]:args[2]]),
                              self.seqtype)
        else:
            raise Exception('Method uses 3 integer arguments at most.')

    def subset(self, keys):
        """Returns a row-wise (by sample) subset of the current alignment

        Parameters
        ----------
        keys : str or list
            Record name or list of record names

        Returns
        -------
        SequenceAlignment
            Create a subset of the current SequenceAlignment containing only the specified records.

        """
        return type(self)(MSA(ids=keys, alignment=self[keys]), self.seqtype)

    def labelpartition(self, label, start, end, coding=True):
        NotImplementedError()

    def xgap(self, all=False):
        """Remove columns containing gap character from the current alignment

        Parameters
        ----------
        all : bool
            If True, removes a column only when whole column is gapped.
            If False, removes a column even when only one gap character is present

        Returns
        -------
        SequenceAlignment
            Creates a new SequenceAlignment free of gap characters.
        """
        gapchar = '-'*self.charsize
        xgap_cols = []
        for i in range(self.length):
            if all:
                if not np.all(gapchar == self.sequences[:, i]):
                    xgap_cols.append(i)
            else:
                if not np.any(gapchar == self.sequences[:, i]):
                    xgap_cols.append(i)
        return type(self)(MSA(ids=self.ids, alignment=self.sequences[:, xgap_cols]), self.seqtype)

    def resample_cols(self):
        """Creates a new SequenceAlignment using resampled alignment columns with replacement from the current data

        Returns
        -------
        SequenceAlignment

        """
        randlist = np.random.choice(self.length, self.length, replace=True)
        return type(self)(MSA(ids=self.ids, alignment=self.sequences[:, randlist]), self.seqtype)

    def reorder(self, ordered_key_list):
        """Reorder alignment based on the order of a a given list of keys

        Parameters
        ----------
        ordered_key_list : list
            List of record names arranged based on how samples should be reordered

        Returns
        -------
        SequenceAlignment
            Reordered alignment

        """
        sequences = []
        for key in ordered_key_list:
            index = self.ids.index(key)
            sequences.append(self.sequences[index])
        return type(self)(MSA(ids=ordered_key_list, alignment=np.array(sequences)), self.seqtype)

    def to_fasta(self, path, linewidth=60):
        """Save the alignment as a FASTA-formatted file

        Parameters
        ----------
        path : str
            Filename/path of FASTA file
        linewidth : int
            Number of characters per line

        """
        # TODO : Check if basedir of path exists
        with open(path, 'w') as f:
            print(self.__class__.alignment_to_fasta(self, linewidth=linewidth), file=f)

    def to_phylip(self, path):  # TODO
        NotImplementedError()

    @staticmethod
    def parse_fasta(path, seqtype='nucl', output_type='array'):
        """Read FASTA format entirely using only built-ins.

        Parameters
        ----------
        path : str
            File path (absolute or relative) where the FASTA file is located.
        seqtype : str
            'nucl' (Nucleotide), 'prot' (Protein), 'cod' (Codon-based)
        output_type : 'array', 'aln', optional (default = 'array')
            Choose between output as array (array) or an alingment (aln)

        Returns
        -------
        OrderedDict
            FASTA headers are stored as dictionary keys and its corresponding sequence is stored as its value.

        """
        lengths = set()
        seq_array = SequenceArray.parse_fasta(path)
        for key, seq in seq_array.items():
            lengths.add(len(seq))
        if output_type == 'ndarray':
            if len(lengths) == 1:
                return SequenceAlignment(seq_array, seqtype)
        elif output_type == 'dict':
            return seq_array

    @staticmethod
    def concat(*alignments):
        """Concatenate multiple sequence alignments together

        Parameters
        ----------
        alignments : SequenceAlignment

        Returns
        -------
        SequenceAlignment
            New concatenated SequenceAlignment

        """
        concaternated_alignment = alignments[0]
        for alignment in alignments[1:]:
            concaternated_alignment += alignment
        return concaternated_alignment

    @staticmethod
    def alignment_to_fasta(alignment, linewidth=60):
        """Save the alignment as a FASTA-formatted file

        Parameters
        ----------
        alignment : SequenceAlignment
        linewidth : int
            Number of characters per line

        Returns
        -------
        str
            FASTA-formatted string

        """
        return SequenceArray.array_to_fasta(alignment.ids, alignment.sequences, linewidth=linewidth)

    @staticmethod
    def composition(alignment_obj, seqtype='nucl'):
        """Returns the character composition of the sequence alignment

        Parameters
        ----------
        alignment_obj : SequenceAlignment
        seqtype : str
            'nucl' (Nucleotide), 'prot' (Protein), 'cod' (Codon-based)

        Returns
        -------
        OrderedDict

        """
        sequence_obj = SequenceArray(
            OrderedDict([(seqid, ''.join(sequence_as_list))
                         for seqid, sequence_as_list in zip(alignment_obj.ids, alignment_obj.sequences)]))
        return SequenceArray.composition(sequence_obj, seqtype=seqtype)


class NucleotideAlignment(SequenceAlignment):

    def __init__(self, input_obj, name='', description=''):
        """Create a new NucleotideAlignment from a tuple, dictionary, file or FASTA-formatted string.

        Parameters
        ----------
        input_obj : tuple or dict or str
            Alignment objects can be instantiated by passing one of the following:
            - Tuple of list of record names and ndarray of sequences
            - Dictionary-like object
            - File path (absolute or relative)
        name : str
            Name of the set of sequence records
        description : str
            Short description

        """
        super().__init__(input_obj, 'nucl', charsize=1, name=name, description=description)

    def basecomp(self):
        """Returns the base composition of the current nucleotide alignment

        Returns
        -------
        OrderedDict

        """
        basecomp_of = super().composition(self, seqtype=self.seqtype)
        for key, comp in basecomp_of.items():
            basecomp_of[key]['AT'] = comp['A'] + comp['T']
            basecomp_of[key]['GC'] = comp['G'] + comp['C']
        return basecomp_of


class ProteinAlignment(SequenceAlignment):

    def __init__(self, input_obj, name='', description=''):
        """Create a new ProteinAlignment from a tuple, dictionary, file or FASTA-formatted string.

        Parameters
        ----------
        input_obj : tuple or dict or str
            Alignment objects can be instantiated by passing one of the following:
            - Tuple of list of record names and ndarray of sequences
            - Dictionary-like object
            - File path (absolute or relative)
        name : str
            Name of the set of sequence records
        description : str
            Short description

        """
        super().__init__(input_obj, 'prot', charsize=1, name=name, description=description)

    def aacomp(self):
        return super().composition(self, seqtype=self.seqtype)


class CodonAlignment(NucleotideAlignment):

    def __init__(self, input_obj, name='', description=''):
        """Create a new CodonAlignment from a tuple, dictionary, file or FASTA-formatted string.

        Parameters
        ----------
        input_obj : tuple or dict or str
            Alignment objects can be instantiated by passing one of the following:
            - Tuple of list of record names and ndarray of sequences
            - Dictionary-like object
            - File path (absolute or relative)
        name : str
            Name of the set of sequence records
        description : str
            Short description

        """
        SequenceAlignment.__init__(self, input_obj, seqtype='cod', charsize=3, name=name, description=description)
        # Create nucleotide alignment
        ntaln_lst = list()
        for seq in self.sequences:
            ntaln_concat = list()
            for seq_seq in seq:
                ntaln_concat.append(''.join(seq_seq))
            ntaln_lst.append(''.join(ntaln_concat))
        self.nucl_aln = NucleotideAlignment(
            MSA(ids=self.ids, alignment=np.array(np.array([list(seq) for seq in ntaln_lst], dtype='U1'), dtype='U1')))

        self.pos = OrderedDict()
        self.pos[1] = self.nucl_aln.colx(0, None, 3)
        self.pos[2] = self.nucl_aln.colx(1, None, 3)
        self.pos[3] = self.nucl_aln.colx(2, None, 3)

    def make_raxml_codon_partition_file(self, save_path):
        """Make RAxML partition file for a codon alignment

        Parameters
        ----------
        save_path: str
            Partition file save path

        """
        # TODO : check if basedir of save_path exists
        ordinal_suffix = {1: 'st', 2: 'nd', 3: 'rd', 4: 'th', 5: 'th', 6: 'th', 7: 'th', 8: 'th', 9: 'th', 0: 'th'}
        # TODO : Warn if file already exists
        with open(save_path, 'w') as f:
            for i in range(1, 4):
                print('DNA, {0}{1}pos={0}-{2}\\3'.format(i, ordinal_suffix[i], self.length*3), file=f)

    @staticmethod
    def composition(codon_aln_obj, fold_counts=(), pos=3):
        """Return the character composition of a CodonAlignment depending on codon position and fold count

        Parameters
        ----------
        codon_aln_obj : CodonAlignment
        fold_counts : int
            1,2,3,4,6 fold codon degeneracy
        pos : int
            1 (1st position), 2 (2nd position), 3 (3rd position)

        Returns
        -------
        OrderedDict

        """
        pos -= 1  # input is 1-indexed but Python is 0-indexed
        codon_filter_set = set([codon for codon, fold in CODON_FOLD.items() if fold in fold_counts])
        filtered_sequences = OrderedDict()
        for seqid, seq_ndarray in codon_aln_obj.items():
            if pos == -1:
                filtered_sequences[seqid] = ''.join(
                    [codon for codon in seq_ndarray if codon in codon_filter_set]
                )
            else:
                filtered_sequences[seqid] = ''.join(
                    [codon[pos] for codon in seq_ndarray if codon in codon_filter_set]
                )
        sequence_obj = SequenceArray(filtered_sequences)
        return SequenceArray.composition(sequence_obj, seqtype='cod')
