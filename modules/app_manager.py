'''
Manages app.py functionality
'''
from datetime import datetime
import json

from requests import get, exceptions as req_exc
from validators import url as vdt_url

from modules import py_gfm_donations_analysis_web


def url_manager(url):
    '''
    validates and checks URL

    <type url> str
    <desc url> user-generated url
    '''
    errors = []

    if "gofundme.com" not in url or not vdt_url(url) or not len(url.split('/')) == 5:
        errors.append(
            f"Not a valid URL ex. https://www.gofundme.com/f/[campaign_url_title]"
        )
        return False, errors
    else:
        status, errs = url_check(url)
        if status != 200:
            errors.extend(errs)
            return False, errors
        else:
            results = py_gfm_donations_analysis_web.main(url)
        return True, results


def url_check(url):
    exception_errs = []
    try:
        req = get(url)
        req.raise_for_status()
    except (req_exc.HTTPError,
            req_exc.ConnectionError,
            req_exc.ConnectTimeout,
            req_exc.InvalidURL,
            req_exc.ReadTimeout,
            req_exc.RequestException) as rqx_err:
            exception_errs.append(
                f"Request Exception Error: {str(rqx_err)}"
            )
    if exception_errs:
        return req.status_code, exception_errs
    else:
        return req.status_code, None
