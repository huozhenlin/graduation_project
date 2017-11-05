/**
 * Created by hzl on 2017/8/21.
 */
var data = ["景点", "酒店", "特色美食"];
var objArr = [];
hostname="http://"+location.host;

for (var i = 0; i < data.length; i++) {
    var obj = new Object();
    obj.id = i;
    obj.value = data[i];
    objArr.push(obj);
}
$(function () {
    //加载多选框的数据
    var ul = $("#ul");
    for (var i = 0; i < objArr.length; i++) {
        ul.append("<li><div class='checkbox'></div><label><input type='checkbox' value=" + objArr[i].id + " onclick='Choose(this)'/>" + objArr[i].value + "</label></li>");
    }
    for (var i = 0; i <= 1; i++) {
        showTask1(i)
    }
});
//显示多选框
function show(t) {
    //设置多选框显示的位置，在选择框的中间
    var left = t.offsetLeft + t.clientWidth / 2 - $("#panel")[0].clientWidth / 2
    var top = t.offsetTop + t.clientHeight + document.body.scrollTop;
    $("#panel").css("display", "block");
    $("#panel").css("margin-left", left);
    $("#panel").css("margin-top", top + 5);
}
//隐藏多选框
function hide() {
    $("#panel").css("display", "none");
}
//全选操作
function CheckAll(t) {
    var name = "";
    var ids = "";
    var popoverContent = $($(t).parent().parent().parent().children()[2]);
    popoverContent.find("input[type=checkbox]").each(function (i, th) {
        th.checked = t.checked;
        if (t.checked) {
            name += $(th).parent().text() + ",";
            ids += $(th).val() + ",";
        }
    });
    name = name.substr(0, name.length - 1);
    ids = ids.substr(0, ids.length - 1);
    $("#txt").val(name);
    $("#ids").val(ids);
}

//勾选某一个操作
function Choose(t) {
    var oldName = $("#txt").val();
    var name = oldName == "" ? "," + $("#txt").val() : "," + $("#txt").val() + ",";
    var ids = oldName == "" ? "," + $("#ids").val() : "," + $("#ids").val() + ",";
    var newName = $(t).parent().text();
    var newid = $(t).val();

    if (t.checked) {//选中的操作
        $("#txt").val(name += newName + ",");
        $("#ids").val(ids += newid + ",");
    } else {//去掉选中的操作
        var index = name.indexOf("," + newName + ",");
        var len = newName.length;
        name = name.substring(0, index) + name.substring(index + len + 1, name.length);

        var index = ids.indexOf("," + newid + ",");
        var len = newid.length;
        ids = ids.substring(0, index) + ids.substring(index + len + 1, ids.length);
    }
    name = name.substr(1, name.length - 2);
    ids = ids.substr(1, ids.length - 2);
    $("#txt").val(name);
    $("#ids").val(ids);
}

//异步处理，添加任务
function addTask1() {
    var ajaxCallUrl = hostname + "/ycx/addjob";
    $.ajax({
        cache: true,
        type: "POST",
        url: ajaxCallUrl,
        timeout: 3000,
        data: $('#myForm').serialize(),// 你的formid
        async: false,
        error: function (request) {
            alert('添加成功');
            showTask1(0);
            showTask1(1);
        },
        success: function (data) {
            alert('添加成功');
            showTask1(0);
            showTask1(1);
        }
    });

}
//启动任务
function start(id) {
    alert('定时任务启动成功');
    var url = hostname + '/ycx/startings?id=' + id;
    $.getJSON(url, function (res) {
        // var result = res;
        // if (result['startmess'] == 'ok') {
        //     alert('定时爬虫启动成功')
        // } else {
        //     alert('定时爬虫启动失败')
        // }
    })
}

//异步处理，删除任务
function deleteTask(id) {
    // 先删除队列中的任务
    var url = hostname + '/ycx/pushjob?id=' + id;
    $.getJSON(url, function (res) {

    });
    // 删除数据库中的任务
    var url = hostname + '/ycx/deljob?id=' + id;
    $.getJSON(url, function (res) {
        var result = res;
        if (result['delmes'] == 'ok') {
            alert('成功');
            showTask1(0);
            showTask1(1);
        } else {
            alert('失败')
        }
    })

}

