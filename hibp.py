import requests
import json

misperrors = {'error': 'Error'}
mispattributes = {'input': ['email-dst', 'email-src'], 'output': ['text']}
moduleinfo = {'version': '0.1', 'author': 'Aurélien Schwab', 'description': 'Module to access haveibeenpwned.com API.', 'module-type': ['hover']}
moduleconfig = ['user-agent']

haveibeenpwned_api_url = 'https://api.haveibeenpwned.com/api/v2/breachedaccount/'
default_user_agent = 'MISP-Module'

def handler(q=False):
    if q is False:
        return False
    request = json.loads(q)
    for input_type in mispattributes['input']:
        if input_type in request:
            email = request[input_type]
            break
    else:
        misperrors['error'] = "Unsupported attributes type"
        return misperrors

    r = requests.get(haveibeenpwned_api_url + email, headers={'user-agent': default_user_agent})
    if r.status_code == 200:
        breaches = json.loads(r.text)
        if breaches:
            return {'results': [{'types': mispattributes['output'], 'values': breaches}]}
    elif r.status_code == 404:
        return {'results': [{'types': mispattributes['output'], 'values': 'OK (Not Found)'}]}
    else:
        misperrors['error'] = 'haveibeenpwned.com API not accessible (HTTP ' + str(r.status_code) + ')'
        return misperrors['error']

def introspection():
    return mispattributes

def version():
    moduleinfo['config'] = moduleconfig
    return moduleinf
