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
                div.innerHTML = div.innerHTML + '<div class="panel panel-default"><div class="panel-body"><table style="table-layout:fixed" width="100%"><tr><td style="width:33%"><h5>开始时间：' + data[i][1] + '</h5></td><td style="width:24%"><h5>游客：' + data[i][4] + '(' + data[i][5] + ')</h5></td><td style="width:24%"><h5>类型：' + data[i][6] + '</h5></td><td style="width:24%">已付押金：'+data[i][3]+'</td><td align="right" style="width:3%"><h5><a data-toggle="modal" data-target="#mo" onclick="ActivityComplateCheck(\''+data[i][0]+'\', \''+data[i][1]+'\', '+data[i][3]+')" href="#">完成</a></h5></td></tr></table></div></div>'
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
function ActivityComplateCheck(id, created, costed){
    var endtime = Date.parse(new Date());
    var cost = parseInt((endtime - Date.parse(new Date(created)))/(1000*60));
    var ret = costed - cost;
    if(ret > 0){
        var body = '本次消费为' + cost + '元，将从押金中扣除，多余的' + ret + '元将返回';
    }else{
        var body = '本次消费为' + cost + '元，将从押金中扣除，其次仍需支付' + ret + '元';
    }
    document.getElementById("modal_header").innerHTML = '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button><h4 class="modal-title">确认要提交吗？</h4>';
    document.getElementById("modal_body").innerHTML = body;
    document.getElementById("modal_footer").innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal">关闭</button><button type="button" data-dismiss="modal" class="btn btn-primary" onclick="ActivityComplate(\''+id+'\', \''+cost+'\')">提交</button>';
}

// member拉黑的确认模态框
function MemberInBlackModal(id){
    document.getElementById('modal_header').innerHTML = '确认要拉黑该用户？';
    document.getElementById('modal_body').innerHTML = '拉黑用户之后要联系超级管理员才能恢复';
    document.getElementById("modal_footer").innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal">关闭</button><button type="button" data-dismiss="modal" class="btn btn-primary" onclick="MemberInBlack('+id+')">确定</button>';
}

// member拉黑
function MemberInBlack(id){
    $.ajax({
        url: "/member",
        type: "PUT",
        data: {type: "1", id: id},
        success: function(arg){
            MainMemberClick();
        }
    })
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
                div.innerHTML = div.innerHTML + '<div class="panel panel-default"><div class="panel-body"><table style="table-layout:fixed" width="100%"><tr><td style="width:25%"><h5>' + data[i][1] + '(' + data[i][2] + ')</h5></td><td style="width:25%"><h5>创建时间：' + data[i][4] + '</h5></td><td style="width:20%"><h5>信誉：' + data[i][3] + '</h5></td><td style="width:25%"><h5>游玩次数：'+data[i][5]+'</h5></td><td><a data-toggle="modal" data-target="#mo" onclick="MemberInBlackModal('+data[i][0]+')">拉黑</a></td></tr></table></div></div>';
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
                div.innerHTML = div.innerHTML + '<div class="panel panel-default"><div class="panel-body"><table style="table-layout:fixed" width="100%"><tr><td style="width:25%"><h5>' + data[i][1] + '(' + data[i][2] + ')</h5></td><td style="width:25%"><h5>创建时间：' + data[i][4] + '</h5></td><td style="width:20%"><h5>信誉：' + data[i][3] + '</h5></td><td style="width:25%"><h5>游玩次数：'+data[i][5]+'</h5></td><td><a data-toggle="modal" data-target="#mo" onclick="MemberInBlackModal('+data[i][0]+')">拉黑</a></td></tr></table></div></div>';
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
                div.innerHTML = div.innerHTML + '<div class="panel panel-default"><div class="panel-body"><table width="100%"><tr><td width="20%">'+data[i][1]+'</td><td width="25%">'+data[i][6]+'</td><td width="25%">引进时间：'+data[i][4]+'</td><td width="25%">上次维修时间：'+data[i][7]+'</td><td width="5%"><a onclick="FixedShip('+data[i][0]+', 2)">完成</a></td></tr><tr><td colspan="5">描述：'+data[i][3]+'</td></tr></table></div></div>'
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
                div.innerHTML = div.innerHTML + '<div class="panel panel-default"><div class="panel-body"><table width="100%"><tr><td width="20%">'+data[i][1]+'</td><td width="25%">'+data[i][6]+'</td><td width="25%">引进时间：'+data[i][4]+'</td><td width="25%">上次维修时间：'+data[i][7]+'</td><td width="5%"><a onclick="FixedShip('+data[i][0]+', 1)">维修</a></td></tr><tr><td colspan="5">描述：'+data[i][3]+'</td></tr></table></div></div>'
            }
        }
    })
}

