import re
import requests
from itertools import accumulate
from bs4 import BeautifulSoup as bs

ALPHA = 'ABCDEFGHIJKLMNOPQRST'

def read_file(path):
    with open(path, 'r') as f:
        return f.read().strip()


def ogs_auth():

    headers = {}
    creds = {
        'username': 'n_sweep',
        'password': read_file('/home/n/.config/ogs/pw'),
    }
    cookies = requests.post('https://online-go.com/api/v0/login', data=creds).cookies

    if 'csrftoken' in cookies:
        headers['Referer'] = 'https://online-go.com'
        headers['X-CSRFToken'] = cookies['csrftoken']

    r = requests.get(
        'https://online-go.com/api/v1/me',
        cookies=cookies,
        headers=headers
    )

    print(r.status_code, r.text)
    print(r.url)


def sgf_data() -> dict:
    r = requests.get('https://www.red-bean.com/sgf/proplist_ff.html')
    soup = bs(r.content, 'html.parser')
    lines = soup.find('pre').text.strip().split('\n')
    field_lengths = [len(d) for d in lines.pop(1).split(' ') if d]

    coords = list(zip(
        accumulate(field_lengths, lambda a, v: a + v + 2, initial=0),
        field_lengths
    ))

    processed_lines = list(map(lambda ln: [ln[x:x+l].strip() for x, l in coords], lines))
    keys = [field.lower().replace(' ', '_') for field in processed_lines.pop(0)]

    return {ln[0]: dict(zip(keys[1:], ln[1:])) for ln in processed_lines}


def main():
    game = ogs_auth


if __name__ == '__main__':
    main()
