
//获取cookie
function get_cookie(name) {
    var xsrf_cookies = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return xsrf_cookies[1]
}


//提交修改密码请求
$(document).ready(function(){
    $('#submit_pd').click(function (event) {
        event.preventDefault();
        $.ajax({
            'url': '/my_admin/modify_pd',
            'type': 'post',
            'data': {
               'password': $('#user-password').val(),
               'password2': $('#user-password2').val(),
            },
            'headers':{
                 "X-XSRFTOKEN":get_cookie("_xsrf")
            },
            'success': function (data) {
               if(data['status'] == 200){
                   swal({
                    'title': '修改成功',
                    'text': data['msg'],
                    'type': 'success',
					'showCancelButton': false,
                    'showConfirmButton': false,
					'timer': 1500,
                    'closeOnConfirm': false
                    },function () {
                       window.location = '/my_admin/user_account';
                    });

               }else {
                    swal({
                        title: "修改失败",
                        text: "错误信息：<span style='color: gray'>"+data['msg']+"<span>",
                        html: true
                    });
               }
            }
        });
    });
});

//提交修改邮箱请求
$(document).ready(function(){
    $('#submit_email').click(function (event) {
        event.preventDefault();
        $.ajax({
            'url': '/my_admin/modify_email',
            'type': 'post',
            'data': {
               'e-mail': $('#user-email').val(),
            },
            'headers':{
                 "X-XSRFTOKEN":get_cookie("_xsrf")
            },
            'success': function (data) {
               if(data['status'] == 200){
                   swal({
                    'title': '修改成功',
                    'text': data['msg'],
                    'type': 'success',
					'showCancelButton': false,
                    'showConfirmButton': false,
					'timer': 1500,
                    'closeOnConfirm': false
                    },function () {
                       window.location = '/my_admin/user_account';
                    });

               }else {
                    swal({
                        title: "修改失败",
                        text: "错误信息：<span style='color: gray'>"+data['msg']+"<span>",
                        html: true
                    });
               }
            }
        });
    });
});

