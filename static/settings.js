window.onload = () => {
    document.getElementById('password_element').style.top = '120%';
    $.get(document.location.origin + '/getSettings', function(data) {
        if(data.error == 'Invalid session') {
            window.location.href = document.location.origin + '/login';
        }else{
            document.getElementById('username').value = data.username;
            document.getElementById('student_id').value = data.student_id;
            document.getElementById('email').value = data.email;
            document.getElementById('real_name').value = data.real_name;
            document.getElementById('bio').value = data.bio;
        }
    });
}

document.getElementById('change_password').addEventListener('click', function() {
    document.getElementById('password_overlay').style.display = 'block';
    setTimeout(function() {
        document.getElementById('password_element').style.top = '50%';
    }, 300);
});

document.getElementById('close_change_password').addEventListener('click', function() {
    document.getElementById('password_element').style.top = '-20%';
    setTimeout(function() {
        document.getElementById('password_overlay').style.display = 'none';
        document.getElementById('password_element').style.top = '120%';
    }, 300);
});