// activity可选择的状态
var ACTIVITY_STATUS = ['正在游玩', '已付款', '预约', '销毁']
// member可选择的状态
var MEMBER_REPUTATION = ['良', '差']
// ship可选择状态
var SHIP_STATUS = ['正在使用', '空闲', '维修']
var SHIP_TYPE = ['游船', '步行球']
// ad、GB可选状态
var AD_TYPE = ['待审核', '过期', '活动', '审核不通过']

// 添加管理员
function AddAdmin(){
    $.ajax({
        url: '/admin/key',
        type: 'put',
        data: {account: document.getElementById('admin_account').value,
                key: document.getElementById('admin_key').value,
                type: document.getElementById('admin_type').value},
        success: function(arg){
            window.location.reload();
        }
    });
}

// 批量删除过期活动
function OverActivitySubmit(){
    var items2 = { 'item': [] };
        $("input[name='act']:checked").each(function(i, n){
            items2['item'].push(n.value);
        });
        $.ajax({
            url: '/admin/activity/over',
            type: 'delete',
            data: items2,
            success: function(arg){
                window.location.reload();
            }
        });
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
                window.location.reload();
            }
        })
    }
}

// 预约转正在进行
function Reservation2Activity(id, shipId, userId){
    $.ajax({
        url: "/activity",
        type: "PUT",
        data: {type: "1", id: id, shipId: shipId, userId: userId},
        success: function(arg){
            window.location.reload();
        }
    })
}

// 销毁预约
function DestroyReservation(id, shipId, userId){
    $.ajax({
        url: "/activity",
        type: "PUT",
        data: {type: "2", id: id, shipId: shipId, userId: userId},
        success: function(arg){
            window.location.reload();
        }
    })
}

// 注销
function Logout(){
    $.ajax({
        url: "/admin",
        type: "DELETE",
        data: {},
        success: function(arg){
        }
    })
}

// 超级管理员登录模拟提交
function FormKeySubmit(){
    document.getElementById("f_key").submit()
}

