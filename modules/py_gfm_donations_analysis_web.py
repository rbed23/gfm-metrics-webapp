'''performs basic metrics analysis on GFM donations'''
from collections import OrderedDict
from statistics import mean, median
import json
from operator import itemgetter
from string import capwords
import sys

import requests


def create_gfm_gateway_call(url, limit, offset):
    '''
    creates a json response call to the GoFundMe gateway (GFMGW)
    <type gfmcn> str
    <desc gfmcn> url campaign designation
        ex URL = "habitat-for-the-pathak-family"
    <type limit> int
    <desc limit> maximum number of donations to return in single call
        *** hard set at 100 by GFM Gateway***
    <type offset> int
    <desc offset> used to retrieve the next set of donations, if >100 total

    <<type gwurl>> str
    <<desc gwurl>> url used to parse info from the GFM gateway api
        ex URL = "https://gateway.gofundme.com/
                    web-gateway/v1/feed/habitat-for-the-pathak-family/"
        donations?limit=100&sort=recent"
    '''
    SORT_DIRECTION = 'recent'   # most recent donations listed first

    gfmcn = url.split('/')[4]
    gwurl = f"https://gateway.gofundme.com/web-gateway/v1/feed/{gfmcn}/"
    gwurl += f"donations?limit={limit}&offset={offset}&sort={SORT_DIRECTION}"
    print(f'calling <{gwurl}')

    return gwurl


def get_donations_list(url):
    '''
    gets the list of donations from GFMGW call
    <type gfmcn> str
    <desc gfmcn> url campaign designation

    <<type donations>> list
    <<desc donations>> list of dicts of individual donation information
    '''
    donations = []
    errors = []
    DONATIONS_LIMIT = 100     # maximum returned donations (GFM limit)
    offset_value = 0          # starting offset value
    finished_flag = False
    while not finished_flag:

        gwurl = create_gfm_gateway_call(url, DONATIONS_LIMIT, offset_value)
        offset_value += DONATIONS_LIMIT

        try:
            u_response = requests.get(gwurl).content.decode('utf-8')
        except Exception as err:
            errors.append(
                f"GFM Gateway Error: {str(err)}"
            )
            return errors

        json_response = json.loads(u_response)
        donations.extend(json_response['references']['donations'])

        if not json_response['meta']['has_next']:
            finished_flag = True

    return donations


def get_consolidated_list(ip):
    '''
    get consolidated list of donors, except Anonymous
    <type ip> list
    <desc ip> cleaned dononations

    <<type op>> list
    <<desc op>> consolidated list of donors
    '''
    names = [x['name'] for x in ip if x['name'][0] != 'anonymous']
    duplicates = []
    op = []
    for each in ip:
        full_name = " ".join([capwords(n) for n in each['name'] if n])
        if each['name'] in duplicates:
            pass
        elif names.count(each['name']) > 1:  # if name appears more than once
            # sum the donation amounts based on the name
            summed_amt = sum([float(y['amount']) for
                              y in ip if y['name'] == each['name']])
            details = [{
                        'amount': d['amount'],
                        'date': d['created_at'],
                        'donation_id': d['donation_id']
                    } for d in ip if d['name'] == each['name']]

            new_dict = {
                'amount': summed_amt,
                'name': each['name'],
                'details': details,
                'is_anonymous': each['is_anonymous'],
                'profile': each['profile'],
                'verified': each['verified'],
                'full_name': full_name
                }

            op.append(new_dict)  # add the amount to the consolidated list
            duplicates.append(each['name'])

        else:
            details = [{
                    'amount': each['amount'],
                    'date': each['created_at'],
                    'donation_id': each['donation_id']
            }]

            new_dict = {
                'amount': each['amount'],
                'name': each['name'],
                'details': details,
                'is_anonymous': each['is_anonymous'],
                'profile': each['profile'],
                'verified': each['verified'], 
                'full_name': full_name
                }
            op.append(new_dict)
    return op


