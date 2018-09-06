import tensorflow as tf
from tinydb import TinyDB
from tensorflow.python.keras.preprocessing import sequence

db = TinyDB('./data/db.json')


# picked arbitrarily, research shows to be kinda default
batch_size = 100

# @TODO how to process entire information efficiently?
"""
The largest genome size to which each other lesser viral genome
should be padded with 0-s (input data needs to have the same length).

In effect getting large 2100 x 1838258 arrays, making model unusable in terms of performance.

Stripped to fixed length, so species are classified by genome samples - fair enough to make it running at least.
"""
LARGEST_GENOME = 1000  # 1838258


"""Labels of nucleotides being converted into numbers"""
genome_dictionary = {
    '': 0,
    'A': 1,
    'G': 2,
    'C': 3,
    'T': 4,
    'U': 4,
}

"""Virus groups (Baltimore Classification) being converted into numbers"""
groups_dictionary = {
    '': 0,
    'unclassified': 0,
    'ssDNA': 1,
    'dsDNA': 2,
    'dsRNA': 3,
    '(-)ssRNA': 4
}


def train():
    """
    Configuring, training, evaluating and making predictions on gathered data within our model rules.
    """
    # retrieving processed data, ready to pipe into Tensorflow Estimators
    genomes, groups = _preprocess_data(db.all())

    # first 1000 genomes/groups for training
    train_x = {'genome': genomes[:1000]}
    train_y = groups[:1000]

    # second 1000 genomes/groups for evaluating
    test_x = {'genome': genomes[1000:2000]}
    test_y = groups[1000:2000]

    # the last 100 genomes/groups for prediction
    pred_x = {'genome': genomes[2000:2100]}
    pred_y = groups[2000:2100]

    """Basic feature_column, operating on each of genomes arrays"""
    feature_column =\
        tf.feature_column.categorical_column_with_identity('genome', num_buckets=len(groups_dictionary))

    """Embedding feature_column, optimizing and allowing for gathering more meaningful information"""
    embedding_column = tf.feature_column.embedding_column(
        feature_column,
        dimension=250  # picked arbitrarily, best setup may differ
    )

    print('[CLASSIFIER SETUP]')
    # Deep Neural Network classifier
    classifier = tf.estimator.DNNClassifier(
        hidden_units=[100],  # picked arbitrarily, best setup may differ
        feature_columns=[embedding_column],
        n_classes=len(groups_dictionary)  # number of options for classifying
    )

    print('[TRAINING]')
    classifier.train(
        input_fn=lambda: _train_input_fn(train_x, train_y),
        steps=len(genomes)  # picked arbitrarily, best setup may differ
    )

    print('[EVALUATING]')
    classifier.evaluate(
        input_fn=lambda: _eval_input_fn(test_x, test_y)
    )

    print('[PREDICTION]')
    predictions = classifier.predict(
        input_fn=lambda: _predict_input_fn(pred_x)
    )

    correct = 0
    for prediction, expect in zip(predictions, pred_y):
        class_id = prediction['class_ids'][0]
        probability = prediction['probabilities'][class_id]

        if class_id == expect:
            correct += 1

        print(class_id, '{:.1f}'.format(100 * probability), expect, str(class_id == expect))
    print('Correct:', correct)


def _preprocess_data(species):
    """Preprocessing genome sequences into list items, with specified numeric boundary"""
    genomes = []
    groups = []

    print('[PREPROCESSING DATA]')
    for specie in species:
        # @TODO sampling genome
        # for performance reasons the `LARGEST_GENOME` is our data limit for training process
        genomes_array = list(specie['genome'])[:LARGEST_GENOME]

        # converting strings to integers indices within array, based on definitions
        numeric_genome = []
        for nucleotide in genomes_array:
            for nucleotide_type in genome_dictionary.keys():
                if nucleotide_type == nucleotide:
                    numeric_genome.append(genome_dictionary[nucleotide_type])

        # converting string to integer index, based on definitions
        numeric_group = int()
        for group_type in groups_dictionary.keys():
            if group_type == specie['group']:
                numeric_group = groups_dictionary[group_type]

        genomes.append(numeric_genome)
        groups.append(numeric_group)

    # @TODO proportions of each group should be even in all datasets

    # padding with 0-s for equal length
    padded_genomes = sequence.pad_sequences(genomes, maxlen=LARGEST_GENOME, padding='post', value=0)

    print('Sample:', '\n', padded_genomes[:3], '\n', groups[:3])

    return padded_genomes, groups


def _train_input_fn(features, labels):
    """convert into Dataset with shuffle & batch"""
    dataset = tf.data.Dataset.from_tensor_slices((features, labels))
    dataset = dataset.shuffle(1000).repeat().batch(batch_size)

    return dataset


def _eval_input_fn(features, labels):
    dataset = tf.data.Dataset.from_tensor_slices((features, labels))
    dataset = dataset.batch(batch_size)

    return dataset


def _predict_input_fn(features):
    dataset = tf.data.Dataset.from_tensor_slices(features)
    dataset = dataset.batch(batch_size)

    return dataset
