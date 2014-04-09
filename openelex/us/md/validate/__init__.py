import re

from openelex.models import Contest, Candidate, Office, Result
from .election import (Election2000Primary, Election2000General,
    Election2002Primary, Election2002General,
    Election2004Primary, Election2004General,
    Election2006Primary, Election2006General,
    Election2008Primary, Election2008Special, Election2008General,
    Election2010Primary, Election2010General,
    Election2012Primary, Election2012General)

#TODO: Add generic test for unique candidacies per contest
#TODO: Add Result validations

# Election-specific Validators

def validate_contests_2000_primary():
    """Check that there are the correct number of Contest records for the 2000 primary"""
    Election2000Primary().validate_contests()

def validate_contests_2000_general():
    """Check that there are the correct number of Contest records for the 2000 general election"""
    Election2000General().validate_contests()

def validate_contests_2002_primary():
    """Check that there are the correct number of Contest records for the 2002 primary"""
    Election2002Primary().validate_contests()

def validate_contests_2002_general():
    """Check that there are the correct number of Contest records for the 2002 general"""
    Election2002General().validate_contests()

def validate_contests_2004_primary():
    """Check that there are the correct number of Contest records for the 2004 primary"""
    Election2004Primary().validate_contests()

def validate_contests_2004_general():
    """Check that there are the correct number of Contest records for the 2004 general election"""
    Election2004General().validate_contests()

def validate_contests_2006_primary():
    """Check that there are the correct number of Contest records for the 2006 primary"""
    Election2006Primary().validate_contests()

def validate_contests_2006_general():
    """Check that there are the correct number of Contest records for the 2006 general election"""
    Election2006General().validate_contests()

def validate_contests_2008_primary():
    """Check that there are the correct number of Contest records for the 2008 primary"""
    Election2008Primary().validate_contests()

def validate_contests_2008_special():
    """Check that there are the correct number of Contest records for the 2008 special general election for the 4th Congressional District"""
    Election2008Special().validate_contests()

def validate_contests_2008_general():
    """Check that there are the correct number of Contest records for the 2008 general election"""
    Election2008General().validate_contests()

def validate_contests_2010_primary():
    """Check that there are the correct number of Contest records for the 2010 primary"""
    Election2010Primary().validate_contests()

def validate_contests_2010_general():
    """Check that there are the correct number of Contest records for the 2010 general election"""
    Election2010General().validate_contests()

def validate_contests_2012_primary():
    """Check that there are the correct number of Contest records for the 2012 primary"""
    Election2012Primary().validate_contests()

def validate_contests_2012_general():
    """Check that there are the correct number of Contest records for the 2012 general election"""
    Election2012General().validate_contests()

def validate_candidate_count_2000_primary():
    """Check that there are the correct number of Candidate records for the 2000 primary"""
    Election2000Primary().validate_candidate_count()

def validate_candidate_count_2000_general():
    """Check that there are the correct number of Candidate records for the 2000 general election"""
    Election2000General().validate_candidate_count()

def validate_candidate_count_2002_primary():
    """Check that there are the correct number of Candidate records for the 2002 primary"""
    Election2002Primary().validate_candidate_count()

def validate_candidate_count_2002_general():
    """Check that there are the correct number of Candidate records for the 2002 general election"""
    Election2002General().validate_candidate_count()

def validate_candidate_count_2004_primary():
    """Check that there are the correct number of Candidate records for the 2004 primary"""
    Election2004Primary().validate_candidate_count()

def validate_candidate_count_2004_general():
    """Check that there are the correct number of Candidate records for the 2004 general election"""
    Election2004General().validate_candidate_count()

def validate_candidate_count_2006_primary():
    """Check that there are the correct number of Candidate records for the 2006 primary"""
    Election2006Primary().validate_candidate_count()

def validate_candidate_count_2006_general():
    """Check that there are the correct number of Candidate records for the 2006 general election"""
    Election2006General().validate_candidate_count()

def validate_candidate_count_2008_primary():
    """Check that there are the correct number of Candidate records for the 2008 primary"""
    Election2008Primary().validate_candidate_count()

def validate_candidate_count_2008_special():
    """Check that there are the correct number of Contest records for the 2008 special general election for the 4th Congressional District"""
    Election2008Special().validate_candidate_count()

def validate_candidate_count_2008_general():
    """Check that there are the correct number of Candidate records for the 2008 general election"""
    Election2008General().validate_candidate_count()

def validate_candidate_count_2010_primary():
    """Check that there are the correct number of Candidate records for the 2010 primary"""
    Election2010Primary().validate_candidate_count()

