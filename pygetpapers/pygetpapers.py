from pygetpapers.download_tools import download_tools
from pygetpapers.europe_pmc import europe_pmc
from pygetpapers.crossref import crossref
from pygetpapers.arxiv import arxiv


class pygetpapers():

    def __init__(self):
        """This function makes all the constants"""
        import os
        import configparser
        with open(os.path.join(os.path.dirname(__file__), "config.ini")) as f:
            config_file = f.read()
        config = configparser.RawConfigParser(allow_no_value=True)
        config.read_string(config_file)
        self.crossref = crossref()
        self.arxiv = arxiv()
        self.europe_pmc = europe_pmc()
        self.version = config.get("pygetpapers", "version")

        self.download_tools = download_tools("europepmc")

    def handle_adding_terms_from_file(self, args):
        """This functions handles the adding of terms to the query

        :param args: args passed down from argparse

        """
        with open(args.terms, 'r') as f:
            all_terms = f.read()
            terms_list = all_terms.split(',')
            ORed_terms = ' OR '.join(terms_list)
            args.query = f'({args.query} AND ({ORed_terms}))'

    def handle_noexecute(self, args):
        """This functions handles the assigning of apis for no execute command

        :param args: args passed down from argparse

        """
        if args.api == "eupmc":
            self.europe_pmc.eupmc_noexecute(args.query, synonym=args.synonym)
        elif args.api == "crossref":
            self.crossref.noexecute(args.query, size=10)
        elif args.api == "arxiv":
            self.arxiv.noexecute(args.query)

    def handle_update(self, args):
        """This functions handles the assigning of apis for update

        :param args: args passed down from argparse

        """
        import logging
        if args.api == "eupmc":
            self.europe_pmc.eupmc_update(args)
        elif args.api == "crossref":
            logging.warning("update currently not supported for crossref")
        elif args.api == "arxiv":
            logging.warning("update currently not supported for arxiv")

    def handle_query_download(self, args):
        """This functions handles the assigning of apis for query download

        :param args: args passed down from argparse

        """
        if args.api == "eupmc":
            self.europe_pmc.eupmc_apipaperdownload(args.query, args.limit,
                                                   onlymakejson=args.onlyquery, getpdf=args.pdf, makecsv=args.makecsv,
                                                   makehtml=args.makehtml,
                                                   makexml=args.xml, references=args.references, citations=args.citations,
                                                   supplementaryFiles=args.supp, zipFiles=args.zip, synonym=args.synonym)
        elif args.api == "crossref":
            self.crossref.download_and_save_results(
                args.query, args.limit, filter=args.filter)
        elif args.api == "arxiv" and args.password == "CEVOPEN2021":
            self.arxiv.arxiv(args.query, args.limit, getpdf=args.pdf,
                             makecsv=args.makecsv, makexml=args.xml, makehtml=args.makehtml)

    def handle_write_configuration_file(self, args):
        """This functions handles the writing the args to a configuration file

        :param args: This functions handles the assigning of apis for update

        """
        import configparser
        parser = configparser.ConfigParser()

        parsed_args = vars(args)

        parser.add_section('SAVED')
        for key in parsed_args.keys():
            parser.set('SAVED', key, str(parsed_args[key]))

        with open('saved_config.ini', 'w') as f:
            parser.write(f)

    def handle_logfile(self, args, level):
        """This functions handles storing of logs in a logfile

        :param args: args passed down from argparse
        :param level: level of logger

        """
        import logging
        logging.basicConfig(filename=args.logfile,
                            level=level, filemode='w')
        console = logging.StreamHandler()
        console.setLevel(level)
        formatter = logging.Formatter('%(levelname)s: %(message)s')
        # tell the handler to use this format
        console.setFormatter(formatter)
        logging.getLogger().addHandler(console)
        logging.info(f'Making log file at {args.logfile}')

    def handle_restart(self, args):
        """This functions handles the assigning of apis for restarting the downloads

        :param args: args passed down from argparse

        """
        import logging
        if args.api == "eupmc":
            self.europe_pmc.eupmc_restart(args)
        elif args.api == "crossref":
            logging.warning("Restart currently not supported for crossref")
        elif args.api == "arxiv":
            logging.warning("Restart currently not supported for arxiv")

    def handle_adding_date_to_query(self, args):
        """This functions handles the adding date to the query

        :param args: args passed down from argparse

        """
        from time import gmtime, strftime

        if args.startdate and not args.enddate:
            args.enddate = strftime("%Y-%d-%m", gmtime())
        if args.startdate and args.enddate:
            args.query = f'({args.query}) AND (FIRST_PDATE:[{args.startdate} TO {args.enddate}])'
        elif args.enddate:
            args.query = f'({args.query}) AND (FIRST_PDATE:[TO {args.enddate}])'

    def handlecli(self):
        """Handles the command line interface using argparse"""
        version = self.version
        import os
        import configargparse
        import logging
        import sys
        from time import gmtime, strftime
        default_path = strftime("%Y_%m_%d_%H_%M_%S", gmtime())
        parser = configargparse.ArgParser(
            description=f"Welcome to Pygetpapers version {version}. -h or --help for help", add_config_file_help=False)
        parser.add_argument('--config', is_config_file=True,
                            help='config file path to read query for pygetpapers')

        parser.add_argument("-v", "--version",
                            default=False, action="store_true", help="output the version number")
        parser.add_argument("-q", "--query",
                            type=str, default=False,
                            help="query string transmitted to repository API. Eg. \"Artificial Intelligence\" or \"Plant Parts\". To escape special characters within the quotes, use backslash. Incase of nested quotes, ensure that the initial quotes are double and the qutoes inside are single. For eg: `'(LICENSE:\"cc by\" OR LICENSE:\"cc-by\") AND METHODS:\"transcriptome assembly\"' ` is wrong. We should instead use `\"(LICENSE:'cc by' OR LICENSE:'cc-by') AND METHODS:'transcriptome assembly'\"` ")

        parser.add_argument("-o", "--output",
                            type=str, help="output directory (Default: Folder inside current working directory named )", default=os.path.join(os.getcwd(), default_path))
        parser.add_argument("--save_query", default=False, action='store_true',
                            help="saved the passed query in a config file")
        parser.add_argument("-x", "--xml", default=False, action='store_true',
                            help="download fulltext XMLs if available")
        parser.add_argument("-p", "--pdf", default=False, action='store_true',
                            help="download fulltext PDFs if available")
        parser.add_argument("-s", "--supp", default=False, action='store_true',
                            help="download supplementary files if available	")
        parser.add_argument("-z", "--zip", default=False, action='store_true',
                            help="download files from ftp endpoint if available	")
        parser.add_argument("--references",
                            type=str, default=False,
                            help="Download references if available. Requires source for references (AGR,CBA,CTX,ETH,HIR,MED,PAT,PMC,PPR).")
        parser.add_argument("-n", "--noexecute", default=False, action='store_true',
                            help="report how many results match the query, but don't actually download anything")

        parser.add_argument("--citations", type=str, default=False,
                            help="Download citations if available. Requires source for citations (AGR,CBA,CTX,ETH,HIR,MED,PAT,PMC,PPR).")
        parser.add_argument("-l", '--loglevel', default="info",
                            help="Provide logging level.  Example --log warning <<info,warning,debug,error,critical>>, default='info'")
        parser.add_argument("-f", "--logfile", default=False,
                            type=str,
                            help="save log to specified file in output directory as well as printing to terminal")
        parser.add_argument("-k", "--limit", default=100,
                            type=int, help="maximum number of hits (default: 100)")

        parser.add_argument('-r', "--restart", default=False,
                            type=str,
                            help="Reads the json and makes the xml files. Takes the path to the json as the input")

        parser.add_argument("-u", "--update", default=False,
                            type=str,
                            help="Updates the corpus by downloading new papers. Takes the path of metadata json file of the orignal corpus as the input. Requires -k or --limit (If not provided, default will be used) and -q or --query (must be provided) to be given. Takes the path to the json as the input.")
        parser.add_argument("--onlyquery", action='store_true',
                            help="Saves json file containing the result of the query in storage. The json file can be given to --restart to download the papers later.")
        parser.add_argument("-c", "--makecsv", default=False, action='store_true',
                            help="Stores the per-document metadata as csv.")
        parser.add_argument("--makehtml", default=False, action='store_true',
                            help="Stores the per-document metadata as html.")
        parser.add_argument("--synonym", default=False, action='store_true',
                            help="Results contain synonyms as well.")
        parser.add_argument("--startdate", default=False,
                            type=str,
                            help="Gives papers starting from given date. Format: YYYY-MM-DD")
        parser.add_argument("--enddate", default=False,
                            type=str,
                            help="Gives papers till given date. Format: YYYY-MM-DD")
        parser.add_argument("--terms", default=False,
                            type=str,
                            help="Location of the txt file which contains terms serperated by a comma which will be OR'ed among themselves and AND'ed with the query")
        parser.add_argument("--api", default='eupmc', type=str,
                            help="API to search [eupmc, crossref,arxiv] (default: eupmc)")
        parser.add_argument("--filter", default=None, type=str,
                            help="filter by key value pair, passed straight to the crossref api only")
        parser.add_argument("--password", default=None, type=str,
                            help="password for testing out hidden features")
        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit()
        args = parser.parse_args()
        for arg in vars(args):
            if vars(args)[arg] == "False":
                vars(args)[arg] = False

        if os.path.exists(args.output):
            os.chdir(args.output)
        elif not args.noexecute and not args.update and not args.restart:
            os.makedirs(args.output)
            os.chdir(args.output)
        if args.save_query:
            self.handle_write_configuration_file(args)
        levels = {
            'critical': logging.CRITICAL,
            'error': logging.ERROR,
            'warn': logging.WARNING,
            'warning': logging.WARNING,
            'info': logging.INFO,
            'debug': logging.DEBUG
        }
        level = levels.get(args.loglevel.lower())

        if args.logfile:
            self.handle_logfile(args, level)

        else:
            logging.basicConfig(
                level=level, format='%(levelname)s: %(message)s')

        if args.restart:
            self.handle_restart(args)

        if args.version:
            logging.info(version)
            sys.exit(1)

        if not args.query and not args.restart:
            logging.warning('Please specify a query')
            sys.exit(1)

        self.handle_adding_date_to_query(args)

        if args.terms:
            self.handle_adding_terms_from_file(args)

        logging.info(f'Final query is {args.query}')

        if args.noexecute:
            self.handle_noexecute(args)

        elif args.update:
            self.handle_update(args)
        else:
            if args.query:
                self.handle_query_download(args)


def demo():
    """Shows demo to use the library to download papers"""
    callgetpapers = pygetpapers()
    query = "artificial intelligence"
    numberofpapers = 210
    callgetpapers.europe_pmc.eupmc_apipaperdownload(query, numberofpapers)


def main():
    """Runs the CLI"""
    callpygetpapers = pygetpapers()
    callpygetpapers.handlecli()


if __name__ == "__main__":
    main()
