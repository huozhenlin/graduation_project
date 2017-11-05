/**
 * Created by hzl on 2017/8/22.
 */

//获取端口+ip
hostname = "http://" + location.host;
history_num = 0;
now_num = 0;
$(function () {
    getNum();
    // getNums();
    getSplider();

    $('#queue_spliders').click(function () {
        getQueue();
    });

    $('#all_spliders').click(function () {
        getSplider();
    });

    $('#analyse_data').click(function () {
        getAnalyseSplider()

    })
});

//获取爬虫队列及配置，异步方式
function getQueue() {
    $('#show').html('');
    var url = hostname + "/ycx/queue";
    //异步方式请求json
    $.getJSON(url, function (res) {
        var result = res['splider'];
        if (result.length == 0) {

            $('#show').append("<h1 style='text-align: center'>暂无展示数据</h1>")
        } else {
            for (i = 0; i < result.length; i++) {
                var id = result[i];
                innerQueueHtml(id)
            }
        }
    })
}

//获取个数
function getNum() {
    var url = hostname + "/ycx/queue";
    //异步方式请求json
    $.getJSON(url, function (res) {
        var result = res['splider'];
        //设置数目
        $('#splider_num').html('');
        $('#splider_num').append(
            "<h4><strong>爬虫队列</strong></h4>" +
            "<div style=\"margin-top: 10px\"></div>" +
            "<h5><span>爬虫队列中，定时爬虫</span>" + result.length + "<span>个</span></h5>"
        )
    })
};

