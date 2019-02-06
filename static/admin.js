// activity可选择的状态
var ACTIVITY_STATUS = ['正在游玩', '已付款', '预约', '销毁']
// member可选择的状态
var MEMBER_REPUTATION = ['良', '差']
// ship可选择状态
var SHIP_STATUS = ['正在使用', '空闲', '维修']
var SHIP_TYPE = ['游船', '步行球']
// ad、GB可选状态
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
        td.innerHTML = '<input class="form-control" id="'+td_id+'_input" type="text" onblur="GbPutData(this.value, ' + td_id + ', '+id+', this.id, \''+key+'\')" value="' + value + '" >'
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
        url: "/admin/ad",
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
function Data2Excel(uri){
    $.ajax({
        url: "/admin/"+uri,
        type: "PUT",
        data: {},
        success: function(arg){
            document.getElementById('download_a').click();
        }
    })
}