// 船只维修或修完完成
function FixedShip(id, type){
    $.ajax({
        url: "/ship",
        type: "PUT",
        data: {id: id, type: type},
        success: function(arg){
            MainShipClick();
        }
    })
}

// 管理员密钥提交方法
function FormKeySubmit(){
    document.getElementById("f_key").submit();
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
    document.getElementById('add_act_phone').value = value;
    $.ajax({
        url: "/member",
        type: "GET",
        data: {type: "4", phone: value},
        success: function(arg){
            var data = jQuery.parseJSON(arg);
            if(data[0] == "差"){
                alert('该用户信誉较差，请三思');
            }
        }
    })
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
            document.getElementById('add_title').innerHTML = '添加预约'
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
            var select1 = document.getElementById('gb_pid_select');
            var data = jQuery.parseJSON(arg);
            var l = data.length / 2;
            select.options.length = 0;
            select.add(new Option('请选择', '请选择'));
            select1.options.length = 0;
            select1.add(new Option('请选择', '请选择'));
            for (var i=0; i<l; i++){
                select.add(new Option(data[i], data[i+l]));
                select1.add(new Option(data[i], data[i+l]));
            }
        }
    })
}

// 广告套餐
function AdPackage(){
    document.getElementById("modal_header").innerHTML = '广告规则'
    document.getElementById("modal_footer").innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal">OK</button>'
    document.getElementById("modal_body").innerHTML = '<p>1、广告仅允许视频或图片轮播</p><p>2、视频大小不得超过130M</p><p>3、图片数量不得超过3张</p><p>4、广告投放时间最短为一星期<\p>'
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
    if(p1.files[0].size > 131457280){
        alert('文件大小超过130M');
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
            alert('上传成功');
            MainAdClick();
        }
    })
}

// 获取正在进行的广告
function ActivityAd(){
    $.ajax({
        url: "/ad",
        type: "GET",
        data: {type: "1"},
        success: function(arg){
            var reselts = jQuery.parseJSON(arg);
            var div = document.getElementById('main_ad_new')
            div.innerHTML = ''
            for (var i=0; i<reselts.length; i++){
                div.innerHTML = div.innerHTML + '<div class="panel panel-default"><div class="panel-body"><table width="100%"><tr><td width="10%">'+reselts[i][1]+'</td><td width="30%">'+reselts[i][2]+'</td><td width="30%">'+reselts[i][3]+'</td><td width="20%">'+reselts[i][4]+'</td><td width="10%"><a onclick="DestroyAd('+reselts[i][0]+')">销毁</a>&nbsp;&nbsp;<a data-toggle="modal" data-target="#preview_ad" onclick="PreviewAd('+reselts[i][0]+',\''+reselts[i][5]+'\')">预览</a></td></tr></table></div></div>'
            }
        }
    })
}

