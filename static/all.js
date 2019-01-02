// 导航栏的搜索点击监听
function Search(){
    alert(document.getElementById("key").value);
}

// 首页mid组件初始化
function MidInit(){
    setInterval(MidInfo1, 10000);
    setInterval(MidInfo, 1000);
}

// 首页mid除天气外的数据
function MidInfo(){
    $.ajax({
        url: "/mid",
        type: "POST",
        data: {weather:"0"},
        success: function(arg){
            var data = jQuery.parseJSON(arg);
            document.getElementById("activity").innerHTML = "正在进行：" + data.activity
            document.getElementById("ship").innerHTML = "空闲游船：" + data.ship
            document.getElementById("last").innerHTML = "过去7天游玩数据：" + data.last
            document.getElementById("time").innerHTML = "当前日期和时间：" + data.time
            document.getElementById("brokeship").innerHTML = "无法使用游船：" + data.brokeship
        }
    })
}

// 首页mid组件天气数据
function MidInfo1(){
    $.ajax({
        url: "/mid",
        type: "POST",
        data: {weather:"1"},
        success: function(arg){
            var data = jQuery.parseJSON(arg);
            document.getElementById("weather").innerHTML = "当前天气：" + data.weather
        }
    })
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
                div.innerHTML = div.innerHTML + '<div class="panel panel-default"><div class="panel-body"><table style="table-layout:fixed" width="100%"><tr><td style="width:33%"><h5>开始时间：' + data[i][1] + '</h5></td><td style="width:24%"><h5>游客：' + data[i][4] + '(' + data[i][5] + ')</h5></td><td style="width:24%"><h5>类型：' + data[i][6] + '</h5></td><td style="width:24%">已付押金：'+data[i][3]+'</td><td align="right" style="width:3%"><h5><a data-toggle="modal" data-target="#mo" onclick="ActivityComplateCheck(\''+data[i][0]+'\', \''+data[i][1]+'\')" href="#">完成</a></h5></td></tr></table></div></div>'
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
    var cost = parseInt((endtime - Date.parse(new Date(created)))/(1000*60))
    document.getElementById("modal_header").innerHTML = '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button><h4 class="modal-title">确认要提交吗？</h4>'
    document.getElementById("modal_body").innerHTML = '本次消费为' + cost + '元';
    document.getElementById("modal_footer").innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal">关闭</button><button type="button" data-dismiss="modal" class="btn btn-primary" onclick="ActivityComplate(\''+id+'\', \''+cost+'\')">提交</button>';
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

// ship标签页刷新
function MainShipClick(){
    $.ajax({
        url: "/ship",
        type: "GET",
        data: {type: "1"},
        success: function(arg){
            var data = jQuery.parseJSON(arg);
            var div = document.getElementById("main_ship_active")
            div.innerHTML = ""
            for (var i=0, l=data.length; i<l; i++){
                div.innerHTML = div.innerHTML + '<div class="panel panel-default"><div class="panel-body"><table width="100%"><tr><td width="25%">'+data[i][1]+'</td><td width="25%">'+data[i][6]+'</td><td width="25%">引进时间：'+data[i][4]+'</td><td width="25%">上次维修时间：'+data[i][7]+'</td></tr><tr><td colspan="4">描述：'+data[i][3]+'</td></tr></table></div></div>'
            }
        }
    })
    $.ajax({
        url: "/ship",
        type: "GET",
        data: {type: "2"},
        success: function(arg){
            var data = jQuery.parseJSON(arg);
            var div = document.getElementById("main_broke_ship")
            div.innerHTML = ""
            for (var i=0, l=data.length; i<l; i++){
                div.innerHTML = div.innerHTML + '<div class="panel panel-default"><div class="panel-body"><table width="100%"><tr><td width="25%">'+data[i][1]+'</td><td width="25%">'+data[i][6]+'</td><td width="25%">引进时间：'+data[i][4]+'</td><td width="25%">上次维修时间：'+data[i][7]+'</td></tr><tr><td colspan="4">描述：'+data[i][3]+'</td></tr></table></div></div>'
            }
        }
    })
    $.ajax({
        url: "/ship",
        type: "GET",
        data: {type: "10086"},
        success: function(arg){
            var data = jQuery.parseJSON(arg);
            var div = document.getElementById("main_idle_ship")
            div.innerHTML = ""
            for (var i=0, l=data.length; i<l; i++){
                div.innerHTML = div.innerHTML + '<div class="panel panel-default"><div class="panel-body"><table width="100%"><tr><td width="25%">'+data[i][1]+'</td><td width="25%">'+data[i][6]+'</td><td width="25%">引进时间：'+data[i][4]+'</td><td width="25%">上次维修时间：'+data[i][7]+'</td></tr><tr><td colspan="4">描述：'+data[i][3]+'</td></tr></table></div></div>'
            }
        }
    })
}

// 管理员密钥提交方法
function FormKeySubmit(){
    document.getElementById("f_key").submit()
}

// 手工添加activity
function AddActivity(){
    var phone = document.getElementById('add_act_phone').value
    var t = document.getElementById('add_act_select_ship').value
    var cost = document.getElementById('add_activity_cost').value
    if(phone=="请选择" || t=="请选择" || cost==''){
        alert('选项不能为空')
    }else{
        $.ajax({
            url: "/activity",
            type: "POST",
            data: {type: 1, phone: phone, cost: cost, t: t},
            success: function(arg){
                MainActivityClick();
            }
        })
    }
}

// 添加activity模态框里的select选择事件
function AddActivitySelected(value){
    document.getElementById('add_act_phone').value = value
}

// 添加activity模态框的select option动态添加，key是显示的值，value是实际的指
function AddActivitySelectOption(k){
    $.ajax({
        url: "/member",
        type: "GET",
        data: {type: "2", key: k},
        success: function(arg){
            var select = document.getElementById('add_act_select');
            var data = jQuery.parseJSON(arg);
            var l = data.length / 2;
            select.options.length = 0;
            select.add(new Option('请选择', '请选择'))
            for (var i=0; i<l; i++){
                select.add(new Option(data[i], data[i+l]));
            }
        }
    })
}

// 添加活动时初始化模态框信息
function AddActivityInitShip(){
    document.getElementById('add_title').innerHTML = '添加活动';
    document.getElementById('add_btn').innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal">关闭</button><button type="button" class="btn btn-primary" onclick="AddActivity()" data-dismiss="modal">提交</button>';
    $.ajax({
        url: "/ship",
        type: "GET",
        data: {type: "3"},
        success: function(arg){
            var select = document.getElementById('add_act_select_ship');
            var data = jQuery.parseJSON(arg);
            select.options.length = 0;
            select.add(new Option('请选择', '请选择'))
            for (var i=0; i<data.length; i++){
                select.add(new Option(data[i], data[i]));
            }
        }
    })
}

// 首页预约标签初始化
function MainReservationInit(){
    $.ajax({
        url: "/activity",
        type: "GET",
        data: {type: "2"},
        success: function(arg){
            var data = jQuery.parseJSON(arg);
            var div = document.getElementById("main_reservation")
            div.innerHTML = ''
            for (var i=0, l=data.length; i<l; i++){
                div.innerHTML = div.innerHTML + '<div class="panel panel-default"><div class="panel-body"><table width="100%"><tr><td width="30%">'+data[i][6]+'('+data[i][7]+')</td><td width="30%">'+data[i][1]+'</td><td width="30%">'+data[i][12]+'</td><td width="5%" style="align:right"><a href="#" onclick="Reservation2Activity(\''+data[i][0]+'\', \''+data[i][4]+'\')">开始</a></td><td width="5%" style="align:right"><a href="#" onclick="DestroyReservation(\''+data[i][0]+'\', \''+data[i][4]+'\')">销毁</a></td></tr></table></div></div>'
            }
        }
    })
}

// 预约转正在进行
function Reservation2Activity(id, shipId){
    $.ajax({
        url: "/activity",
        type: "PUT",
        data: {type: "1", id: id, shipId: shipId},
        success: function(arg){
            MainReservationInit();
        }
    })
}

// 销毁预约
function DestroyReservation(id, shipId){
    $.ajax({
        url: "/activity",
        type: "PUT",
        data: {type: "2", id: id, shipId: shipId},
        success: function(arg){
            MainReservationInit();
        }
    })
}

// 手工添加预约
function AddReservation(){
    var phone = document.getElementById('add_act_phone').value
    var t = document.getElementById('add_act_select_ship').value
    var cost = document.getElementById('add_activity_cost').value
    if(phone=="请选择" || t=="请选择" || cost==''){
        alert('选项不能为空')
    }else{
        $.ajax({
            url: "/activity",
            type: "POST",
            data: {type: 2, phone: phone, cost: cost, t: t},
            success: function(arg){
                MainReservationInit();
            }
        })
    }
}

// 添加预约时初始化游船信息
function AddReservationInitShip(){
    $.ajax({
        url: "/ship",
        type: "GET",
        data: {type: "3"},
        success: function(arg){
            document.getElementById('add_title').innerHTML = '添加活动'
            document.getElementById('add_btn').innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal">关闭</button><button type="button" class="btn btn-primary" onclick="AddReservation()" data-dismiss="modal">提交</button>'
            var select = document.getElementById('add_act_select_ship');
            var data = jQuery.parseJSON(arg);
            select.options.length = 0;
            select.add(new Option('请选择', '请选择'))
            for (var i=0; i<data.length; i++){
                select.add(new Option(data[i], data[i]));
            }
        }
    })
}

// activity筛选，用户select点击
function ActivitySearchSelected(value){
    document.getElementById('act_search_phone').value = value;
    ActivitySearch();
}

// activity search改变筛选条件之后触发
function ActivitySearch(){
    $.ajax({
        url: "/activity",
        type: "GET",
        data: {
            type: "3", create: document.getElementById('create').value,
            created: document.getElementById('created').value,
            phone: document.getElementById('act_search_phone').value,
            ship: document.getElementById('act_search_ship').value
        },
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

// 添加activity模态框的select option动态添加，key是显示的值，value是实际的指
function ActivitySearchSelectOption(k){
    $.ajax({
        url: "/member",
        type: "GET",
        data: {type: "3", key: k},
        success: function(arg){
            var select = document.getElementById('act_search_select');
            var data = jQuery.parseJSON(arg);
            var l = data.length / 2;
            select.options.length = 0;
            select.add(new Option('请选择', '请选择'))
            for (var i=0; i<l; i++){
                select.add(new Option(data[i], data[i+l]));
            }
        }
    })
}

// 广告套餐
function AdPackage(){
    document.getElementById("modal_header").innerHTML = '广告规则'
    document.getElementById("modal_footer").innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal">OK</button>'
    document.getElementById("modal_body").innerHTML = '<p>1、广告仅允许视频或图片轮播</p><p>2、视频长度不得超过9s</p><p>3、图片数量不得超过3张</p><p>4、广告投放时间最短为一星期<\p>'
}

// 添加广告的资源控制
function AddAdResource(type){
    if(type == 'video'){
        document.getElementById("ad_model_footer").innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal">关闭</button><button type="button" class="btn btn-primary" onclick="AddAd(\'v\')" data-dismiss="modal">提交</button>'
        document.getElementById("ad_resource").innerHTML = '<label for="p1">请选择视频</label><input type="file" id="p1" name="p1" accept="video/*">'
    }else{
        document.getElementById("ad_model_footer").innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal">关闭</button><button type="button" class="btn btn-primary" onclick="AddAd(\'p\')" data-dismiss="modal">提交</button>'
        document.getElementById("ad_resource").innerHTML = '<label for="p1">请选择图片</label><input type="file" id="p1" name="p1" accept="image/*"><input type="file" id="p2" name="p2" accept="image/*"><input type="file" id="p3" name="p3" accept="image/*">'
    }
}

// 添加广告默认点击图片单选框
function AddAdResourceInit(){
    document.getElementById('ad_resource_type_pic').onclick();
    document.getElementById('ad_resource_type_pic').checked = 'checked'
}

// 上传广告信息，由于要使用ajax上传图片，所以用FormData
function AddAd(t){
    var ip1 = document.getElementById('sponsor');
    var ip2 = document.getElementById('endtime');
    var ip3 = document.getElementById('cost');
    var ip4 = document.getElementById('content');
    var p1 = document.getElementById('p1');
    if(ip1.value=='' || ip2.value=='' || ip3.value=='' || ip4.value=='' || p1.value==''){
        alert('输入框组不能为空');
        return
    }
    var d = new FormData();
    d.append('sponsor', ip1.value);
    d.append('endtime', ip2.value);
    d.append('cost', ip3.value);
    d.append('content', ip4.value);
    d.append('type', '1');
    d.append('p1', document.getElementById('p1').files[0]);
    d.append('num', '1');
    if(t=='v'){
        d.append('t', '.mp4');
    }else{
        d.append('t', '.png');
        if(document.getElementById('p2').value){
            d.append('p2', document.getElementById('p2').files[0]);
            d.append('num', '2');
        }
        if(document.getElementById('p3').value){
            d.append('p3', document.getElementById('p3').files[0]);
            d.append('num', '3');
        }
    }
    $.ajax({
        url: "/ad",
        type: "POST",
        data: d,
        processData: false,
        contentType: false,
        async: false,
        cache: false,
        success: function(arg){
            alert('ajax返回');
        }
    })
}