<template>
  <div class="content">
    <Card :bordered="false" class="myCard">
      <p slot="title" style="text-align: left; margin-top: 3px;">Pattern Compare</p>
      <div style="margin-left: 10px; position: absolute; margin-top: 15px;">

          <span>Source:</span>
          <Select v-model="selectSource" @on-change="handleselectSource()" style="width:80px" size="small">
            <Option v-for="item in patternList" :value="item.value" :key="item.value">{{ item.label }}</Option>
          </Select>

          <span style="margin-left: 4px;">Target:</span>
          <Select v-model="selectTarget" @on-change="handleselectTarget()" style="width:80px" size="small">
            <Option v-for="item in patternList" :value="item.value" :key="item.value">{{ item.label }}</Option>
          </Select>

      </div>
      <div id="compare_container"></div>
      <div id="hist_chart" style="width: 287px;height: 97px;"></div>
    </Card>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'patterncompare',
  data() {
    return {
      base_url: 'http://127.0.0.1:8420/',
      patternList: [],
      selectSource: 'Pat_1',
      selectTarget: 'Pat_2'
    }
  },
  watch: {},
  computed: {},
  created() {
  },
  mounted() {
    this.getpatternList();
    this.getcomparedata();
  },
  methods: {
    getpatternList() {
      var patternNum = 0;
      axios.get(this.base_url + 'getPatternOverview')
        .then(res => {
          patternNum = res.data.total;
          for (var i = 1; i <= patternNum; i++) {
            this.patternList.push({
              value: 'Pat_' + i,
              label: 'Pat_' + i
            })
          }
        });
    },
    getcomparedata() {
      axios.get(this.base_url + 'getPatterncompare?source=' + this.selectSource + '&target=' + this.selectTarget)
        .then(res => {
          this.drawCompare(res.data);
        });
    },
    handleselectSource() {
      this.getcomparedata();
    },
    handleselectTarget() {
      this.getcomparedata();
    },
    drawCompare(data) {
      console.log(data);
      $('#compare_container').empty();
      //获取画布
      const margin = {top: 5, left: 5, right: 5, bottom: 5};
      const container = d3.select("#compare_container")
        .append('svg')
        .attr('id', 'compareInfo');

      const svg = d3.select("#compareInfo");
      const height = d3.select("#compare_container")._groups[0][0].clientHeight - margin.top - margin.bottom;
      const width = d3.select("#compareInfo")._groups[0][0].clientWidth;
      const g = svg.append("g")
        .attr("id", "maingroup")
        .attr('transform', `translate(${margin.left},${margin.top})`);


      // 初始化一个对象，用于存储每个轴的最大值
      const maxValue = [];

      // 遍历 radarData 数组
      data.radarData.forEach(data => {
        // 遍历每个对象中的 value 数组
        data.value.forEach((item, i) => {
          // 如果当前轴不存在于 maxValues 中，或者当前值大于 maxValues 中该轴的值
          if (typeof maxValue[i] === 'undefined' || item.value > maxValue[i]) {
            // 将当前值赋给该轴
            maxValue[i] = item.value;
          }
        });
      });

      const Color_list = ["#09A9FF", "#F5A119"];

      // var color = d3.scaleOrdinal()
      //   .range(["#08A9FF ", "#F5A118"]);
      var color = d3.scaleOrdinal()
        .range(Color_list);

      var axesDomain = data.radarData[0].value.map(d => d.axis);
      var axesLength = data.radarData[0].value.map(d => d.axis).length;
      var radius = 68;
      var angleSlice = Math.PI * 2 / axesLength;
      var axisCircles = 5;

      var axisLabelFactor = 1.12;

      var rScale_1 = d3.scaleLinear()
        .domain([0, maxValue[0]])
        .range([0, radius]);

      var rScale_2 = d3.scaleLinear()
        .domain([0, maxValue[1]])
        .range([0, radius]);

      var rScale_3 = d3.scaleLinear()
        .domain([0, maxValue[2]])
        .range([0, radius]);

      var rScale_4 = d3.scaleLinear()
        .domain([0, maxValue[3]])
        .range([0, radius]);


      var radarLine = d3.lineRadial()
        .curve(d3.curveCardinalClosed)
        .radius((d, i) => {
          if (i === 0) {
            return rScale_1(d);
          } else if (i === 1) {
            return rScale_2(d);
          } else if (i === 2) {
            return rScale_3(d);
          } else {
            return rScale_4(d);
          }
        })
        .angle((d, i) => i * angleSlice);

      var axisGrid = g.append("g")
        .attr('transform', `translate(${width / 2 + 5},${26 * margin.top})`)
        .attr("class", "axisWrapper");

      axisGrid.selectAll(".levels")
        .data(d3.range(1, (axisCircles + 1)).reverse())
        .enter()
        .append("circle")
        .attr("class", "gridCircle")
        .attr("r", (d, i) => radius / axisCircles * d)
        .style("fill", "#CDCDCD")
        .style("stroke", "#CDCDCD")
        .style("fill-opacity", 0.1);

      // 四根轴线
      g.append("g")
        .append("line")
        .attr("x1", 77)
        .attr("y1", 130)
        .attr("x2", 218)
        .attr("y2", 130)
        .attr("fill", "none")
        .attr("stroke", "#DCDCDC");

      g.append("g")
        .append("line")
        .attr("x1", 148)
        .attr("y1", 65)
        .attr("x2", 148)
        .attr("y2", 198)
        .attr("fill", "none")
        .attr("stroke", "#DCDCDC");


      g.append("g")
        .append("text")
        .attr("x", 115)
        .attr("y", 56)
        .attr("font-size", 12)
        .text("Total Events");

      g.append("g")
        .append("text")
        .attr("x", 232)
        .attr("y", 125)
        .attr("font-size", 12)
        .text("Total");

      g.append("g")
        .append("text")
        .attr("x", 224)
        .attr("y", 140)
        .attr("font-size", 12)
        .text("Learners");

      g.append("g")
        .append("text")
        .attr("x", 115)
        .attr("y", 212)
        .attr("font-size", 12)
        .text("Event Diversity");

      g.append("g")
        .append("text")
        .attr("x", 25)
        .attr("y", 125)
        .attr("font-size", 12)
        .text("Total");

      g.append("g")
        .append("text")
        .attr("x", 8)
        .attr("y", 140)
        .attr("font-size", 12)
        .text("Knowledge");


      var device = d => data.radarData.map(d => d.name)[d]

      const plots = g.append('g')
        .selectAll('g')
        .data(data.radarData)
        .join('g')
        .attr("data-name", (d, i) => device(i))
        .attr("fill", "none")
        .attr("stroke", "steelblue");

      plots.append("g")
        .attr('transform', `translate(${width / 2 + 5},${26 * margin.top})`)
        .append('path')
        .attr("d", d => radarLine(d.value.map(v => v.value)))
        .attr("fill", (d, i) => color(i))
        .attr("fill-opacity", 0.1)
        .attr("stroke", (d, i) => color(i))
        .attr("stroke-width", 2);

      var dotRadius = 3;
      var pat_li = 0;
      g.append("g")
        .attr('transform', `translate(${width / 2 + 5},${26 * margin.top})`)
        .selectAll("g")
        .data(data.radarData)
        .join("g")
        .selectAll("circle")
        .data(d => d.value)
        .join("circle")
        .attr("r", dotRadius)
        .attr("cx", (d, i) => {
          if (i === 0) {
            return rScale_1(d.value) * Math.cos(angleSlice * i - Math.PI / 2);
          } else if (i === 1) {
            return rScale_2(d.value) * Math.cos(angleSlice * i - Math.PI / 2);
          } else if (i === 2) {
            return rScale_3(d.value) * Math.cos(angleSlice * i - Math.PI / 2);
          } else {
            return rScale_4(d.value) * Math.cos(angleSlice * i - Math.PI / 2);
          }
        })
        .attr("cy", (d, i) => {
          if (i === 0) {
            return rScale_1(d.value) * Math.sin(angleSlice * i - Math.PI / 2);
          } else if (i === 1) {
            return rScale_2(d.value) * Math.sin(angleSlice * i - Math.PI / 2);
          } else if (i === 2) {
            return rScale_3(d.value) * Math.sin(angleSlice * i - Math.PI / 2);
          } else {
            return rScale_4(d.value) * Math.sin(angleSlice * i - Math.PI / 2);
          }
        })
        .attr("fill", function (d, i) {
          if (i % axesLength == 0) {
            pat_li += 1;
          }
          return color(pat_li - 1);
        })
        .style("fill-opacity", 0.8);

      // const pat_name = data.radarData.map(d => d.name);
      // g.append("g")
      //   .selectAll("rect")
      //   .data(pat_name)
      //   .enter()
      //   .append("rect")
      //   .attr("x", (d, i) => width - 20 * margin.right)
      //   .attr("y", (d, i) => margin.top * 2 + i * 15)
      //   .attr("width", 20)
      //   .attr("height", 8)
      //   .attr("rx", 3)
      //   .attr("ry", 3)
      //   .attr("fill", (d, i) => color(i));
      //
      // g.append("g")
      //   .selectAll("text")
      //   .data(pat_name)
      //   .join("text")
      //   .attr("x", (d, i) => width - 15 * margin.right)
      //   .attr("y", (d, i) => margin.top * 3.3 + i * 15)
      //   .text(d => d)
      //   .attr("font-size", 10);

      //柱状图
      const barheight = 50;
      const barwidth = width / 2 - 4.4 * margin.left;

      const x_Scale = d3.scaleLinear()
        .domain(d3.extent(data.hist[0])).nice()
        .range([margin.left, barwidth]);

      const bins_1 = d3.histogram().domain(x_Scale.domain()).thresholds(x_Scale.ticks(10))(data.hist[0]);
      const bins_2 = d3.histogram().domain(x_Scale.domain()).thresholds(x_Scale.ticks(10))(data.hist[1]);

      var max_yscale = d3.max(bins_1, d => d.length) > d3.max(bins_2, d => d.length) ? d3.max(bins_1, d => d.length) : d3.max(bins_2, d => d.length);

      const y_Scale = d3.scaleLinear()
        .domain([0, max_yscale]).nice()
        .range([barheight - margin.bottom, margin.top]);

      const xAxis = g => g
        .call(
          d3.axisBottom(x_Scale).tickSizeOuter(0).tickSize(4).tickFormat((i) => i % 3 == 0 ? i : '')
        )
        .call(
          g => g.append("text")
            .attr("x", barwidth)
            .attr("y", -8)
            .attr("fill", "#000")
            .attr("font-weight", "small")
            .attr("text-anchor", "end")
            .text(data.hist[0].x)
        );


      const yAxis = g => g
        .call(d3.axisLeft(y_Scale).tickSize(4).ticks(3))
        .call(
          g => g.select(".tick:last-of-type text").clone()
            .attr("x", 6)
            .attr("text-anchor", "start")
            .attr("font-weight", "bold")
            .text(data.hist[0].y)
        );


      //底部直方图
      var myChart = echarts.init(document.getElementById('hist_chart'));

      // 清除图表
      myChart.clear();


      var data1 = data.hist[0];
      var data2 = data.hist[0];

      // 计算数据的频次
      function calculateFrequency(data) {
        var dataMap = {};
        data.forEach(function (value) {
          var key = Math.floor(value / 10) * 10; // 这里假设按照20为一个区间进行分组
          dataMap[key] = (dataMap[key] || 0) + 1;
        });
        return Object.keys(dataMap).map(Number).sort((a, b) => a - b); // 按分数区间排序
      }

      var seriesData1 = calculateFrequency(data1);
      var seriesData2 = calculateFrequency(data2);

      var xAxisData = seriesData1.map(String); // 使用分数区间作为 x 轴数据


      var option = {
        legend: {
          data: [data.radarData[0].name, data.radarData[1].name],
          top: '2%',
          right: '2%',
          itemHeight: 8,
          itemWidth: 14,
          textStyle: {
            color: '#000',
            fontSize: 8
        }
        },
        grid: {
          left: 30,
          right: 3,
          top: 20,
          bottom: 30
        },
        xAxis: {
          type: 'category',
          data: xAxisData, // 使用分数区间作为 x 轴数据
          axisTick: {
            show: false
          },
          axisLabel: {
            show: true,
            fontSize: 8
          },
          name: 'Learning Performance',
          nameLocation: 'center',
          nameTextStyle: {
            fontSize: 12,
            padding: [2, 0, 0, 0]
          }
        },
        yAxis: {
          type: 'value',
          name: 'Learners',
          nameLocation: 'top',
          nameTextStyle: {
            fontSize: 12,
            padding: [0, 0, 30, 0]
          },
          splitNumber: 3,
          axisLabel: {
            show: true,
            fontSize: 8
          },
        },
        series: [
          {
            name: data.radarData[0].name,
            type: 'bar',
            data: seriesData1,
            itemStyle: {
              color: Color_list[0]
            }
          },
          {
            name: data.radarData[1].name,
            type: 'bar',
            data: seriesData2,
            itemStyle: {
              color: Color_list[1]
            }
          }
        ]
      };
      myChart.setOption(option);


      //X轴
      // g.append("g")
      //   .call(xAxis)
      //   .attr('transform', `translate(${margin.left * 1.8}, ${height - barheight + margin.top * 6})`)
      //   .call(
      //     g => g.selectAll(".tick line")
      //       .clone()
      //       .attr("stroke-opacity", 0.1)
      //       .attr("y1", -barheight + margin.top + margin.bottom)
      //   )
      //   .selectAll("text")
      //   .style("font-size", "10px");
      // //Y轴
      // g.append("g")
      //   .call(yAxis)
      //   .attr('transform', `translate(${margin.left * 2.8}, ${height - barheight - 3 * margin.top})`)
      //   .call(
      //     g => g.selectAll(".tick line")
      //       .clone()
      //       .attr("stroke-opacity", 0.1)
      //       .attr("stroke-width", 1)
      //       .attr("x1", barwidth)
      //   )
      //   .selectAll("text")
      //   .style("font-size", "10px");
      // //柱状图
      // g.append("g")
      //   .attr('transform', `translate(${margin.left * 1.8}, ${height - barheight - 3 * margin.top})`)
      //   .attr("fill", color(0))
      //   .selectAll("rect")
      //   .data(bins_1)
      //   .enter()
      //   .append("rect")
      //   .attr("x", d => x_Scale(d.x0) + 1)
      //   .attr("width", d => Math.max(0, x_Scale(d.x1) - x_Scale(d.x0) - 1))
      //   .attr("y", d => y_Scale(d.length))
      //   .attr("height", d => y_Scale(0) - y_Scale(d.length));
      //
      //
      // //右侧直方图
      // //X轴
      // g.append("g")
      //   .call(xAxis)
      //   .attr('transform', `translate(${barwidth + margin.left * 4.5}, ${height - barheight + margin.top * 6})`)
      //   .call(
      //     g => g.selectAll(".tick line")
      //       .clone()
      //       .attr("stroke-opacity", 0.1)
      //       .attr("y1", -barheight + margin.top + margin.bottom)
      //   )
      //   .selectAll("text")
      //   .style("font-size", "10px");
      // //Y轴
      // g.append("g")
      //   .call(yAxis)
      //   .attr('transform', `translate(${barwidth + margin.left * 5.5}, ${height - barheight - 3 * margin.top})`)
      //   .call(
      //     g => g.selectAll(".tick line")
      //       .clone()
      //       .attr("stroke-opacity", 0.1)
      //       .attr("stroke-width", 1)
      //       .attr("x1", barwidth)
      //   )
      //   .selectAll("text")
      //   .style("font-size", "10px");
      // //柱状图
      // g.append("g")
      //   .attr('transform', `translate(${barwidth + margin.left * 4.5}, ${height - barheight - 3 * margin.top})`)
      //   .attr("fill", color(1))
      //   .selectAll("rect")
      //   .data(bins_2)
      //   .enter()
      //   .append("rect")
      //   .attr("x", d => x_Scale(d.x0) + 1)
      //   .attr("width", d => Math.max(0, x_Scale(d.x1) - x_Scale(d.x0) - 1))
      //   .attr("y", d => y_Scale(d.length))
      //   .attr("height", d => y_Scale(0) - y_Scale(d.length));
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
div#compare_container {
  height: 232px;
  width: 285px;
}

svg#compareInfo {
  height: 232px;
  width: 285px;
}
</style>