def validate_candidate_count_2010_general():
    """Check that there are the correct number of Candidate records for the 2010 general election"""
    Election2010General().validate_candidate_count()

def validate_candidate_count_2012_primary():
    """Check that there are the correct number of Candidate records for the 2012 primary"""
    Election2012Primary().validate_candidate_count()

def validate_candidate_count_2012_general():
    """Check that there are the correct number of Candidate records for the 2012 general election"""
    Election2012General().validate_candidate_count()

def validate_result_count_2000_primary():
    """Should have results for every candidate and contest in 2000 primary"""
    Election2000Primary().validate_result_count()

def validate_2000_primary_congress_county_results():
    """Confirm that county level results are created for congressional races in the 2000 primary"""
    results = Result.objects.filter(state='MD',
        reporting_level='county',
        election_id='md-2000-03-07-primary',
        contest_slug__startswith='us-house-of-representatives')

    district_1_results_d = results.filter(contest_slug='us-house-of-representatives-1-d')
    # 11 counties intersect with district 1 * 4 Democratic candidates = 44
    # results
    count = district_1_results_d.count()
    assert count  == 44, ("There should be 44 results for District 1, instead"
        "there are %d" % count) 
    # Bennett Bozman got 3429 votes in Worcester county
    result = results.get(candidate_slug='bennett-bozman',
        jurisdiction='Worcester')
    assert result.votes == 3429, ("Bennett Bozman should have 3429 votes in "
        "Worcester County, instead has %d" % result.votes) 

    district_8_results_r = results.filter(contest_slug='us-house-of-representatives-8-r')
    # 1 county intersects with district 8 * 1 Republican candidate = 1
    count = district_8_results_r.count()
    assert count == 1, ("There should be 1 result for District 8, instead "
        "there are %d" % count)
    # Constance A. Morella got 35472 votes in Montgomery county 
    result = results.get(candidate_slug='constance-a-morella',
        jurisdiction='Montgomery')
    assert result.votes == 35472, ("Constance A. Morella should have 35472 "
        "votes in Montgomery county.  Instead has %d" % result.votes)

def validate_result_count_2000_general():
    """Should have results for every candidate and contest in 2000 general election"""
    # TODO: Include precincts if it's not too hard
    reporting_levels = ['county', 'state_legislative']
    Election2000General().validate_result_count(reporting_levels)

def validate_result_count_2002_primary():
    """Should have results for every candidate and contest in 2002 primary"""
    Election2002Primary().validate_result_count()

def validate_result_count_2002_general():
    """Should have results for every candidate and contest in 2002 general"""
    Election2002General().validate_result_count()

def validate_result_count_2004_primary():
    """Should have results for every candidate and contest in 2004 primary"""
    # TODO: Include precincts if it's not too hard
    reporting_levels = ['county', 'state_legislative']
    Election2004Primary().validate_result_count(reporting_levels)

def validate_result_count_2004_general():
    """Should have results for every candidate and contest in 2004 general election"""
    # TODO: Include precincts if it's not too hard
    reporting_levels = ['county', 'state_legislative']
    Election2004General().validate_result_count(reporting_levels)

def validate_result_count_2006_primary():
    """Should have results for every candidate and contest in 2006 primary"""
    # TODO: Include precincts if it's not too hard
    reporting_levels = ['county', 'state_legislative']
    Election2006Primary().validate_result_count(reporting_levels)

def validate_result_count_2006_general():
    """Should have results for every candidate and contest in 2006 general election"""
    # TODO: Include precincts if it's not too hard
    reporting_levels = ['county', 'state_legislative']
    Election2006General().validate_result_count(reporting_levels)

def validate_result_count_2008_primary():
    """Should have results for every candidate and contest in 2008 primary"""
    # TODO: Include precincts if it's not too hard
    reporting_levels = ['county', 'state_legislative']
    Election2008Primary().validate_result_count(reporting_levels)

def validate_result_count_2008_special():
    """Check that there are the correct number of Contest records for the 2008 special general election for the 4th Congressional District"""
    Election2008Special().validate_result_count()

