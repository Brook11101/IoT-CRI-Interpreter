import {app, BrowserWindow, ipcMain} from "electron";
import path = require("path");
import {readJsonFile, searchModuleName} from "./json_loader";
import {spawn} from "child_process";

//页面变化时发送消息事件

interface PythonArgs {
    trigger_device: string;
    trigger_condition: string;
    trigger_DAC: string;
    trigger_DSN: string;
    query_device: string;
    query_content: string;
    query_DAC: string;
    query_DSN: string;
    action_device: string;
    action_execution: string;
    action_DAC: string;
    action_DSN: string;
    is_pro: boolean;
    priority: string;
}

function runPythonScript(args: PythonArgs): void {
    const python = spawn("python", [
        "../applet_executor/applet_executor.py",
        args["trigger_device"],
        args["trigger_condition"],
        args["trigger_DAC"],
        args["trigger_DSN"],
        args["query_device"],
        args["query_content"],
        args["query_DAC"],
        args["query_DSN"],
        args["action_device"],
        args["action_execution"],
        args["query_DAC"],
        args["action_DSN"],
        String(args["is_pro"]),
        args["priority"],
    ]);

    python.stdout.on("data", (data: Buffer) => {
        console.log(`stdout: ${data.toString()}`);
    });

    python.stderr.on("data", (data: Buffer) => {
        console.error(`stderr: ${data.toString()}`);
    });

    python.on("close", (code: number) => {
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


//这个args是输入栏里的每一项参数
ipcMain.on("start_button_click", (event, arg) => {
    console.log("start!");
    console.log(arg);
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

ipcMain.on("trigger_DAC_change", (event, select_trigger, select_account) => {
    console.log(select_trigger+"   "+select_account);
    let trigger_json = readJsonFile(
        "../../data/electron_json/trigger/" + select_trigger + ".json"
    );
    win.webContents.send("update-trigger-DSN", trigger_json, select_account);
});

ipcMain.on("query_DAC_change", (event, select_query, select_account) => {
    let query_json = readJsonFile(
        "../../data/electron_json/query/" + select_query + ".json"
    );
    win.webContents.send("update-query-DSN", query_json, select_account);
});

ipcMain.on("action_DAC_change", (event, select_action, select_account) => {
    let action_json = readJsonFile(
        "../../data/electron_json/action/" + select_action + ".json"
    );
    win.webContents.send("update-action-DSN", action_json, select_account);
});
