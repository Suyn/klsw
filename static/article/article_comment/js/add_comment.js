
function get_cookie(name) {
    var xsrf_cookies = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return xsrf_cookies[1]
}

$(document).ready(function() {
	$("#submit").click(function(event) {

		event.preventDefault();
		var comments=$("#comment").val();
		$.ajax({
	    	"url":"/my_article/article_comment",
        	"type":"post",
        	"data": {
	        	"comment": comments,
            	"article_id": $("#comment_post_ID").val(),
			},
        	"headers": {
	    		"X-XSRFTOKEN":get_cookie("_xsrf")
			},
        	"success":function(data) {
	    	if(data["status"]==200) {
	        	swal({
	            	title:"<small>评论成功</small>",
                	text:"<span style='color:gray'>"+data["msg"]+"</span>",
                	html:true
            },function() {
	// {#$('ol[name="add_article_comment"]').prepend('<li id=""> <span> <img src="../../static/avatar_images/useravatars/ {{current_user.avatar}}" class="avatar avatar-120" height="120" width="120"> </span>\n'+'  <div class="mhcc">\n'+"    <address>\n"+" " +#}
     // {#   "{{current_user.name}}"+now_time.toLocaleTimeString()+"\n"+"    </address>\n"+"        <p>"+comments+"</p>\n"+"  </div>\n"+"  </li>")#}
	        window.location.reload();
	})
	    }else {
	        	swal({
	            	title:"<small>评论失败</small>",
                	text:"错误信息：<span style='color:gray'>"+data["msg"]+"<span>",
                	html:true,
            	})}
	    }
	})})
});

    // {#function get_cookie(name){var xsrf_cookies=document.cookie.match("\\b"+name+"=([^;]*)\\b");return xsrf_cookies[1]}$(document).ready(function(){$("#submit").click(function(event){var now_time=new Date();event.preventDefault();var comments=$("#comment").val();$.ajax({"url":"/my_article/article_comment","type":"post","data":{"comment":comments,"article_id":$("#comment_post_ID").val(),},"headers":{"X-XSRFTOKEN":get_cookie("_xsrf")},"success":function(data){if(data["status"]==200){swal({title:"<small>评论成功</small>",text:"<span style='color: gray'>"+data["msg"]+"</span>",html:true},function(){$('ol[name="add_article_comment"]').prepend('<li id=""> <span> <img src="../../static/avatar_images/useravatars/{{ current_user.avatar }}" class="avatar avatar-120" height="120" width="120"> </span>\n'+'  <div class="mhcc">\n'+"    <address>\n"+"   {{ current_user.name }}  "+now_time.toLocaleTimeString()+"\n"+"    </address>\n"+"        <p>"+comments+"</p>\n"+"  </div>\n"+"  </li>")})}else{swal({title:"<small>评论失败</small>",text:"错误信息：<span style='color: gray'>"+data["msg"]+"<span>",html:true})}}})})});#}
