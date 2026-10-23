export const Constants = {
    RegExpInteger: /^-?[0-9]+$/,
    RegExpNonNegativeInteger: /^[0-9]+$/,
    RegExpFloat: /^-?[0-9]+(\.[0-9]+)?$/,
    RegExpNonNegativeFloat: /^[0-9]+(\.[0-9]+)?$/,
}

export const Instance_OT = {
    labelTask: null,
    btnSelectTask: null,
    foldinTask: null,
    foldinTaskMenu: null,
    switchSensorOn: null,
    inputJointNumber: null,
    btnSetJobNo: null,
    btnMeasurement: null,
}

export const Variable_WebApp = {
    taskNames: [],
    activeTask: "T_ROB1",
}

export const Variable_Controller = {
    ActiveWeldIRB: null,
    SensJoint: null,
}

export const Signal_Controller = {
    soAwSensor: null,
}