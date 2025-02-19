import os
import logging
from habanero import Crossref
from pygetpapers.download_tools import DownloadTools


class CrossRef:
    """CrossRef class which handles crossref repository"""

    def __init__(self):
        """[summary]"""
        self.download_tools = DownloadTools("crossref")

    def crossref(
        self,
        query,
        size,
        filter_dict=None,
        update=None,
        makecsv=False,
        makexml=False,
        makehtml=False,
    ):
        """Makes the query to CROSSREF rest api then returns research papers.

        :param query: the query passed on to payload
        :param size: total number of papers
        :param filter_dict: Default value = None) Key Value pair passed down to the crossref api
        :param update: Default value = None) Weather to update the dict with old papers
        :param makehtml:
        :param makecsv:
        :param makexml:

        """
        crossref_client = self.initiate_crossref()
        logging.info("Making request to crossref")

        if update:
            cursor = update["cursor_mark"]
        else:
            cursor = "*"
        crossref_client = crossref_client.works(
            query={query}, filter=filter_dict, cursor_max=size, cursor=cursor
        )
        doi_list = []
        logging.info("Got request result from crossref")
        for item in crossref_client["message"]["items"]:
            doi_list.append(item["DOI"])
        logging.debug("Added DOIs to a list")
        total_number_of_results = crossref_client["message"]["total-results"]
        cursor_mark = crossref_client["message"]["next-cursor"]
        total_result_list = self.make_list_of_required_size_from_crossref_result(
            crossref_client, size
        )
        json_return_dict = self.download_tools.make_dict_from_returned_list(
            total_result_list, key_in_dict="DOI"
        )
        for paper in json_return_dict:
            self.download_tools.add_keys_for_conditions(
                paper, json_return_dict)
        dict_to_return = self.download_tools.make_dict_to_return(
            cursor_mark, json_return_dict, total_number_of_results, update
        )
        return_dict = dict_to_return["total_json_output"]
        self.download_tools.handle_creation_of_csv_html_xml(
            makecsv, makehtml, makexml, return_dict, "crossref-result"
        )
        return dict_to_return

    @staticmethod
    def make_list_of_required_size_from_crossref_result(crossref_client, size):
        """[summary]

        :param crossref_client: [description]
        :type crossref_client: [type]
        :param size: [description]
        :type size: [type]
        :return: [description]
        :rtype: [type]
        """
        total_result_list = crossref_client["message"]["items"]
        total_result_list = total_result_list[:size]
        return total_result_list

    def initiate_crossref(self):
        """[summary]

        :return: [description]
        :rtype: [type]
        """
        cr = Crossref()
        Crossref(mailto="ayushgarg@science.org.in")
        version = self.download_tools.get_version()
        Crossref(ua_string=f"pygetpapers/version@{version}")
        return cr

    def crossref_update(
        self,
        query,
        size,
        filter_dict=None,
        update=None,
        makecsv=False,
        makexml=False,
        makehtml=False,
    ):
        """[summary]

        :param query: [description]
        :type query: [type]
        :param size: [description]
        :type size: [type]
        :param filter_dict: [description], defaults to None
        :type filter_dict: [type], optional
        :param update: [description], defaults to None
        :type update: [type], optional
        :param makecsv: [description], defaults to False
        :type makecsv: bool, optional
        :param makexml: [description], defaults to False
        :type makexml: bool, optional
        :param makehtml: [description], defaults to False
        :type makehtml: bool, optional
        """
        os.chdir(os.path.dirname(update))
        update = self.download_tools.readjsondata(update)
        logging.info("Reading old json metadata file")
        self.download_and_save_results(
            query,
            size,
            filter_dict=filter_dict,
            update=update,
            makecsv=makecsv,
            makexml=makexml,
            makehtml=makehtml,
        )

    def noexecute(self, query, filter_dict=None, **kwargs):
        """Noexecute command for the crossref

        :param query: total number of papers
        :param filter_dict: Default value = None) Key Value pair passed down to the crossref api

        """
        returned_result = self.crossref(
            query, size=10, filter_dict=filter_dict, **kwargs
        )
        totalhits = returned_result["total_hits"]
        logging.info("Total number of hits for the query are %s", totalhits)

    def download_and_save_results(
        self,
        query,
        size,
        filter_dict=None,
        update=None,
        makecsv=False,
        makexml=False,
        makehtml=False,
    ):
        """Downloads and saves results for the query

        :param query: total number of papers
        :param filter_dict: Default value = None) Key Value pair passed down to the crossref api
        :param update: Default value = None) Weather to update the dict with old papers
        :param size: total number of papers
        :param makehtml:
        :param makexml:
        :param makecsv:

        """
        returned_result = self.crossref(
            query,
            size,
            filter_dict=filter_dict,
            update=update,
            makecsv=makecsv,
            makexml=makexml,
            makehtml=makehtml,
        )
        self.download_tools.make_json_files_for_paper(
            returned_result, key_in_dict="DOI", name_of_file="crossref-result"
        )