// activity完成的方法
function ActivityComplate(id, cost){
    $.ajax({
        url: "/activity",
        type: "GET",
        data: {type: "200", id: id, cost: cost},
        success: function(arg){
            window.location.reload();
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

// activity中表格还原
function ActivityPutData(value, td_id, id, input_id, key){
    td_id.innerHTML = value;
    $.ajax({
        url: "/admin/activity",
        type: "POST",
        data: {key: key, id: id, value: value, type: '1'},
        success: function(arg){
        }
    })
}

// activity中点击表格单元格生成input
function ActivityTdOnClickInput(id, td_id, value, key){
    var input_id = td_id + '_input';
    if(document.getElementById(input_id) == null){
        var td = document.getElementById(td_id);
        td.innerHTML = '<input class="form-control" id="'+td_id+'_input" type="text" onblur="ActivityPutData(this.value, ' + td_id + ', '+id+', this.id, \''+key+'\')" value="' + value + '" >'
        document.getElementById(input_id).focus();
    }
}

// activity点击表格生成select
function ActivityTdOnClickSelect(id, td_id, value, key){
    var select_id = td_id + '_select';
    if(document.getElementById(select_id) == null){
        var td = document.getElementById(td_id);
        td.innerHTML = '<select class="form-control" id="'+select_id+'" onchange="ActivityPutData(this.value, '+td_id+', '+id+', this.id, \''+key+'\')">';
        var td_select = document.getElementById(select_id);
        for(var index in ACTIVITY_STATUS){
            if(ACTIVITY_STATUS[index] == value){
                td_select.innerHTML = td_select.innerHTML + '<option value="'+ACTIVITY_STATUS[index]+'" selected = "selected">'+ACTIVITY_STATUS[index]+'</option>';
            }else{
                td_select.innerHTML = td_select.innerHTML + '<option value="'+ACTIVITY_STATUS[index]+'">'+ACTIVITY_STATUS[index]+'</option>';
            }
        }
    }
}

// activity的表格隐藏与显示
function ActivityDisplayTr(id, tid){
    var tr = document.getElementById(id);
    var ttr = document.getElementById(tid);
    if(tr.style.display == 'none'){
        tr.style.display = '';
        ttr.style.display = '';
    }else{
        tr.style.display = 'none';
        ttr.style.display = 'none';
    }
}

// 添加会员
function AddMember(){
    var username = document.getElementById('member_name').value;
    var phone = document.getElementById('member_phone').value;
    var sex = document.getElementById('member_sex').value;
    if(username=='' || phone==''){
        alert('输入框组不能为空');
        return
    }
    $.ajax({
        url: "/admin/member",
        type: "POST",
        data: {username: username, phone: phone, sex: sex, type: '3'},
        success: function(arg){
            window.location.reload();
        }
    })
}

// member表格还原
function MemberPutData(value, td_id, id, input_id, key){
    td_id.innerHTML = value;
    $.ajax({
        url: "/admin/member",
        type: "POST",
        data: {key: key, id: id, value: value, type: '1'},
        success: function(arg){
        }
    })
}

// member点击表格生成input
function MemberTdOnClickInput(id, td_id, value, key){
    var input_id = td_id + '_input';
    if(document.getElementById(input_id) == null){
        var td = document.getElementById(td_id);
        td.innerHTML = '<input class="form-control" id="'+td_id+'_input" type="text" onblur="MemberPutData(this.value, ' + td_id + ', '+id+', this.id, \''+key+'\')" value="' + value + '" >'
        document.getElementById(input_id).focus();
    }
}

// member点击表格生成select
function MemberTdOnClickSelect(id, td_id, value, key){
    var select_id = td_id + '_select';
    if(document.getElementById(select_id) == null){
        var td = document.getElementById(td_id);
        td.innerHTML = '<select class="form-control" id="'+select_id+'" onchange="MemberPutData(this.value, '+td_id+', '+id+', this.id, \''+key+'\')">';
        var td_select = document.getElementById(select_id);
        for(var index in MEMBER_REPUTATION){
            if(MEMBER_REPUTATION[index] == value){
                td_select.innerHTML = td_select.innerHTML + '<option value="'+MEMBER_REPUTATION[index]+'" selected = "selected">'+MEMBER_REPUTATION[index]+'</option>';
            }else{
                td_select.innerHTML = td_select.innerHTML + '<option value="'+MEMBER_REPUTATION[index]+'">'+MEMBER_REPUTATION[index]+'</option>';
            }
        }
    }
}

// 初始化维护完毕模态框
function InitFinishBrokeShip(id){
    var footer = document.getElementById('finish_modal_footer');
    footer.innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>';
    footer.innerHTML = footer.innerHTML + '<button type="button" class="btn btn-primary" onclick="FinishBrokeShip('+id+')" data-dismiss="modal">提交</button>';
}

// 游船报废
function ScrapShip(id){
    $.ajax({
        url: '/admin/ship/broking',
        type: 'delete',
        data: {id: id},
        success: function(arg){
            window.location.reload();
        }
    });
}

// 维修完毕
function FinishBrokeShip(id){
    $.ajax({
        url: '/admin/ship/broking',
        type: 'put',
        data: {id: id,
            cost: document.getElementById('cost').value,
            reason: document.getElementById('reason').value},
        success: function(arg){
            window.location.reload();
        }
    });
}

// 初始化维护游船模态框
function InitBrokeShip(id){
    var footer = document.getElementById('broke_modal_footer');
    footer.innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>';
    footer.innerHTML = footer.innerHTML + '<button type="button" class="btn btn-primary" onclick="BrokeShip('+id+')" data-dismiss="modal">提交</button>';
}

// 维护游船
function BrokeShip(id){
    $.ajax({
        url: '/admin/ship/normal',
        type: 'put',
        data: {reason: document.getElementById('broke').value, id: id, type: '1'},
        success: function(arg){
            window.location.reload();
        }
    });
}

// 批量删除游船
function ReDeleteShip(){
    var items2 = { 'item': [] };
    $("input[name='ship_check']:checked").each(function(i, n){
        items2['item'].push(n.value);
    });
    $.ajax({
        url: '/admin/ship/normal',
        type: 'delete',
        data: items2,
        success: function(arg){
            FreeSpotShipType();
        }
    });
}

// 添加游船
function AddShip(){
    $.ajax({
        url: "/admin/ship/free",
        type: "POST",
        data: {shipname: document.getElementById('ship_name').value,
                type: document.getElementById('ship_type').value},
        success: function(arg){
            window.location.reload();
        }
    })
}

// ship表格还原
function ShipPutData(value, td_id, id, input_id, key){
    td_id.innerHTML = value;
    $.ajax({
        url: "/admin/ship",
        type: "POST",
        data: {key: key, id: id, value: value, type: '1'},
        success: function(arg){
        }
    })
}

// ship点击表格生成input
function ShipTdOnClickInput(id, td_id, value, key){
    var input_id = td_id + '_input';
    if(document.getElementById(input_id) == null){
        var td = document.getElementById(td_id);
        td.innerHTML = '<input class="form-control" id="'+td_id+'_input" type="text" onblur="ShipPutData(this.value, ' + td_id + ', '+id+', this.id, \''+key+'\')" value="' + value + '" >'
        document.getElementById(input_id).focus();
    }
}

// ship点击表格生成select
function ShipTdOnClickSelect(id, td_id, value, key, l){
    var select_id = td_id + '_select';
    if(document.getElementById(select_id) == null){
        var td = document.getElementById(td_id);
        td.innerHTML = '<select class="form-control" id="'+select_id+'" onchange="ShipPutData(this.value, '+td_id+', '+id+', this.id, \''+key+'\')">';
        var td_select = document.getElementById(select_id);
        for(var index in l){
            if(l[index] == value){
                td_select.innerHTML = td_select.innerHTML + '<option value="'+l[index]+'" selected = "selected">'+l[index]+'</option>';
            }else{
                td_select.innerHTML = td_select.innerHTML + '<option value="'+l[index]+'">'+l[index]+'</option>';
            }
        }
    }
}

// 批量删除过期广告
function DeleteOverAd(){
    var items2 = { 'item': [] };
        $("input[name='ad_check']:checked").each(function(i, n){
            items2['item'].push(n.value);
        });
        $.ajax({
            url: '/admin/ad/over',
            type: 'delete',
            data: items2,
            success: function(arg){
                window.location.reload();
            }
        });
}

// 广告下架
function OverAd(id){
    $.ajax({
        url: "/admin/ad/over",
        type: "post",
        data: {id: id},
        success: function(arg){
            window.location.reload();
        }
    })
}

// 广告续约
function RenewAd(id){
    if(document.getElementById('reendtime').value == '' ||
        document.getElementById('recost').value == ''){
        alert('输入框组不能为空');
        return
    }
    $.ajax({
        url: "/admin/ad/over",
        type: "put",
        data: {id: id,
            endtime: document.getElementById('reendtime').value,
            cost: document.getElementById('recost').value
        },
        success: function(arg){
            window.location.reload();
        }
    })
}

// 广告续约模态框初始化
function InitRenewAd(id){
    var footer = document.getElementById('renew_footer');
    footer.innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>';
    footer.innerHTML = footer.innerHTML + '<button type="button" class="btn btn-primary" onclick="RenewAd('+id+')">续约</button>';
}

// 审核广告模态框初始化
function InitExamineModal(id){
    var footer = document.getElementById('examine_modal_footer');
    footer.innerHTML = '<button type="button" class="btn btn-primary" onclick="ExamineNotPass('+id+')" data-dismiss="modal">审核不通过</button>';
    footer.innerHTML = footer.innerHTML + '<button type="button" class="btn btn-primary" onclick="ExaminePass('+id+')" data-dismiss="modal">审核通过</button>'
    footer.innerHTML = footer.innerHTML + '<button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>';
}

// 更换广告默认点击图片单选框
function PutAdResourceInit(id, sponsor, endtime, cost, content){
    document.getElementById('put_ad_resource_type_pic').onclick();
    document.getElementById('put_ad_resource_type_pic').checked = 'checked';
    document.getElementById('ad_sponsor_id').value = id;
    document.getElementById('ad_sponsor_name').value = sponsor;
    document.getElementById('reendtime').value = endtime;
    document.getElementById('recost').value = cost;
    document.getElementById('recontent').value = content;
}

// 更换广告资源
function PutAd(t){
    var pp1 = document.getElementById('pp1');
    if(pp1.value == '' || document.getElementById('reendtime').value == '' ||
    document.getElementById('recost').value == '' || document.getElementById('recontent').value == ''){
        alert('输入框不能为空');
        return
    }
    if(pp1.files[0].size > 131457280){
        alert('文件大小超过130M');
        return
    }
    var d = new FormData();
    d.append('endtime', document.getElementById('reendtime').value);
    d.append('cost', document.getElementById('recost').value);
    d.append('content', document.getElementById('recontent').value);
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
            window.location.reload();
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

// 广告审核不通过
function ExamineNotPass(id){
    if(document.getElementById('reason').value == ''){
        alert('不通过原因不能为空');
        return
    }
    $.ajax({
        url: "/admin/ad/examine",
        type: "put",
        data: {type: '2', id: id,
            reason: document.getElementById('reason').value},
        success: function(arg){
            window.location.reload();
        }
    })
}

// 广告审核通过
function ExaminePass(id){
    $.ajax({
        url: "/admin/ad/examine",
        type: "put",
        data: {type: '1', id: id},
        success: function(arg){
            window.location.reload();
        }
    })
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
            window.location.reload();
        }
    })
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
                        img_div.innerHTML = img_div.innerHTML + '<div class="item active"><img src="../../'+reselts[i][0]+'" alt="资源无法加载"><div class="carousel-caption">'+content+'</div></div>'
                    }else{
                        img_div.innerHTML = img_div.innerHTML + '<div class="item"><img src="../../'+reselts[i][0]+'" alt="资源无法加载"><div class="carousel-caption">'+content+'</div></div>'
                    }
                }
            }else{
                document.getElementById('ad_carousel_control').innerHTML = ''
                document.getElementById('ad_preview_main').innerHTML = '<embed src="../../'+reselts[0][0]+'" width="560" height="480" />'
            }
        }
    })
}

