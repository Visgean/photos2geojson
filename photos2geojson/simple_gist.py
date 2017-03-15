import requests


GIST_BASE_URL = 'https://api.github.com/gists'

def upload_gist(filename, data, public=False):
    payload = {
        "public": public,
        "description": '',
        "files": {
            filename: {
                "content": data
                }
            }
    }


    r = requests.post(GIST_BASE_URL, 
        json=payload
    )

    r.raise_for_status()
    return r.json()['html_url']