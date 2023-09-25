Monitor(Mutex Lock_Name , Priority , TimeWindow, Preference){
    If Wemo_Switch is switched on
    Query{
        Wemo_Switch History of Switched On
    }
    Filter{
        let check = WemoSwitch.historyOfSwitchedOff[0].SwitchName
        let ingredient = WemoSwitch.attributeSOCKETONN.SwitchedOnAt;
        let searchTerm = 'Home';
        if (ingredient.indexOf(searchTerm) !== -1 && check.indexOf('switchA')! == -1) {
            // run the action
            if(Meta.currentUserTime.hour() == 12)
                WemoSwitch.attributeSocketOffDiscrete.skip();
        } else {
            WemoSwitch.attributeSocketOffDiscrete.skip();
        }
    }
    Delay{
        1 Hour 20 Min 12 Sec
    }
    Then{
        Turn off Wemo_Switch
        Turn on Yeelight_Bulb
    }
}

function fibonacci(n: number): number {
    if (n === 1 || n === 2)
        return 1;
    let fibPrev = 1;
    let fibCurr = 1;
    for (let i = 3; i <= n; i++) {
        const fibNext = fibPrev + fibCurr;
        fibPrev = fibCurr;
        fibCurr = fibNext;
    }
    return fibCurr;
}
let a = fibonacci(5);
if (a > 10)
    WemoSwitch.attributeSocketOffDiscrete.skip()