import re
import requests

def validate_url(url):
    regex = re.compile(
                r'^(?:http|ftp)s?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None


def verify_url_accessibility(url):
    url_get_call = requests.get(url)
    if url_get_call.status_code == 200:
        return True
    else:
        print("The provided repo is not accessible.")
        return False