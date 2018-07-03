
//获取cookie
function get_cookie(name) {
    var xsrf_cookies = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return xsrf_cookies[1]
}


//转到添加文章
$(document).ready(function(){
    // 添加新文章
    $('#add_article').click(function (event) {
        event.preventDefault();
        window.location = '/my_article/publish_articles';
    });


    //编辑文章
    var list = $('button[class="am-btn am-btn-default am-btn-xs am-text-secondary"]');
    for(var i=0;i<list.length;i++){
        list[i].onclick=function (e) {
            e.preventDefault();
        var unique_code = this.getAttribute('data-unique');
        window.location = '/my_admin/article_edit?unique_id='+ unique_code;
        }
    };


    //删除文章
    var delete_flag = $('button[class="am-btn am-btn-default am-btn-xs am-text-danger"]');
    var tr_select = $('tr[class="tr_select"]');
    for(var j=0;j<delete_flag.length;j++){
        delete_flag[j].onclick=function (e) {
            e.preventDefault();
            var delete_unique_code = this.getAttribute('data-unique');
        // window.location = '/my_admin/article_delete?delete_unique_id='+ delete_unique_code;

            swal({
				  title: "确定删除该文章吗",
				  text: "您即将删除该文章",
				  type: "info",
				  showCancelButton: true,
				  closeOnConfirm: false,
				  showLoaderOnConfirm: true,
                  confirmButtonText: "确定",
				  cancelButtonText: "取消",
				},
				function(){

            $.ajax({
            'url': '/my_admin/article_delete',
            'type': 'post',
            'data': {
               'delete_unique_id': delete_unique_code,
            },
            'headers':{
                 "X-XSRFTOKEN":get_cookie("_xsrf")
            },
            'success': function (data) {
               if(data['status'] == 200){
                   setTimeout(function(){
				    swal({
				  title: "<small>"+data['msg']+"</small>",
				  html: true,
				});
				  }, 2000);
                   window.location.reload();
               }else {
                    setTimeout(function(){
				    swal({
				  title: "<small>"+data['msg']+"</small>",
				  html: true,
				});
				  }, 2000);
               }
            }
        });
				});

        }
    };


    //复制
    //复制操作
        var copy_url = $('button[class="am-btn am-btn-default am-btn-xs"]');

        copy_url.click(function (e) {
            e.preventDefault();
            if(clipboard){
                alert('复制成功！');
                return ;
            }
        });
        var btns = document.querySelectorAll('button');
        var clipboard = new ClipboardJS(btns);



});