// ad表格还原
function AdPutData(value, td_id, id, input_id, key){
    td_id.innerHTML = value;
    $.ajax({
        url: "/admin/ad/now",
        type: "POST",
        data: {key: key, id: id, value: value, type: '1'},
        success: function(arg){
        }
    })
}

// ad点击表格生成input
function AdTdOnClickInput(id, td_id, value, key){
    var input_id = td_id + '_input';
    if(document.getElementById(input_id) == null){
        var td = document.getElementById(td_id);
        td.innerHTML = '<input class="form-control" id="'+td_id+'_input" type="text" onblur="AdPutData(this.value, ' + td_id + ', '+id+', this.id, \''+key+'\')" value="' + value + '" >'
        document.getElementById(input_id).focus();
    }
}

// ad点击表格生成select
function AdTdOnClickSelect(id, td_id, value, key){
    var select_id = td_id + '_select';
    if(document.getElementById(select_id) == null){
        var td = document.getElementById(td_id);
        td.innerHTML = '<select class="form-control" id="'+select_id+'" onchange="AdPutData(this.value, '+td_id+', '+id+', this.id, \''+key+'\')">';
        var td_select = document.getElementById(select_id);
        for(var index in AD_TYPE){
            if(AD_TYPE[index] == value){
                td_select.innerHTML = td_select.innerHTML + '<option value="'+AD_TYPE[index]+'" selected = "selected">'+AD_TYPE[index]+'</option>';
            }else{
                td_select.innerHTML = td_select.innerHTML + '<option value="'+AD_TYPE[index]+'">'+AD_TYPE[index]+'</option>';
            }
        }
    }
}

// 添加activity模态框的select option动态添加，key是显示的值，value是实际的指
function SearchActivitySearchSelectOption(k){
    $.ajax({
        url: "/member",
        type: "GET",
        data: {type: "3", key: k},
        success: function(arg){
            var select = document.getElementById('select_activity_phone');
            var select1 = document.getElementById('select_member_phone');
            var select2 = document.getElementById('select_gb_phone');
            var data = jQuery.parseJSON(arg);
            var l = data.length / 2;
            select.options.length = 0;
            select.add(new Option('请选择', ''));
            select1.options.length = 0;
            select1.add(new Option('请选择', ''));
            select2.options.length = 0;
            select2.add(new Option('请选择', ''));
            for (var i=0; i<l; i++){
                select.add(new Option(data[i], data[i+l]));
                select1.add(new Option(data[i], data[i+l]));
                select2.add(new Option(data[i], data[i+l]));
            }
        }
    })
}

// activity筛选，用户select点击
function SearchActivitySearchSelected(value){
    document.getElementById('activity_phone').value = value;
    ActivitySearch();
}

// 添加activity模态框的select option动态添加，key是显示的值，value是实际的指
function ActivitySearchSelectOption(k){
    $.ajax({
        url: "/member",
        type: "GET",
        data: {type: "3", key: k},
        success: function(arg){
//            var select = document.getElementById('act_search_select');
            var select1 = document.getElementById('gb_pid_select');
            var data = jQuery.parseJSON(arg);
            var l = data.length / 2;
//            select.options.length = 0;
//            select.add(new Option('请选择', '请选择'));
            select1.options.length = 0;
            select1.add(new Option('请选择', '请选择'));
            for (var i=0; i<l; i++){
//                select.add(new Option(data[i], data[i+l]));
                select1.add(new Option(data[i], data[i+l]));
            }
        }
    })
}

// 批量删除gb
function DeleteGb(){
    var items2 = { 'item': [] };
    $("input[name='gb_check']:checked").each(function(i, n){
        items2['item'].push(n.value);
    });
    $.ajax({
        url: '/admin/gb/over',
        type: 'delete',
        data: items2,
        success: function(arg){
            window.location.reload();
        }
    });
}

// 添加团建
function AddGroupBuilding(){
    var i1 = document.getElementById('gb_phone');
    var i2 = document.getElementById('gb_count');
    var i3 = document.getElementById('gb_gname');
    var i4 = document.getElementById('gb_extra');
    var i5 = document.getElementById('gb_endtime');
    var i6 = document.getElementById('gb_cost');
    if(i1.value=='' || i2.value=='' || i3.value=='' || i4.value=='' || i5.value=='' || i6.value==''){
        alert('输入框组不能为空');
    }
    if(i2.value > 70){
        alert('人数不可超过70人');
        return
    }
    $.ajax({
        url: "/gb",
        type: "POST",
        data: {type: "1", phone: i1.value, count: i2.value, gname: i3.value, extra: i4.value, endtime: i5.value, cost: i6.value},
        success: function(arg){
            window.location.reload();
        }
    })
}

// 结束正在活动中的团建
function OverGb(id){
    $.ajax({
        url: "/admin/gb/over",
        type: "POST",
        data: {id: id},
        success: function(arg){
            window.location.reload();
        }
    })
}

// gb审核模态框初始
function InitExamineGbModal(id){
    var footer = document.getElementById('examine_modal_footer');
    footer.innerHTML = '<button type="button" class="btn btn-primary" onclick="GbExamineNotPass('+id+')" data-dismiss="modal">审核不通过</button>';
    footer.innerHTML = footer.innerHTML + '<button type="button" class="btn btn-primary" onclick="GbExaminePass('+id+')" data-dismiss="modal">审核通过</button>'
    footer.innerHTML = footer.innerHTML + '<button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>';
}

// gb审核通过
function GbExaminePass(id){
    $.ajax({
        url: "/admin/gb/examine",
        type: "POST",
        data: {id: id, type: '1'},
        success: function(arg){
            window.location.reload();
        }
    })
}

// gb审核不通过
function GbExamineNotPass(id){
    if(document.getElementById('reason').value == ''){
        alert('输入框不能为空');
        return
    }
    $.ajax({
        url: "/admin/gb/examine",
        type: "POST",
        data: {id: id, type: '2',
            reason: document.getElementById('reason').value},
        success: function(arg){
            window.location.reload();
        }
    })
}

