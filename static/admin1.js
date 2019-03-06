// 删除景区
function DeleteSpot(id){
    $.ajax({
        url: "/admin/spot",
        type: "delete",
        data: {id: id},
        success: function(arg){
            window.location.reload();
        }
    })
}

// 修改景区信息模态框
function InitChangeSpot(id, name, address, phone, discount){
    var footer = document.getElementById('change_spot_footer');
    footer.innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>';
    footer.innerHTML = footer.innerHTML + '<button type="button" class="btn btn-primary" data-dismiss="modal" onclick="ChangeSpot('+id+')">提交</button>';
    document.getElementById('rename').value = name;
    document.getElementById('readdress').value = address;
    document.getElementById('rephone').value = phone;
    document.getElementById('rediscount').value = discount;
}

// 修改景区信息
function ChangeSpot(id){
    if(document.getElementById('rename').value=='' ||
        document.getElementById('readdress').value=='' ||
        document.getElementById('rephone').value=='' ||
        document.getElementById('rediscount').value==''){
        alert('输入框组不能为空');
        return
    }
    $.ajax({
        url: "/admin/spot",
        type: "put",
        data: {id: id, name: document.getElementById('rename').value,
            address: document.getElementById('readdress').value,
            phone: document.getElementById('rephone').value,
            discount: document.getElementById('rediscount').value},
        success: function(arg){
            window.location.reload();
        }
    })
}

// 添加景区
function AddSpot(){
    if(document.getElementById('name').value=='' ||
        document.getElementById('address').value=='' ||
        document.getElementById('phone').value=='' ||
        document.getElementById('discount').value==''){
        alert('输入框组不能为空');
        return
    }
    $.ajax({
        url: "/admin/spot",
        type: "post",
        data: {name: document.getElementById('name').value,
            address: document.getElementById('address').value,
            phone: document.getElementById('phone').value,
            discount: document.getElementById('discount').value},
        success: function(arg){
            window.location.reload();
        }
    })
}

// 添加船只类型
function AddShipType(){
    if(document.getElementById('type').value==''){
        alert('输入框不能为空');
        return
    }
    $.ajax({
        url: "/admin/ship/finish",
        type: "post",
        data: {type: document.getElementById('type').value},
        success: function(arg){
            window.location.reload();
        }
    })
}

// 删除船只类型
function DeleteShipType(id){
    $.ajax({
        url: "/admin/ship/finish",
        type: "delete",
        data: {id: id},
        success: function(arg){
            window.location.reload();
        }
    })
}

// 填充库存船只
function ShowStockShip(data){
    var table = document.getElementById('stock_table');
    table.innerHTML = '';
    var th = table.insertRow(0);
    th.innerHTML = '<th><span class="glyphicon glyphicon-plus" aria-hidden="true" data-toggle="modal" data-target="#add_ship"></span>船只编号</th><th>船只名称</th><th>船只主题色</th><th>船只规模</th><th>船只型号</th><th>钱/分</th><th>状态</th><th>引进时间</th><th>操作</th>';
    for (var i=0, l=data.length; i<l; i++){
        var tr = table.insertRow(i+1);
        tr.innerHTML = '<td>'+data[i][0]+'</td><td>'+data[i][1]+'</td><td>'+data[i][2]+'</td><td>'+data[i][3]+'</td><td>'+data[i][4]+'</td><td>'+data[i][5]+'</td><td>'+data[i][6]+'</td><td>'+data[i][7]+'</td><td><a href="#" data-toggle="modal" data-target="#save_ship" onclick="SaveShipModel('+data[i][0]+')">维护</a>/<a href="#" data-toggle="modal" data-target="#change_ship" onclick="InitChangeShipModel('+data[i][0]+', \''+data[i][1]+'\', \''+data[i][2]+'\', \''+data[i][3]+'\', \''+data[i][4]+'\', \''+data[i][5]+'\')">修改信息</a>/<a href="#" onclick="DeleteShip('+data[i][0]+')">删除</a></td>';
    }
}

// 库存界面景区select
function StockShipsSpot(){
    $.ajax({
        url: "/admin/ship",
        type: "delete",
        data: {type: '1'},
        success: function(arg){
            var select = document.getElementById('spot_select');
            var select1 = document.getElementById('spot');
            var data = jQuery.parseJSON(arg);
            for (var i=0, l=data.length; i<l; i++){
                select.innerHTML = select.innerHTML + '<option value="'+data[i][0]+'">'+data[i][1]+'</option>';
                select1.innerHTML = select1.innerHTML + '<option value="'+data[i][0]+'">'+data[i][1]+'</option>';
            }
        }
    })
}

