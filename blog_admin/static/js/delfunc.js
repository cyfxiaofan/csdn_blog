//定义逻辑删除方法
function delfunc(obj) {
    //获取当前路由名称
    var url = window.location.pathname;
    console.log(url) ; //  /industry/showsecondindustry/1/   ,   /industry/
    //获取当前所点击对象的 id
    var i_id = $(obj).parent().parent().attr('id');
    console.log(i_id);
    var csrfToken = $('[name=csrfmiddlewaretoken]').val();
    //获取当前点击对象的  判断他的颜色 来决定 -->status
    if ($(obj).next().css('backgroundColor') === ('rgb(132, 199, 193)')){
        var status = 0
    }else{
        var status = 1
    }
    console.log(status);
    //获取到主路由 匹配到逻辑删除方法   /industry/delcatagory/
    var delpath = '/'+url.split('/')[1]+'/'+'delthis/';

    //定义showCanceMessage 方法 给出询问提示窗口
function showCancelMessage() {
    swal({
        title: "确定修改吗?",
        text: '您正在执行敏感操作',
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "确定!",
        cancelButtonText: "取消!",
        closeOnConfirm: false,
        closeOnCancel: false
    }, function (isConfirm) {
        //如果点击的是确定按钮！ 发送ajax   没有表单  不加csrf_token
        if (isConfirm) {
            $.ajax({
            async:true,  //同步
            type:'post',
            url:delpath,
            dataType:'json',  //返回的数据类型
            data:{csrfmiddlewaretoken:csrfToken,i_id:i_id,status:status},
            success:function (data) {
                if (data.msg==1){
                    swal("已修改!", data.successmsg, "success");
                }else{
                    if ($(obj).next().css('backgroundColor') === ('rgb(132, 199, 193)')){
                       $(obj).prop('checked',false)
                    }else{
                       $(obj).prop('checked',true)
                    }
                    swal("修改失败!", data.msg, "error");
                    }
                 },
                // error:function () {
                //     if ($(obj).next().css('backgroundColor') === ('rgb(132, 199, 193)')){
                //        $(obj).prop('checked',false)
                //     }else{
                //        $(obj).prop('checked',true)
                //     }
                //     swal("权限不足!", '您没有删除权限！', "error");
                //
                // }
             })
        } else {

                if ($(obj).next().css('backgroundColor') === ('rgb(132, 199, 193)')){
                   $(obj).prop('checked',false)
                }else{
                   $(obj).prop('checked',true)
                }
                swal("操作已取消！", "您取消了操作", "error");
        }
    });
}


showCancelMessage()

}


//定义评论状态方法
function commentfunc(obj) {
    //获取当前路由名称
    var url = window.location.pathname
    console.log(url)  //  /industry/showsecondindustry/1/   ,   /industry/
    //获取当前所点击对象的 id
    var i_id = $(obj).parent().parent().attr('id')
    console.log(i_id)
    //获取当前点击对象的  判断他的颜色 来决定 -->status
    if ($(obj).next().css('backgroundColor') === ('rgb(132, 199, 193)')){
        var status = 0
    }else{
        var status = 1
    }
    console.log(status)
    //获取到主路由 匹配到逻辑删除方法   /industry/delcatagory/
    var delpath = '/'+url.split('/')[1]+'/'+'commentthis/'

    //定义showCanceMessage 方法 给出询问提示窗口
function showCancelMessage() {
    swal({
        title: "确定修改吗?",
        text: "您正在改变这篇文章的的评论状态!",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "确定!",
        cancelButtonText: "取消!",
        closeOnConfirm: false,
        closeOnCancel: false
    }, function (isConfirm) {
        //如果点击的是确定按钮！ 发送ajax   没有表单  不加csrf_token
        if (isConfirm) {

            $.ajax({
            async:true,  //同步
            type:'get',
            url:delpath,
            dataType:'json',  //返回的数据类型
            data:{i_id:i_id,status:status},
            success:function (data) {
                if (data.msg==1){
                    swal("已修改!", "数据同步成功！.", "success");
                }else{
                    swal("修改失败!", "发生了未知的错误信息.", "error");
                }
            }
                 })
        } else {

                if ($(obj).next().css('backgroundColor') === ('rgb(132, 199, 193)')){
                   $(obj).prop('checked',false)
                }else{
                   $(obj).prop('checked',true)
                }
                swal("操作已取消！", "您取消了操作", "error");
        }
    });
}


showCancelMessage()

}


