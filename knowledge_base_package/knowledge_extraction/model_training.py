from SimilarSentences import SimilarSentences
import shutil


def train_model():
    shutil.rmtree('./model', ignore_errors=True)
    shutil.rmtree('./trained_model', ignore_errors=True)
    model = SimilarSentences('sentences.txt', "train")
    model.train()


def find_similarity(quest, n_sentences):
    model = SimilarSentences('model.zip', "predict")

    text = quest
    text = text.lower()

    simple = model.predict(text, n_sentences, "simple")
    detailed = model.predict(text, n_sentences, "detailed")
    print(simple)
    print(detailed)

    return simple, detailed