// gb修改团建信息模态框
function InitChangeGbModal(id, count, name, cost, endtime, extra){
    document.getElementById('regb_count').value = count;
    document.getElementById('regb_gname').value = name;
    document.getElementById('regb_cost').value = cost;
    document.getElementById('regb_endtime').value = endtime;
    document.getElementById('regb_extra').value = extra;
    var footer = document.getElementById('change_gb_footer');
    footer.innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>';
    footer.innerHTML = footer.innerHTML + '<button type="button" class="btn btn-primary" onclick="ChangeGbModal('+id+')" data-dismiss="modal">提交</button>';
}

// gb修改团建信息
function ChangeGbModal(id){
    if(document.getElementById('regb_count').value=='' ||
        document.getElementById('regb_gname').value=='' ||
        document.getElementById('regb_cost').value=='' ||
        document.getElementById('regb_endtime').value=='' ||
        document.getElementById('regb_extra').value==''){
        alert('输入框组不能为空');
    }
    $.ajax({
        url: "/admin/gb/broke",
        type: "POST",
        data: {id: id,
            count: document.getElementById('regb_count').value,
            name: document.getElementById('regb_gname').value,
            cost: document.getElementById('regb_cost').value,
            endtime: document.getElementById('regb_endtime').value,
            extra: document.getElementById('regb_extra').value},
        success: function(arg){
            window.location.reload();
        }
    })
}

// gb表格还原
function GbPutData(value, td_id, id, input_id, key){
    td_id.innerHTML = value;
    $.ajax({
        url: "/admin/gb",
        type: "POST",
        data: {key: key, id: id, value: value, type: '1'},
        success: function(arg){
        }
    })
}

// gb点击表格生成input
function GbTdOnClickInput(id, td_id, value, key){
    var input_id = td_id + '_input';
    if(document.getElementById(input_id) == null){
        var td = document.getElementById(td_id);
        td.innerHTML = '<input class="form-control" id="'+td_id+'_input" type="text" onblur="GbPutData(this.value, ' + td_id + ', '+id+', this.id, \''+key+'\')" value="' + value + '" >';
        document.getElementById(input_id).focus();
    }
}

// Gb点击表格生成select
function GbTdOnClickSelect(id, td_id, value, key){
    var select_id = td_id + '_select';
    if(document.getElementById(select_id) == null){
        var td = document.getElementById(td_id);
        td.innerHTML = '<select class="form-control" id="'+select_id+'" onchange="GbPutData(this.value, '+td_id+', '+id+', this.id, \''+key+'\')">';
        var td_select = document.getElementById(select_id);
        for(var index in AD_TYPE){
            if(AD_TYPE[index] == value){
                td_select.innerHTML = td_select.innerHTML + '<option value="'+AD_TYPE[index]+'" selected = "selected">'+AD_TYPE[index]+'</option>';
            }else{
                td_select.innerHTML = td_select.innerHTML + '<option value="'+AD_TYPE[index]+'">'+AD_TYPE[index]+'</option>';
            }
        }
    }
}

// 删除表格行数据的模态框的按钮
function DeleteModelu(id, row, uri, isA){
    var footer = document.getElementById('modal_table_footer');
    footer.innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>';
    footer.innerHTML = footer.innerHTML + '<button onclick="DeleltRow('+id+', '+row+', \''+uri+'\')" type="button" class="btn btn-primary" data-dismiss="modal">确定</button>';
}

// 删除表格中的一行数据，数据库
function DeleltRow(id, row, uri){
    $.ajax({
        url: "/admin/" + uri,
        type: "DELETE",
        data: {id: id},
        success: function(arg){
            document.getElementById('table').deleteRow(row-1);
        }
    })
}

// activity添加一行数据
function AddActivityTableRow(row_count){
    var nstatus = document.getElementById('nstatus'+row_count);
    var ncreated = document.getElementById('ncreated'+row_count);
    var nendtime = document.getElementById('nendtime'+row_count);
    var ncost = document.getElementById('ncost'+row_count);
    var nuser = document.getElementById('nuser'+row_count);
    var nship = document.getElementById('nship'+row_count);
    if(nstatus.value=="" || ncreated.value=="" || nendtime.value=="" || ncost.value=="" || nuser.value=="" || nship.value==""){
        alert('输入框数据不允许为空');
        return
    }
    $.ajax({
        url: "/admin/activity",
        type: "POST",
        data: {type: '2', status: nstatus.value, created: ncreated.value, endtime: nendtime.value, cost: ncost.value, user: nuser.value, ship: nship.value},
        success: function(arg){
            var data = jQuery.parseJSON(arg);
            var tr = document.getElementById('row'+row_count);
            tr.innerHTML = '<td><span onclick="DeleteModelu('+data[0]+', '+row_count+', \'activity\')" class="glyphicon glyphicon-remove" data-toggle="modal" data-target="#delete_table_modal">'+data[0]+'</span></td>';
            tr.innerHTML = tr.innerHTML + '<td id="status_'+data[0]+'" onclick="ActivityTdOnClickSelect('+data[0]+', this.id, \''+data[1]+'\', \'status\')">'+data[1]+'</td>';
            tr.innerHTML = tr.innerHTML + '<td id="created_'+data[0]+'" onclick="ActivityTdOnClickInput('+data[0]+', this.id, \''+data[2]+'\', \'created\')">'+data[2]+'</td>';
            tr.innerHTML = tr.innerHTML + '<td id="endtime_'+data[0]+'" onclick="ActivityTdOnClickInput('+data[0]+', this.id, \''+data[3]+'\', \'endtime\')">'+data[3]+'</td>';
            tr.innerHTML = tr.innerHTML + '<td id="cost_'+data[0]+'" onclick="ActivityTdOnClickInput('+data[0]+', this.id, \''+data[4]+'\', \'cost\')">'+data[4]+'</td>';
            tr.innerHTML = tr.innerHTML + '<td>'+data[5]+'</td>';
            tr.innerHTML = tr.innerHTML + '<td>'+data[6]+'</td>';
        }, error: function(arg){
            alert('输入的数据不符合条件');
        }
    })
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
                window.location.reload();
            }
        })
    }
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