//异步处理,展示任务
function showTask1(num) {

    var url = hostname + '/ycx/showjob?status=' + num+'&type=1';
    $.ajax({
        type: "get",
        url: url,
        dataType: 'json',
        success: function (data) {

            //遍历json,生成不同的div放到盒子中
            if (num == 0) {
                //清空盒子中的内容
                $("#spliding").html('');
                $.each(data, function (index, n) {
                    // 预处理
                    var type;
                    var types;
                    if (n.type == 0) {
                        type = "即时爬虫";
                    } else if (n.type == 1) {
                        type = "定时爬虫"
                    } else {
                        type = "数据分析"
                    }
                    var datas = ["景点", "酒店", "特色美食"];
                    var str = n.spider_task;
                    var new_strs=new Array();
                    var strs = str.split(","); //字符分割
                    for (s = 0; s < strs.length; s++) {
                        // alert(datas[strs[s]]);
                        new_strs.push(datas[strs[s]])
                    }
                    var types=new_strs.join(",");
                    $("#spliding").append(
                        // "<li><a href='" + n.url + "'>" + n.title + "</a></li>"
                        "<div class=\"col-md-3 col-sm-6 col-xs-12\" style=\"background-color: #f0efee\">" +
                        "<div class=\"box-header\" style=\"cursor: move; height: 50px\">" +
                        "<h4 class=\"box-title\"><i class=\"fa fa-tasks\"></i>" + n.name + "</h4>" +
                        "<div class=\"pull-right box-tools\" style=\"margin-top: -30px\">" +
                        "<div class=\"btn-group\" data-toggle=\"btn-toggle\">" +
                        "<button type=\"button\" class=\"btn btn-default \" onclick='start(" + n.id + ")'>" +
                        "<i class=\"fa fa-play text-green\" style=\"color: green\"></i>" +
                        "</button>" +
                        // "<button type=\"button\" class=\"btn btn-default\" onclick='stop(" + n.id + ")'>" +
                        // "<i class=\"fa fa-square text-red\" style=\"color: red\"></i>" +
                        // "</button>" +
                        "</div>" +
                        "<button type=\"button\" class=\"btn btn-default\" onclick='deleteTask(" + n.id + ")'><i class=\"fa fa-times\"></i>" +
                        "</button>" +
                        "</div>" +
                        "</div>" +
                        "<div class=\"box-body\">" +
                        "<div class=\"row\">" +
                        "<div class=\"col-md-12\">" +
                        "<p><strong>爬虫id：</strong>" + n.id +
                        "</p>" +
                        "</div>" +
                        "<div class=\"col-md-12\">" +
                        "<p><strong>爬虫起止时间：</strong>" + n.time + "&nbsp;&nbsp; &nbsp;&nbsp;" +
                        "</p>" +
                        "</div>" +
                        "<div class=\"col-md-12\">" +
                        "<p><strong>爬虫种类：</strong>" + type +
                        "</p>" +
                        "</div>" +
                        "<div class=\"col-md-12\">" +
                        "<p><strong>爬虫任务：</strong>" + types +
                        "</p>" +
                        "</div>" +
                        "</div>" +
                        "</div>" +
                        "</div>"
                    );
                });
            } else {
                $('#history_spliding').html('');
                $.each(data, function (index, n) {
                    // 预处理
                    var type;
                    var types;
                    if (n.type == 0) {
                        type = "即时爬虫";
                    } else if (n.type == 1) {
                        type = "定时爬虫"
                    } else {
                        type = "数据分析"
                    }
                    var datas = ["演唱会类", "展会类", "时政类", "体育赛事类", "异常天气类"];
                    var str = n.spider_task;
                    var new_strs=new Array();
                    var strs = str.split(","); //字符分割
                    for (s = 0; s < strs.length; s++) {
                        // alert(datas[strs[s]]);
                        new_strs.push(datas[strs[s]])
                    }
                    var types=new_strs.join(",");

                    $("#history_spliding").append(
                        // "<li><a href='" + n.url + "'>" + n.title + "</a></li>"
                        "<div class=\"col-md-3 col-sm-6 col-xs-12\" style=\"background-color: #f0efee\">" +
                        "<div class=\"box-header\" style=\"cursor: move; height: 50px\">" +
                        "<h4 class=\"box-title\"><i class=\"fa fa-tasks\"></i>" + n.name + "</h4>" +
                        "<div class=\"pull-right box-tools\" style=\"margin-top: -30px\">" +
                        "<div class=\"btn-group\" data-toggle=\"btn-toggle\">" +
                        "</button>" +
                        "</div>" +
                        "<button type=\"button\" class=\"btn btn-default\" onclick='deleteTask(" + n.id + ")'><i class=\"fa fa-times\"></i>" +
                        "</button>" +
                        "</div>" +
                        "</div>" +
                        "<div class=\"box-body\">" +
                        "<div class=\"row\">" +
                        "<div class=\"col-md-12\">" +
                        "<p><strong>爬虫id：</strong>" + n.id +
                        "</p>" +
                        "</div>" +
                        "<div class=\"col-md-12\">" +
                        "<p><strong>爬虫起止时间：</strong>" + n.time + "&nbsp;&nbsp; &nbsp;&nbsp;" +
                        "</p>" +
                        "</div>" +
                        "<div class=\"col-md-12\">" +
                        "<p><strong>爬虫种类：</strong>" + type +
                        "</p>" +
                        "</div>" +
                        "<div class=\"col-md-12\">" +
                        "<p><strong>爬虫任务：</strong>" + types +
                        "</p>" +
                        "</div>" +
                        "</div>" +
                        "</div>" +
                        "</div>"
                    );
                });
            }

        }
    });
}