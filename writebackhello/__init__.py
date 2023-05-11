import logging

import urllib.request
from inscriptis import get_text

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    headers = {"my-http-header": "some-value"}

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    run_inscriptis()
    
    if name:
        return func.HttpResponse(f"Hello {name}!", headers=headers)
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             headers=headers, status_code=400
        )


def run_inscriptis():
    url = "https://www.fhgr.ch"
    html = urllib.request.urlopen(url).read().decode('utf-8')
    text = get_text(html)
    logging.info(text)





