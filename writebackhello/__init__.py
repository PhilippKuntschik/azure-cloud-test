import logging
import time

import urllib.request
from inscriptis import get_text

import azure.functions as func


def main(req: func.HttpRequest, connect_sql: func.Out[func.SqlRow]) -> func.HttpResponse:
    headers = {"my-http-header": "some-value"}

    name = req.params.get('name')
    url = req.params.get('url')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    content = run_inscriptis()
    store_to_database(name, content)
    
    if name:
        return func.HttpResponse(f"Hello {name}!", headers=headers)
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             headers=headers, status_code=400
        )

def run_inscriptis(url = "http://heise.de"):
    html = urllib.request.urlopen(url).read().decode('utf-8')
    text = get_text(html)
    logging.info(text)
    return text

def store_to_database(name, content):
    connect_sql.set(func.SqlRow({"timestamp": time.time(), "name": name, "content": content}))
       