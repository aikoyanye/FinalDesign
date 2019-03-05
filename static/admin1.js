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