//定义是否置顶方法
function istop(obj) {
    //获取当前路由名称
    var url = window.location.pathname
    console.log(url)  //  /industry/showsecondindustry/1/   ,   /industry/
    //获取当前所点击对象的 id
    var i_id = $(obj).parent().parent().attr('id')
    console.log(i_id)
    //获取当前点击对象的  判断他的颜色 来决定 -->status
    if ($(obj).next().css('backgroundColor') === ('rgb(132, 199, 193)')){
        var status = 0
    }else{
        var status = 1
    }
    console.log(status)
    //获取到主路由 匹配到逻辑删除方法   /industry/delcatagory/
    var delpath = '/'+url.split('/')[1]+'/'+'istop/'

    //定义showCanceMessage 方法 给出询问提示窗口
function showCancelMessage() {
    swal({
        title: "确定修改吗?",
        text: "您正在改变这篇文章的的置顶状态!",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "确定!",
        cancelButtonText: "取消!",
        closeOnConfirm: false,
        closeOnCancel: false
    }, function (isConfirm) {
        //如果点击的是确定按钮！ 发送ajax   没有表单  不加csrf_token
        if (isConfirm) {

            $.ajax({
            async:true,  //同步
            type:'get',
            url:delpath,
            dataType:'json',  //返回的数据类型
            data:{i_id:i_id,status:status},
            success:function (data) {
                if (data.msg==1){
                    swal("已修改!", "数据同步成功！.", "success");
                }else{
                    swal("修改失败!", "发生了未知的错误信息.", "error");
                }
            }
                 })
        } else {

                if ($(obj).next().css('backgroundColor') === ('rgb(132, 199, 193)')){
                   $(obj).prop('checked',false)
                }else{
                   $(obj).prop('checked',true)
                }
                swal("操作已取消！", "您取消了操作", "error");
        }
    });
}
showCancelMessage()
}

//定义是否推荐方法
function istofirst(obj) {
    //获取当前路由名称
    var url = window.location.pathname
    console.log(url)  //  /industry/showsecondindustry/1/   ,   /industry/
    //获取当前所点击对象的 id
    var i_id = $(obj).parent().parent().attr('id')
    console.log(i_id)
    //获取当前点击对象的  判断他的颜色 来决定 -->status
    if ($(obj).next().css('backgroundColor') === ('rgb(132, 199, 193)')){
        var status = 0
    }else{
        var status = 1
    }
    console.log(status)
    //获取到主路由 匹配到逻辑删除方法   /industry/delcatagory/
    var delpath = '/'+url.split('/')[1]+'/'+'istofirst/'

    //定义showCanceMessage 方法 给出询问提示窗口
function showCancelMessage() {
    swal({
        title: "确定修改吗?",
        text: "您正在改变这篇文章的的推荐状态!",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "确定!",
        cancelButtonText: "取消!",
        closeOnConfirm: false,
        closeOnCancel: false
    }, function (isConfirm) {
        //如果点击的是确定按钮！ 发送ajax   没有表单  不加csrf_token
        if (isConfirm) {

            $.ajax({
            async:true,  //同步
            type:'get',
            url:delpath,
            dataType:'json',  //返回的数据类型
            data:{i_id:i_id,status:status},
            success:function (data) {
                if (data.msg==1){
                    swal("已修改!", "数据同步成功！.", "success");
                }else{
                    swal("修改失败!", "发生了未知的错误信息.", "error");
                }
            }
                 })
        } else {

                if ($(obj).next().css('backgroundColor') === ('rgb(132, 199, 193)')){
                   $(obj).prop('checked',false)
                }else{
                   $(obj).prop('checked',true)
                }
                swal("操作已取消！", "您取消了操作", "error");
        }
    });
}
showCancelMessage()
}