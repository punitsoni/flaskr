function ajax_del_posts()
{
	var xmlhttp;
	xmlhttp = new XMLHttpRequest();
	xmlhttp.open("POST", "del_posts", true);
	xmlhttp.send();
	xmlhttp.onreadystatechange = function()
	{
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            /*document.getElementById("del_posts_resp").innerHTML
                = "All posts deleted";*/
            document.getElementById("dynamic_msg").innerHTML =
            "<div class=\"alert alert-success\"> \
                <button type=\"button\" class=\"close\" \
                data-dismiss=\"alert\">&times;</button> \
                <strong>Success!</strong> All posts deleted.</div>";
        }
    }
}