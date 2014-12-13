function ajax_del_posts()
{
	var xmlhttp;
	xmlhttp = new XMLHttpRequest();
	xmlhttp.open("POST", "del_posts", true);
	xmlhttp.send();
	xmlhttp.onreadystatechange = function()
	{
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            document.getElementById("del_posts_resp").innerHTML
                = "All posts deleted";
        }
    }
}