// 获取待审核的广告
function ExamineAd(){
    $.ajax({
        url: "/ad",
        type: "GET",
        data: {type: "2"},
        success: function(arg){
            var reselts = jQuery.parseJSON(arg);
            var div = document.getElementById('main_ad_break')
            div.innerHTML = ''
            for (var i=0; i<reselts.length; i++){
                div.innerHTML = div.innerHTML + '<div class="panel panel-default"><div class="panel-body"><table width="100%"><tr><td width="10%">'+reselts[i][1]+'</td><td width="30%">'+reselts[i][2]+'</td><td width="30%">'+reselts[i][3]+'</td><td width="20%">'+reselts[i][4]+'</td><td width="10%"><a onclick="DestroyAd('+reselts[i][0]+')">销毁</a>&nbsp;&nbsp;<a data-toggle="modal" data-target="#preview_ad" onclick="PreviewAd('+reselts[i][0]+',\''+reselts[i][5]+'\')">预览</a></td></tr></table></div></div>'
            }
        }
    })
}

// 获取关闭的广告
function ClosedAd(){
    $.ajax({
        url: "/ad",
        type: "GET",
        data: {type: "3"},
        success: function(arg){
            var reselts = jQuery.parseJSON(arg);
            var div = document.getElementById('main_ad_old')
            div.innerHTML = ''
            for (var i=0; i<reselts.length; i++){
                div.innerHTML = div.innerHTML + '<div class="panel panel-default"><div class="panel-body"><table width="100%"><tr><td width="10%">'+reselts[i][1]+'</td><td width="30%">'+reselts[i][2]+'</td><td width="30%">'+reselts[i][3]+'</td><td width="20%">'+reselts[i][4]+'</td><td width="10%"><a data-toggle="modal" data-target="#preview_ad" onclick="PreviewAd('+reselts[i][0]+',\''+reselts[i][5]+'\')">预览</a></td></tr></table></div></div>'
            }
        }
    })
}

// 获取审核失败的广告
function FalseAd(){
    $.ajax({
        url: "/ad",
        type: "GET",
        data: {type: "4"},
        success: function(arg){
            var reselts = jQuery.parseJSON(arg);
            var div = document.getElementById('main_ad_false');
            div.innerHTML = '';
            for (var i=0; i<reselts.length; i++){
                div.innerHTML = div.innerHTML + '<div class="panel panel-default"><div class="panel-heading">审核失败原因：'+reselts[i][6]+'</div><div class="panel-body"><table width="100%"><tr><td width="10%">'+reselts[i][1]+'</td><td width="30%">'+reselts[i][2]+'</td><td width="30%">'+reselts[i][3]+'</td><td width="20%">'+reselts[i][4]+'</td><td width="5%"><a data-toggle="modal" data-target="#preview_ad" onclick="PreviewAd('+reselts[i][0]+',\''+reselts[i][5]+'\')">预览</a></td><td><a data-toggle="modal" data-target="#put_ad_resource" onclick="PutAdResourceInit('+reselts[i][0]+', \''+reselts[i][1]+'\')">更换</a></td></tr></table></div></div>'
            }
        }
    })
}

