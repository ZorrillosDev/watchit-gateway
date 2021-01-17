import requests, os, random, time
from pathlib import Path
from resource.py import Log
from xmlrpc.client import ProtocolError
from resource.py.subs.opensubs import OPEN_SUBS_RECURSIVE_SLEEP_REQUEST
root_path = os.path.dirname(os.path.realpath(__file__))

# Session keep alive
# http://docs.python-requests.org/en/master/user/advanced/#request-and-response-objects
_agents = [
    'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/21.0',
    'Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'
]

def download_file(uri, _dir):
    """
    Take from the boring centralized network
    :param uri:
    :param _dir:
    :return:
    """
    session = requests.Session()
    directory = "%s/torrents/%s" % (root_path, _dir)
    dirname = os.path.dirname(directory)
    file_check = Path(directory)

    # already exists?
    if file_check.exists():
        print(f"{Log.WARNING}File already exists: {_dir}{Log.ENDC}")
        return directory

    # print(f"{Log.OKGREEN}Downloading file: {directory}{Log.ENDC}")
    # Create if not exist dir
    Path(dirname).mkdir(parents=True, exist_ok=True)
    response = session.get(uri, verify=True, stream=True, timeout=60, headers={
        'User-Agent': _agents[random.randint(0, 3)]
    })

    # Check status for response
    if response.status_code == requests.codes.ok:
        print(f"{Log.WARNING}Trying download to: {directory}{Log.ENDC}")
        with open(directory, "wb") as out:
            for block in response.iter_content(256):
                if not block: break
                out.write(block)
            out.close()

    print(f"{Log.OKGREEN}File stored in: {directory}{Log.ENDC}")
    return directory



def download_scrap_subs(current_imdb_code, sub_collection):
    """
    Download scrapped subs
    :param current_imdb_code:
    :param sub_collection:
    :return:
    """
    for lang, sub_lang in sub_collection.items():  # Key - Lang
        lang_cleaned = re.sub('[^a-zA-Z0-9 \n\.]', '', lang).replace(' ', '_')
        langs_dir = f"{current_imdb_code}/subs/{lang_cleaned}"
        for sub in sub_lang:  # Iterate over links
            url_link = sub['link']
            file_name = f"{url_link.rsplit('/', 1)[-1]}.zip"
            file_dir = "%s/%s" % (langs_dir, file_name)
            download_file(url_link, file_dir)
            sub['link'] = f"{lang_cleaned}/{file_name}"


def download_opensubs(current_imdb_code, sub_collection):
    """
    Api source download opensubs
    :param current_imdb_code:
    :param sub_collection:
    :return:
    """
    try:
        # TODO need process download over API
        # TODO https://github.com/agonzalezro/python-opensubtitles/blob/master/APPENDIX.md
        pass
    except ProtocolError as e:
        print("\n\033[93mWait", str(OPEN_SUBS_RECURSIVE_SLEEP_REQUEST * 2), 'seconds\033[0m\n')
        time.sleep(OPEN_SUBS_RECURSIVE_SLEEP_REQUEST * 2)
        return download_opensubs(current_imdb_code, sub_collection)
    except (TypeError, Exception) as e:
        print(e)
        print('No sub')


API_NEEDED = {'opensubs': download_opensubs}
