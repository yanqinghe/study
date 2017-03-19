//前提：价格高
var pre = {
    //定义第一层的前提
    preLvl1: {
        priceH: {
            name: 'price', //前提:价格
            value: 'h'
        },
        priceL: {
            name: 'price',
            value: 'l',
        },
        speedH: {
            name: 'speed',
            value: '40'
        },
        speedL: {
            name: 'speed',
            value: '30',
        },
        lifeTimeL: {
            name: 'lifeTime',
            value: 'long'
        },
        lifeTimeS: {
            name: 'lifeTime',
            value: 'short'
        }
    },
    preLvl2: {

    }
};
//定义推理过程结论
var conclusion = {
    conclusionLvl1: [{
        name: 'transporterType', //传送带的类型
        value: 'jfbpd', //胶帆布平带
    }, {
        name: 'transporterType',
        value: 'jlppd', //锦纶片平带
    }],
};
//定义事实
var factor = {
    factorLvl1: [{
        name: 'factor1',
        value: 'allow'
    }, {
        name: 'joint',
        value: 'yes'
    }, {
        name: 'joint',
        value: 'no'
    }]
}
var rule = {
    ruleLvl1: [{
        ruleName: '低价格和30的带速',
        ruleId: '001',
        poninter: [pre.preLvl1[priceL], pre.preLvl1[speedL]],
        result: conclusion.conclusionLvl1[0]
    }, {
        ruleName: '高价格和30的带速',
        ruleId: '002',
        poninter: [pre.preLvl1[priceH], pre.preLvl1[speedL]],
        result: conclusion.conclusionLvl1[0]
    }, {
        ruleName: '寿命长和30的带速',
        ruleId: '003',
        poninter: [pre.preLvl1[lifeTimeL], pre.preLvl1[speedL]],
        result: conclusion.conclusionLvl1[0]
    }]
}
var pre1 = {
    name: 'price',
    value: 'h'
};
//前提：带速30
var pre3 = {
    name: 'speed',
    value: '30',
};
//前提:
var pre4 = {
    name: 'speed',
    value: '40'
};
var pre2 = {
    name: 'price',
    value: 'l'
};

var rule1 = {
    ruleName: '推理',
    ruleId: '0001',
    pointer: [pre1, pre3]
};

var rule2 = {
    name: 'price',
    poninter: [{
        value: 'l', //价廉
    }]
}