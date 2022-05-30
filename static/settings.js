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

document.getElementById('save_password').addEventListener('click', function() {
    var old_password = document.getElementById("old_password").value;
    var new_password = document.getElementById("new_password").value;
    var confirm_password = document.getElementById("confirm_password").value;

    if(old_password == '' || new_password == '' || confirm_password == '') {
        alert('Please fill in all fields');
        return;
    }

    if(new_password != confirm_password) {
        alert('New password and confirm password do not match');
        return;
    }

    $.post(document.location.origin + '/api/changePassword', {
        old_password: old_password,
        new_password: new_password
    }, function(data) {
        window.location.href = document.location.origin + '/login';
        if(data.error == 'Invalid session') {
        }else{
            alert(data.message);
        }
    });
});