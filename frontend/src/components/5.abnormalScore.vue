<template>
  <div class="content">
    <Card :bordered="false" class="myCard">
      <p slot="title" style="text-align: left;  margin-top: 3px;">Abnormal Detection
        <Button type="info" @click="handleIS()" size="small" style="margin-left: 100px;">Inference Score</Button>
        <Button type="info" @click="handleRV()" size="small" style="margin-left: 20px;">Raw Value</Button>
        <span style="margin-left: 20px; font-weight: normal;">Attribute:</span>
        <Select v-model="selectAttr" @on-change="handleselectAttr()" style="width:130px; height: 24px;" size="small">
          <Option v-for="item in AttrList" :value="item.value" :key="item.value">{{ item.label }}</Option>
        </Select>

        <span style="margin-left: 20px; font-weight: normal;">Rank by Count:</span>
        <Button @click="rankByAscending" icon="ios-trending-up"
                style="color: black; font-size: 13px; padding: 0px 0px; width: 20px; height: 20px; position: absolute; top: 10px; left: 785px;"></Button>
        <Button @click="rankByDescending" icon="ios-trending-down"
                style="color: black; font-size: 13px; padding: 0px 0px; width: 20px; height: 20px; position: absolute; top: 10px; left: 810px;"></Button>

      </p>
      <div id="abnormal_container"></div>
    </Card>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: 'abnormalscore',
  data() {
    return {
      base_url: 'http://127.0.0.1:8420/',
      AttrList: [
        {
          value: '1',
          label: 'Type of Result'
        },
        {
          value: '2',
          label: 'Type of Difficulty'
        },
        {
          value: '3',
          label: 'Type of Knowledge'
        },
        {
          value: '4',
          label: 'Time for Practice'
        }
      ],
      selectAttr: '1',
      selectDataType: 'IS'
    }
  },
  watch: {},
  computed: {},
  created() {
  },
  mounted() {
    // this.drawAbnormal();
    this.getdata();
  },
  methods: {
    getdata() {
      axios.get(this.base_url + 'getAbnormal?type=' + this.selectDataType + '&attr=' + this.selectAttr)
        .then(res => {
          this.drawAbnormal(res.data);
          this.$store.state.selectNor = res.data;
        });
    },
    handleselectAttr() {
      this.getdata();
    },
    rankByAscending() {
      this.$store.state.selectNor.bardata.sort(function (a, b) {
        return b.ab_count - a.ab_count;
      });
      this.drawAbnormal(this.$store.state.selectNor);
    },
    rankByDescending() {
      this.$store.state.selectNor.bardata.sort(function (a, b) {
        return a.ab_count - b.ab_count;
      });
      this.drawAbnormal(this.$store.state.selectNor);
    },
    handleIS() {
      this.selectDataType = 'IS';
      this.getdata();
    },
    handleRV() {
      this.selectDataType = 'RV';
      this.getdata();
    },
    drawAbnormal(data) {
      console.log(data);
      $('#abnormal_container').empty();
      const filterId = (data) => {
        return data['x']
      };//获取学号
      const allIds = Array.from(new Set(data.bardata.map(d => filterId(d))));

      const filterDate = (datum) => {
        return datum['time']
      };//获取时间
      const allDate = Array.from(new Set(data.rectInfo.map(d => filterDate(d))));

      //获取画布
      const margin = {top: 5, left: 5, right: 5, bottom: 5};
      const container = d3.select("#abnormal_container")
        .append('svg')
        .attr('id', 'abnormalInfo');

      const svg = d3.select("#abnormalInfo");
      //浏览器的高度
      const client_height = d3.select("#abnormal_container")._groups[0][0].clientHeight - margin.top - margin.bottom;
      //浏览器宽度
      const client_width = d3.select("#abnormal_container")._groups[0][0].clientWidth - margin.left - margin.right;
      const rect_content_width = 32;
      const rect_content_height = 42;
      const temp_width = rect_content_width * allDate.length;
      const temp_height = rect_content_height * allIds.length;

      const width = client_width > temp_width ? client_width : temp_width;
      const height = client_height > temp_height ? client_height : temp_height;
      document.getElementById("abnormalInfo").setAttribute('height', height + 'px');
      document.getElementById("abnormalInfo").setAttribute('width', width + 'px');

      const colorList = ['#e9c46b', '#C07A92', '#287271', '#834026', '#354e87', '#EDDDC3', '#8ab07d', '#e2c3c9', '#E66F51', '#2a9d8c'];


      const g = svg.append("g")
        .attr("id", "maingroup")
        .attr('transform', `translate(${margin.left},${margin.top})`);


      const yscale = d3.scaleBand().domain(allIds).range([height - margin.bottom, margin.top * 19]);
      const xscale = d3.scaleBand().domain(allDate).range([margin.left * 38, width - 4 * margin.right]);
      const rscale = d3.scaleLinear().domain([d3.min(data.rectInfo.map(d => d.value)), d3.max(data.rectInfo.map(d => d.value))]).range([1, 30]);

      const maxRadius = 18; // 最大半径

      const maxmin_scalr = d3.scaleLinear()
        .domain([data.globalMin, data.globalMax])
        .range([2, maxRadius]);

      const anglePadding = 0.2; // 角度间距
      const pie = d3.pie().value(() => 1); // 创建等角度饼图

      //背景色的弧线
      const arc3 = d3.arc()
        .innerRadius(0)
        .outerRadius(18)
        .padAngle(0.08);


      //数据的弧线
      const arc = d3.arc()
        .innerRadius(0)
        .outerRadius(d => maxmin_scalr(d.data))
        .cornerRadius(1)
        .padAngle(anglePadding);

      //是否异常的弧线
      const arc_abnormal = d3.arc()
        .innerRadius(19)
        .outerRadius(21)
        .padAngle(0.1);

      g.append("g")
        .selectAll("g")
        .data(data.rectInfo)
        .join("g")
        .attr("transform", (d, i) => `translate(${xscale(d.time)},${yscale(d.id)})`)
        .attr("stroke", "white")
        .selectAll("path")
        .data(d => pie(d.value))
        .attr("class", "p")
        .join("path")
        .attr("d", arc3)
        .attr("fill", '#d4d4d4');


      g.append("g")
        .selectAll("g")
        .data(data.rectInfo)
        .join("g")
        .attr("transform", (d, i) => `translate(${xscale(d.time)},${yscale(d.id)})`)
        .selectAll("path")
        .data(d => pie(d.value))
        .attr("class", "p")
        .join("path")
        .attr("d", arc)
        .attr("fill", '#483D8B');

      g.append("g")
        .selectAll("g")
        .data(data.rectInfo)
        .join("g")
        .attr("transform", (d, i) => `translate(${xscale(d.time)},${yscale(d.id)})`)
        .selectAll("path")
        .data(d => pie(d.type))
        .attr("class", "p")
        .join("path")
        .attr("d", arc_abnormal)
        .attr("fill", d => {
          return d.data == '0' ? 'white' : '#940410';
        });


      //时间片名称
      g.append("g")
        .selectAll("text")
        .data(allDate)
        .join("text")
        .text(d => 'T' + d.slice(1))
        .attr("x", (d, i) => margin.left * 38 + i * xscale.bandwidth())
        .attr("y", margin.top * 14)
        .style("text-anchor", "middle")
        .attr("font-size", "9pt");

      //学习者名称
      g.append("g")
        .selectAll("text")
        .data(allIds)
        .join("text")
        .text(d => d)
        .attr("x", margin.left * 24)
        .attr("y", (d, i) => margin.top * 19 + i * yscale.bandwidth())
        .style("text-anchor", "middle")
        .attr("font-size", "9pt")
        .attr("font-weight", "bold")
        .attr("fill", (d, i) => {
          return colorList[data.bardata[i].type];
        });

      g.append("g")
        .selectAll("text")
        .data(data.bardata)
        .join("text")
        .text(d => {
          return "【" + d.ab_score + "】";
        })
        .attr("x", margin.left * 18)
        .attr("y", (d, i) => margin.top * 22 + i * yscale.bandwidth())
        .attr("font-size", 12);

      g.append("g")
        .selectAll("text")
        .data(data.bardata)
        .join("text")
        .text(d => {
          return d.ab_count;
        })
        .attr("x", margin.left * 11.5)
        .attr("y", d => yscale(d.x) + 16)
        .attr("font-size", 12);


      //折线图
      const line_height = 25;
      const ylineScale = d3.scaleLinear()
        .domain([d3.min(data.linedata.map(d => d.y)), d3.max(data.linedata.map(d => d.y))]) // 适当设置 Y 轴范围
        .range([line_height, 0]).nice();


      // 创建一个折线生成器
      const line = d3.line()
        .x(d => xscale(d.x))
        .y(d => ylineScale(d.y));

      const area = d3
        .area()
        .curve(d3.curveCardinal.tension(0.95))
        .x(d => xscale(d.x))
        .y0(d => ylineScale(d3.min(data.linedata.map(d => d.y))))
        .y1(d => ylineScale(d.y));

      // 添加 X 轴
      g.append("g")
        .attr('transform', `translate(${-5 * margin.left},${11 * margin.top})`)
        .call(d3.axisBottom(xscale).ticks(2).tickSize(0).tickFormat(""))
        .selectAll(".domain")
        .attr("stroke", '#AFABAB')
        .attr("stroke-width", 2);

      // 添加 Y 轴
      g.append("g")
        .attr('transform', `translate(${37.8 * margin.left},${margin.top * 6})`)
        .call(d3.axisLeft(ylineScale).ticks(2).tickSize(0).tickFormat(""))
        .selectAll(".domain")
        .attr("stroke", '#AFABAB')
        .attr("stroke-width", 2);


      g.append("g")
        .attr('transform', `translate(${0.3 * margin.left},${6 * margin.top})`)
        .append("path")
        .datum(data.linedata)
        .attr("fill", "none")
        .attr("stroke", "#96BDE6")
        .attr("stroke-width", 2)
        .attr("d", line);

      g.append("g")
        .attr('transform', `translate(${0.25 * margin.left},${6 * margin.top})`)
        .append("path")
        .datum(data.linedata)
        .style("fill", "#A5C7EA")
        .attr("opacity", 0.7)
        .style("stroke", "none")
        .attr("d", d => area(d));

      g.append("g")
        .selectAll("circle")
        .data(data.linedata)
        .join("circle")
        .attr("cx", d => xscale(d.x))
        .attr("cy", d => ylineScale(d.y) + 6 * margin.top)
        .attr("r", 3)
        .attr("fill", 'white')
        .style("stroke", '#96BDE6');

      const dropX = width / 3;
      const dropY = height / 2;
      // 创建水滴形状的路径
      const dropPath = "M" + dropX + "," + (dropY - 40) + " " + // 顶点
        "C" + (dropX + 35) + "," + (dropY - 70) + " " + // 第一个控制点
        (dropX - 35) + "," + (dropY - 70) + " " + // 第二个控制点
        dropX + "," + (dropY - 40) + "Z"; // 结束点

      // 获取最大值
      const maxValue = Math.max(...data.linedata.map(point => point.y));
      const maxPoint = data.linedata.find(point => point.y === maxValue);

      // 获取最小值
      const minValue = Math.min(...data.linedata.map(point => point.y));
      const minPoint = data.linedata.find(point => point.y === minValue);

      // 创建最大值的水滴形状的气泡
      g.append("g")
        .attr("transform", `translate(${-margin.left * 73.2 + xscale(maxPoint.x)},${-ylineScale(maxPoint.y) - 1209 * margin.top})`)
        .append("path")
        .attr("d", dropPath)
        .style("fill", "#A5C7EA")
        .style("stroke", "#96BDE6");


      g.append("g")
        .append("text")
        .attr("x", xscale(maxPoint.x) - 2 * margin.left)
        .attr("y", ylineScale(maxPoint.y) + 3 * margin.top)
        .attr("font-size", "8")
        .text(maxValue);

      // 创建最小值的水滴形状的气泡
      g.append("g")
        .attr("transform", `translate(${xscale(minPoint.x) - margin.left * 73.2},${ylineScale(minPoint.y) - 1209 * margin.top})`)
        .append("path")
        .attr("d", dropPath)
        .style("fill", "#A5C7EA")
        .style("stroke", "#96BDE6");

      g.append("g")
        .append("text")
        .attr("x", xscale(minPoint.x) - 2 * margin.left)
        .attr("y", ylineScale(minPoint.y) + 3 * margin.top)
        .attr("font-size", "8")
        .text(minValue);


      //左侧柱状图
      const barscale = d3.scaleLinear()
        .domain([d3.min(data.bardata.map(d => d.ab_count)), d3.max(data.bardata.map(d => d.ab_count))])
        .range([2, 70]);

      g.append("g")
        .append("line")
        .attr("x1", margin.left * 15)
        .attr("y1", margin.top * 15)
        .attr("x2", margin.left * 15)
        .attr("y2", height - 3 * margin.bottom)
        .attr("stroke", '#AFABAB')
        .attr("stroke-width", 2);

      g.append("g")
        .selectAll("rect")
        .data(data.bardata)
        .join("rect")
        .attr("x", d => margin.left * 15 - barscale(d.ab_count))
        .attr("y", d => yscale(d.x) - yscale.bandwidth() / 4)
        .attr("rx", 3)
        .attr("ry", 3)
        .attr("width", d => {
          return barscale(d.ab_count);
        })
        .attr("height", 13)
        .style("fill", '#AFABAB');


      g.append("g")
        .append("text")
        .attr("x", 19 * margin.left)
        .attr("y", 12 * margin.top)
        .attr("font-size", "12")
        .attr("font-weight", "bold")
        .text('Number');

      g.append("g")
        .append("text")
        .attr("x", 18 * margin.left)
        .attr("y", 15 * margin.top)
        .attr("font-size", "12")
        .text('【score】');

      g.append("g")
        .append("text")
        .attr("x", margin.left)
        .attr("y", 14 * margin.top)
        .attr("font-size", "12")
        .attr("font-weight", "bold")
        .text('Total Count');

      g.append("g")
        .append("text")
        .attr("x", 14 * margin.left)
        .attr("y", 8.3 * margin.top)
        .attr("font-size", "10")
        .text('Value');

      g.append("g")
        .append("text")
        .attr("x", 4.8 * margin.left)
        .attr("y", 5 * margin.top)
        .attr("font-size", "10")
        .text('Low');

      g.append("g")
        .append("text")
        .attr("x", 24 * margin.left)
        .attr("y", 2 * margin.top)
        .attr("font-size", "10")
        .text('High');

      g.append("g")
        .append("rect")
        .attr("x", 3 * margin.left)
        .attr("y", -margin.top / 2)
        .attr("rx", 6)
        .attr("ry", 6)
        .attr("width", 135)
        .attr("height", 48)
        .attr("fill", 'none')
        .attr("stroke", "gray")
        .attr("stroke-dasharray", 2);

      function generateLegendData(count) {
        const legend_Data = [];
        let value = 2;
        for (let i = 0; i < count; i++) {
          legend_Data.push(value);
          value += 2;
        }
        return legend_Data;
      }

      const numberOfLegend = 6;
      const legend_Data = generateLegendData(numberOfLegend);

      const legend_outerRadius = 20;
      const legend_innerRadius = 0;
      const legend_startAngle = -Math.PI / 6;
      const legend_endAngle = Math.PI / 6;

      const legend__rscale = d3.scaleLinear().domain([d3.min(legend_Data), d3.max(legend_Data)]).range([legend_innerRadius, legend_outerRadius]);

      const arc_legend = d3.arc()
        .innerRadius(legend_innerRadius)
        .outerRadius(d => {
          return legend__rscale(d);
        })
        .startAngle(legend_startAngle)
        .endAngle(legend_endAngle);

      g.append("g")
        .selectAll("path")
        .data(legend_Data)
        .join("path")
        .attr("transform", (d, i) => `translate(${10 + i * 24},${32})`)
        .attr("d", arc_legend)
        .attr("fill", "#483D8B");


    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
div#abnormal_container {
  height: 329px;
  width: 1106px;
  overflow-y: auto;
  overflow-x: hidden;
}

</style>
