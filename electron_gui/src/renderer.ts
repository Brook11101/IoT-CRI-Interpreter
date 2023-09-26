import {ipcRenderer} from "electron";

//规定了逻辑处理函数与页面元素变化时接收通知并处理

//这个函数用来生成下拉列表中的每一项（对应其显示文本与真实值）
function refreshSelect(elem: HTMLSelectElement, selectDict: object) {
    elem.innerHTML = "";
    for (let item of Object.values(selectDict)) {
        let option = document.createElement("option");
        option.value = item["module_name"];
        option.text = item["name"];
        elem.add(option);
    }
}

function refreshDACSelect(elem: HTMLSelectElement, selectDict: object) {
    elem.innerHTML = "";
    for (let item of Object.values(selectDict)[0]["live_channels"]) {
        if (item["offline"] != "true") {
            let option = document.createElement("option");
            option.value = item["id"];
            option.text = item["user_name_field"];
            elem.add(option);
        }
    }
}

function refreshDSNSelect(elem: HTMLSelectElement, json_dict: object, select_account: string) {
    elem.innerHTML = "";
    for (let item of Object.values(json_dict)[0]["live_channels"]) {
        if (item["id"] == select_account) {
            for (let mac of item["macaddress"]) {
                let option = document.createElement("option");
                option.value = mac["value"];
                option.text = mac["label"];
                elem.add(option);
            }
        }
    }
}

function getAllSelects() {
    let trigger_device = document.getElementById(
        "trigger_device"
    ) as HTMLSelectElement;
    let trigger_condition = document.getElementById(
        "trigger_condition"
    ) as HTMLSelectElement;
    let trigger_DAC = document.getElementById(
        "trigger_DAC"
    ) as HTMLSelectElement;
    let trigger_DSN = document.getElementById(
        "trigger_DSN"
    ) as HTMLSelectElement;
    let query_device = document.getElementById(
        "query_device"
    ) as HTMLSelectElement;
    let query_content = document.getElementById(
        "query_content"
    ) as HTMLSelectElement;
    let query_DAC = document.getElementById(
        "query_DAC"
    ) as HTMLSelectElement;
    let query_DSN = document.getElementById(
        "query_DSN"
    ) as HTMLSelectElement;
    let action_device = document.getElementById(
        "action_device"
    ) as HTMLSelectElement;
    let action_execution = document.getElementById(
        "action_execution"
    ) as HTMLSelectElement;
    let action_DAC = document.getElementById(
        "action_DAC"
    ) as HTMLSelectElement;
    let action_DSN = document.getElementById(
        "action_DSN"
    ) as HTMLSelectElement;

    let is_pro = document.getElementById("pro_chk") as HTMLInputElement;
    let priority = document.getElementById("priority") as HTMLSelectElement;

    return {
        trigger_device: trigger_device.options[trigger_device.selectedIndex].value,
        trigger_condition:
        trigger_condition.options[trigger_condition.selectedIndex].value,
        trigger_DAC: trigger_DAC.options[trigger_DAC.selectedIndex].value,
        trigger_DSN: trigger_DSN.options[trigger_DSN.selectedIndex].value,
        query_device: query_device.options[query_device.selectedIndex].value,
        query_content: query_content.options[query_content.selectedIndex].value,
        query_DAC: query_DAC.options[query_DAC.selectedIndex].value,
        query_DSN: query_DSN.options[query_DSN.selectedIndex].value,
        action_device: action_device.options[action_device.selectedIndex].value,
        action_execution: action_execution.options[action_execution.selectedIndex].value,
        action_DAC: action_DAC.options[action_DAC.selectedIndex].value,
        action_DSN: action_DSN.options[action_DSN.selectedIndex].value,
        is_pro: is_pro.checked,
        priority: priority.options[priority.selectedIndex].text,
    };
}

window.addEventListener("load", () => {
    ipcRenderer.send("refresh_button_click");
});

