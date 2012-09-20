import requests

def portforward_get(request):
    headers = {
        "User-Agent" : "python-quantumclient",
        "Content-Type" : "application/json",
        "Accept" : "application/json",
        "X-Auth-Token" : request.user.token.id
    }
    r = requests.get('http://0.0.0.0/v2.0/dhportforward.json', headers=headers)
    r.json
