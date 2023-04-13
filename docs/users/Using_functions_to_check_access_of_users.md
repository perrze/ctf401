# Using_functions_to_check_access_of_users

## Python Function to use

```python
def check_if_user_access(request, roles):
    token = None
    if "jwt" in request.headers:
        token = request.headers["jwt"]
    if not token:
        return False
        # return True
    for role in roles:
        result = requests.post(BASE_URL+"/users/check/" +
                               role, json={"token": token})
        if result.status_code == 200:
            return True
    return False
```

This function takes in:

- **request** variables the request var defined by default in a Flask path
- **roles** a list of roles (Example: ["admin","player"])

It uses the jwt headers so users must send a request to your Flask path with this headers:
`'jwt' : eyJhbGciOiJIU[...]j7Y`

It returns **True** if user has access to this role, **False** otherwise

It uses the global constant **BASE_URL** as the base link for the API. For example during dev we used "http://api.ctf401.bb0.fr"

## Use it in your Flask app

You have to add the call to the function at the start of your path:

```python=
@app.route('/users/create', methods=['POST'])
def createUser():
    if not (check_if_user_access(request, ["admin"])):
        return "Unauthorized", 401
```

It will return a 401 error if not well connected or the jwt not in headers
