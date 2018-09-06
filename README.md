# Tensorflow Prediction
Collection of scripts being used in building Deep Neural Network Tensorflow Model for viral genomes classification.
 
 From data fetching, through clearing and storing the unified dataset within in-file DB, to Estimator based production-ready prediction classificator.

## Model & Motivation

The genomes contains raw biological information about species and could be reasonable factor for classification based on chains of nucleotides.

Where the human would find it difficult to maintain, the machine (ML) can use it's operational capabilities to predicate basing on genomes like DNA/RNA.

After many adjustments to fit the case into rough borders of minimal resources and simplicity (just for experimentation & personal research), the gathered genomes of viruses are used to predicate by it into 7 taxonomy groups ([Baltimore Classification](https://en.wikipedia.org/wiki/Virus#Classification)):

```
I: dsDNA viruses (e.g. Adenoviruses, Herpesviruses, Poxviruses)
II: ssDNA viruses (+ strand or "sense") DNA (e.g. Parvoviruses)
III: dsRNA viruses (e.g. Reoviruses)
IV: (+)ssRNA viruses (+ strand or sense) RNA (e.g. Picornaviruses, Togaviruses)
V: (−)ssRNA viruses (− strand or antisense) RNA (e.g. Orthomyxoviruses, Rhabdoviruses)
VI: ssRNA-RT viruses (+ strand or sense) RNA with DNA intermediate in life-cycle (e.g. Retroviruses)
VII: dsDNA-RT viruses DNA with RNA intermediate in life-cycle (e.g. Hepadnaviruses)
```

Accomplished partially with less than moderate results.

## Installation

Will install python setup based on pip's freezed `requirements.txt`.

```
make install
```

### Fetch genomes data from NCBI
Fetches viruses genomes and metadata to text files in specific specie directory.

```
make fetch_data
```

### Store genomes with metadata into database
Processes saved files from `fetch` and stores them normalized and unified in JSON format file (TinyDB).

```
make store_into_db
```

### Train the genomes prediction model
Train the neural network and watch the prediction result 👊

```
make train
```

#### Analyze stored data
Show basic information about stored species and their genomes (eg count, largest genome, groups counts etc).

```
make analyze_data
```

## Highly influenced by (many thanks 👏) 

- [NCBI Genomes Database](https://www.ncbi.nlm.nih.gov/nuccore/176120924)
- [Tensorflow Basic Text Classification Tutorial](https://www.tensorflow.org/tutorials/keras/basic_text_classification)
- [Tensorflow feature_columns](https://www.tensorflow.org/guide/feature_columns)
- [Tensorflow premade_estimators](https://www.tensorflow.org/guide/premade_estimators)
- [Sebastian Ruder's Text Classification with Estimators tutorial](http://ruder.io/text-classification-tensorflow-estimators/) ([Source](https://github.com/eisenjulian/nlp_estimator_tutorial/blob/master/nlp_estimators.py))
- [Text Classification with the High Level API](https://medium.com/quantitative-technologies/text-classification-with-the-high-level-tensorflow-api-390809987a4f) ([Source](https://github.com/quantitative-technologies/tensorflow-text-classification/blob/master/perceptron.py))
