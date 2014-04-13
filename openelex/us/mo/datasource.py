"""
Standardize names of data files on Missouri Secretary of State website
and save to mappings/filenames.json
"""
from BeautifulSoup import BeautifulSoup
from collections import defaultdict
import copy
import os.path
import re

import requests
import unicodecsv

from openelex.api import elections as elec_api
from openelex.base.datasource import BaseDatasource


class Datasource(BaseDatasource):
    MAPPING_METHODS = [
        {
            'method': '_build_sosenr_mappings',
            'portal': 'http://enr.sos.mo.gov/sosenr/state.asp?',
        },
        {
            'method': '_build_enrviews_mappings',
            'portal': 'http://enr.sos.mo.gov/ENR/Views/TabularData.aspx?',
        },
        {
            'method': '_build_enrweb_allresults_mappings',
            'portal': 'http://sos.mo.gov/enrweb/allresults.asp?',
        },
        {
            'method': '_build_enrweb_allresults_mappings',
            'portal': 'http://sos.mo.gov/Enrweb/allresults.asp?',
        },
        {
            'method': '_build_enrweb_allresults_mappings',
            'portal': 'http://www.sos.mo.gov/enrweb/allresults.asp?',
        },
        {
            'method': '_build_enrweb_electionselect_mappings',
            'portal': 'http://sos.mo.gov/enrweb/electionselect.asp?',
        },
    ]

    OCD_ID_ROOT = 'ocd-division/country:us/state:mo'

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
                election['slug'] = self._get_election_slug(election)
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
                'by_enrweb': {},
            }
            self._counties = _counties
            by_fips = _counties['by_fips']
            by_name = _counties['by_name']
            by_ocd = _counties['by_ocd']
            by_enrweb = _counties['by_enrweb']

            input_file = open(
                os.path.join(os.path.dirname(__file__), 'mappings', 'mo.csv'),
                'r')
            reader = unicodecsv.DictReader(input_file,)
            for row in reader:
                by_fips[row['fips']] = row
                by_name[row['county']] = row
                by_ocd[row['ocd_id']] = row
                by_enrweb[row['enrweb_name']] = row
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
            method_name = '_build_useless_mappings'

            for mapping_method in self.MAPPING_METHODS:
                if portal_link.startswith(mapping_method['portal']):
                    method_name = mapping_method['method']

            mappings.extend(getattr(self, method_name)(election))
        return mappings

    def _get_election_slug(self, election):
        """
        Build standard identifier for an election
        """
        return "-".join([
            self.state,
            election['start_date'],
            election['race_type'].lower()
        ])

    def _get_election_filename_base(self, election, county=None):
        filename = '{start_date}__{state}__{race_type}__'.format(
            start_date=election['start_date'].replace('-', ''),
            state=self.state.lower(),
            race_type=election['race_type'])
        if election['special']:
            filename += 'special__'
        return filename

    def _build_useless_mappings(self, election):
        return [{
            'not_implemented': 'useless',
            'raw_url': election['portal_link'],
        }]

    def _build_sosenr_mappings(self, election):
        return [{
            'not_implemented': 'sosenr',
            'raw_url': election['portal_link'],
        }]

    def _build_enrviews_mappings(self, election):
        return [{
            'not_implemented': 'enrviews',
            'raw_url': election['portal_link'],
        }]

    def _build_enrweb_allresults_mappings(self, election):
        mappings = []

        state_mapping = {
            'ocd_id': self.OCD_ID_ROOT,
            'election': '{state}-{start_date}-{race_type}'.format(
                state=self.state,
                start_date=election.get('start_date', ''),
                race_type=election['race_type']),
            'raw_url': election['portal_link'],
            'generated_name': (
                self._get_election_filename_base(election) + 'state.html'),
            'name': 'Missouri',
        }
        mappings.append(state_mapping)

        if election['county_level']:
            county_mapping = copy.copy(state_mapping)
            county_mapping['raw_url'] += '&cids=' + '%2C+'.join(
                sorted(self._get_enrweb_county_ids(election).values()))
            county_mapping['raw_url'] = county_mapping['raw_url'].replace(
                'allresults.asp', 'countyresults.asp')
            county_mapping['generated_name'] = (
                self._get_election_filename_base(election) + 'county.html')
            mappings.append(county_mapping)

        return mappings

    def _get_enrweb_county_ids(self, election):
        main_url = election['portal_link']
        county_select_url = main_url.replace(
            'allresults.asp', 'countyselect.asp')

        r = requests.get(county_select_url)
        soup = BeautifulSoup(r.text)
        county_options = soup.find('select', {
            'name': 'cboCounties',
        }).findAll('option')

        county_ids = {}
        counties_by_name = self.counties['by_enrweb']
        for county_option in county_options:
            enrweb_county_name = county_option.text
            try:
                standardized_county_name = counties_by_name[
                    enrweb_county_name]['county']
            except KeyError:
                continue
            county_id = dict(county_option.attrs)['value']
            county_ids[standardized_county_name] = county_id

        return county_ids

    def _build_enrweb_electionselect_mappings(self, election):
        return [{
            'not_implemented': 'enrweb_electionselect',
            'raw_url': election['portal_link'],
        }]