window.onload = () => {
    ipcRenderer.on("load_trigger_devices", (event, arg) => {
        let trigger_device_elem = document.getElementById(
            "trigger_device"
        ) as HTMLSelectElement;
        refreshSelect(trigger_device_elem, arg);
        ipcRenderer.send("trigger_device_change", trigger_device_elem.options[0].text);
    });

    ipcRenderer.on("load_query_devices", (event, arg) => {
        let query_device_elem = document.getElementById(
            "query_device"
        ) as HTMLSelectElement;
        refreshSelect(query_device_elem, arg);
        ipcRenderer.send("query_device_change", query_device_elem.options[0].text);
    });

    ipcRenderer.on("load_action_devices", (event, arg) => {
        let action_device_elem = document.getElementById(
            "action_device"
        ) as HTMLSelectElement;
        refreshSelect(action_device_elem, arg);
        ipcRenderer.send("action_device_change", action_device_elem.options[0].text);
    });


    document.getElementById("start_button")?.addEventListener("click", () => {
        ipcRenderer.send("start_button_click", getAllSelects());
    });
    document.getElementById("refresh_button")?.addEventListener("click", () => {
        ipcRenderer.send("refresh_button_click");
    });

    document.getElementById("trigger_device")?.addEventListener("change", () => {
        let trigger_device = document.getElementById(
            "trigger_device"
        ) as HTMLSelectElement;
        let select_trigger =
            trigger_device.options[trigger_device.selectedIndex].text;
        ipcRenderer.send("trigger_device_change", select_trigger);
    });
    document.getElementById("query_device")?.addEventListener("change", () => {
        let query_device = document.getElementById(
            "query_device"
        ) as HTMLSelectElement;
        let select_content =
            query_device.options[query_device.selectedIndex].text;
        ipcRenderer.send("query_device_change", select_content);
    });
    document.getElementById("action_device")?.addEventListener("change", () => {
        let action_device = document.getElementById(
            "action_device"
        ) as HTMLSelectElement;
        let select_content =
            action_device.options[action_device.selectedIndex].text;
        ipcRenderer.send("action_device_change", select_content);
    });

    document.getElementById("trigger_DAC")?.addEventListener("change", () => {
        let trigger_device = document.getElementById(
            "trigger_device"
        ) as HTMLSelectElement;
        let trigger_DAC = document.getElementById(
            "trigger_DAC"
        ) as HTMLSelectElement;
        let select_trigger =
            trigger_device.options[trigger_device.selectedIndex].value;
        let select_account =
            trigger_DAC.options[trigger_DAC.selectedIndex].value;
        ipcRenderer.send("trigger_DAC_change", select_trigger, select_account);
    });

    document.getElementById("query_DAC")?.addEventListener("change", () => {
        let query_device = document.getElementById(
            "query_device"
        ) as HTMLSelectElement;
        let query_DAC = document.getElementById(
            "query_DAC"
        ) as HTMLSelectElement;
        let select_query =
            query_device.options[query_device.selectedIndex].value;
        let select_account =
            query_DAC.options[query_DAC.selectedIndex].value;
        ipcRenderer.send("query_DAC_change", select_query, select_account);
    });

    document.getElementById("action_DAC")?.addEventListener("change", () => {
        let action_device = document.getElementById(
            "action_device"
        ) as HTMLSelectElement;
        let action_DAC = document.getElementById(
            "action_DAC"
        ) as HTMLSelectElement;
        let select_action =
            action_device.options[action_device.selectedIndex].value;
        let select_account =
            action_DAC.options[action_DAC.selectedIndex].value;
        ipcRenderer.send("action_DAC_change", select_action, select_account);
    });


    //根据Trigger Device选项的变化来更新对应的Trigger Condition列表，同时也会更新Device_Account（即设为默认的第一个）
    ipcRenderer.on("update-trigger-condition", (event, arg) => {
        let trigger_condition_elem = document.getElementById(
            "trigger_condition"
        ) as HTMLSelectElement;
        refreshSelect(trigger_condition_elem, arg);
        let trigger_DAC_elem = document.getElementById(
            "trigger_DAC"
        ) as HTMLSelectElement;
        refreshDACSelect(trigger_DAC_elem, arg);

        //注意，你必须要在Trigger_Device使得condition和account更新完了后才可以发送更新device_name的请求
        let trigger_device = document.getElementById(
            "trigger_device"
        ) as HTMLSelectElement;
        let select_trigger_value =
            trigger_device.options[trigger_device.selectedIndex].value;
        let trigger_DAC = document.getElementById(
            "trigger_DAC"
        ) as HTMLSelectElement;
        let select_account =
            trigger_DAC.options[trigger_DAC.selectedIndex].value;
        ipcRenderer.send("trigger_DAC_change", select_trigger_value, select_account);
    });

    ipcRenderer.on("update-query-content", (event, arg) => {
        let query_content_elem = document.getElementById(
            "query_content"
        ) as HTMLSelectElement;
        refreshSelect(query_content_elem, arg);
        let query_DAC_elem = document.getElementById(
            "query_DAC"
        ) as HTMLSelectElement;
        refreshDACSelect(query_DAC_elem, arg)

        let query_device = document.getElementById(
            "query_device"
        ) as HTMLSelectElement;
        let select_query_value =
            query_device.options[query_device.selectedIndex].value;
        let query_DAC = document.getElementById(
            "query_DAC"
        ) as HTMLSelectElement;
        let select_account =
            query_DAC.options[query_DAC.selectedIndex].value;
        ipcRenderer.send("query_DAC_change", select_query_value, select_account);
    });

    //根据Action Device的变化来更新Action Execution
    ipcRenderer.on("update-action-execution", (event, arg) => {
        let action_execution_elem = document.getElementById(
            "action_execution"
        ) as HTMLSelectElement;
        refreshSelect(action_execution_elem, arg);
        let action_DAC_elem = document.getElementById(
            "action_DAC"
        ) as HTMLSelectElement;
        refreshDACSelect(action_DAC_elem, arg)

        let action_device = document.getElementById(
            "action_device"
        ) as HTMLSelectElement;
        let select_action_value =
            action_device.options[action_device.selectedIndex].value;
        let action_DAC = document.getElementById(
            "action_DAC"
        ) as HTMLSelectElement;
        let select_account =
            action_DAC.options[action_DAC.selectedIndex].value;
        ipcRenderer.send("action_DAC_change", select_action_value, select_account);
    });

    ipcRenderer.on("update-trigger-DSN", (event, trigger_json, select_account) => {
        let trigger_DSN_elem = document.getElementById(
            "trigger_DSN"
        ) as HTMLSelectElement;
        refreshDSNSelect(trigger_DSN_elem, trigger_json, select_account);
    });

    ipcRenderer.on("update-query-DSN", (event, query_json, select_account) => {
        let query_DSN_elem = document.getElementById(
            "query_DSN"
        ) as HTMLSelectElement;
        refreshDSNSelect(query_DSN_elem, query_json, select_account);
    });

    ipcRenderer.on("update-action-DSN", (event, action_json, select_account) => {
        let action_DSN_elem = document.getElementById(
            "action_DSN"
        ) as HTMLSelectElement;
        refreshDSNSelect(action_DSN_elem, action_json, select_account);
    });
};
