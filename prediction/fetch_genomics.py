import ftputil
import os
import shutil
import tempfile
import re
import random
import gzip
import pathlib

HOST = 'ftp.ncbi.nlm.nih.gov'
FTP_WORKDIR = '/genomes/refseq/viral'

# structure
LATEST_ASSEMBLY = 'latest_assembly_versions'

# entire species count to fetch
DATA_LIMIT = 2100


def fetch():
    """
    Downloads viral genomes from NCBI datasets with associated metadata,
    saving those temporary and unarchiving into `data/raw` folder.

    The folder is named after virus specie and contains genomic .fna file
    with .gbff containing the genome (unused) and metadata.

    Preserves upper `DATA_LIMIT` and maintains to be idempotent,
    being safe in multiple runs, leading to the same results.
    """
    def _save_to_specie_dir(file_patterns):
        """Saving to directory closure, for handling multiple files"""
        for pattern in file_patterns:
            regex = re.compile(pattern, re.I)
            found = list(filter(regex.match, files_in_specie))

            fd, path = tempfile.mkstemp()
            try:
                host.download(found[0], path)

                with gzip.open(path) as file:
                    pathlib.Path('data/raw/' + specie).mkdir(exist_ok=True)
                    file_name = 'data/raw/' + specie + '/' + found[0].replace('.gz', '')

                    with open(file_name, 'wb') as extracted_file:
                        shutil.copyfileobj(file, extracted_file)

                        print('[SAVED]:', file_name)
            finally:
                os.remove(path)

        print('[COUNT]: specie no. -', len(_count_files_without_hidden('data/raw')), 'of', DATA_LIMIT)

    # ensure path existence
    pathlib.Path('data/raw')\
        .mkdir(parents=True, exist_ok=True)

    # noinspection PyDeprecation
    with ftputil.FTPHost(HOST, 'anonymous', '') as host:
        print('[CONNECTED]')
        host.chdir(FTP_WORKDIR)
        species = host.listdir(host.curdir)

        species_num = DATA_LIMIT - len(_count_files_without_hidden('data/raw'))
        print('[START]: path -', FTP_WORKDIR)
        print('[STATUS]: in species - viruses, num:', len(species), ', like:', random.sample(species, 10))

        if species_num <= 0:
            raise ValueError('Already filled limit of:', DATA_LIMIT)

        try:
            for specie in random.sample(species, species_num):
                try:
                    latest_data_dir = specie + '/' + LATEST_ASSEMBLY
                    host.chdir(latest_data_dir)
                except Exception as e:
                    print('[ERROR]: latest data folder does not exist', str(e))
                    continue

                # there is always single file inside (structure pattern)
                dir_contents = host.listdir(host.curdir)
                specie_dir = dir_contents[0]

                host.chdir(specie_dir)
                files_in_specie = host.listdir(host.curdir)

                _save_to_specie_dir(
                    [specie_dir + '_genomic\.fna.*',
                     specie_dir + '_genomic\.gbff.*']
                )

                # back to root of species
                host.chdir(FTP_WORKDIR)
        except Exception as e:
            print('[ERROR]:', str(e))
        finally:
            files = _count_files_without_hidden('data/raw')
            print('[FINISHED]: found species -', species_num, ', saved -', len(files))


def _count_files_without_hidden(path):
    """Returns files list without hidden unix .files"""
    return [name for name in os.listdir(path) if not name.startswith('.')]
