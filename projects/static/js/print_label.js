function get_param(){
    var queryString = decodeURIComponent(window.location.search);
    queryString = queryString.substring(1);
    var queries = queryString.split("&");

    document.getElementById("smpl_no").innerHTML = queries[0] + " - " + queries[5];
    document.getElementById("customer").innerHTML = queries[1];
    document.getElementById("size").innerHTML = queries[3] + "-" + queries[4] + "metres";
    document.getElementById("mill_id").innerHTML = queries[6];
    document.getElementById("grade").innerHTML = queries[7];

}