// activity可选择的状态
var ACTIVITY_STATUS = ['正在游玩', '已付款', '预约', '销毁']
// member可选择的状态
var MEMBER_REPUTATION = ['良', '差']
// ship可选择状态
var SHIP_STATUS = ['正在使用', '空闲', '维修']
var SHIP_TYPE = ['游船', '步行球']
// ad可选状态
var AD_TYPE = ['待审核', '过期', '活动', '审核不通过']

// 超级管理员登录模拟提交
function FormKeySubmit(){
    document.getElementById("f_key").submit()
}

// activity中表格还原
function ActivityPutData(value, td_id, id, input_id, key){
    td_id.innerHTML = value;
    $.ajax({
        url: "/admin/activity",
        type: "POST",
        data: {key: key, id: id, value: value},
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

// member表格还原
function MemberPutData(value, td_id, id, input_id, key){
    td_id.innerHTML = value;
    $.ajax({
        url: "/admin/member",
        type: "POST",
        data: {key: key, id: id, value: value},
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

// ship表格还原
function ShipPutData(value, td_id, id, input_id, key){
    td_id.innerHTML = value;
    $.ajax({
        url: "/admin/ship",
        type: "POST",
        data: {key: key, id: id, value: value},
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

// ad表格还原
function AdPutData(value, td_id, id, input_id, key){
    td_id.innerHTML = value;
    $.ajax({
        url: "/admin/ad",
        type: "POST",
        data: {key: key, id: id, value: value},
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