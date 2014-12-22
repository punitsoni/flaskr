function ajax_del_posts()
{
    /* TODO: rewrite using jQuery */
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

function getLocation()
{
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        x.innerHTML = "Geolocation is not supported by this browser.";
    }
}

function showPosition(pos)
{
    var loc = document.getElementById("loc-info");
    $("#loc-info").append("<strong>Your location is</strong> <br>" +
        "Latitute: " + pos.coords.latitude + "<br>" +
        "Longitude: " + pos.coords.longitude + "<br>");

    $("#loc-info").append("<strong>Approximate address</strong> <br>");

    /* google geolocation API */
    var uri = "https://maps.googleapis.com/maps/api/geocode/" +
        "json?latlng=" + pos.coords.latitude + "," + pos.coords.longitude +
        "&sensor=false";

    $.getJSON(uri, function(data, status) {
        var len = data.results.length;
        var addr = data.results[0].formatted_address;
        console.log("Address returned by google:");
        $("#loc-info").append(addr);
        for(var i=0; i<len; i++) {
            console.log(data.results[i].formatted_address);
        }
    });
}

function sysinfo_refresh()
{
    var sysinfo;
    (function worker() {
      $.ajax({
        url: '/ajax/sysinfo', 
        dataType: "json",
        success: function(data) {
                console.log(data);
                $("#mem_usage_bar").attr("aria-valuenow",
                  data.sysinfo.mem_usage_percent)
                $("#mem_usage_bar").css("width",
                  data.sysinfo.mem_usage_percent + "%")
                $("#mem_usage_bar").html(data.sysinfo.mem_usage_percent + " %");

                $("#cpu_bar0").attr("aria-valuenow",
                  data.sysinfo.cpu_util)
                $("#cpu_bar0").css("width",
                  data.sysinfo.cpu_util + "%")
                $("#cpu_bar0").html(data.sysinfo.cpu_util + " %");                

            },
        complete: function() {
                // Schedule the next request when the current one's complete
                setTimeout(worker, 2000);
            }
      });
    })();
}

/* Executed after window is loaded */
window.onload = function() {
/*    var payload = '䉁䅃䍂䉁䅃䍂䉁䅃䉁䅃䍂䉁䅃䍂䉁䅃䉁䅃䍂䉁䅃䍂䍂䉁䅃䍂䉁䅃';

    new Hexdump(payload, {
        container: 'hexdump'
        , base: 'hex'
        , width: 7
        , byteGrouping: 1
        , html: true
        , lineNumber: true
        , style: {
            lineNumberLeft: ''
            , lineNumberRight: ':'
            , stringLeft: '|'
            , stringRight: '|'
            , hexLeft: ''
            , hexRight: ''
            , hexNull: '.g'
            , stringNull: '.'
        }
    });
    console.log("Page Loaded.");*/
    getLocation();
}