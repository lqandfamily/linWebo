var myChart = echarts.init(document.querySelector('.current-data-chart'));

//Json请求
$.get("http://127.0.0.1/curData", function (data) {
    //准备数据
    var dataTitle = [];
    var dataView = [];
    for (var i = 0; i < data.length; i++) {
        dataTitle[i] = data[i].affair;
        viewTmp = {value: parseInt(data[i].view), name: data[i].affair}
        dataView[i] = viewTmp;
    }


// 指定图表的配置项和数据
    option = {
        tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
            orient: 'vertical',
            left: 10,

            data: dataTitle
            /*            data: ["孙杨外教离开中国游泳队", "新冠肺炎世界疫情形势", "傅首尔美伢 带娃云同框",
                            "张伟丽成功卫冕", "乔安娜", "韩网评韩国十大美女", "给女孩",
                            "湖北以外省份首次无本土确诊病例", "当不会做饭的人做饭时", "国家卫健委回应抗疫补助发放标准"],*/
        },
        series: [
            {
                name: '热搜量',
                type: 'pie',
                radius: ['50%', '70%'],
                avoidLabelOverlap: false,
                label: {
                    show: false,
                    position: 'center'
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: '30',
                        fontWeight: 'bold'
                    }
                },
                labelLine: {
                    show: false
                },
                data: dataView
                /*
                data: [
                    {value: 335, name: '孙杨外教离开中国游泳队'},
                    {value: 310, name: '新冠肺炎世界疫情形势'},
                    {value: 234, name: '傅首尔美伢 带娃云同框'},
                    {value: 135, name: '张伟丽成功卫冕'},
                    {value: 1548, name: '韩网评韩国十大美女'},
                    {value: 1548, name: '给女孩'},
                    {value: 1548, name: '湖北以外省份首次无本土确诊病例'},
                ]*/
            }
        ]
    };
// 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
});