// 船只租借界面景区select
function ActivityStockShipsSpot(){
    $.ajax({
        url: "/admin/ship",
        type: "delete",
        data: {type: '1'},
        success: function(arg){
            var select = document.getElementById('spot_select');
            var data = jQuery.parseJSON(arg);
            for (var i=0, l=data.length; i<l; i++){
                select.innerHTML = select.innerHTML + '<option value="'+data[i][0]+'">'+data[i][1]+'</option>';
            }
        }
    })
}

// activity界面船只类型select
function ActivityStockShipsShipType(){
    $.ajax({
        url: "/admin/ship",
        type: "delete",
        data: {type: '2'},
        success: function(arg){
            var select = document.getElementById('type_select');
            var data = jQuery.parseJSON(arg);
            for (var i=0, l=data.length; i<l; i++){
                select.innerHTML = select.innerHTML + '<option value="'+data[i][0]+'">'+data[i][1]+'</option>';
            }
        }
    })
}

// 库存界面船只类型select
function StockShipsShipType(){
    $.ajax({
        url: "/admin/ship",
        type: "delete",
        data: {type: '2'},
        success: function(arg){
            var select = document.getElementById('type_select');
            var select1 = document.getElementById('type');
            var data = jQuery.parseJSON(arg);
            for (var i=0, l=data.length; i<l; i++){
                select.innerHTML = select.innerHTML + '<option value="'+data[i][0]+'">'+data[i][1]+'</option>';
                select1.innerHTML = select1.innerHTML + '<option value="'+data[i][0]+'">'+data[i][1]+'</option>';
            }
        }
    })
}

// 添加船只
function AddReShip(){
    if(document.getElementById('shipname').value=='' ||
        document.getElementById('color').value=='' ||
        document.getElementById('size').value=='' ||
        document.getElementById('model').value=='' ||
        document.getElementById('cost').value==''){
        alert('输入框组不能为空');
        return
    }
    $.ajax({
        url: "/admin/ship",
        type: "post",
        data: {shipname: document.getElementById('shipname').value,
            color: document.getElementById('color').value,
            size: document.getElementById('size').value,
            model: document.getElementById('model').value,
            cost: document.getElementById('cost').value,
            typeId: document.getElementById('type').value,
            spotId: document.getElementById('spot').value},
        success: function(arg){
            StockSpotShipType();
        }
    })
}

// 库存页面景区和游船类型筛选
function StockSpotShipType(){
    $.ajax({
        url: "/admin/ship",
        type: "delete",
        data: {typeId: document.getElementById('type_select').value,
            spotId: document.getElementById('spot_select').value,
            status: document.getElementById('status_select').value,
            type: '3'},
        success: function(arg){
            ShowStockShip(jQuery.parseJSON(arg));
        }
    })
}

// 维护船只模态框
function SaveShipModel(id){
    var footer = document.getElementById('save_ship_footer');
    footer.innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>';
    footer.innerHTML = footer.innerHTML + '<button type="button" class="btn btn-primary" data-dismiss="modal" onclick="SaveShip('+id+')">提交</button>';
}

// 维护游船
function SaveShip(id){
    if(document.getElementById('reason').value==''){
        alert('输入框不能为空');
        return
    }
    $.ajax({
        url: "/admin/ship",
        type: "put",
        data: {id: id, type: '1', reason: document.getElementById('reason').value},
        success: function(arg){
            StockSpotShipType();
        }
    })
}

// 修改船只信息模态框初始化
function InitChangeShipModel(id, shipname, color, size, model, cost){
    document.getElementById('reshipname').value = shipname;
    document.getElementById('recolor').value = color;
    document.getElementById('resize').value = size;
    document.getElementById('remodel').value = model;
    document.getElementById('recost').value = cost;
    var footer = document.getElementById('change_ship_footer');
    footer.innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>';
    footer.innerHTML = footer.innerHTML + '<button type="button" class="btn btn-primary" data-dismiss="modal" onclick="ChangeShipModel('+id+')">提交</button>';
}

// 修改船只信息模
function ChangeShipModel(id){
    if(document.getElementById('reshipname').value=='' ||
        document.getElementById('recolor').value=='' ||
        document.getElementById('resize').value=='' ||
        document.getElementById('remodel').value=='' ||
        document.getElementById('recost').value==''){
        alert('输入框组不能为空');
        return
    }
    $.ajax({
        url: "/admin/ship",
        type: "put",
        data: {shipname: document.getElementById('reshipname').value,
            color: document.getElementById('recolor').value,
            size: document.getElementById('resize').value,
            model: document.getElementById('remodel').value,
            cost: document.getElementById('recost').value,
            type: '2', id: id},
        success: function(arg){
            StockSpotShipType();
        }
    })
}

