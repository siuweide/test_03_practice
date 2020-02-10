


function SelectInit(defaultProjectId, defaultModuleId){
    console.log("初始化下拉框");
    var cmbProject = document.getElementById("selectProject");
    var cmbModule = document.getElementById("selectModule");

    dataList = [];

    // 设置默认选项
    function setDefaultOption(obj, id) {
        console.log("obj", obj.options.length);
        console.log("============id=============?", id);
        for (var i = 0; i < obj.options.length; i++) {
            if (obj.options[i].value == id) {
                obj.selectedIndex = i;
                return;
            }
        }
    }

    // 创建下拉选项
    function addOption(cmb, obj) {
        var option = document.createElement("option"); // 先创建一个option
        cmb.options.add(option); // 再把option添加到对应的下拉框里面（这里是指项目的下拉框）
        option.innerHTML = obj.name; // 再每个option里添加它的名称（这里是指项目的名称）
        option.value = obj.id; // 再每个option里添加它的id（这里是指项目的id）
    }

    //改变项目
    function changeProject() {
        cmbModule.options.length = 0;
        console.log("项目默认选项的索引", cmbProject.selectedIndex);
        var pid = cmbProject.options[cmbProject.selectedIndex].value;
        console.log("这个才是真正的项目id", pid);

        for (var i = 0; i < dataList.length; i++) {
            if (dataList[i].id == pid) {
                var modules = dataList[i].moduleList;
                console.log("对应的模块列表", modules);
                for (var j = 0; j < modules.length; j++) {
                    addOption(cmbModule, modules[j]);
                }
            }
        }

        setDefaultOption(cmbModule, defaultModuleId);
    }

    function getSelectData() {
        $.get("/case/get_select_data", {},function(resp) {
            if(resp.code === 10200) {
                dataList = resp.data;
                console.log("想要的数据格式--》",dataList);
                for (var i = 0; i < dataList.length; i++) {
                    console.log("每一个项目的数据", dataList[i]);
                    addOption(cmbProject, dataList[i]);
                }
                setDefaultOption(cmbProject, defaultProjectId);
                changeProject();
                cmbProject.onchange = changeProject;
            }
            setDefaultOption(cmbProject, defaultProjectId);

        });
    }

    getSelectData();

}

