"""The module offers classes to access the wr_api_

.. _wr_api: http://www.wordreference.com/docs/api.aspx
"""
__author__ = "Federico Vaga <federico.vaga@vaga.pv.it>"
__license__ = "GPL v3"
__docformat__ = 'reStructuredText'

import requests
import json

available_lang = {
    "ar": "Arabic",
    "zh": "Chinese",
    "cz": "cz",
    "en": "English",
    "fr": "French",
    "gr": "Greek",
    "it": "Italian",
    "ja": "Japanese",
    "ko": "Korean",
    "pl": "Polish",
    "pt": "Portuguese",
    "ro": "Romanian",
    "es": "Spanish",
    "tr": "Turkish",
}


translations = ["FirstTranslation",
                "SecondTranslation",
                "ThirdTranslation",
                "FourthTranslation",
                ]


class TranslatorException(Exception):
    def __init__(self, msg):
        super(self.__class__, self).__init__(msg)


class Translation(object):
    """The Translation object represents a single translation for a given term.
    The aim of the object is mainly to format the string representation
    with ``__str__()``
    """
    def __init__(self, term):
        """It initializes a translation for the given term ``term``.
        The ``term`` must be a dictionary compatible with the wordreference
        API format for translations. The class performs a validation
        on ``term`` and it raises ``Exception`` if it does not comply with
        the word reference API format.
        """
        self.term = term

        if "OriginalTerm" not in self.term:
            raise TranslatorException("Missing OriginalTerm")
        if "FirstTranslation" not in self.term:
            raise TranslatorException("Missing Translation")
        if "Note" not in self.term:
            raise TranslatorException("Missing Note")

        self.orig = self.term["OriginalTerm"]

        self.trans = []
        for tr in translations:
            if tr not in self.term:
                break
            self.trans.append(self.term[tr])

        self.note = self.term["Note"]

    def __str__(self):
        # First the original word
        string = "{term}".format(**self.orig)
        if len(self.orig["POS"]) > 0:
            string += " [{POS}]".format(**self.orig)
        if len(self.orig["usage"]) > 0 or len(self.orig["sense"]):
            string += ","
        if len(self.orig["usage"]) > 0:
            string += " {usage}".format(**self.orig)
        if len(self.orig["sense"]) > 0:
            string += " ({sense})".format(**self.orig)

        # Then the translations
        for tr in self.trans:
            string += "\n\t{term}".format(**tr)
            if len(tr["POS"]) > 0:
                string += " [{POS}]".format(**tr)
            if len(tr["sense"]) > 0:
                string += ", ({sense})".format(**tr)

        # And then the notes
        if len(self.note) > 0:
            string += "\n\tNote: {note}".format(self.note)
        return string


class Translator(object):
    """The Translator object performs word translations between
    two different languages.
    """
    url_tmpl = "http://api.wordreference.com/{apikey}/json/{dictionary}/{term}"
    url_web = "http://www.wordreference.com/{dictionary}/{term}"

    def __init__(self, api_key=None):
        """In order to be accessed, the wordreference API needs an *API key*.
        The object will raise an ``Exception`` if you do not provide a
        value for ``api_key``.
        """
        if api_key is None:
            raise TranslatorException("A wordreference API key is necessary")
        self.api_key = api_key

    def __add_translations(self, dictionary, data):
        dictionary["translation"] = []
        if "term0" not in data:
            raise TranslatorException("No entry found. Check API key. Or word spell")

        d = data["term0"]
        if "PrincipalTranslations" in d:
            for t in sorted(d["PrincipalTranslations"].items(),
                            key=lambda t: t[0]):
                dictionary["translation"].append(Translation(t[1]))

        if "AdditionalTranslations" in d:
            for t in sorted(d["AdditionalTranslations"].items(),
                            key=lambda t: t[0]):
                dictionary["translation"].append(Translation(t[1]))

    def __add_compounds(self, dictionary, data):
        dictionary["compound"] = []
        if "original" in data and "Compounds" in data["original"]:
            for t in sorted(data["original"]["Compounds"].items(),
                            key=lambda t: t[0]):
                dictionary["compound"].append(Translation(t[1]))

    def search(self, lang_from, lang_to, term):
        """It searches for the translation of the given ``term`` from
        one language (``lang_from``) to another (``lang_to``).

        The search result is a dictionary with the following structure

        .. code-block:: python

          {
            "url" : "http://www.wordreference.com/{dictionary}/{term}",
            "translation" : [Translation(), ...],
            "compound": [Translation(), ...],
          }

        :returns: a dictionary that contains all the :py:class:`Translation`
        """
        if lang_from not in available_lang:
            raise TranslatorException("Language {} not supported".format(lang_from))
        if lang_to not in available_lang:
            raise TranslatorException("Language {} not supported".format(lang_to))

        lang_dict = "{_from}{_to}".format(_from=lang_from, _to=lang_to)
        web = self.url_web.format(dictionary=lang_dict,
                                  term=term)
        url = self.url_tmpl.format(apikey=self.api_key,
                                   dictionary=lang_dict,
                                   term=term)
        r = requests.get(url)
        r.raise_for_status()

        data = json.loads(r.text)

        dictionary = {
            "url": web,
        }
        self.__add_translations(dictionary, data)
        self.__add_compounds(dictionary, data)
        return dictionary
