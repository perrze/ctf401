# Tips_for_developping_frontend

## JavaScript libraries

### JQuery

JQuery is used here mainly to send request to API.
To do it use like this: (For a get)

```javascript=
function login(){
    let email=$("#emailLoginModal").val();
    let password=$("#passwordLoginModal").val();
    $.ajax({
        url: BASE_URL+'/users/login?email='+email+"&password="+password,
        type: 'get',
        statusCode: {
            200: function(response) {
                var token = response.token;
                Cookies.set('jwt',token,{ expires :1,sameSite:'Lax' });
                getUser();
                $('#loginModal').modal('hide');
            },
            401: function(xhr) {
                console.log("401");
                console.log(xhr.responseText);
    $('#tooltipLoginModal').removeAttr('hidden');
            }
            
        }
    });
}
```

It can also be used for manipulate HTML. For example you can add text inside an HTML markup:

```javascript=
$("#welcomeLoggedIn").html("Welcome, "+ (Cookies.get("email").split('@'))[0]);
```

But also to add a whole HTML file:

```javascript=
$("#divLoginModal").load('/snippets/users/loginModal.html');
```

It can be useful to use Snippets instead of static HTML

## Snippets

Snippets are sm all HTML code that can be used in many differents pages (like login interface) without the need of putting them in static in code.
For example, to add the infos of the user on top right if he is connected, we use:

```htmlbars=
<span class="d-flex pt-3" id="userManagement"</span>
```

And the javascript on top of this is calling the HTML file.
