pygetpapers user documentation
=======================================

.. figure:: https://user-images.githubusercontent.com/62711517/117457208-93c60b00-af7b-11eb-9c00-a7077786a430.png
   :alt: pygetpapers

   pygetpapers

-  pygetpapers is a tool to assist text miners. It makes requests to
   open access scientific text repositories, analyses the hits, and
   systematically downloads the articles without further interaction.

-  It comes with the packages ``pygetpapers`` and ``downloadtools``
   which provide various functions to download, process and save
   research papers and their metadata.

-  The main medium of its interaction with users is through a
   command-line interface.

-  ``pygetpapers`` has a modular design which makes maintenance easy and
   simple. This also allows adding support for more repositories simple.



History
-------------------------
``getpapers`` is a tool written by Rik Smith-Unna funded by ContentMine
at https://github.com/ContentMine/getpapers. The OpenVirus community
requires a Python version and Ayush Garg has written an implementation
from scratch, with some enhancements.

Formats supported by pygetpapers
--------------------------------------------------

pygetpapers gives fulltexts in xml and pdf format. The metadata for
papers can be saved in many formats including JSON, CSV, HTML. Queries
can be saved in form of an ini configuration file. The additional files
for papers can also be downloaded. References and citations for papers
are given in XML format. Log files can be saved in txt format.

Architecture
-------------------------

.. figure:: https://raw.githubusercontent.com/petermr/pygetpapers/main/archietecture.png
   :alt: Architecture

   Architecture

About the author and community
--------------------------------------------------

``pygetpapers`` has been developed by Ayush Garg under the dear guidance
of the OpenVirus community and Peter Murray Rust. Ayush is currently a
high school student who believes that the world can only truly progress
when knowledge is open and accessible by all.

Testers from OpenVirus have given a lot of useful feedback to Ayush
without which this project would not have been possible.

The community has taken time to ensure that everyone can contribute to
this project. So, YOU, the developer, reader and researcher can also
contribute by testing, developing, and sharing.

Installation
-------------------------

Ensure that ``pip`` is installed along with python. Download python
from: https://www.python.org/downloads/ and select the option Add Python
to Path while installing.

Check out https://pip.pypa.io/en/stable/installing/ if difficulties
installing pip.

.. raw:: html

   <hr>

Way one (recommended):
---------------------------

