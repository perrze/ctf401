/* -------------------------------------------------------------------------- */
/*                 Write here functions needed across website                 */
/* -------------------------------------------------------------------------- */

/* ----------------------------- Global Var sets ---------------------------- */
let BASE_URL="http://api.ctf401.bb0.fr"

$( document ).ready(function(){
    if(Cookies.get("jwt")==undefined){
        $("#divLoginModal").load('/snippets/users/loginModal.html');
        $("#userManagement").load('/snippets/users/loginButton.html');
    }else{
        $("#userManagement").load('/snippets/users/loggedIn.html'); 
    }
});
