from tinydb import TinyDB

db = TinyDB('./data/db.json')


def analyze():
    """Shows basic information about stored genomes, eg crucial 'Lagest genome' or groups counts"""
    print('[STATS]')
    stats = {
        'All species': len(db.all()),
        'Largest genome': _largest_genome(),
    }

    _print_dictionary(stats.items())

    # @TODO rewrite into single entire db iteration
    print('Groups')
    _print_dictionary(_count_groups().items())


def _print_dictionary(dictionary):
    """Fancy-print the dictionary into console"""
    for key, value in dictionary:
        print('{}: {}.'.format(key, value))


def _count_groups():
    """Labels and numbers of respective species in groups"""
    groups = {}

    for specie in db:
        group = specie['group']

        if group not in groups:
            groups[group] = 1
        else:
            groups[group] += 1

    return groups


def _largest_genome():
    """Largest genome in database"""
    size = 0

    for specie in db:
        curr_size = len(specie['genome'])

        if size < curr_size:
            size = curr_size

        if curr_size == 1838258:
            print(specie['specie'])

    return size
