""" File contains spacyPrediction singleton class for prediction """
from spacy.cli import download
from spacy.util import get_installed_models
import spacy

# Download spacy model file
if not get_installed_models():
    download('en_core_web_trf')


class SpacyPrediction:
    """ class help to perform spacy based NER prediction """
    __instance = None

    def __init__(self) -> None:
        if SpacyPrediction.__instance is not None:
            raise Exception(
                "Not possible to create more than one spacy model instance")
        self.__connect()

    @classmethod
    def __connect(cls):
        """ initialize spacy model object """
        try:
            SpacyPrediction.__instance = spacy.load('en_core_web_trf')
        except AttributeError as err:
            print("Error while create spacy object instance {}".format(err))

    @classmethod
    def gpe_prediction(cls, raw_text):
        gpe_data: list = []
        doc = SpacyPrediction.__instance(raw_text)
        for ent in doc.ents:
            if ent.label_ == "GPE":
                gpe_data.append(
                    {"text": ent.text, "start_index": ent.start_char})
        return gpe_data

    @classmethod
    def get_instance(cls):
        """ get model object """
        if SpacyPrediction.__instance is None:
            SpacyPrediction()
            if SpacyPrediction.__instance is None:
                raise Exception('spacy object is None')
        return SpacyPrediction.__instance
