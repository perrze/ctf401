function login(){
    let email=$("#emailLoginModal").val();
    let password=$("#passwordLoginModal").val();
    // console.log("Password: "+password)
    $.ajax({
        url: BASE_URL+'/users/login?email='+email+"&password="+password,
        type: 'get',
        statusCode: {
            200: function(response) {
                // console.log("200");
                // console.log(response);
                var token = response.token;
                // console.log(token);
                Cookies.set('jwt',token,{ expires :1,sameSite:'Lax' });
                // await new Promise(r => setTimeout(r, 2000));
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

function logout(){
    Cookies.remove('jwt');
    Cookies.remove('email');
    Cookies.remove('userid');
    Cookies.remove('description');
    Cookies.get('jwt');
    location.reload();
}

function getUser(){
    let jwt = Cookies.get("jwt");
    $.ajax({
        url: BASE_URL+'/users/check/jwt',
        type: 'get',
        headers : {jwt: jwt},
        statusCode: {
            200: function(response) {
                // console.log("200")
                console.log(response);
                Cookies.set('email',response.email,{ expires :1,sameSite:'Lax' });
                Cookies.set('userid',response.id_user,{ expires :1,sameSite:'Lax' });
                Cookies.set('description',response.description,{ expires :1,sameSite:'Lax' });
                Cookies.set('roles',String(response.roles),{ expires :1,sameSite:'Lax' });
                location.reload();
            },
            401: function(xhr) {
                console.log("401");
                console.log(xhr.responseText);
                
            }
            
        }
    });
}

