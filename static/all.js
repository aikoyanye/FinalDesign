function Search(){
    alert(document.getElementById("key").value);
}

function MainActivityClick(){
    $.ajax({
        url: "/activity",
        type: "GET",
        data: {type: "1"},
        success: function(arg){
            var data = jQuery.parseJSON(arg);
            var div = document.getElementById("main_activity_play")
            div.innerHTML = ""
            for (var i=0, l=data.length; i<l; i++){
                div.innerHTML = div.innerHTML + '<div class="panel panel-default"><div class="panel-body"><table style="table-layout:fixed" width="100%"><tr><td style="width:33%"><h5>开始时间：' + data[i][1] + '</h5></td><td style="width:32%"><h5>游客：' + data[i][4] + '(' + data[i][5] + ')</h5></td><td style="width:32%"><h5>类型：' + data[i][6] + '</h5></td><td align="right" style="width:3%"><h5><a onclick="ActivityComplate(\''+data[i][0]+'\', \''+data[i][1]+'\')" href="#">完成</a></h5></td></tr></table></div></div>'
            }
        }
    })
    $.ajax({
        url: "/activity",
        type: "GET",
        data: {type: "0"},
        success: function(arg){
            var data = jQuery.parseJSON(arg);
            var div = document.getElementById("main_activity_played")
            div.innerHTML = ""
            for (var i=0, l=data.length; i<l; i++){
                div.innerHTML = div.innerHTML + '<div class="panel panel-default"><div class="panel-body"><table width="100%"><tr><td width="45%">开始时间：'+data[i][1]+'</td><td width="45%">结束时间：'+data[i][2]+'</td></tr><tr><td width="33%">游客：'+data[i][6]+'('+data[i][7]+')</td><td width="33%">类型：'+data[i][8]+'</td><td width="33%">花费：'+data[i][3]+'</td></tr></table></div></div>'
            }
        }
    })
}

function ActivityComplate(id, created){
    var endtime = Date.parse(new Date())
//    alert((endtime - Date.parse(new Date(created)))/(1000*60))

    $.ajax({
        url: "/activity",
        type: "GET",
        data: {type: "200", id: id, cost: (endtime - Date.parse(new Date(created)))/(1000*60)*1},
        success: function(arg){
            MainActivityClick()
        }
    })
}