import { Instance_OT, Variable_WebApp, Variable_Controller, Signal_Controller } from './global-data.js';

export async function init() {
    await initControllerSignals();
    await initControllerVariables();
    await initSubscriptions();
    await initWebAppVariables();

    await InitUI();
}

export async function initWebAppVariables() {
    Variable_WebApp.taskNames = [];
    const tasks = await RWS.Rapid.getTasks();
    const reg = {};
    for (let i = 0; i < tasks.length; i++) {
        reg[tasks[i].getName()] = i;
    }
    for (let i = 0; i < tasks.length; i++) {
        const name = tasks[i].getName();
        if ((/^T_ROB\d+$/i).test(name)) {
            const taskNum = (/\D*(\d+)$/).exec(name)[1];
            if (reg[`tAwSys_${taskNum}`] !== undefined) {
                Variable_WebApp.taskNames.push(name);
            }
        }
    }
}

export async function initControllerSignals() {
    Signal_Controller.soAwSensor = await RWS.IO.getSignal("soAwSensor");
}

export async function initControllerVariables() {
    Variable_Controller.ActiveWeldIRB = await RWS.Rapid.getSharedData('ActiveWeldIRB');
    Variable_Controller.ActiveWeldIRB.addCallbackOnChanged((newValue) => {
        Variable_WebApp.activeTask = newValue;
        Instance_OT.labelTask.innerText = Variable_WebApp.activeTask;
    });

}

export async function initSubscriptions() {
    try {
        await Variable_Controller.ActiveWeldIRB.subscribe();
    } catch (error) {
        console.error(`Subscription failed. >>> ${error}`);
    }
}

export async function InitUI() {
    Instance_OT.labelTask = document.getElementById("labelTask");
    Instance_OT.labelTask.innerText = Variable_WebApp.activeTask;

    Instance_OT.btnSelectTask = new FPComponents.Button_A();
    Instance_OT.btnSelectTask.text = "Select Task";
    Instance_OT.btnSelectTask.onclick = function () {
        Instance_OT.foldinTask.show();
    };
    Instance_OT.btnSelectTask.attachToId("btnSelectTask");


    Instance_OT.switchSensorOn = new FPComponents.Switch_A();
    Instance_OT.switchSensorOn.desc = "Sensor On"
    let sensorValue = await Signal_Controller.soAwSensor.getValue();
    Instance_OT.switchSensorOn.active = sensorValue == 1;
    Instance_OT.switchSensorOn.onchange = async function (active) {
        await Signal_Controller.soAwSensor.setValue(active ? 1 : 0);

    }
    Instance_OT.switchSensorOn.attachToId("switchSensorOn");

    Instance_OT.btnSetJobNo = new FPComponents.Button_A();
    Instance_OT.btnSetJobNo.text = "Set Job No";
    Instance_OT.btnSetJobNo.onclick = function () {
        // This function will execute when the button is clicked.
    };
    Instance_OT.btnSetJobNo.attachToId("btnSetJobNo");

    Instance_OT.btnMeasurement = new FPComponents.Button_A();
    Instance_OT.btnMeasurement.text = "Measurement";
    Instance_OT.btnMeasurement.onclick = function () {
        // This function will execute when the button is clicked.
    };
    Instance_OT.btnMeasurement.attachToId("btnMeasurement");

    Instance_OT.foldinTask = new FPComponents.Foldin_A();
    Instance_OT.foldinTask.contentId = "foldinTask";
    Instance_OT.foldinTask.width = 350;
    Instance_OT.foldinTask.attachToBody();
    Instance_OT.foldinTaskMenu = new FPComponents.Menu_A();
    const model = {
        content: [
            {
                type: "gap"
            },
            {
                type: "label",
                label: "Select Rapid Task"
            },
            {
                type: "gap"
            }
        ]
    };
    for (let i = 0; i < Variable_WebApp.taskNames.length; i++) {
        model.content.push({
            type: "button",
            label: Variable_WebApp.taskNames[i],
            onclick: async () => {
                await Variable_Controller.ActiveWeldIRB.setValue(Variable_WebApp.taskNames[i]);
                Instance_OT.foldinTask.hide();
            },
        });
    }
    Instance_OT.foldinTaskMenu.model = model;
    Instance_OT.foldinTaskMenu.attachToId("foldinTask");
}