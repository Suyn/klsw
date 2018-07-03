

//获取cookie
function get_cookie(name) {
    var xsrf_cookies = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return xsrf_cookies[1]
}


//simditor编辑器官网:http://simditor.tower.im/
// 初始化simditor的函数
$(document).ready(function() {
    var editor,toolbar;
    //编辑器工具栏里显示哪些工具
    toolbar = ['title', 'bold', 'italic', 'underline', 'strikethrough',
                'fontScale', 'color', '|', 'ol', 'ul', 'blockquote', 'code',
                'table', '|', 'link', 'image', 'hr', '|', 'indent', 'outdent', 'alignment'];
    //编辑器简体中文
    Simditor.locale = 'zh-CN';
    //初始化simditor
    editor = new Simditor({
        textarea: $('#editor'),//获取在哪个div上显示编辑器
        toolbar: toolbar,   //编辑器的工具栏
        pasteImage: true   //支持复制粘贴
    });
    // 加到window上去,其他地方才能访问到editor这个变量
    window.editor = editor;
});


//点击提交文档按钮函数
$(document).ready(function () {
    $('#submit-article-btn').click(function () {
        //获取输入函数
        var title = $('#article_title').val();
        var article = window.editor.getValue();
        var classify = $('#classify').val();
        var abstract = $('#article_abstract').val();
        var article_unique_id = $('#article_unique_id').val();
        var formdata = new FormData();
        formdata.append('title', title);
        formdata.append('abstract', abstract);
        formdata.append('article', article);
        formdata.append('classify', classify);
        formdata.append('article_unique_id', article_unique_id);
        formdata.append('article_pic', $('#article_pic')[0].files[0]);
        alert(formdata);
        $.ajax({
            'url': '/my_admin/article_edit',
            'type': 'post',
            'data': formdata,
            'cache': false,
            'processData': false,
            'contentType': false,
            'headers': {
                "X-XSRFTOKEN":get_cookie("_xsrf")
            },
            'success': function (data) {
                if (data['status'] == 200) {
                    swal({
                        'title': '正确',
                        'text': data['msg'],
                        'type': 'success',
                        'showCancelButton': false,
                        'showConfirmButton': false,
                        'timer': 1000,
                    },function () {
                       window.location = '/my_article/publish_articles';
                    });
                }else{
                    swal({
                        'title': '错误',
                        'text': data['msg'],
                        'type': 'error',
                        'showCancelButton': false,
                        'showConfirmButton': false,
                        'timer': 1000,
                    })
                }
            }
        })
    });

});