def fix_names(name):
    names_array = ["","",""]
    
    split_name = name.strip().split(" ")

    if len(split_name) == 2:
        names_array[0] = split_name[0].lower()
        names_array[2] = split_name[1].lower()

    elif len(split_name) == 3:
        # double spaces in between first/last names
        if split_name[1] == "" or split_name[1] == " ":
            names_array[0] = split_name[0].lower()
            names_array[2] = split_name[2].lower()        
        # middle initial
        elif len(split_name[1]) == 1 and split_name[1].isupper():
            names_array[0] = split_name[0].lower()
            names_array[1] = split_name[1].lower()
            names_array[2] = split_name[2].lower()
        # trailing first name letter
        elif len(split_name[1]) < 3 and split_name[1].islower():
            names_array[0] = split_name[0].lower() + split_name[1]
            names_array[2] = split_name[2].lower()
        # trailing last name letter
        elif len(split_name[2]) < 3 and split_name[2].islower():
            names_array[0] = split_name[0].lower()
            names_array[2] = split_name[1].lower() + split_name[2]
        # middle name
        elif len(split_name[1]) >=3:
            names_array[0] = split_name[0].lower()
            names_array[1] = split_name[1].lower()
            names_array[2] = split_name[2].lower()

    elif len(split_name) == 1:
        names_array[0] = split_name[0].lower()

    else:
        names_array[0] = split_name[0].lower()
        names_array[1] = " ".join(split_name[1:len(split_name)-1])
        names_array[2] = split_name[len(split_name)-1].lower()

    return names_array


def main(url):
    print(f"Called script using <{url}> as input...")

    # get clean list of donations from the GFM Gateway
    donations_list = get_donations_list(url)

    cleaned_list = [{'amount': x['amount'],
                     'name': fix_names(x['name']),
                     'is_anonymous': x['is_anonymous'],
                     'created_at': x['created_at'],
                     'donation_id': x['donation_id'],
                     'profile': x['profile_url'],
                     'verified': x['verified']} for x in donations_list]

    # consolidate donors
    donations = [x["amount"] for x in cleaned_list]

    consolidated_list = get_consolidated_list(cleaned_list)

    anondonations_list = [OrderedDict([
                            ('amount', x['amount']),
                            ('created_at', x['created_at'])
                            ])
                        for x in cleaned_list
                        if x['is_anonymous']]

    nonanondonations_list = [
        {
            'amount': x['amount'],
            'created_at': sorted([
                y['date'] for y in x['details']],
                reverse=True)[0], # most recent date
            'full_name': x['full_name']
        } for x in consolidated_list if not x['is_anonymous']]

    big_donor_list = sorted(
        [{
            "amount": x['amount'],
            "full_name": x['full_name']
         } for x in consolidated_list], key=lambda k: k['amount'], reverse=True)
                        
    big_donor_list_50 = [x for x in big_donor_list if x['amount'] >= sum(donations)*0.50]
    big_donor_list_25 = [x for x in big_donor_list if x['amount'] < sum(donations)*0.50 and x['amount'] >= sum(donations)*0.25]
    big_donor_list_20 = [x for x in big_donor_list if x['amount'] < sum(donations)*0.25 and x['amount'] >= sum(donations)*0.20]
    big_donor_list_10 = [x for x in big_donor_list if x['amount'] < sum(donations)*0.20 and x['amount'] >= sum(donations)*0.10]
    big_donor_list_05 = [x for x in big_donor_list if x['amount'] < sum(donations)*0.10 and x['amount'] >= sum(donations)*0.05]
    big_donor_list_03 = [x for x in big_donor_list if x['amount'] < sum(donations)*0.05 and x['amount'] >= sum(donations)*0.03]
    big_donor_list_02 = [x for x in big_donor_list if x['amount'] < sum(donations)*0.03 and x['amount'] >= sum(donations)*0.02]
    big_donor_list_01 = [x for x in big_donor_list if x['amount'] < sum(donations)*0.02 and x['amount'] >= sum(donations)*0.01]

    response = {
        "donations_complete": consolidated_list,
        "num_donations": len(cleaned_list),
        "num_donors": len(consolidated_list),
        "list_donations": donations,
        "list_anonymous": anondonations_list,
        "list_nonanonymous": nonanondonations_list,
        "big_donor_01": big_donor_list_01,
        "big_donor_02": big_donor_list_02,
        "big_donor_03": big_donor_list_03,
        "big_donor_05": big_donor_list_05,
        "big_donor_10": big_donor_list_10,
        "big_donor_20": big_donor_list_20,
        "big_donor_25": big_donor_list_25,
        "big_donor_50": big_donor_list_50
    }

    with open('response.json', 'w+') as w:
        w.write(json.dumps(response, indent=4))

    return response


if __name__ == "__main__":
    if len(sys.argv) == 2:
        # If there are keyword arguments
        main(sys.argv[1])
    elif len(sys.argv) == 1:
        # If no keyword arguments
        url_input = input("Please enter a valid gofundme.com URL:\n::  ")
        main(url_input)