// 更换广告的资源控制
function PutAdResource(type){
    if(type == 'video'){
        document.getElementById("put_ad_resource_footer").innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal">关闭</button><button type="button" class="btn btn-primary" onclick="PutAd(\'v\')" data-dismiss="modal">提交</button>'
        document.getElementById("put_ad_resource_body").innerHTML = '<label for="pp1">请选择视频</label><input type="file" id="pp1" name="pp1" accept="video/*">'
    }else{
        document.getElementById("put_ad_resource_footer").innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal">关闭</button><button type="button" class="btn btn-primary" onclick="PutAd(\'p\')" data-dismiss="modal">提交</button>'
        document.getElementById("put_ad_resource_body").innerHTML = '<label for="pp1">请选择图片</label><input type="file" id="pp1" name="pp1" accept="image/*"><input type="file" id="pp2" name="pp2" accept="image/*"><input type="file" id="pp3" name="pp3" accept="image/*">'
    }
}

// 更换广告默认点击图片单选框
function PutAdResourceInit(id, sponsor){
    document.getElementById('put_ad_resource_type_pic').onclick();
    document.getElementById('put_ad_resource_type_pic').checked = 'checked';
    document.getElementById('ad_sponsor_id').value = id;
    document.getElementById('ad_sponsor_name').value = sponsor;
}

// 更换广告资源
function PutAd(t){
    var pp1 = document.getElementById('pp1');
    if(pp1.value == ''){
        alert('输入框不能为空');
        return
    }
    if(pp1.files[0].size > 131457280){
        alert('文件大小超过130M');
        return
    }
    var d = new FormData();
    d.append('type', '3');
    d.append('pp1', document.getElementById('pp1').files[0]);
    d.append('num', '1');
    d.append('sponsor', document.getElementById('ad_sponsor_name').value);
    d.append('id', document.getElementById('ad_sponsor_id').value);
    if(t=='v'){
        d.append('t', '.mp4');
    }else{
        d.append('t', '.png');
        if(document.getElementById('pp2').value){
            d.append('pp2', document.getElementById('pp2').files[0]);
            d.append('num', '2');
        }
        if(document.getElementById('pp3').value){
            d.append('pp3', document.getElementById('pp3').files[0]);
            d.append('num', '3');
        }
    }
    $.ajax({
        url: "/ad",
        type: "PUT",
        data: d,
        processData: false,
        contentType: false,
        async: false,
        cache: false,
        success: function(arg){
            alert('更换成功');
            MainAdClick();
        }
    })
}

// 主页广告标签初始化
function MainAdClick(){
     ActivityAd();
     ExamineAd();
     ClosedAd();
     FalseAd();
}

// 销毁广告
function DestroyAd(id){
    $.ajax({
        url: "/ad",
        type: "PUT",
        data: {type: "1", id: id},
        success: function(arg){
            MainAdClick();
        }
    })
}

// 预览广告
function PreviewAd(id, content){
    $.ajax({
        url: "/ad",
        type: "PUT",
        data: {type: "2", id: id},
        success: function(arg){
            var reselts = jQuery.parseJSON(arg);
            if(reselts[0][1] == '.png'){
                var img_div = document.getElementById('ad_preview_main');
                var control_div = document.getElementById('ad_carousel_control');
                img_div.innerHTML = ''
                control_div.innerHTML = '<a class="left carousel-control" href="#ad_preview_carousel" role="button" data-slide="prev"><span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span><span class="sr-only">Previous</span></a>'
                control_div.innerHTML = control_div.innerHTML + '<a class="right carousel-control" href="#ad_preview_carousel" role="button" data-slide="next"><span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span><span class="sr-only">Next</span></a>'
                for(i=0; i<reselts.length; i++){
                    if(i==0){
                        img_div.innerHTML = img_div.innerHTML + '<div class="item active"><img src="'+reselts[i][0]+'" alt="资源无法加载"><div class="carousel-caption">'+content+'</div></div>'
                    }else{
                        img_div.innerHTML = img_div.innerHTML + '<div class="item"><img src="'+reselts[i][0]+'" alt="资源无法加载"><div class="carousel-caption">'+content+'</div></div>'
                    }
                }
            }else{
                document.getElementById('ad_carousel_control').innerHTML = ''
                document.getElementById('ad_preview_main').innerHTML = '<embed src="'+reselts[0][0]+'" width="560" height="480" />'
            }
        }
    })
}

// 添加团建
function AddGroupBuilding(){
    var i1 = document.getElementById('gb_phone');
    var i2 = document.getElementById('gb_count');
    var i3 = document.getElementById('gb_gname');
    var i4 = document.getElementById('gb_extra');
    var i5 = document.getElementById('gb_endtime');
    var i6 = document.getElementById('gb_cost');
    if(i2.value > 70){
        alert('人数不可超过70人');
        return
    }
    $.ajax({
        url: "/gb",
        type: "POST",
        data: {type: "1", phone: i1.value, count: i2.value, gname: i3.value, extra: i4.value, endtime: i5.value, cost: i6.value},
        success: function(arg){
            alert('添加团建成功');
            MainGroupBuilding();
        }
    })
}

// 团建规则
function GroupBuildingPackage(){
    document.getElementById("modal_header").innerHTML = '团建规则'
    document.getElementById("modal_footer").innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal">OK</button>'
    document.getElementById("modal_body").innerHTML = '<p>1、要提前一些时间预约</p><p>2、食物可以自带也可以在园区内购买，须提前通知</p><p>3、人数上限为70人</p><p>4、爱护环境，人人有责<\p>'
}

// 团建标签主页刷新
function MainGroupBuilding(){
    $.ajax({
        url: "/gb",
        type: "GET",
        data: {type: "1"},
        success: function(arg){
            var reselts = jQuery.parseJSON(arg);
            var div = document.getElementById('activity_gb');
            div.innerHTML = ''
            for(i=0; i<reselts.length; i++){
                div.innerHTML = div.innerHTML + '<div class="panel panel-default"><div class="panel-body"><table width="100%"><tr><td width="">'+reselts[i][8]+'</td><td width="">'+reselts[i][3]+'</td><td width="">'+reselts[i][5]+'</td><td width="">'+reselts[i][6]+'</td><td width="">'+reselts[i][7]+'</td><td width=""><a onclick="DestroyGb('+reselts[i][0]+')">完成</a></td></tr><tr><td>'+reselts[i][4]+'</td></tr></table></div></div>'
            }
        }
    })
    $.ajax({
        url: "/gb",
        type: "GET",
        data: {type: "2"},
        success: function(arg){
            var reselts = jQuery.parseJSON(arg);
            var div = document.getElementById('check_gb');
            div.innerHTML = ''
            for(i=0; i<reselts.length; i++){
                div.innerHTML = div.innerHTML + '<div class="panel panel-default"><div class="panel-body"><table width="100%"><tr><td width="">'+reselts[i][8]+'</td><td width="">'+reselts[i][3]+'</td><td width="">'+reselts[i][5]+'</td><td width="">'+reselts[i][6]+'</td><td width="">'+reselts[i][7]+'</td><td width=""><a onclick="DestroyGb('+reselts[i][0]+')">销毁</a></td></tr><tr><td>'+reselts[i][4]+'</td></tr></table></div></div>'
            }
        }
    })
    $.ajax({
        url: "/gb",
        type: "GET",
        data: {type: "3"},
        success: function(arg){
            var reselts = jQuery.parseJSON(arg);
            var div = document.getElementById('finish_gb');
            div.innerHTML = ''
            for(i=0; i<reselts.length; i++){
                div.innerHTML = div.innerHTML + '<div class="panel panel-default"><div class="panel-body"><table width="100%"><tr><td width="">'+reselts[i][8]+'</td><td width="">'+reselts[i][3]+'</td><td width="">'+reselts[i][5]+'</td><td width="">'+reselts[i][6]+'</td><td width="">'+reselts[i][7]+'</td><td width=""></td></tr><tr><td>'+reselts[i][4]+'</td></tr></table></div></div>'
            }
        }
    })
    $.ajax({
        url: "/gb",
        type: "GET",
        data: {type: "4"},
        success: function(arg){
            var reselts = jQuery.parseJSON(arg);
            var div = document.getElementById('broke_gb');
            div.innerHTML = ''
            for(i=0; i<reselts.length; i++){
                div.innerHTML = div.innerHTML + '<div class="panel panel-default"><div class="panel-heading">审核失败原因：'+reselts[i][8]+'</div><div class="panel-body"><table width="100%"><tr><td width="">'+reselts[i][9]+'</td><td width="">'+reselts[i][3]+'</td><td width="">'+reselts[i][5]+'</td><td width="">'+reselts[i][6]+'</td><td width="">'+reselts[i][7]+'</td><td width=""><a onclick="DestroyGb('+reselts[i][0]+')">销毁</a></td></tr><tr><td>'+reselts[i][4]+'</td></tr></table></div></div>'
            }
        }
    })
}

function DestroyGb(id){
    $.ajax({
        url: "/gb",
        type: "PUT",
        data: {type: "1", id: id},
        success: function(arg){
            MainGroupBuilding();
        }
    })
}