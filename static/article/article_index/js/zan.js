function get_cookie(name) {
    var xsrf_cookies = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return xsrf_cookies[1]
}



$.fn.postLike = function() {
    if ($(this).hasClass('done')) {
        return false;
    } else {
        $(this).addClass('done');
        var id = $(this).data("id"),
        rateHolder = $(this).children('.count');
        $.ajax({
	    	"url":"/my_article/article_details",
        	"type":"post",
        	"data": {
            	"article_id": id,
			},
        	"headers": {
	    		"X-XSRFTOKEN":get_cookie("_xsrf"),
			},
        	"success":function(data) {
	    	    if (data['status']==200){
	    	        $(rateHolder).html(data['msg']);
                }else{
	    	        swal(data['msg']);
                }
        }
	    });
        return false;
    }
};
$(document).on("click", ".favorite",
function() {
    $(this).postLike();
});

