const Instance_OT = {
    labelTask: null,
    btnSwitchTask: null,
    foldinTask: null,
    foldinTaskMenu: null,
    btnSensorOn: null,
    btnSetJobNo: null,
    btnMeasurement: null,
}

const Variable_ArcWelding = {
    taskNames: [],
    activeTask: "T_ROB1",
    ActiveWeldIRB: null,
}

fpComponentsEnableLog(); 
await initData();
await subscribeData();

initFoldin();

Instance_OT.labelTask = document.getElementById("labelTask");

Instance_OT.btnSwitchTask = new FPComponents.Button_A();
Instance_OT.btnSwitchTask.text = "Switch Task";
Instance_OT.btnSwitchTask.onclick = function () {
    Instance_OT.foldinTask.show();
};
Instance_OT.btnSwitchTask.attachToId("btnSwitchTask");

Instance_OT.btnSensorOn = new FPComponents.Button_A();
Instance_OT.btnSensorOn.text = "Sensor On";
Instance_OT.btnSensorOn.onclick = function () {
    // This function will execute when the button is clicked.
};
Instance_OT.btnSensorOn.attachToId("btnSensorOn");

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

function initFoldin() {
    Instance_OT.foldinTask = new FPComponents.Foldin_A();
    Instance_OT.foldinTask.contentId = "foldinTask";
    Instance_OT.foldinTask.width = 350;
    Instance_OT.foldinTask.attachToBody();

    initMenu();
}

function initMenu() {
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

    for (let i = 0; i < Variable_ArcWelding.taskNames.length; i++) {
        model.content.push({
            type: "button",
            label: Variable_ArcWelding.taskNames[i],
            onclick: async () => {              
                let rapidData = null;
                let newValue = null;
                rapidData = await RWS.Rapid.getSharedData('ActiveWeldIRB');
                newValue = await rapidData.getValue();
                await rapidData.setValue(Variable_ArcWelding.taskNames[i]);

                Instance_OT.foldinTask.hide();
            },
        });
    }

    Instance_OT.foldinTaskMenu.model = model;

    Instance_OT.foldinTaskMenu.attachToId("foldinTask");
}

async function initData() {
    Variable_ArcWelding.taskNames = [];
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
                Variable_ArcWelding.taskNames.push(name);
            }
        }
    }

}

async function subscribeData() {
    Variable_ArcWelding.ActiveWeldIRB = await RWS.Rapid.getSharedData('ActiveWeldIRB');
    Variable_ArcWelding.ActiveWeldIRB.addCallbackOnChanged((newValue) => {
        console.log(`ActiveWeldIRB value changed: ${newValue}.`);
        Variable_ArcWelding.activeTask = newValue;
        Instance_OT.labelTask.innerText = newValue;
    });

    try {
        await Variable_ArcWelding.ActiveWeldIRB.subscribe();
    } catch (error) {
        var resource = Variable_ArcWelding.ActiveWeldIRB.getResourceString();
        console.error(`Subscription to '${resource}' failed. >>> ${error}`);
    }
}