import requests
from os import getenv
urlHere='http://localhost:'

def test_get_200(base_url,uri):
    url=base_url+uri
    print("Running GET test on : "+uri)
    try:
        req = requests.get(url)
        if req.status_code==200:
            return True
        else:
            return False
    except:
        return False
    
def print_result(boolean,uri):
    if boolean:
        print("[\033[32;40mOK\033[0m] "+uri)
    else:
        print("[\033[31;40mKO\033[0m] "+uri)


def test_root_api(url):
    # /users
    port='5001'
    print_result(test_get_200(url,port),port)
    # /players
    port='5002'
    print_result(test_get_200(url,port),port)
    # /teams
    port='5003'
    print_result(test_get_200(url,port),port)
    # /challenges
    port='5004'
    print_result(test_get_200(url,port),port)
    # /games
    port='5005'
    print_result(test_get_200(url,port),port)
    
    
if __name__=="__main__":
    url=getenv('BASE_URL',urlHere)
    test_root_api(url)
