from collections import OrderedDict, namedtuple, Counter
from types import MethodType

__all__ = ['BASES', 'CODONS', 'STOP_CODONS', 'AMINO_ACIDS', 'GENETIC_CODE', 'CODON_FOLD', 'MSA']

# Nucleotide and amino acid constants
BASES = 'TCAG'
CODONS = [a+b+c for b in BASES for a in BASES for c in BASES]
STOP_CODONS = ['TGA', 'TAG', 'TAA']
AMINO_ACIDS = 'ARNDCQEGHILKMFPSTWYV'

# Generate genetic code from CODONS and AMINO ACIDS
#
# Description
# -----------
# `transl_code` is an intermediate string with AA letter value at even positions and corresponding count at odd
# positions. `transl_code` creates a new string `transl` of amino acids matching the order of codons in `CODONS`.
# `transl` is created by inserting AA letters into the string based on the number right of it.
#
# Once created, `transl` has the same length as well as order of its corresponding codon in `CODONS`.
# Then, the corresponding codon-AA pair are stored in an OrderedDict `GENETIC_CODE`.
# Note that stop codon 1-letter AA are "*"
#
# Codon-AA pairs can also be retrieved by position in the `GENETIC_CODE` OrderedDict.
# The method `by_index` uses 1-based indexing to retrieve codon-AA pairs such that the first pair in the
# OrderedDict is retrieved using x[1] instead of x[0].
#
transl_code = 'F2L6I3M1V4S4P4T4A4Y2*2H2Q2N2K2D2E2C2*1W1R4S2R2G4'
transl = ''.join([str(a*int(b)) for a, b in zip(transl_code[::2], transl_code[1::2])])
GENETIC_CODE = OrderedDict(zip(CODONS, transl))


def _by_index(self, x):
    assert x - 1 >= 0, IndexError('Value of x must be integer greater than 0.')
    assert x - 1 < len(list(self.items())), IndexError('Value of x cannot be greater than 64.')
    return list(self.items())[x - 1]

GENETIC_CODE.by_index = MethodType(_by_index, GENETIC_CODE)

# Determine degeneracy of genetic code for a particular codon
#
# Description
# -----------
# Codon-AA do not have unique one-to-one correspondence. Many AAs correspond to more than one codon.
# To determine if the AA a particular codon is coding for is degenerate and if so, how many codons code for the same AA
# (-fold degeneracy), the number of times an AA appears as the value in `GENETIC_CODE` is counted and referenced back
# to the particular codon.
_codon_to_aa_count = Counter(GENETIC_CODE.values())
CODON_FOLD = OrderedDict(sorted([(codon, _codon_to_aa_count[aa]) for codon, aa in GENETIC_CODE.items()],
                                key=lambda x: x[1]))

# Multiple sequence alignment object
MSA = namedtuple('MSA', 'ids alignment')
