if (Cookies.get('session_token') != undefined){
    document.getElementById('login').style.display = 'none';
    document.getElementById('logout').style.display = 'flex';
}else{
    document.getElementById('login').style.display = 'block';
    document.getElementById('logout').style.display = 'none';
}
