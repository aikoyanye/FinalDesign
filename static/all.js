function Search(){
    alert(document.getElementById("key").value);
}

// 上次点击的id
var last_click_id = "a"
function Active(id){
    document.getElementById(last_click_id).className  = ""
    last_click_id = id
    document.getElementById(last_click_id).className  = "active"
}