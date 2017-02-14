PyWordReference
===============
PyWordReference is a Python module that uses the `WordReference API`_
to get access to the wordreference's dictionaries.

The PyWordReference module includes the following objects:
- Translator: it performs searches
- Translation: it represents a single translation

Installation
============
To install the module run:

    # python setup.py install

This command installs the module in the environment in use by your python installation.

To create a tarball for distribution

    $ python setup.py sdist


Translator
==========
Usage
-----
The implementation is minimal and its main purpose is to get
all the possible translations of a given term. Following an example:

    >>> import PyWordReference
    >>> wr = PyWordReference.Translator()
    >>> res = wr.search("en", "it", "hello")

The Translator object can be used to perform searches. The syntax is very
simple:

    def search(self, lang_from, lang_to, term):

What the search method returns is a Python dictionary with
the following structure:

    {
    "translation" : [Translation(), ...],
    "compound": [Translation(), ...],
    }

The most common usage of this module is to print the translation with
a nice formatted string.

    >>> import PyWordReference
    >>> wr = PyWordReference.Translator()
    >>> res = wr.search("en", "it", "hello")
    >>> print(res["translation"][0])
    hello, UK: hallo [interj], (greeting)
            salve, buongiorno, buonasera [inter]
            ciao [inter], (informale)


.. _`WordReference API`: http://www.wordreference.com/docs/api.aspx