// 船只维护完毕
function SavedShip(id){
    $.ajax({
        url: "/admin/ship/broking",
        type: "delete",
        data: {id: id},
        success: function(arg){
            window.location.reload();
        }
    })
}

// 删除船只
function DeleteShip(id){
    $.ajax({
        url: "/admin/ship",
        type: "delete",
        data: {id: id, type: '4'},
        success: function(arg){
            StockSpotShipType();
        }
    })
}

// 删除船只
function ReturnShip(id){
    $.ajax({
        url: "/admin/ship",
        type: "delete",
        data: {id: id, type: '4'},
        success: function(arg){
            window.location.reload();
        }
    })
}

// 船只审核入库
function ShipExaminePass(id){
    $.ajax({
        url: "/admin/ship/free",
        type: "put",
        data: {id: id},
        success: function(arg){
            window.location.reload();
        }
    })
}

// 游船租借管理页面筛选数据展示
function ShowLeaseShipData(data){
    var table = document.getElementById('lease_table');
    table.innerHTML = '';
    var th = table.insertRow(0);
    th.innerHTML = '<th>船只编号</th><th>船只名称</th><th>船只主题色</th><th>船只规模</th><th>船只型号</th><th>租金(钱/每分)</th><th>操作</th>';
    for (var i=0, l=data.length; i<l; i++){
        var tr = table.insertRow(i+1);
        tr.innerHTML = '<td>'+data[i][0]+'</td><td>'+data[i][1]+'</td><td>'+data[i][2]+'</td><td>'+data[i][3]+'</td><td>'+data[i][4]+'</td><td>'+data[i][5]+'</td><td><a href="#" onclick="InitAddActivityModel('+data[i][0]+')" data-toggle="modal" data-target="#add_activity">出租</a></td>';
    }
}

// 船只租借管理页面筛选
function LeaseSpotShipTypeSelect(){
    $.ajax({
        url: "/admin/activity",
        type: "put",
        data: {typeId: document.getElementById('type_select').value,
            spotId: document.getElementById('spot_select').value},
        success: function(arg){
            ShowLeaseShipData(jQuery.parseJSON(arg));
        }
    })
}

// 船只出租页面选择会员返回租金
function AddActivitySelect(value){
    document.getElementById('add_act_phone').value = value;
    $.ajax({
        url: "/admin/activity",
        type: "post",
        data: {type: "1", phone: value,
                shipId: document.getElementById('shipId').value},
        success: function(arg){
            var data = jQuery.parseJSON(arg);
            document.getElementById('cost').value = (data*60).toFixed(2);
            document.getElementById('show_cost').innerHTML = '根据景区和会员计算出租金为'+data+'元/每分，故押金为'+(data*60).toFixed(2)+'元';
        }
    })
}

// 船只出租页面模态框
function InitAddActivityModel(shipId){
    document.getElementById('shipId').value = shipId;
    var footer = document.getElementById('add_activity_footer');
    footer.innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>';
    footer.innerHTML = footer.innerHTML + '<button type="button" class="btn btn-primary" data-dismiss="modal" onclick="AddReActivity()">提交</button>';
}

// 船只出租
function AddReActivity(){
    $.ajax({
        url: "/admin/activity",
        type: "post",
        data: {shipId: document.getElementById('shipId').value,
            phone: document.getElementById('add_act_select').value,
                cost: document.getElementById('cost').value, type: '2'},
        success: function(arg){
            LeaseSpotShipTypeSelect();
        }
    })
}

// 押金结算模态框初始化
function InitDepositShipModel(id, created, shipId, phone, cost){
    var endtime = Date.parse(new Date());
    var cost_time = (endtime - Date.parse(new Date(created)))/(1000*60);
    $.ajax({
        url: "/admin/activity/order",
        type: "put",
        data: {type: "1", phone: phone,
                shipId: shipId, cost_time: cost_time},
        success: function(arg){
            var data = jQuery.parseJSON(arg);
            var final_cost;
            if(cost > data){
                document.getElementById('show_cost').innerHTML = '此次租借船只的租金为'+data+'元，从押金中扣除，剩余的'+(cost-data).toFixed(2)+'元退还给用户';
                final_cost = data;
            }else{
                document.getElementById('show_cost').innerHTML = '此次租借船只的租金为'+data+'元，从押金中扣除，还需缴纳'+(data-cost).toFixed(2)+'元租金';
                final_cost = data + (data - cost);
            }
            var footer = document.getElementById('deposit_activity_footer');
            footer.innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>';
            footer.innerHTML = footer.innerHTML + '<button type="button" class="btn btn-primary" data-dismiss="modal" onclick="SettlementDeposit('+id+', \''+final_cost.toFixed(2)+'\', '+shipId+', \''+phone+'\')">提交</button>';
        }
    })
}