// activity添加表格行
function ActivityAddRow(){
    var table = document.getElementById('table');
    var row_count = table.rows.length+1;
    var tr = table.insertRow(row_count-1);
    tr.id = 'row' + (row_count).toString();
    tr.innerHTML = '<td><span class="glyphicon glyphicon-ok" onclick="AddActivityTableRow('+row_count+')"></span></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="nstatus'+row_count+'"></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="ncreated'+row_count+'"></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="nendtime'+row_count+'"></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="ncost'+row_count+'"></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="nuser'+row_count+'"></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="nship'+row_count+'"></td>';
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

// ad添加一行数据
function AddAdTableRow(row_count){
    var nname = document.getElementById('nname'+row_count);
    var ncreated = document.getElementById('ncreated'+row_count);
    var nendtime = document.getElementById('nendtime'+row_count);
    var ncost = document.getElementById('ncost'+row_count);
    var ntype = document.getElementById('ntype'+row_count);
    var ncontent = document.getElementById('ncontent'+row_count);
    var nreason = document.getElementById('nreason'+row_count);
    if(nname.value=="" || ncreated.value=="" || nendtime.value=="" || ncost.value=="" || ntype.value=="" || ncontent.value=="" || nreason.value==""){
        alert('输入框内容不能空');
        return
    }
    $.ajax({
        url: "/admin/ad/now",
        type: "POST",
        data: {name: nname.value, created: ncreated.value, endtime: nendtime.value, cost: ncost.value, type: ntype.value, content: ncontent.value, reason: nreason.value},
        success: function(arg){
            var data = jQuery.parseJSON(arg);
            var tr = document.getElementById('row'+row_count);
            tr.innerHTML = '<td><span onclick="DeleteModelu('+data[0]+', '+row_count+', \'ad\')" class="glyphicon glyphicon-remove" data-toggle="modal" data-target="#delete_table_modal">'+data[0]+'</span></td>';
            tr.innerHTML = tr.innerHTML + '<td id="name_'+row_count+'" onclick="AdTdOnClickInput('+data[0]+', \'name_'+row_count+'\', \''+data[1]+'\', \'name\')">'+data[1]+'</td>';
            tr.innerHTML = tr.innerHTML + '<td id="created_'+row_count+'" onclick="AdTdOnClickInput('+data[0]+', \'created_'+row_count+'\', \''+data[2]+'\', \'created\')">'+data[2]+'</td>';
            tr.innerHTML = tr.innerHTML + '<td id="endtime_'+row_count+'" onclick="AdTdOnClickInput('+data[0]+', \'endtime_'+row_count+'\', \''+data[3]+'\', \'endtime\')">'+data[3]+'</td>';
            tr.innerHTML = tr.innerHTML + '<td id="cost_'+row_count+'" onclick="AdTdOnClickInput('+data[0]+', \'cost_'+row_count+'\', \''+data[4]+'\', \'cost\')">'+data[4]+'</td>';
            tr.innerHTML = tr.innerHTML + '<td id="type_'+row_count+'" onclick="AdTdOnClickInput('+data[0]+', \'type_'+row_count+'\', \''+data[5]+'\', \'type\')">'+data[5]+'</td>';
            tr.innerHTML = tr.innerHTML + '<td id="content_'+row_count+'" onclick="AdTdOnClickInput('+data[0]+', \'content_'+row_count+'\', \''+data[6]+'\', \'content\')">'+data[6]+'</td>';
            tr.innerHTML = tr.innerHTML + '<td id="reason_'+row_count+'" onclick="AdTdOnClickInput('+data[0]+', \'reason_'+row_count+'\', \''+data[7]+'\', \'reason\')">'+data[7]+'</td>';
        }, error: function(arg){
            alert('输入的数据不符合条件');
        }
    })
}

// ad添加表格行
function AdAddRow(){
    var table = document.getElementById('table');
    var row_count = table.rows.length+1;
    var tr = table.insertRow(row_count-1);
    tr.id = 'row' + (row_count).toString();
    tr.innerHTML = '<td><span class="glyphicon glyphicon-ok" onclick="AddAdTableRow('+row_count+')"></span></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="nname'+row_count+'"></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="ncreated'+row_count+'"></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="nendtime'+row_count+'"></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="ncost'+row_count+'"></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="ntype'+row_count+'"></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="ncontent'+row_count+'"></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="nreason'+row_count+'"></td>';
}

// gb添加一行数据
function AddGbTableRow(row_count){
    var ncount = document.getElementById('ncount'+row_count);
    var nname = document.getElementById('nname'+row_count);
    var nextre = document.getElementById('nextre'+row_count);
    var ncreated = document.getElementById('ncreated'+row_count);
    var nendtime = document.getElementById('nendtime'+row_count);
    var ntype = document.getElementById('ntype'+row_count);
    var ncost = document.getElementById('ncost'+row_count);
    var nreason = document.getElementById('nreason'+row_count);
    if(ncount.value=="" || nname.value=="" || nextre.value=="" || ncreated.value=="" || nendtime.value=="" || ntype.value=="" || ncost.value=="" || nreason.value==""){
        alert('输入框内容不能空');
        return
    }
    $.ajax({
        url: "/admin/gb",
        type: "POST",
        data: {count: ncount.value, gname: nname.value, extre: nextre.value, created: ncreated.value, endtime: nendtime.value, type: ntype.value, cost: ncost.value, reason: nreason.value},
        success: function(arg){
            var data = jQuery.parseJSON(arg);
            var tr = document.getElementById('row'+row_count);
            tr.innerHTML = '<td><span onclick="DeleteModelu('+data[0]+', '+row_count+', \'gb\')" class="glyphicon glyphicon-remove" data-toggle="modal" data-target="#delete_table_modal">'+data[0]+'</span></td>';
            tr.innerHTML = tr.innerHTML + '<td id="count_'+row_count+'" onclick="GbTdOnClickInput('+data[0]+', \'count_'+row_count+'\', \''+data[2]+'\', \'count\')">'+data[2]+'</td>';
            tr.innerHTML = tr.innerHTML + '<td id="gname_'+row_count+'" onclick="GbTdOnClickInput('+data[0]+', \'gname_'+row_count+'\', \''+data[3]+'\', \'gname\')">'+data[3]+'</td>';
            tr.innerHTML = tr.innerHTML + '<td id="extre_'+row_count+'" onclick="GbTdOnClickInput('+data[0]+', \'extre_'+row_count+'\', \''+data[4]+'\', \'extra\')">'+data[4]+'</td>';
            tr.innerHTML = tr.innerHTML + '<td id="created_'+row_count+'" onclick="GbTdOnClickInput('+data[0]+', \'created_'+row_count+'\', \''+data[6]+'\', \'created\')">'+data[6]+'</td>';
            tr.innerHTML = tr.innerHTML + '<td id="endtime_'+row_count+'" onclick="GbTdOnClickInput('+data[0]+', \'endtime_'+row_count+'\', \''+data[5]+'\', \'endtime\')">'+data[5]+'</td>';
            tr.innerHTML = tr.innerHTML + '<td id="type_'+row_count+'" onclick="GbTdOnClickSelect('+data[0]+', \'type_'+row_count+'\', \''+data[7]+'\', \'type\')">'+data[7]+'</td>';
            tr.innerHTML = tr.innerHTML + '<td id="cost_'+row_count+'" onclick="GbTdOnClickInput('+data[0]+', \'cost_'+row_count+'\', \''+data[8]+'\', \'cost\')">'+data[8]+'</td>';
            tr.innerHTML = tr.innerHTML + '<td id="reason_'+row_count+'" onclick="GbTdOnClickInput('+data[0]+', \'reason_'+row_count+'\', \''+data[9]+'\', \'reason\')">'+data[9]+'</td>';
        }, error: function(arg){
            alert('输入的数据不符合条件');
        }
    })
}

// gb添加表格行
function GbAddRow(){
    var table = document.getElementById('table');
    var row_count = table.rows.length+1;
    var tr = table.insertRow(row_count-1);
    tr.id = 'row' + (row_count).toString();
    tr.innerHTML = '<td><span class="glyphicon glyphicon-ok" onclick="AddGbTableRow('+row_count+')"></span></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="ncount'+row_count+'"></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="nname'+row_count+'"></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="nextre'+row_count+'"></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="ncreated'+row_count+'"></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="nendtime'+row_count+'"></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="ncost'+row_count+'"></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="ntype'+row_count+'"></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="nreason'+row_count+'"></td>';
}

// member添加一行数据
function AddMemberTableRow(row_count){
    var nusername = document.getElementById('nusername'+row_count);
    var nphone = document.getElementById('nphone'+row_count);
    var nreputation = document.getElementById('nreputation'+row_count);
    var ncreated = document.getElementById('ncreated'+row_count);
    var ntime = document.getElementById('ntime'+row_count);
    if(nusername.value=="" || nphone.value=="" || nreputation.value=="" || ncreated.value=="" || ntime.value==""){
        alert('输入框内容不能空');
        return
    }
    $.ajax({
        url: "/admin/member",
        type: "POST",
        data: {type: '2', username: nusername.value, phone: nphone.value, reputation: nreputation.value, created: ncreated.value, time: ntime.value},
        success: function(arg){
            var data = jQuery.parseJSON(arg);
            var tr = document.getElementById('row'+row_count);
            tr.innerHTML = '<td><span onclick="DeleteModelu('+data[0]+', '+row_count+', \'member\')" class="glyphicon glyphicon-remove" data-toggle="modal" data-target="#delete_table_modal">'+data[0]+'</span></td>';
            tr.innerHTML = tr.innerHTML + '<td id="username_'+row_count+'" onclick="MemberTdOnClickInput('+data[0]+', \'count_'+row_count+'\', \''+data[1]+'\', \'username\')">'+data[1]+'</td>';
            tr.innerHTML = tr.innerHTML + '<td id="phone_'+row_count+'" onclick="MemberTdOnClickInput('+data[0]+', \'phone_'+row_count+'\', \''+data[2]+'\', \'phone\')">'+data[2]+'</td>';
            tr.innerHTML = tr.innerHTML + '<td id="reputation_'+row_count+'" onclick="MemberTdOnClickInput('+data[0]+', \'reputation_'+row_count+'\', \''+data[3]+'\', \'reputation\')">'+data[3]+'</td>';
            tr.innerHTML = tr.innerHTML + '<td id="created_'+row_count+'" onclick="MemberTdOnClickInput('+data[0]+', \'created_'+row_count+'\', \''+data[4]+'\', \'created\')">'+data[4]+'</td>';
            tr.innerHTML = tr.innerHTML + '<td id="time_'+row_count+'" onclick="MemberTdOnClickInput('+data[0]+', \'time_'+row_count+'\', \''+data[5]+'\', \'time\')">'+data[5]+'</td>';
        }, error: function(arg){
            alert('输入的数据不符合条件');
        }
    })
}

// member添加表格行
function MemberAddRow(){
    var table = document.getElementById('table');
    var row_count = table.rows.length+1;
    var tr = table.insertRow(row_count-1);
    tr.id = 'row' + (row_count).toString();
    tr.innerHTML = '<td><span class="glyphicon glyphicon-ok" onclick="AddMemberTableRow('+row_count+')"></span></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="nusername'+row_count+'"></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="nphone'+row_count+'"></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="nreputation'+row_count+'"></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="ncreated'+row_count+'"></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="ntime'+row_count+'"></td>';
}

// ship添加一行数据
function AddShipTableRow(row_count){
    var nshipname = document.getElementById('nshipname'+row_count);
    var nstatus = document.getElementById('nstatus'+row_count);
    var ndescroption = document.getElementById('ndescroption'+row_count);
    var ncreated = document.getElementById('ncreated'+row_count);
    var ntime = document.getElementById('ntime'+row_count);
    var ntype = document.getElementById('ntype'+row_count);
    if(nshipname.value=="" || nstatus.value=="" || ndescroption.value=="" || ncreated.value=="" || ntype.value==""){
        alert('输入框内容不能空');
        return
    }
    $.ajax({
        url: "/admin/ship",
        type: "POST",
        data: {shipname: nshipname.value, status: nstatus.value, descroption: ndescroption.value, created: ncreated.value, time: ntime.value, type: ntype.value},
        success: function(arg){
            var data = jQuery.parseJSON(arg);
            var tr = document.getElementById('row'+row_count);
            tr.innerHTML = '<td><span onclick="DeleteModelu('+data[0]+', '+row_count+', \'ship\')" class="glyphicon glyphicon-remove" data-toggle="modal" data-target="#delete_table_modal">'+data[0]+'</span></td>';
            tr.innerHTML = tr.innerHTML + '<td id="shipname_'+row_count+'" onclick="ShipTdOnClickInput('+data[0]+', \'shipname_'+row_count+'\', \''+data[1]+'\', \'shipname\')">'+data[1]+'</td>';
            tr.innerHTML = tr.innerHTML + '<td id="status_'+row_count+'" onclick="ShipTdOnClickSelect('+data[0]+', \'status_'+row_count+'\', \''+data[2]+'\', \'phone\', SHIP_STATUS)">'+data[2]+'</td>';
            tr.innerHTML = tr.innerHTML + '<td id="descroption_'+row_count+'" onclick="ShipTdOnClickInput('+data[0]+', \'descroption_'+row_count+'\', \''+data[3]+'\', \'descroption\')">'+data[3]+'</td>';
            tr.innerHTML = tr.innerHTML + '<td id="created_'+row_count+'" onclick="ShipTdOnClickInput('+data[0]+', \'created_'+row_count+'\', \''+data[4]+'\', \'created\')">'+data[4]+'</td>';
            tr.innerHTML = tr.innerHTML + '<td id="time_'+row_count+'" onclick="ShipTdOnClickInput('+data[0]+', \'time_'+row_count+'\', \''+data[5]+'\', \'time\')">'+data[5]+'</td>';
            tr.innerHTML = tr.innerHTML + '<td id="type_'+row_count+'" onclick="ShipTdOnClickSelect('+data[0]+', \'type_'+row_count+'\', \''+data[6]+'\', \'type\', SHIP_TYPE)">'+data[6]+'</td>';
        }, error: function(arg){
            alert('输入的数据不符合条件');
        }
    })
}

// ship添加表格行
function ShipAddRow(){
    var table = document.getElementById('table');
    var row_count = table.rows.length+1;
    var tr = table.insertRow(row_count-1);
    tr.id = 'row' + (row_count).toString();
    tr.innerHTML = '<td><span class="glyphicon glyphicon-ok" onclick="AddShipTableRow('+row_count+')"></span></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="nshipname'+row_count+'"></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="nstatus'+row_count+'"></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="ndescroption'+row_count+'"></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="ncreated'+row_count+'"></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="ntime'+row_count+'"></td>';
    tr.innerHTML = tr.innerHTML + '<td><input type="text" class="form-control" id="ntype'+row_count+'"></td>';
}

// key点击表格生成input
function KeyTdOnClickInput(id, td_id, value, key){
    var input_id = td_id + '_input';
    if(document.getElementById(input_id) == null){
        var td = document.getElementById(td_id);
        td.innerHTML = '<input class="form-control" id="'+td_id+'_input" type="text" onblur="KeyPutData(this.value, ' + td_id + ', '+id+', this.id, \''+key+'\')" value="' + value + '" >'
        document.getElementById(input_id).focus();
    }
}

// key表格还原
function KeyPutData(value, td_id, id, input_id, key){
    td_id.innerHTML = value;
    $.ajax({
        url: "/admin/key",
        type: "POST",
        data: {key: key, id: id, value: value},
        success: function(arg){
        }
    })
}

// 导出数据
function Data2Excel(uri, type){
    $.ajax({
        url: "/admin"+uri,
        type: "put",
        data: {type: type},
        success: function(arg){
            document.getElementById('download_a').click();
        }
    })
}

// activity搜索筛选
function ActivitySearch(){
    $.ajax({
        url: "/admin/search",
        type: "put",
        data: {created: document.getElementById('activity_created').value,
            endtime: document.getElementById('activity_endtime').value,
            phone: document.getElementById('activity_phone').value,
            status: document.getElementById('activity_status').value,
            type: '1'},
        success: function(arg){
            ShowActivitySearch(jQuery.parseJSON(arg));
        }
    })
}

// activity搜索初始化
function InitActivitySearch(){
    document.getElementById('activity_search_table').style.display = '';
    document.getElementById('ship_search_table').style.display = 'none';
    document.getElementById('member_search_table').style.display = 'none';
    document.getElementById('ad_search_table').style.display = 'none';
    document.getElementById('gb_search_table').style.display = 'none';
    $.ajax({
        url: "/admin/search",
        type: "post",
        data: {type: '1'},
        success: function(arg){
            ShowActivitySearch(jQuery.parseJSON(arg));
        }
    })
}

// activity结果展示
function ShowActivitySearch(data){
    var table = document.getElementById('main_search_table');
    table.innerHTML = '';
    var th = table.insertRow(0);
    th.innerHTML = '<th>活动编号</th><th>活动状态</th><th>租船起始时间</th><th>船只归还时间</th><th>押金</th><th>租金</th><th>会员名称</th><th>会员电话</th><th>船只名称</th>';
    for (var i=0, l=data.length; i<l; i++){
        var tr = table.insertRow(i+1);
        tr.innerHTML = '<td>'+data[i][0]+'</td><td>'+data[i][1]+'</td><td>'+data[i][2]+'</td><td>'+data[i][3]+'</td><td>'+data[i][4]+'</td><td>'+data[i][5]+'</td><td>'+data[i][6]+'</td><td>'+data[i][7]+'</td><td>'+data[i][8]+'</td>';
    }
}

// ship搜索初始化
function InitShipSearch(){
    document.getElementById('activity_search_table').style.display = 'none';
    document.getElementById('ship_search_table').style.display = '';
    document.getElementById('member_search_table').style.display = 'none';
    document.getElementById('ad_search_table').style.display = 'none';
    document.getElementById('gb_search_table').style.display = 'none';
    $.ajax({
        url: "/admin/search",
        type: "post",
        data: {type: '2'},
        success: function(arg){
            ShowShipSearch(jQuery.parseJSON(arg));
        }
    })
    $.ajax({
        url: "/admin/ship",
        type: "delete",
        data: {type: '1'},
        success: function(arg){
            var select = document.getElementById('ship_spot');
            var data = jQuery.parseJSON(arg);
            select.innerHTML = '<option value="">请选择</option>';
            for (var i=0, l=data.length; i<l; i++){
                select.innerHTML = select.innerHTML + '<option value="'+data[i][0]+'">'+data[i][1]+'</option>';
            }
        }
    })
    $.ajax({
        url: "/admin/ship",
        type: "delete",
        data: {type: '2'},
        success: function(arg){
            var select = document.getElementById('ship_type');
            var data = jQuery.parseJSON(arg);
            select.innerHTML = '<option value="">请选择</option>';
            for (var i=0, l=data.length; i<l; i++){
                select.innerHTML = select.innerHTML + '<option value="'+data[i][0]+'">'+data[i][1]+'</option>';
            }
        }
    })
}

// ship搜索筛选
function ShipSearch(){
    $.ajax({
        url: "/admin/search",
        type: "put",
        data: {spot: document.getElementById('ship_spot').value,
            t: document.getElementById('ship_type').value,
            status: document.getElementById('ship_status').value,
            type: '2'},
        success: function(arg){
            ShowShipSearch(jQuery.parseJSON(arg));
        }
    })
}

// ship结果展示
function ShowShipSearch(data){
    var table = document.getElementById('main_search_table');
    table.innerHTML = '';
    var th = table.insertRow(0);
    th.innerHTML = '<th>船只编号</th><th>船只主题色</th><th>船只规模</th><th>船只型号</th><th>钱/分</th><th>状态</th><th>引进时间</th>';
    for (var i=0, l=data.length; i<l; i++){
        var tr = table.insertRow(i+1);
        tr.innerHTML = '<td>'+data[i][1]+'</td><td>'+data[i][2]+'</td><td>'+data[i][3]+'</td><td>'+data[i][4]+'</td><td>'+data[i][5]+'</td><td>'+data[i][6]+'</td><td>'+data[i][7]+'</td>';
    }
}

// member筛选，用户select点击
function SearchMemberSearchSelected(value){
    document.getElementById('member_phone').value = value;
    MemberSearch();
}

// member 搜索初始化
function InitMemberSearch(){
    document.getElementById('activity_search_table').style.display = 'none';
    document.getElementById('ship_search_table').style.display = 'none';
    document.getElementById('member_search_table').style.display = '';
    document.getElementById('ad_search_table').style.display = 'none';
    document.getElementById('gb_search_table').style.display = 'none';
    $.ajax({
        url: "/admin/search",
        type: "post",
        data: {type: '3'},
        success: function(arg){
            ShowMemberSearch(jQuery.parseJSON(arg));
        }
    })
}

// member搜索筛选
function MemberSearch(){
    $.ajax({
        url: "/admin/search",
        type: "put",
        data: {created: document.getElementById('member_created').value,
            endtime: document.getElementById('member_endtime').value,
            reputation: document.getElementById('member_reputation').value,
            phone: document.getElementById('member_phone').value,
            type: '3'},
        success: function(arg){
            ShowMemberSearch(jQuery.parseJSON(arg));
        }
    })
}

// member 搜索结果展示
function ShowMemberSearch(data){
    var table = document.getElementById('main_search_table');
    table.innerHTML = '';
    var th = table.insertRow(0);
    th.innerHTML = '<th>会员编号</th><th>会员昵称</th><th>会员电话</th><th>信誉</th><th>注册时间</th><th>游玩次数</th><th>折扣</th><th>性别</th>';
    for (var i=0, l=data.length; i<l; i++){
        var tr = table.insertRow(i+1);
        tr.innerHTML = '<td>'+data[i][0]+'</td><td>'+data[i][1]+'</td><td>'+data[i][2]+'</td><td>'+data[i][3]+'</td><td>'+data[i][4]+'</td><td>'+data[i][5]+'</td><td>'+data[i][6]+'</td><td>'+data[i][6]+'</td>';
    }
}

// 筛选ad名称的select option动态添加，key是显示的值，value是实际的指
function AdSearchSelectOption(k){
    $.ajax({
        url: "/admin/ad/broke",
        type: "put",
        data: {key: k},
        success: function(arg){
            var select = document.getElementById('select_ad_name');
            var data = jQuery.parseJSON(arg);
            var l = data.length;
            select.options.length = 0;
            select.add(new Option('请选择', ''));
            for (var i=0; i<l; i++){
                select.add(new Option(data[i][0], data[i][0]));
            }
        }
    })
}

// 筛选ad名称的select点击事件
function AdSearchSelect(value){
    document.getElementById('ad_name').value = value;
    AdSearch();
}

// ad 搜索初始化
function InitAdSearch(){
    document.getElementById('activity_search_table').style.display = 'none';
    document.getElementById('ship_search_table').style.display = 'none';
    document.getElementById('member_search_table').style.display = 'none';
    document.getElementById('ad_search_table').style.display = '';
    document.getElementById('gb_search_table').style.display = 'none';
    $.ajax({
        url: "/admin/search",
        type: "post",
        data: {type: '4'},
        success: function(arg){
            ShowAdSearch(jQuery.parseJSON(arg));
        }
    })
}

// ad搜索筛选
function AdSearch(){
    $.ajax({
        url: "/admin/search",
        type: "put",
        data: {created: document.getElementById('ad_created').value,
            endtime: document.getElementById('ad_endtime').value,
            t: document.getElementById('ad_type').value,
            name: document.getElementById('ad_name').value,
            type: '4'},
        success: function(arg){
            ShowAdSearch(jQuery.parseJSON(arg));
        }
    })
}

// ad搜索结果展示
function ShowAdSearch(data){
    var table = document.getElementById('main_search_table');
    table.innerHTML = '';
    var th = table.insertRow(0);
    th.innerHTML = '<th>编号</th><th>广告商名称</th><th>创建时间</th><th>结束时间</th><th>花费</th><th>状态</th><th>广告内容</th><th>审核不通过原因</th>';
    for (var i=0, l=data.length; i<l; i++){
        var tr = table.insertRow(i+1);
        tr.innerHTML = '<td>'+data[i][0]+'</td><td>'+data[i][1]+'</td><td>'+data[i][2]+'</td><td>'+data[i][3]+'</td><td>'+data[i][4]+'</td><td>'+data[i][5]+'</td><td>'+data[i][6]+'</td><td>'+data[i][7]+'</td>';
    }
}

// gb筛选，用户select点击
function GbSearchSelected(value){
    document.getElementById('gb_phone').value = value;
    GbSearch();
}

// gb 搜索初始化
function InitGbSearch(){
    document.getElementById('activity_search_table').style.display = 'none';
    document.getElementById('ship_search_table').style.display = 'none';
    document.getElementById('member_search_table').style.display = 'none';
    document.getElementById('ad_search_table').style.display = 'none';
    document.getElementById('gb_search_table').style.display = '';
    $.ajax({
        url: "/admin/search",
        type: "post",
        data: {type: '5'},
        success: function(arg){
            ShowGbSearch(jQuery.parseJSON(arg));
        }
    })
}

// gb搜索筛选
function GbSearch(){
    $.ajax({
        url: "/admin/search",
        type: "put",
        data: {created: document.getElementById('gb_created').value,
            endtime: document.getElementById('gb_endtime').value,
            t: document.getElementById('gb_type').value,
            phone: document.getElementById('gb_phone').value,
            type: '5'},
        success: function(arg){
            ShowGbSearch(jQuery.parseJSON(arg));
        }
    })
}

// gb搜索结果展示
function ShowGbSearch(data){
    var table = document.getElementById('main_search_table');
    table.innerHTML = '';
    var th = table.insertRow(0);
    th.innerHTML = '<th>编号</th><th>会员编号</th><th>人数</th><th>团建名称</th><th>要求</th><th>开始时间</th><th>结束时间</th><th>状态</th><th>花费</th><th>审核不通过原因</th>';
    for (var i=0, l=data.length; i<l; i++){
        var tr = table.insertRow(i+1);
        tr.innerHTML = '<td>'+data[i][0]+'</td><td>'+data[i][1]+'</td><td>'+data[i][2]+'</td><td>'+data[i][3]+'</td><td>'+data[i][4]+'</td><td>'+data[i][6]+'</td><td>'+data[i][5]+'</td><td>'+data[i][7]+'</td><td>'+data[i][8]+'</td><td>'+data[i][9]+'</td>';
    }
}

// 站内模糊搜索
function FuzzySearch(){
    if(document.getElementById('key_word').value == ''){
        alert('搜索框内容不能为空');
        return
    }
    var type = document.getElementById('search_select').value;
    $.ajax({
        url: "/admin/search",
        type: "delete",
        data: {key: document.getElementById('key_word').value,
            type: type},
        success: function(arg){
            if(type=='activity'){
                ShowActivitySearch(jQuery.parseJSON(arg));
            }else if(type=='ship'){
                ShowShipSearch(jQuery.parseJSON(arg));
            }else if(type=='member'){
                ShowMemberSearch(jQuery.parseJSON(arg));
            }else if(type=='ad'){
                ShowAdSearch(jQuery.parseJSON(arg));
            }else if(type=='gb'){
                ShowGbSearch(jQuery.parseJSON(arg));
            }
        }
    })
}