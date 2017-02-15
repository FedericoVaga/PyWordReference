PyWordReference README
======================
PyWordReference is a Python module that uses the `WordReference API`_
to get access to the wordreference's dictionaries.

The PyWordReference module includes the following objects:

- Translator: it performs searches
- Translation: it represents a single translation

Documentation
-------------
You can generate a more detailed documentation (sphinx based) that includes
also the API by running make from the doc directory.

.. code:: sh

  make -C doc html

Compatibility
-------------
PyWordReference is complatible with *Python 3*. All the tests are performed
on *Python 3*. The compatiblity with previous Python versions is not
guaranteed.

Installation
------------
To install the module run:

.. code:: sh

  python3 setup.py install

This command installs the module in the environment in use by your python installation.

To create a tarball for distribution

.. code:: sh

  python3 setup.py sdist

Unittest
--------
A dummy unittest is also available. It is really dummy, I did it just to
practice with the Python unittest environment

.. code:: sh

  cd unittest
  export WR_API_KEY=<your-api-key>
  python3 -m unittest -v pywordreference

Usage
-----
The implementation is minimal and its main purpose is to get all
the possible translations for a given term. The ``search`` method
retrieves the translations.

.. code:: Python

  def search(self, lang_from, lang_to, term):

What the search ``search`` method returns is a Python dictionary with
the following structure:

.. code:: Python

    {
        "translation" : [Translation(), ],
        "compound": [Translation(), ],
    }

The most common usage of this module is to print the ``Translation`` with
a nice formatted string.

Following a complete example

.. code:: Python

    >>> import PyWordReference
    >>> wr = PyWordReference.Translator(api_key)
    >>> res = wr.search("en", "it", "hello")
    >>> print(res["translation"][0])
    hello, UK: hallo [interj], (greeting)
            salve, buongiorno, buonasera [inter]
            ciao [inter], (informale)
    >>> res = wr.search("it", "en", "ciao")
    >>> print(res["translation"][0])
    ciao [inter], informale (saluto amichevole)
        hello [interj], (greeting)
        hi, hey [interj], (informal)


.. _`WordReference API`: http://www.wordreference.com/docs/api.aspx