def validate_results_2008_special():
    candidates = {
        'donna-edwards': {
            'votes_montgomery': 6733,
            'votes_prince_georges': 9748,
        },
        'peter-james':  {
            'votes_montgomery': 2993,
            'votes_prince_georges': 645,
        },
        'thibeaux-lincecum': {
            'votes_montgomery': 148,
            'votes_prince_georges': 68,
        },
        'adrian-petrus': {
            'votes_montgomery': 0,
            'votes_prince_georges': 1,
        },
        'steve-schulin': {
            'votes_montgomery': 13,
            'votes_prince_georges': 2,
        },
        'other-writeins':  {
            'votes_montgomery': 60,
            'votes_prince_georges': 51,
        },
    }

    for candidate, props in candidates.items():
        result = Result.objects.get(election_id='md-2008-06-17-special-general',
            candidate_slug=candidate, jurisdiction="Montgomery County")
        assert result.votes == props['votes_montgomery']
        result = Result.objects.get(election_id='md-2008-06-17-special-general',
            candidate_slug=candidate, jurisdiction="Prince George's County")
        assert result.votes == props['votes_prince_georges']

    for result in Result.objects.filter(election_id='md-2008-06-17-special-general',
            candidate_slug__in=['adrian_petrus', 'steve-shulin', 'other_writeins']):
        assert result.write_in

def validate_result_count_2008_general():
    """Should have results for every candidate and contest in 2008 general election"""
    # TODO: Include precincts if it's not too hard
    reporting_levels = ['county', 'state_legislative']
    Election2008General().validate_result_count(reporting_levels)

def validate_result_count_2010_primary():
    """Should have results for every candidate and contest in 2010 primary"""
    # TODO: Include precincts if it's not too hard
    reporting_levels = ['county', 'state_legislative']
    Election2010Primary().validate_result_count(reporting_levels)

def validate_result_count_2010_general():
    """Should have results for every candidate and contest in 2010 general election"""
    # TODO: Include precincts if it's not too hard
    reporting_levels = ['county', 'state_legislative']
    Election2010General().validate_result_count(reporting_levels)

def validate_result_count_2012_primary():
    """Should have results for every candidate and contest in 2012 primary"""
    # TODO: Include precincts if it's not too hard
    reporting_levels = ['county', 'state_legislative']
    Election2012Primary().validate_result_count(reporting_levels)

def validate_result_count_2012_general():
    """Should have results for every candidate and contest in 2012 general election"""
    # TODO: Include precincts if it's not too hard
    reporting_levels = ['county', 'state_legislative']
    Election2012General().validate_result_count(reporting_levels)

def validate_unique_prez_2012_general():
    """Should only be a single contest for 2012 prez general"""
    count = Contest.objects.filter(election_id='md-2012-11-06-general', slug='president').count()
    expected = 1
    try:
        assert count == expected
        print "PASS: %s general prez contest found for 2012" % count
    except AssertionError:
        raise AssertionError("expected 2012 general prez contest count (%s) did not match actual count (%s)" % (expected, count))

def validate_obama_candidacies_2012():
    """Should only be two Obama candidacies in 2012 (primary and general)"""
    kwargs = {
        'election_id__startswith': 'md-2012',
        'slug': 'barack-obama',
    }
    count = Candidate.objects.filter(**kwargs).count()
    expected = 2
    try:
        assert count == expected
        print "PASS: %s obama candidacies found for %s" % (count, '2012')
    except AssertionError:
        raise AssertionError("expected obama 2012 candidacies (%s) did not match actual count(%s)" % (expected, count))

def validate_obama_primary_candidacy_2012():
    """Should only be one Obama primary candidacy for 2012"""
    elec_id= 'md-2012-04-03-primary'
    kwargs = {
        'election_id': elec_id,
        'contest_slug': 'president-d',
        'slug': 'barack-obama',
    }
    try:
        cand = Candidate.objects.get(**kwargs)
        print "PASS: 1 obama primary candidacy found for 2012: %s" % "-".join(cand.key)
    except Candidate.DoesNotExist:
        raise Candidate.DoesNotExist("zero obama primary candidacies found for 2012")
    except Candidate.MultipleObjectsReturned as e:
        raise Candidate.MultipleObjectsReturned("multiple obama primary candidacies found for 2012: %s" %  e)


# Validators that are not specific to a particular election