//获取爬虫数及配置，异步方式
function getSplider() {

    // 就绪爬虫url
    var url1 = hostname + '/ycx/showjob?status=0';
    //历史爬虫url
    var url2 = hostname + '/ycx/showjob?status=1';
    url_list = [url1, url2];
    $('#show').html('');
    // 正在进行的爬虫
    $.getJSON(url1, function (res) {
        var result = res;
        var num = 0;
        for (var ee in result) {
            num++;
        }
        // alert(result.length)
        now_num = num;
        $('#show').append(
            "<div class=\"col-xs-12\" style=\"padding: 15px 0px\">" +
            "<span class=\"label label-primary\">就绪/正在进行的爬虫：</span>" +
            "</div>" +
            "<div id=\"spliding\"></div>" +
            "<div class=\"col-xs-12\" style=\"padding: 15px 0px\">" +
            "<span class=\"label label-primary\">历史爬虫：</span>" +
            "</div>" +
            "<div id=\"history_spliding\"></div>"
        );
        $.each(res, function (index, n) {
            // 预处理
            var type;
            var types;
            if (n.type == 0) {
                type = "即时爬虫";
            } else if (n.type == 1) {
                type = "定时爬虫"
            }else if (n.type == 4) {
                type = "频率爬虫"
            } else if (n.type == 2) {
                type = "即时数据分析"
            }else {
                type = "定时数据分析"
            }
            var datas = ["景点", "酒店", "特色美食"];
            var str = n.spider_task;
            // alert(str)
            var new_strs = new Array();
            var strs = str.split(","); //字符分割
            for (s = 0; s < strs.length; s++) {
                // alert(datas[strs[s]]);
                new_strs.push(datas[strs[s]])
            }
            var types = new_strs.join(",");
            $("#spliding").append(
                // "<li><a href='" + n.url + "'>" + n.title + "</a></li>"
                "<div class=\"col-md-3 col-sm-6 col-xs-12\" style=\"background-color: #f0efee\">" +
                "<div class=\"box-header\" style=\"cursor: move; height: 50px\">" +
                "<h4 class=\"box-title\"><i class=\"fa fa-tasks\"></i>" + n.name + "</h4>" +
                // "<div class=\"pull-right box-tools\" style=\"margin-top: -30px\">" +
                // "<div class=\"btn-group\" data-toggle=\"btn-toggle\">" +
                // "<button type=\"button\" class=\"btn btn-default \" onclick='start(" + n.id + ")'>" +
                // "<i class=\"fa fa-play text-green\" style=\"color: green\"></i>" +
                // "</button>" +
                // "<button type=\"button\" class=\"btn btn-default\" onclick='stop(" + n.id + ")'>" +
                // "<i class=\"fa fa-square text-red\" style=\"color: red\"></i>" +
                // "</button>" +
                // "</div>" +
                // "<button type=\"button\" class=\"btn btn-default\" onclick='deleteTask(" + n.id + ")'><i class=\"fa fa-times\"></i>" +
                // "</button>" +
                // "</div>" +
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

    });

    // 历史爬虫
    $.getJSON(url2, function (res) {
        var result = res;
        var num = 0;
        for (var ee in result) {
            num++;
        }
        if (num ==1){
            history_num = num-1;
        }else {
            history_num=num
        }

        $('#spliders').html('');
        $('#spliders').append(
            "<h4><strong>爬虫数量</strong></h4>" +
            "<div style=\"margin-top: 10px\"></div>" +
            "<h5><span>就绪/正在工作</span>" + now_num + "<span>个，历史" + history_num + "个</span></h5>"
        );
        $.each(res, function (index, n) {
            // 预处理
            var type;
            var types;
            if (n.type == 0) {
                type = "即时爬虫";
            } else if (n.type == 1) {
                type = "定时爬虫"
            } else if (n.type == 4) {
                type = "频率爬虫"
            }else if (n.type == 2) {
                type = "即时数据分析"}
            else {
                type = "定时数据分析"
            }
            var datas = ["景点", "酒店", "特色美食"];
            var str = n.spider_task;
            var new_strs = new Array();
            var strs = str.split(","); //字符分割
            for (s = 0; s < strs.length; s++) {
                // alert(datas[strs[s]]);
                new_strs.push(datas[strs[s]])
            }
            var types = new_strs.join(",");
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
    });
}

//渲染队列模板
function innerQueueHtml(id) {
    var url = hostname + "/ycx/querybyid?id=" + id;
    // alert(url);
    $.ajax({
        type: "get",
        url: url,
        dataType: 'json',
        success: function (data) {
            n = data;
            // 遍历json,生成不同的div放到盒子中
            // 预处理
            var type;
            var types;
            if (n.type == 0) {
                type = "即时爬虫";
            } else if (n.type == 1) {
                type = "定时爬虫"}
            else if (n.type == 4) {
                type = "频率爬虫"
            }else if(n.type ==2) {
                type = "即时数据分析"
            } else if(n.type ==3) {
                type = "定时数据分析"
            }
            var datas = [];
            var str = n.spider_task;
            var new_strs = new Array();
            var strs = str.split(","); //字符分割
            for (s = 0; s < strs.length; s++) {
                // alert(datas[strs[s]]);
                new_strs.push(datas[strs[s]])
            }
            var types = new_strs.join(",");

            $("#show").append(
                // "<li><a href='" + n.url + "'>" + n.title + "</a></li>"
                "<div class=\"col-md-4 col-sm-6 col-xs-12\" style=\"background-color: #f0efee\">" +
                "<div class=\"box-header\" style=\"cursor: move; height: 50px\">" +
                "<h4 class=\"box-title\"><i class=\"fa fa-tasks\"></i>" + n.name + "</h4>" +
                "<div class=\"pull-right box-tools\" style=\"margin-top: -30px\">" +
                "<div class=\"btn-group\" data-toggle=\"btn-toggle\">" +
                "</div>" +
                "<button type=\"button\" class=\"btn btn-default\" onclick='deleteTask1(" + n.id + ")'><i class=\"fa fa-times\"></i>" +
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
        }
    });
}

//异步处理，删除任务
function deleteTask(id) {
    var url = hostname + '/deljob?id=' + id;
    $.getJSON(url, function (res) {
        var result = res;
        if (result['delmes'] == 'ok') {
            alert('成功');
            getSplider();
        } else {
            alert('失败')
        }
    })
}

//异步处理，删除任务
function deleteTask1(id) {
    // 先删除队列中的任务
    var url = hostname + '/ycx/pushjob?id=' + id;
    $.getJSON(url, function (res) {
        if (result['delmes'] == 'ok') {
            alert('成功');
             getAnalyseSplider();
            getNums()
        } else {
            alert('失败')
        }
    });

}

//渲染数据分析模板
function getAnalyseSplider() {

    // 就绪爬虫url
    var url1 = hostname + '/json2all?status=0';
    //历史爬虫url
    var url2 = hostname + '/json2all?status=1';
    url_list = [url1, url2];
    $('#show').html('');
    // 正在进行的爬虫
    $.getJSON(url1, function (res) {
        var result = res['objects'];
        // var num = 0;
        // for (var ee in result) {
        //     num++;
        // }
        // now_nums = num;
        $('#show').append(
            "<div class=\"col-xs-12\" style=\"padding: 15px 0px\">" +
            "<span class=\"label label-primary\">就绪/正在进行的分析任务：</span>" +
            "</div>" +
            "<div id=\"analysing\"></div>" +
            "<div class=\"col-xs-12\" style=\"padding: 15px 0px\">" +
            "<span class=\"label label-primary\">历史分析任务：</span>" +
            "</div>" +
            "<div id=\"history_analysing\"></div>"
        );
        $.each(res['objects'], function (index, n) {
            // 预处理
            var type;
            var types;
            if (n.type == 0) {
                type = "即时爬虫";
            } else if (n.type == 1) {
                type = "定时爬虫"
            } else if (n.type == 2) {
                type = "即时数据分析"
            }else {
                type ='定时数据分析'
            }
            var datas = ["景点", "酒店", "特色美食"];
            var str = n.spider_task;
            var new_strs = new Array();
            var strs = str.split(","); //字符分割
            for (s = 0; s < strs.length; s++) {
                // alert(datas[strs[s]]);
                new_strs.push(datas[strs[s]])
            }
            var types = new_strs.join(",");
            $("#analysing").append(
                // "<li><a href='" + n.url + "'>" + n.title + "</a></li>"
                "<div class=\"col-md-3 col-sm-6 col-xs-12\" style=\"background-color: #f0efee\">" +
                "<div class=\"box-header\" style=\"cursor: move; height: 50px\">" +
                "<h4 class=\"box-title\"><i class=\"fa fa-tasks\"></i>" + n.name + "</h4>" +
                "</div>" +
                "<div class=\"box-body\">" +
                "<div class=\"row\">" +
                "<div class=\"col-md-12\">" +
                "<p><strong>任务id：</strong>" + n.id +
                "</p>" +
                "</div>" +
                "<div class=\"col-md-12\">" +
                "<p><strong>任务创建时间：</strong>" + n.time + "&nbsp;&nbsp; &nbsp;&nbsp;" +
                "</p>" +
                "</div>" +
                "<div class=\"col-md-12\">" +
                "<p><strong>爬虫种类：</strong>" + type +
                "</p>" +
                "</div>" +
                "<div class=\"col-md-12\">" +
                "<p><strong>分析任务：</strong>" + types +
                "</p>" +
                "</div>" +
                "</div>" +
                "</div>" +
                "</div>"
            );
        });

    });

    // 历史爬虫
    $.getJSON(url2, function (res) {
        var result = res['objects'];
        var num = 0;
        for (var ee in result) {
            num++;
        }
        // history_nums = num;
        // $('#analyse_num').html('');
        // $('#analyse_num').append(
        //     "<h4><strong>数据分析</strong></h4>" +
        //     "<div style=\"margin-top: 10px\"></div>" +
        //     "<h5><span>就绪/正在工作</span>" + now_nums + "<span>个，历史" + history_nums + "个</span></h5>"
        // );
        $.each(res['objects'], function (index, n) {
            // 预处理
            var type;
            var types;
            if (n.type == 0) {
                type = "即时爬虫";
            } else if (n.type == 1) {
                type = "定时爬虫"
            } else if (n.type == 2) {
                type = "即时数据分析"
            }else {
                type ='定时数据分析'
            }
            var datas = ["景点", "酒店", "特色美食"];
            var str = n.types;
            var new_strs = new Array();
            var strs = str.split(","); //字符分割
            for (s = 0; s < strs.length; s++) {
                // alert(datas[strs[s]]);
                new_strs.push(datas[strs[s]])
            }
            var types = new_strs.join(",");
            $("#history_analysing").append(
                // "<li><a href='" + n.url + "'>" + n.title + "</a></li>"
                "<div class=\"col-md-3 col-sm-6 col-xs-12\" style=\"background-color: #f0efee\">" +
                "<div class=\"box-header\" style=\"cursor: move; height: 50px\">" +
                "<h4 class=\"box-title\"><i class=\"fa fa-tasks\"></i>" + n.name + "</h4>" +
                "<div class=\"pull-right box-tools\" style=\"margin-top: -30px\">" +
                "<div class=\"btn-group\" data-toggle=\"btn-toggle\">" +
                "</button>" +
                "</div>" +
                "<button type=\"button\" class=\"btn btn-default\" onclick='deleteTask2(" + n.id + ")'><i class=\"fa fa-times\"></i>" +
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
    });
}

function getNums() {
    var now_nums=0;
    var history_nums=0;

    // 就绪爬虫url
    var url1 = hostname + '/ycx/showjob?status=0';
    //历史爬虫url
    var url2 = hostname + '/ycx/showjob?status=1';
    $.getJSON(url1, function (res) {
        var result = res;
        var num = 0;
        for (var ee in result) {
            num++;
        }
        now_nums = num;
    });

    $.getJSON(url2, function (res) {
        var result = res;
        var num = 0;
        for (var ee in result) {
            num++;
        }
        history_nums = num;
        $('#analyse_num').html('');
        $('#analyse_num').append(
            "<h4><strong>数据分析</strong></h4>" +
            "<div style=\"margin-top: 10px\"></div>" +
            "<h5><span>就绪/正在工作</span>" + now_nums + "<span>个，历史" + history_nums + "个</span></h5>"
        );
    });

}
//异步处理，删除任务
function deleteTask2(id) {
    var url = hostname + '/deljson?delete=' + id;
    $.getJSON(url, function (res) {
        var result = res;
        if (result['delmes'] == 'ok') {
            alert('成功');
            getAnalyseSplider();
            getNum()
        } else {
            alert('失败')
        }
    })
}