-  Ensure git cli is installed and is available in path. Check out
   (https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

-  Enter the command:
   ``pip install git+git://github.com/petermr/pygetpapers``

-  Ensure pygetpapers has been installed by reopening the terminal and
   typing the command ``pygetpapers``

-  You should see a help message come up.

.. raw:: html

   <hr>

Way two:
-------------

-  Manually clone the repository and run ``python setup.py install``
   from inside the repository directory

-  Ensure pygetpapers has been installed by reopening the terminal and
   typing the command ``pygetpapers``

-  You should see a help message come up.

.. raw:: html

   <hr>

Usage
-------------------------

-  Type the command ``pygetpapers`` to run the help.

::

    usage: pygetpapers [-h] [--config CONFIG] [-v] [-q QUERY] [-o OUTPUT]
                       [--save_query] [-x] [-p] [-s] [--references REFERENCES]
                       [-n] [--citations CITATIONS] [-l LOGLEVEL] [-f LOGFILE]
                       [-k LIMIT] [-r RESTART] [-u UPDATE] [--onlyquery] [-c]
                       [--makehtml] [--synonym] [--startdate STARTDATE]
                       [--enddate ENDDATE]

    Welcome to Pygetpapers version 0.0.4. -h or --help for help

    optional arguments:
      -h, --help            show this help message and exit
      --config CONFIG       config file path to read query for pygetpapers
      -v, --version         output the version number
      -q QUERY, --query QUERY
                            query string transmitted to repository API. Eg.
                            "Artificial Intelligence" or "Plant Parts". To escape
                            special characters within the quotes, use backslash.
                            Incase of nested quotes, ensure that the initial
                            quotes are double and the qutoes inside are single.
                            For eg: `'(LICENSE:"cc by" OR LICENSE:"cc-by") AND
                            METHODS:"transcriptome assembly"' ` is wrong. We
                            should instead use `"(LICENSE:'cc by' OR LICENSE:'cc-
                            by') AND METHODS:'transcriptome assembly'"`
      -o OUTPUT, --output OUTPUT
                            output directory (Default: Folder inside current
                            working directory named )
      --save_query          saved the passed query in a config file
      -x, --xml             download fulltext XMLs if available
      -p, --pdf             download fulltext PDFs if available
      -s, --supp            download supplementary files if available
      --references REFERENCES
                            Download references if available. Requires source for
                            references (AGR,CBA,CTX,ETH,HIR,MED,PAT,PMC,PPR).
      -n, --noexecute       report how many results match the query, but don't
                            actually download anything
      --citations CITATIONS
                            Download citations if available. Requires source for
                            citations (AGR,CBA,CTX,ETH,HIR,MED,PAT,PMC,PPR).
      -l LOGLEVEL, --loglevel LOGLEVEL
                            Provide logging level. Example --log warning
                            <<info,warning,debug,error,critical>>, default='info'
      -f LOGFILE, --logfile LOGFILE
                            save log to specified file in output directory as well
                            as printing to terminal
      -k LIMIT, --limit LIMIT
                            maximum number of hits (default: 100)
      -r RESTART, --restart RESTART
                            Reads the json and makes the xml files. Takes the path
                            to the json as the input
      -u UPDATE, --update UPDATE
                            Updates the corpus by downloading new papers. Takes
                            the path of metadata json file of the orignal corpus
                            as the input. Requires -k or --limit (If not provided,
                            default will be used) and -q or --query (must be
                            provided) to be given. Takes the path to the json as
                            the input.
      --onlyquery           Saves json file containing the result of the query in
                            storage. The json file can be given to --restart to
                            download the papers later.
      -c, --makecsv         Stores the per-document metadata as csv.
      --makehtml            Stores the per-document metadata as html.
      --synonym             Results contain synonyms as well.
      --startdate STARTDATE
                            Gives papers starting from given date. Format: YYYY-
                            MM-DD
      --enddate ENDDATE     Gives papers till given date. Format: YYYY-MM-DD

    Args that start with '--' (eg. -v) can also be set in a config file (specified
    via --config). Config file syntax allows: key=value, flag=true, stuff=[a,b,c]
    (for details, see syntax at https://goo.gl/R74nmi). If an arg is specified in
    more than one place, then command line values override config file values which
    override defaults.

Queries are build using ``-q`` flag. The query format can be found at
http://europepmc.org/docs/EBI\_Europe\_PMC\_Web\_Service\_Reference.pdf
A condensed guide can be found at
https://github.com/petermr/pygetpapers/wiki/query-format

Sample queries:
-------------------------

1. The following query downloads 100 full-text XML, pdfs, and
   supplementary files along with the CSV and JSON(default) for the
   topic "lantana" and saves them in a directory called "test".

``pygetpapers -q "lantana" -k 100 -o "test" --supp -c -p -x``

.. figure:: https://user-images.githubusercontent.com/70321942/116696048-03b61d80-a9df-11eb-8bb2-6190aef8a6db.PNG
   :alt: 1


2. The following query just prints out the number of hits for the topic
   ``lantana``

``pygetpapers -n -q "lantana"``

.. figure:: https://user-images.githubusercontent.com/70321942/116695234-ef255580-a9dd-11eb-96d1-a01841a5af21.PNG
   :alt: n


3. The following query just creates the CSV output for metadata of 100
   papers on the topic ``lantana`` in an output directory called "test"

``pygetpapers --onlyquery -q "lantana" -k 100 -o "test" -c``

.. figure:: https://user-images.githubusercontent.com/70321942/116697221-8c818900-a9e0-11eb-8a29-5414314b415d.PNG
   :alt: 3

4. If the user wants to update an existing corpus in the directory test
   which has eupmc\_resuts.json with 100 papers of query ``lantana``
   along with their XML files and pdfs, the following query can be used:

``pygetpapers --update "C:\Users\DELL\test\eupmc_results.JSON" -q "lantana" -k 10 -x -p``

5. If the user wants to download pdfs for a corpus in the directory test
   which has eupmc\_resuts.json which originally only had XML files, or
   the query broke in between and they want to restart the download of
   pdfs and XML, they can use the following query

``pygetpapers --restart "C:\Users\DELL\test\eupmc_results.json" -o "test" -x -p -q "lantana"``

.. figure:: https://user-images.githubusercontent.com/70321942/116698739-58a76300-a9e2-11eb-8b56-1fd177bf9b1c.PNG
   :alt: 5


6. If the user wants references then the following query download
   references.xml file if available. Requires source for references
   (AGR,CBA,CTX,ETH,HIR,MED,PAT,PMC,PPR)

``pygetpapers -q "lantana" -k 10 -o "test" -c -x --references PMC``

.. figure:: https://user-images.githubusercontent.com/70321942/116775022-0f0c5600-aa7e-11eb-9625-eaddd53f9aca.PNG
   :alt: rrr


.. figure:: https://user-images.githubusercontent.com/70321942/116774866-1848f300-aa7d-11eb-907c-259e2047de69.PNG
   :alt: rr


7. if the user wants a synonym then ``--synonym`` provides results that
   contain synonyms as well

``pygetpapers --onlyquery -q "lantana" -k 10 -o "test" -c --synonym``

.. figure:: https://user-images.githubusercontent.com/70321942/116773871-116ab200-aa76-11eb-962a-8cdd6366cc17.PNG
   :alt: s

8.  if the user wants to save the query to use it later
    ``pygetpapers -q "lantana" --save_query``

9.  if user wants to get papers within a date range
    ``pygetpapers -q "lantana" --startdate "2020-01-02" --enddate "2021-09-09"``

10. if the user wants to start query from a configuration file
    ``pygetpapers --config "C:\Users\DELL\test\saved_config.ini"``

Contributions
-------------------------

Contributions are welcome through issues as well as pull requests. For
direct contributions, you can mail the author at ayush@science.org.in.

Feature Requests
-------------------------

To request features, please put them in issues

Legal Implications
-------------------------

pygetpapers users should be careful to understand the law as it applies to their content mining, as they assume full responsibility for their actions when using the software.

Countries with copyright exceptions for content mining:
-------------------------------------------------------------

-  UK
-  Japan

Countries with proposed copyright exceptions:
---------------------------------------------------

-  Ireland
-  EU countries

Countries with permissive interpretations of 'fair use' that might allow content mining:
----------------------------------------------------------------------------------------------

-  Israel
-  USA
-  Canada

General summaries and guides:
-----------------------------------

-  *"The legal framework of text and data mining (TDM)"*, carried out
   for the European Commission in March 2014
   (`PDF <http://ec.europa.eu/internal_market/copyright/docs/studies/1403_study2_en.pdf>`__)
-  *"Standardisation in the area of innovation and technological
   development, notably in the field of Text and Data Mining"*, carried
   out for the European Commission in 2014
   (`PDF <http://ec.europa.eu/research/innovation-union/pdf/TDM-report_from_the_expert_group-042014.pdf>`__)

Contents
----------------------------------------------
.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: User Documentation:

   index

.. toctree::
   :maxdepth: 5
   :caption: Developer Documentation:

   pygetpapers
   download_tools
   europe_pmc
   crossref
   arxiv
   rxivist
   rxiv

