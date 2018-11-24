// 导航栏的搜索点击监听
function Search(){
    alert(document.getElementById("key").value);
}

// activity标签页的刷新
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
                div.innerHTML = div.innerHTML + '<div class="panel panel-default"><div class="panel-body"><table style="table-layout:fixed" width="100%"><tr><td style="width:33%"><h5>开始时间：' + data[i][1] + '</h5></td><td style="width:32%"><h5>游客：' + data[i][4] + '(' + data[i][5] + ')</h5></td><td style="width:32%"><h5>类型：' + data[i][6] + '</h5></td><td align="right" style="width:3%"><h5><a data-toggle="modal" data-target="#check" onclick="ActivityComplateCheck(\''+data[i][0]+'\', \''+data[i][1]+'\')" href="#">完成</a></h5></td></tr></table></div></div>'
//                div.innerHTML = div.innerHTML + '<div class="panel panel-default"><div class="panel-body"><table style="table-layout:fixed" width="100%"><tr><td style="width:33%"><h5>开始时间：' + data[i][1] + '</h5></td><td style="width:32%"><h5>游客：' + data[i][4] + '(' + data[i][5] + ')</h5></td><td style="width:32%"><h5>类型：' + data[i][6] + '</h5></td><td align="right" style="width:3%"><h5><a onclick="ActivityComplate(\''+data[i][0]+'\', \''+data[i][1]+'\')" href="#">完成</a></h5></td></tr></table></div></div>'
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

// activity完成的方法
function ActivityComplate(id, cost){
    $.ajax({
        url: "/activity",
        type: "GET",
        data: {type: "200", id: id, cost: cost},
        success: function(arg){
            MainActivityClick()
        }
    })
}

// activity确认完成的方法
function ActivityComplateCheck(id, created){
    var endtime = Date.parse(new Date())
//    alert((endtime - Date.parse(new Date(created)))/(1000*60))
    var div = document.getElementById("check_cost")
    var btn = document.getElementById("cost_commit")
    var cost = parseInt((endtime - Date.parse(new Date(created)))/(1000*60))
    div.innerHTML = '本次消费为' + cost + '元'
    btn.innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal">关闭</button><button type="button" data-dismiss="modal" class="btn btn-primary" onclick="ActivityComplate(\''+id+'\', \''+cost+'\')">提交</button>'
}

// member标签页刷新
function MainMemberClick(){
    $.ajax({
        url: "/member",
        type: "GET",
        data: {type: "1"},
        success: function(arg){
            var data = jQuery.parseJSON(arg);
            var div = document.getElementById("main_member_active")
            div.innerHTML = ""
            for (var i=0, l=data.length; i<l; i++){
                div.innerHTML = div.innerHTML + '<div class="panel panel-default"><div class="panel-body"><table style="table-layout:fixed" width="100%"><tr><td style="width:25%"><h5>' + data[i][1] + '(' + data[i][2] + ')</h5></td><td style="width:25%"><h5>创建时间：' + data[i][4] + '</h5></td><td style="width:25%"><h5>信誉：' + data[i][3] + '</h5></td><td style="width:25%"><h5>游玩次数：'+data[i][5]+'</h5></td></tr></table></div></div>'
            }
        }
    })
    $.ajax({
        url: "/member",
        type: "GET",
        data: {type: "0"},
        success: function(arg){
            var data = jQuery.parseJSON(arg);
            var div = document.getElementById("main_member")
            div.innerHTML = ""
            for (var i=0, l=data.length; i<l; i++){
                div.innerHTML = div.innerHTML + '<div class="panel panel-default"><div class="panel-body"><table style="table-layout:fixed" width="100%"><tr><td style="width:25%"><h5>' + data[i][1] + '(' + data[i][2] + ')</h5></td><td style="width:25%"><h5>创建时间：' + data[i][4] + '</h5></td><td style="width:25%"><h5>信誉：' + data[i][3] + '</h5></td><td style="width:25%"><h5>游玩次数：'+data[i][5]+'</h5></td></tr></table></div></div>'
            }
        }
    })
}