def validate_aggregate_congressional_district_results():
    """Validate that results have been correctly aggregated from congressional districts split by county"""

    election_id = 'md-2000-03-07-primary'

    # President
    results = Result.objects.filter(election_id=election_id,
        contest_slug='president-d', reporting_level='congressional_district')
    # Maryland has 8 congressional districts
    count = len(results.distinct('jurisdiction'))
    assert count == 8, ("There should be results for 8 congressional "
        "districts.  Instead there are results for %d." % count)
    # 4 candidates * 8 districts = 32 results
    count = results.count()
    assert count == 32, ("There should be 32 results.  Instead there are %d" %
        count)
    # Al Gore got 32426 votes in district 1
    votes = results.get(candidate_slug='al-gore', jurisdiction='1').votes
    assert votes == 32426, ("Al Gore should have 32426 votes in District 1. "
        "Instead there are %d" % votes)

    # U.S. House 
    results = Result.objects.filter(election_id=election_id,
        contest_slug='us-house-of-representatives-1-r',
        reporting_level='congressional_district')
    # Only 1 candidate in 1 district
    count = results.count()
    assert count == 1, ("There should be 1 result.  Instead there are %d" %
        count)
    # Wayne T. Gilchrest got 49232 votes
    votes = results.get(candidate_slug='wayne-t-gilchrest', jurisdiction='1').votes
    assert votes == 49232, ("Wayne T. Gilchrest should have 49232 votes in "
        "District 1. Instead he has %d." % votes) 

    election_id = 'md-2008-02-12-primary'
    
    # President
    results = Result.objects.filter(election_id=election_id,
        contest_slug='president-d', reporting_level='congressional_district')
    # Maryland has 8 congressional districts
    count = len(results.distinct('jurisdiction'))
    assert count == 8, ("There should be results for 8 congressional "
        "districts.  Instead there are results for %d." % count)
    # 9 candidates * 8 districts = 72 results
    count = results.count()
    assert count == 72, ("There should be 72 results.  Instead there are %d" %
        count)
    votes = results.get(candidate_slug='hillary-clinton', jurisdiction='6').votes 
    assert votes == 34322, ("Hillary Clinton should have 34322 votes in "
        "District 6, instead she has %d" % votes) 

    election_id = 'md-2012-04-03-primary'

    # President
    results = Result.objects.filter(election_id=election_id,
        contest_slug='president-d', reporting_level='congressional_district')
    # Maryland has 8 congressional districts
    count = len(results.distinct('jurisdiction'))
    assert count == 8, ("There should be results for 8 congressional "
        "districts.  Instead there are results for %d." % count)
    # 2 candidates * 8 disctricts = 16 results
    count = results.count()
    assert count == 16, ("There should be 16 results.  Instead there are %d" %
        count)
    votes = results.get(candidate_slug='barack-obama', jurisdiction='1').votes
    assert votes == 20343, ("Barack Obama should have 20343 votes in District "
        "1, instead he has %d" % votes)

def validate_precinct_names_normalized():
    """Precinct jurisdiction names should be in the format 'NN-NNN'"""
    precincts = Result.objects.filter(state='MD', reporting_level='precinct').distinct('jurisdiction')
    for precinct in precincts:
        assert re.match(r'\d+-0\d\d', precinct), ("Precinct %s doesn't match "
            "normalized format." % precinct)

def validate_unique_contests():
    """Should have a unique set of contests for all elections"""
    # Get all election ids
    election_ids = list(Contest.objects.distinct('election_id'))
    for elec_id in election_ids:
        contests = Contest.objects.filter(election_id=elec_id)
        # compare the number of contest records to unique set of contests for that election
        count = contests.count()
        expected = len(list(contests.distinct('slug')))
        try:
            assert expected == count
        except AssertionError:
            raise AssertionError("%s contests expected for elec_id '%s', but %s found" % (expected, elec_id, count))
    print "PASS: unique contests counts found for all elections"

def validate_no_baltimore_city_comptroller():
    """Should not have contest, candidates or results for a Baltimore City comptroller"""
    election_id = 'md-2004-11-02-general'
    office = Office.objects.get(state='MD', name='Comptroller')
    count = Contest.objects.filter(election_id=election_id, office=office).count() 
    msg = "There should be no comptroller contest for election {0}"
    assert count == 0, msg.format(election_id)
    count = Candidate.objects.filter(election_id=election_id,
        contest_slug='comptroller').count()
    msg = "There should be no comptroller candidates for election {0}"
    assert count == 0, msg.format(election_id)
    count = Result.objects.filter(election_id=election_id,
        contest_slug='comptroller').count()
    msg = "There should be no comptroller results for election {0}"
    assert count == 0, msg.format(election_id)

def validate_uncommitted_primary_state_legislative_results():
    """Should only have one uncommitted result per legislative district"""
    results = Result.objects.filter(election_id='md-2008-02-12-primary',
        reporting_level='state_legislative',
        contest_slug='president-d',
        candidate_slug='uncommitted-to-any-presidential-candidate')
    count = results.count()
    assert count == 65, ("There should be only one result per "
        "state legislative district, instead there are {0}".format(count))

#def validate_name_parsing():
    #Check assortment of names
    #Check that Other was skipped
#    pass
