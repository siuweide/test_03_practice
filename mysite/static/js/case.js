function getCaseInfo() {
    console.log("获取用例信息");
    var url = window.location.href;
    var caseId = url.split("/")[5];
    console.log("caseId------->", caseId);

    $.post("/case/get_case_info/", {
        cid: caseId
    }, function (resp) {
        if (resp.code === 10200) {
            console.log("url----->", resp.data.url);

            // url
            document.querySelector("#req_url").value = resp.data.url;
            // method
            if (resp.data.method == 1) {
                document.querySelector("#get").setAttribute("checked", "")
            }else if (resp.data.method == 2) {
                document.querySelector("#post").setAttribute("checked", "")
            }
            // header
            var header_json = JSON.parse(resp.data.header);
            headersEditor.set(header_json);
            // 参数类型
            if (resp.data.parameter_type == 1) {
                document.querySelector("#form").setAttribute("checked", "")
            }else if (resp.data.parameter_type == 2) {
                document.querySelector("#json").setAttribute("checked", "")
            }
            // 参数内容
            var par_json = JSON.parse(resp.data.parameter_body);
            parameterEditor.set(par_json);
            // 返回结果
            document.querySelector("#result").value = resp.data.result;
            // 断言方法
            if (resp.data.assert_type == 1) {
                document.querySelector("#include").setAttribute("checked", "")
            }else if (resp.data.assert_type == 2) {
                document.querySelector("#equal").setAttribute("checked", "")
            }
            // 断言结果
            document.querySelector("#assert").value = resp.data.assert_text;
            // 名称
            document.querySelector("#case_name").value = resp.data.name;

            console.log("project_id", resp.data.project);
            console.log("module_id", resp.data.module);
            // 初始化菜单
            SelectInit(resp.data.project, resp.data.module);
        }
    })
}