// 押金结算单选框点击事件
function SettlementDepositRadio(t){
    if(t=='nobroke'){
        document.getElementById('show_broke').innerHTML = '不需要缴纳额外费用';
    }else{
        document.getElementById('show_broke').innerHTML = '需要交付额外1000元维修费，并且会员折扣会收到影响';
    }
}

// 押金结算
function SettlementDeposit(id, final_cost, shipId, phone){
    if($('input:radio[name="broke"]:checked').val() == 'nobroke'){
        $.ajax({
            url: "/admin/activity/order",
            type: "post",
            data: {shipId: shipId, type: '1', id: id, final_cost: final_cost},
            success: function(arg){
                window.location.reload();
            }
        })
    }else{
        $.ajax({
            url: "/admin/activity/order",
            type: "post",
            data: {shipId: shipId, type: '2', id: id, final_cost: final_cost, phone},
            success: function(arg){
                window.location.reload();
            }
        })
    }
}

// 删除结算游园记录
function DeleteReActivity(id){
    $.ajax({
        url: "/admin/activity/over",
        type: "delete",
        data: {id: id},
        success: function(arg){
            window.location.reload();
        }
    })
}

// 修改会员信息模态框
function ChangeMemberModel(id, name, phone, discount){
    document.getElementById('remember_name').value = name;
    document.getElementById('remember_phone').value = phone;
    document.getElementById('remember_discount').value = discount;
    var footer = document.getElementById('change_member_footer');
    footer.innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>';
    footer.innerHTML = footer.innerHTML + '<button type="button" class="btn btn-primary" data-dismiss="modal" onclick="ChangeReMember('+id+')">提交</button>';
}

// 修改会员信息
function ChangeReMember(id){
    if(document.getElementById('remember_name').value=='' ||
    document.getElementById('remember_phone').value=='' ||
    document.getElementById('remember_discount').value==''){
        alert('输入框组不能为空');
        return
    }
    $.ajax({
        url: "/admin/member",
        type: "put",
        data: {id: id, name: document.getElementById('remember_name').value,
            phone: document.getElementById('remember_phone').value,
            discount: document.getElementById('remember_discount').value,
            reputation: document.getElementById('remember_reputation').value},
        success: function(arg){
            window.location.reload();
        }
    })
}

// 展示活动报表数据
function ShowActivityFundsData(data){
    var table = document.getElementById('funds_activity');
    table.innerHTML = '';
    var th = table.insertRow(0);
    th.innerHTML = '<th><a class="glyphicon glyphicon-download-alt" onclick="Data2ExcelFund()"></a><a id="download_a" download="data.xls" href="../static/data.xls"></a>日期</th><th>收入</th>';
    for (var i=0, l=data[0].length; i<l; i++){
        var tr = table.insertRow(i+1);
        tr.innerHTML = '<td>'+data[0][i]+'</td><td>'+data[1][i]+'</td>';
    }
}

// 导出数据
function Data2ExcelFund(){
    $.ajax({
        url: "/admin/fund",
        type: "put",
        data: {start: document.getElementById('fund_start').value,
            end: document.getElementById('fund_end').value},
        success: function(arg){
            document.getElementById('download_a').click();
        }
    })
}

// 活动经费管理，图表用，天
function FundDayChart(){
    $.ajax({
        url: "/admin/fund",
        type: "post",
        data: {type: document.getElementById('fund_type').value,
            start: document.getElementById('fund_start').value,
            end: document.getElementById('fund_end').value},
        success: function(arg){
            var data = jQuery.parseJSON(arg);
            Echarts(data[0], data[1]);
            ShowActivityFundsData(data);
        }
    })
}

// 生成活动经费图表
function Echarts(x, y){
    var myChart = echarts.init(document.getElementById('chart'));
        var option = {
            title: {
                text: '活动经费'
            },
            tooltip: {},
            legend: {
                data:['收入']
            },
            xAxis: {
                data: x
            },
            yAxis: {},
            series: [{
                name: '收入',
                type: 'bar',
                data: y
            }]
        };
        myChart.setOption(option);
}