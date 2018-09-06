import os
from tinydb import TinyDB

db = TinyDB('./data/db.json')

DATA_DIR = 'data/raw'


def store():
    """
    AWARE: destructive operation, will purge the database prior to fill.

    Inserts genomes (previously downloaded with `fetch_genomics.py`)
    into database with associated metadata in unified format.
    """
    db.purge()
    print('[STATUS]: database purged')

    for specie_dir in _files_without_hidden(DATA_DIR):
        specie = specie_dir
        description = {}
        group = 'unclassified'
        genome = ''

        specie_files = DATA_DIR + '/' + specie_dir
        for file_name in _files_without_hidden(specie_files):
            with open(specie_files + '/' + file_name) as file:
                if '.fna' in file_name:
                    for index, line in enumerate(file, start=1):

                        if line.startswith('>'):
                            description[index] = line.rstrip('\n')
                        else:
                            genome += (line.rstrip('\n')).upper()
                elif '.gbff' in file_name:
                    group = _match_specie_group(file.read())

        db.insert({
            'specie': specie,
            'description': description,
            'group': group,
            'genome': genome
        })

        print('[INSERTED]:', specie)

    print('[FINISHED]')


def _match_specie_group(file_metadata):
    """
    Classifies the virus taxonomy group from NCBI based
    structure to broadly used Baltimore Classification

    Based on https://en.wikipedia.org/wiki/Virus#Classification

    Baltimore Classification:
        I: dsDNA viruses (e.g. Adenoviruses, Herpesviruses, Poxviruses)
        II: ssDNA viruses (+ strand or "sense") DNA (e.g. Parvoviruses)
        III: dsRNA viruses (e.g. Reoviruses)
        IV: (+)ssRNA viruses (+ strand or sense) RNA (e.g. Picornaviruses, Togaviruses)
        V: (−)ssRNA viruses (− strand or antisense) RNA (e.g. Orthomyxoviruses, Rhabdoviruses)
        VI: ssRNA-RT viruses (+ strand or sense) RNA with DNA intermediate in life-cycle (e.g. Retroviruses)
        VII: dsDNA-RT viruses DNA with RNA intermediate in life-cycle (e.g. Hepadnaviruses)
    """
    # NCBI based taxonomy
    # https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?mode=Undef&id=10239&lvl=3&lin=f&keep=1&srchmode=1&unlock
    groups_patterns = [
        '; dsDNA viruses, no RNA stage; ',
        '; ssDNA viruses; ',
        '; dsRNA viruses; ',
        '; ssRNA positive-strand viruses, no DNA stage; ',
        '; ssRNA negative-strand viruses; ',
        # '; ',  # no clear match with VI from taxonomy
        # '; '  # no clear match with VII
    ]

    groups = [
        'dsDNA',
        'ssDNA',
        'dsRNA',
        '(+)ssRNA',
        '(-)ssRNA',
        'ssRNA-RT',
        'dsDNA-RT'
    ]

    for pattern in groups_patterns:
        if pattern in file_metadata:
            return groups[groups_patterns.index(pattern)]

    return 'unclassified'


def _files_without_hidden(path):
    """Returns files list without hidden unix .files"""
    return [name for name in os.listdir(path) if not name.startswith('.')]
