
$("#ads_yes").click(function(){
    var options=$("#select1 option:selected");
    //添加ads
    if(options.text()=="期刊"){
        var html_ = ["                                    <button type=\"button\" class=\"btn btn-success btn-circle\">年</button>",
        "                                    <input style=\"width: 100px\" type=\"number\" name=\"Year\" class=\"form-control\">&nbsp;",
        "                                    <button type=\"button\" class=\"btn btn-danger btn-circle\">卷</button>",
        "                                    <input style=\"width: 100px\" type=\"number\" name=\"Volume\" class=\"form-control\">&nbsp;",
        "                                    <button type=\"button\" class=\"btn btn-warning btn-circle\">期</button>",
        "                                    <input style=\"width: 100px\" type=\"number\" name=\"Phase\" class=\"form-control\">&nbsp;&nbsp;&nbsp;"].join("");
        $("#ads").html(html_);
    }
    else{//论文
        var html_ = ["                                    <button type=\"button\" class=\"btn btn-success btn-circle\">作者</button>",
        "                                    <input style=\"width: 150px\" type=\"text\" name=\"Auther\" class=\"form-control\">&nbsp;",
        "                                    <button type=\"button\" class=\"btn btn-danger\">开始页码</button>",
        "                                    <input style=\"width: 100px\" type=\"number\" name=\"Pages_Start\" class=\"form-control\">&nbsp;",
        "                                    <button type=\"button\" class=\"btn btn-warning\">结束页码</button>",
        "                                    <input style=\"width: 100px\" type=\"number\" name=\"Pages_End\" class=\"form-control\">&nbsp;"].join("");
        $("#ads").html(html_);
    }
    $("#ads_no").attr("checked", false);
});

$("#ads_no").click(function(){
    //清空ads
    $("#ads").html("");
    $("#ads_yes").attr("checked", false);
});

function select_change(){
    $("#ads_no").click();
}