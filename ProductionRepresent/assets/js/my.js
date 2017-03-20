//前提：价格高
var pre = {
    //定义第一层的前提
    preLvl0: {
        priceH: {
            name: 'price', //前提:价格
            value: 'h'
        },
        priceL: {
            name: 'price',
            value: 'l',
        },
        speedM: {
            name: 'speed',
            value: '40'
        },
        speedH: {
            name: 'speed',
            value: '50'
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
    preLvl1: {

    }
};
//定义推理过程结论
var conclusion = {
    conclusionLvl0: {

    },
    conclusionLvl1: {
        transporterTypeJfbpd: {
            name: 'transporterType', //传送带的类型
            value: 'jfbpd', //胶帆布平带
        },
        transporterTypeJlppd: {
            name: 'transporterType',
            value: 'jlppd', //锦纶片平带
        },
        transporterTypeHighSpeed: {
            name: 'transporterType',
            value: 'highSpeed'
        }
    },
    conclusionLvl2: {
        concluFinal0: {
            name: "final",
            value: '机械接头的胶帆布平带',
        },
        concluFinal1: {
            name: "final",
            value: '硫化接头的胶帆布平带',
        },
        concluFinal2: {
            name: "final",
            value: "硫化接头的锦纶片平带"
        },
        concluFinal3: {
            name: "final",
            value: "机械接头的锦纶片平带"
        },
        concluFinal4: {
            name: "final",
            value: "环带型高速带"
        },
        concluFinal5: {
            name: "final",
            value: "硫化接头高速带"
        }
    }
};
//定义事实
var factor = {
    factorLvl0: {

    },
    factorLvl1: {
        allow: {
            name: "allow",
            value: 'allow'
        },
        withJoint: {
            name: 'joint',
            value: 'yes'
        },
        withoutJoint: {
            name: 'joint',
            value: 'no'
        }
    }
}
var rule = {
    ruleLvl1: [{
        ruleName: '低价格和30的带速',
        ruleId: '001',
        poninter: [pre.preLvl0[priceL], pre.preLvl0[speedL]],
        result: conclusion.conclusionLvl1[transporterTypeJfbpd]
    }, {
        ruleName: '高价格和30的带速',
        ruleId: '002',
        poninter: [pre.preLvl0[priceH], pre.preLvl0[speedL]],
        result: conclusion.conclusionLvl1[transporterTypeJlppd]
    }, {
        ruleName: '寿命长和40的带速',
        ruleId: '003',
        poninter: [pre.preLvl0[lifeTimeL], pre.preLvl0[speedM]],
        result: conclusion.conclusionLvl1[transporterTypeJlppd]
    }, {
        ruleName: '带速40和寿命短',
        ruleId: '004',
        poninter: [pre.preLvl0[speedM], pre.preLvl[lifeTimeL]],
        result: conclusion.conclusionLvl1[gs]
    }]
}
var Rule = function() {
    this.
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