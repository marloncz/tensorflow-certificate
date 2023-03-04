import csv

from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer


def remove_stopwords(sentence):
    # List of stopwords
    stopwords = [
        "a",
        "about",
        "above",
        "after",
        "again",
        "against",
        "all",
        "am",
        "an",
        "and",
        "any",
        "are",
        "as",
        "at",
        "be",
        "because",
        "been",
        "before",
        "being",
        "below",
        "between",
        "both",
        "but",
        "by",
        "could",
        "did",
        "do",
        "does",
        "doing",
        "down",
        "during",
        "each",
        "few",
        "for",
        "from",
        "further",
        "had",
        "has",
        "have",
        "having",
        "he",
        "he'd",
        "he'll",
        "he's",
        "her",
        "here",
        "here's",
        "hers",
        "herself",
        "him",
        "himself",
        "his",
        "how",
        "how's",
        "i",
        "i'd",
        "i'll",
        "i'm",
        "i've",
        "if",
        "in",
        "into",
        "is",
        "it",
        "it's",
        "its",
        "itself",
        "let's",
        "me",
        "more",
        "most",
        "my",
        "myself",
        "nor",
        "of",
        "on",
        "once",
        "only",
        "or",
        "other",
        "ought",
        "our",
        "ours",
        "ourselves",
        "out",
        "over",
        "own",
        "same",
        "she",
        "she'd",
        "she'll",
        "she's",
        "should",
        "so",
        "some",
        "such",
        "than",
        "that",
        "that's",
        "the",
        "their",
        "theirs",
        "them",
        "themselves",
        "then",
        "there",
        "there's",
        "these",
        "they",
        "they'd",
        "they'll",
        "they're",
        "they've",
        "this",
        "those",
        "through",
        "to",
        "too",
        "under",
        "until",
        "up",
        "very",
        "was",
        "we",
        "we'd",
        "we'll",
        "we're",
        "we've",
        "were",
        "what",
        "what's",
        "when",
        "when's",
        "where",
        "where's",
        "which",
        "while",
        "who",
        "who's",
        "whom",
        "why",
        "why's",
        "with",
        "would",
        "you",
        "you'd",
        "you'll",
        "you're",
        "you've",
        "your",
        "yours",
        "yourself",
        "yourselves",
    ]

    # Sentence converted to lowercase-only
    sentence = sentence.lower()
    # splitting sentence
    sentence = sentence.split()
    # keep only words that are not part of the defined stopwords
    sentence = [word for word in sentence if word not in stopwords]
    # joining remaining words back together
    sentence = " ".join(sentence)

    return sentence


def fit_tokenizer(sentences):
    tokenizer = Tokenizer(oov_token="<OOV>")
    tokenizer.fit_on_texts(sentences)

    return tokenizer


def parse_data_from_file(filename):
    sentences = []
    labels = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        next(reader)

        for row in reader:
            labels.append(row[0])
            sentences.append(remove_stopwords(row[1]))

    return sentences, labels


def get_padded_sequences(tokenizer, sentences):
    # Convert sentences to sequences
    sequences = tokenizer.texts_to_sequences(sentences)

    # Pad the sequences using the post padding strategy
    padded_sequences = pad_sequences(sequences, padding="post")

    return padded_sequences


def tokenize_labels(labels):
    # Instantiate the Tokenizer class
    # No need to pass additional arguments since you will be tokenizing the labels
    label_tokenizer = Tokenizer()

    # Fit the tokenizer to the labels
    label_tokenizer.fit_on_texts(labels)

    # Save the word index
    label_word_index = label_tokenizer.word_index

    # Save the sequences
    label_sequences = label_tokenizer.texts_to_sequences(labels)

    return label_sequences, label_word_index


if __name__ == "__main__":
    sentences, labels = parse_data_from_file("../data/bbc-text.csv")
    tokenizer = fit_tokenizer(sentences)
    word_index = tokenizer.word_index
    print(f"Vocabulary contains {len(word_index)} words\n")

    padded_sequences = get_padded_sequences(tokenizer, sentences)
    print(f"First padded sequence looks like this: \n\n{padded_sequences[0]}\n")
    print(f"Numpy array of all sequences has shape: {padded_sequences.shape}\n")

    label_sequences, label_word_index = tokenize_labels(labels)
    print(f"Vocabulary of labels looks like this {label_word_index}\n")
    print(f"First ten sequences {label_sequences[:10]}\n")
