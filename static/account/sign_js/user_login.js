//获取cookie
function get_cookie(name) {
    var xsrf_cookies = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return xsrf_cookies[1];
}

//提交登录请求
$(document).ready(function(){
    $('#login_submit').click(function (event) {
        event.preventDefault();
        user_email = $('#email').val();
        $.ajax({
            'url': '/user_login',
            'type': 'post',
            'data': {
               'account': $('#username').val(),
               'password':  $('#password').val(),
            },
            'headers':{
                 "X-XSRFTOKEN":get_cookie("_xsrf")
            },
            'success': function (data) {
                var error = document.getElementById('error');
               if(data['status'] == 200){
                   error.innerHTML = '<div class="alert alert-success" role="alert">'+data['msg']+'</div>';
                   setTimeout(function(){window.location = '/my_admin/user_account';},1000);
               }else {
                   error.innerHTML = '<div class="alert alert-success" role="alert">'+data['msg']+'</div>';
               }
            }
        });
    });
});