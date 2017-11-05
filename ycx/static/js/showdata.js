/**
 * Created by hzl on 2017/8/19.
 */


//初始化调用
$(function () {
    showLogin();
    // setInterval("showLogin()", "1000");
});

function showLogin() {
    var s = ['sing', 'sport', 'news', 'weather', 'eshow'];
    for (i = 0; i < s.length; i++) {
        check(s[i])
    }
}
hostname = "http://" + location.host;

// alert(hostname)

//删除提示框
function delInfo(obj) {
    if (confirm("确认要删除？")) {
        article_del(obj)
    }
}

/*删除*/
function article_del(obj) {
    //获取tr下第3个td的值，即是id
    var tr = $(obj).parents("tr");
    var td = tr.children('td').eq(2).html();
    var tablename = tr.attr('class');
    //发生删除请求

    var url = hostname + "/datadelete?table=" + tablename + "&id=" + td;
    $.ajax({
        type: "get",
        url: url,
        dataType: 'json',
        success: function (data) {
            if (data['delmes'] == 'ok')
                var s = ['sing', 'sport', 'news', 'weather', 'eshow'];
            for (i = 0; i < s.length; i++) {
                check(s[i])
            }
        }

    });
}

// 把刚刚采集的数据显示出来
function check(tablename) {
    var url = hostname + '/noanalyse?table=' + tablename;
    // alert(url);
    $.ajax({
        type: "get",
        url: url,
        dataType: 'json',
        success: function (data) {
            if (data['message'] == "none") {
                // 清除盒子里的内容
                $("#" + tablename).html('');
                $("#" + tablename).append("<span style='text-align: center'>暂无数据</span>")
            } else {
                // 清除盒子里的内容
                $("#" + tablename).html('');
                $("#" + tablename).append(
                    "<div class=\"table-responsive\"><table id='" + tablename + "1' border='1' class='table table-hover col-xs-12 ' ></table></div>"
                );
                $.each(data['objects'], function (row, value) {
                    if (row == 0) {
                        $('#' + tablename + "1").append("<tr></tr>");
                    }
                    $("#" + tablename + "1").append("<tr class=" + tablename + "></tr>");
                    $.each(value, function (col, value) {
                        if (row == 0) {
                            // 添加表头元素
                            $("#" + tablename + "1").find("tr").eq(row).append("<td>" + col + "</td>");
                        }
                        // 添加值
                        $("#" + tablename + "1").find("tr").eq(row + 1).append("<td class='info' ondblclick='delInfo(this)'>" + value + "</td>");
                    });
                })
            }

        }
    })

}


