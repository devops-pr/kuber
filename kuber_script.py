# from django.core.validators import URLValidator
# from django.core.exceptions import ValidationError
import re
import requests


def validate_url(url):
    regex = re.compile(
                r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def verify_url_accessibility(url):
    url_get_call = requests.get(url)
    return (url_get_call.status_code)


def clone_repo():
    git_repo = input("Please provide the scm repo: ")
    if not validate_url(git_repo):
        print("The URL is not right. Please enter the url in 'https://<domain>/repos/<repo>' format")
    elif verify_url_accessibility(git_repo) != 200:
        print("The provided repo is not accessible.")


clone_repo()


