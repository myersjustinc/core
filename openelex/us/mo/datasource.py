"""
Standardize names of data files on Missouri Secretary of State website
and save to mappings/filenames.json
"""
from collections import defaultdict
import os.path

import unicodecsv

from openelex.api import elections as elec_api
from openelex.base.datasource import BaseDatasource


class Datasource(BaseDatasource):
    MAPPING_METHODS = [
        {
            'method': '_build_sosenr_mapping',
            'portal': 'http://enr.sos.mo.gov/sosenr/state.asp?',
        },
        {
            'method': '_build_enrviews_mapping',
            'portal': 'http://enr.sos.mo.gov/ENR/Views/TabularData.aspx?',
        },
        {
            'method': '_build_enrweb_allresults_mapping',
            'portal': 'http://sos.mo.gov/enrweb/allresults.asp?',
        },
        {
            'method': '_build_enrweb_electionselect_mapping',
            'portal': 'http://sos.mo.gov/enrweb/electionselect.asp?',
        },
    ]

    def mappings(self, year=None):
        """
        Return array of all elections' standardized metadata,
        optionally filtered by year
        """
        mappings = []
        for election_year, elections in self.elections(year).items():
            mappings.extend(self._build_mappings(election_year, elections))
        return mappings

    def target_urls(self, year=None):
        """
        Get list of source data URLs, optionally filtered by year
        """
        return [item['raw_url'] for item in self.mappings(year)]

    def filename_url_pairs(self, year=None):
        """
        Get tuples of target filenames and source data URLs,
        optionally filtered by year
        """
        return [
            (item['generated_filename'], item['raw_url'])
            for item in self.mappings(year)]

    def elections(self, year=None):
        """
        Retrieve (and cache) election metadata from OpenElections API,
        optionally filtered by year
        """
        # Fetch all elections initially and stash on instance
        if not hasattr(self, '_elections'):
            # Store elections by year
            self._elections = defaultdict(list)
            for election in elec_api.find(self.state):
                election['slug'] = self._elec_slug(election)
                election_year = int(election['start_date'][:4])
                self._elections[election_year].append(election)
        if year:
            year = int(year)
            return {
                year: self._elections[year],
            }
        return self._elections

    @property
    def counties(self):
        """
        Access the contents of the name/FIPS/OCD CSV stored in this
        module.
        """
        if not hasattr(self, '_counties'):
            _counties = {
                'by_fips': {},
                'by_name': {},
                'by_ocd': {},
            }
            self._counties = counties
            by_fips = _counties['by_fips']
            by_name = _counties['by_name']
            by_ocd = _counties['by_ocd']

            input_file = open(
                os.path.join(os.path.dirname(__file__), 'mappings', 'mo.csv'),
                'r')
            reader = unicodecsv.DictReader(input_file,)
            for row in reader:
                by_fips[row['fips']] = row
                by_name[row['county']] = row
                by_ocd[row['ocd_id']] = row
            input_file.close()

        return self._counties

    def _build_mappings(self, year, elections):
        """
        Return elections' standardized metadata for a given year,
        dispatching to the appropriate method depending on what
        reporting system the Secretary of State website is using for
        those elections
        """
        mappings = []
        for election in elections:
            portal_link = election['portal_link']
            method_name = '_build_useless_mapping'

            for mapping_method in self.MAPPING_METHODS:
                if portal_link.startswith(mapping_method['portal']):
                    method_name = mapping_method['method']

            mappings.append(getattr(self, method_name)(election))
        return mappings

    def _elec_slug(self, election):
        """
        Build standard identifier for an election
        """
        return "-".join([
            self.state,
            election['start_date'],
            election['race_type'].lower()
        ])

    def _build_useless_mapping(self, election):
        raise NotImplementedError

    def _build_sosenr_mapping(self, election):
        raise NotImplementedError

    def _build_enrviews_mapping(self, election):
        raise NotImplementedError

    def _build_enrweb_allresults_mapping(self, election):
        raise NotImplementedError

    def _build_enrweb_electionselect_mapping(self, election):
        raise NotImplementedError
