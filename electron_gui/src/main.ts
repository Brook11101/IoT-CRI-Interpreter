import {app, BrowserWindow, ipcMain} from "electron";
import path = require("path");
import {readJsonFile, searchModuleName} from "./json_loader";
import {spawn} from "child_process";
import { it } from "node:test";

//页面变化时发送消息事件

interface PythonArgs {
    rule_name: string;
    trigger_device: string;
    trigger_condition: string;
    trigger_DAC: string;
    trigger_device_info: object[];

    query_device: string;
    query_content: string;
    query_DAC: string;
    query_device_info: object[];

    action_device: string;
    action_execution: string;
    action_DAC: string;
    action_device_info: object[];

    filter_code: string;

    is_pro: boolean;
    priority: string;
}

function runPythonScript(args: PythonArgs) {
    // 定义要执行的命令和参数
    const command = "scrapy";
    const commandArgs = [
        "runspider",
        "-a", "trigger_device=" + args.trigger_device,
        "-a", "trigger_condition=" + args.trigger_condition,
        "-a", "trigger_DAC=" + args.trigger_DAC,
        "-a", "trigger_device_info=" + JSON.stringify(args.trigger_device_info),

        "-a", "query_device=" + args.query_device,
        "-a", "query_content=" + args.query_content,
        "-a", "query_DAC=" + args.query_DAC,
        "-a", "query_device_info=" + JSON.stringify(args.query_device_info),

        "-a", "action_device=" + args.action_device,
        "-a", "action_execution=" + args.action_execution,
        "-a", "action_DAC=" + args.action_DAC,
        "-a", "action_device_info=" + JSON.stringify(args.action_device_info),

        "-a", "is_pro=" + String(args["is_pro"]),
        "-a", "priority=" + args.priority,
        "-a", "rule_name=" + args.rule_name,
        "-a", "filter_code=" + args.filter_code,
        "../applet_executor/ifttt_rule_creator.py",
    ];

    const python = spawn(command, commandArgs);
    python.stdout.on("data", (data) => {
        console.log(`stdout: ${data.toString()}`);
    });
    python.stderr.on("data", (data) => {
        console.error(`stderr: ${data.toString()}`);
    });
    python.on("close", (code) => {
        console.log(`child process exited with code ${code}`);
    });
}

let win: BrowserWindow;
let trigger_devices = readJsonFile(
    "../../data/electron_json/trigger_device_names.json"
);
let query_devices = readJsonFile(
    "../../data/electron_json/query_device_names.json"
);
let action_devices = readJsonFile(
    "../../data/electron_json/action_device_names.json"
);

const createWindow = () => {
    win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, "renderer.js"),
        },
    });
    win.loadFile("../assets/index.html");
    console.log("start!");
};

app.whenReady().then(() => {
    createWindow();
});

function toCamelCase(str: string): string {
    return str.replace(/_([a-z])/g, function (g) { return g[1].toUpperCase(); });
}

ipcMain.on("load_filter_code_option", (event, arg: PythonArgs) => {
    console.log('refresh_options!!')
    console.log(arg)

    let triggerObj = readJsonFile(
        "../../data/electron_json/trigger/" + arg.trigger_device + ".json"
    );
    let trigger_ingredients_name = []
    let trigger_ingredients = triggerObj.find((item: any) => item.module_name === arg.trigger_condition).ingredients;
    for(let item of trigger_ingredients) {
        trigger_ingredients_name.push(item.normalized_name)
    }
    win.webContents.send("update_filter_trigger_ingredient", trigger_ingredients_name);


    let actionObj = readJsonFile(
        "../../data/electron_json/action/" + arg.action_device + ".json"
    );
    let action_options_name = [toCamelCase(arg.action_execution) + ".skip()"]
    win.webContents.send("update_filter_action_options", action_options_name);

    let queryObj = readJsonFile(
        "../../data/electron_json/query/" + arg.query_device + ".json"
    );
    let query_ingredients_name = []
    let query_ingredients = queryObj.find((item: any) => item.module_name === arg.query_content).ingredients;
    for(let item of query_ingredients) {
        query_ingredients_name.push(item.normalized_name)
    }
    win.webContents.send("update_filter_query_ingredients", query_ingredients_name);
})

//这个args是输入栏里的每一项参数
ipcMain.on("start_button_click", (event, arg) => {
    console.log("start!");
    // console.log(arg);
    runPythonScript(arg);
});
//trigger_devices是所有名字的集合体
ipcMain.on("refresh_button_click", () => {
    win.webContents.send("load_trigger_devices", trigger_devices);
    win.webContents.send("load_query_devices", query_devices);
    win.webContents.send("load_action_devices", action_devices);
});

ipcMain.on("trigger_device_change", (event, arg) => {
    let module_name = searchModuleName(trigger_devices, arg);
    let nameObj = readJsonFile(
        "../../data/electron_json/trigger/" + module_name + ".json"
    );
    win.webContents.send("update-trigger-condition", nameObj);
});

ipcMain.on("query_device_change", (event, arg) => {
    let module_name = searchModuleName(query_devices, arg);
    let nameObj = readJsonFile(
        "../../data/electron_json/query/" + module_name + ".json"
    );
    win.webContents.send("update-query-content", nameObj);
});

ipcMain.on("action_device_change", (event, arg) => {
    let module_name = searchModuleName(action_devices, arg);
    let nameObj = readJsonFile(
        "../../data/electron_json/action/" + module_name + ".json"
    );
    win.webContents.send("update-action-execution", nameObj);
});

ipcMain.on("trigger_condition_change", (event, select_trigger, select_trigger_condition, select_account) => {
    let trigger_json = readJsonFile(
        "../../data/electron_json/trigger/" + select_trigger + ".json"
    );
    win.webContents.send("update-trigger-device-info", trigger_json, select_trigger_condition, select_account);
});

ipcMain.on("query_content_change", (event, select_query, select_query_content, select_account) => {
    let query_json = readJsonFile(
        "../../data/electron_json/query/" + select_query + ".json"
    );
    win.webContents.send("update-query-device-info", query_json, select_query_content, select_account);
});

ipcMain.on("action_execution_change", (event, select_action, select_action_execution, select_account) => {
    let action_json = readJsonFile(
        "../../data/electron_json/action/" + select_action + ".json"
    );
    win.webContents.send("update-action-device-info", action_json, select_action_execution, select_account);
});


ipcMain.on("trigger_DAC_change", (event, select_trigger, select_trigger_condition, select_account) => {
    //此处可以直接传value值而不是text值
    let trigger_json = readJsonFile(
        "../../data/electron_json/trigger/" + select_trigger + ".json"
    );
    win.webContents.send("update-trigger-device-info", trigger_json, select_trigger_condition, select_account);
});

ipcMain.on("query_DAC_change", (event, select_query, select_query_content, select_account) => {
    let query_json = readJsonFile(
        "../../data/electron_json/query/" + select_query + ".json"
    );
    win.webContents.send("update-query-device-info", query_json, select_query_content, select_account);
});

ipcMain.on("action_DAC_change", (event, select_action, select_action_execution, select_account) => {
    let action_json = readJsonFile(
        "../../data/electron_json/action/" + select_action + ".json"
    );
    win.webContents.send("update-action-device-info", action_json, select_action_execution, select_account);
});

ipcMain.handle('getEditorContent', async (event) => {
    let win = BrowserWindow.getFocusedWindow(); // 获取当前聚焦的窗口
    let result = await win.webContents.executeJavaScript('window.getEditorContent()');
    return String(result);
});

