# Connect_API_to_auth_API

## Contact users API to authenticate

```python=
global receivedToken
receivedToken = ""
global expireAt
expireAt = 0.0

def connect_services_to_auth():
    global receivedToken
    global expireAt
    with open(CREDS_LOCATION) as f:
        creds = json.load(f)
        email = creds["email"]
        password = creds["password"]

    result = requests.get(BASE_URL+"/users/login?email=" +
                          quote_plus(email)+"&password="+quote_plus(password))

    if result.status_code == 200:
        jsonLoaded = json.loads(result.content)
        receivedToken = jsonLoaded["token"]
        expireAt = jsonLoaded["expire"]
        return True
    else:
        return False
```

To use this function, a JSON file containing credentials must be used. Its location is declared in the global constant **CREDS_LOCATION**.
The format of the JSON is:

```json
{
    "email": "services+users@ctf401.fr",
    "password": "Bonjour1@"
}
```

This functions uses global variables defined just above.
They are storing the jwt and the expire time.
It contacts the users API and uses the global constant **BASE_URL** (Example: "http://api.ctf401.bb0.fr")

## Check the connection to auth API

```python=
def check_connected_to_auth():
    global receivedToken
    global expireAt
    if receivedToken == "" or expireAt <= time():
        connect_services_to_auth()
        return True
    else:
        return True
```

This function is called whenenever another function need to authenticate for example to check access to an API. It prevents too many calls to auth.

## Example of calling another API

```python=
@app.route("/users/temp/testAccess")
def testAccess():
    if not(check_connected_to_auth()): # Check if well connected and validity of creds
        return "Services unauthorized",401
    else:
        global receivedToken
        # API call that need to be auth
        callToAPI=requests.get(BASE_URL+"/users",headers={"jwt": receivedToken}).content
        return callToAPI,200
```

Here is a call to /users which need a JWT to get a result
