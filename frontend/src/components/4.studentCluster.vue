<template>
  <div class="content">
    <Card :bordered="false" class="myCard">
      <p slot="title" style="text-align: left; margin-top: 3px;">Learner Profile
        <span style="margin-left: 20px; font-weight: normal;">Grade:</span>
        <Select v-model="selectClass" style="width:60px" size="small">
          <Option v-for="item in classList" :value="item.value" :key="item.value">{{ item.label }}</Option>
        </Select>
      </p>
      <div style="margin-left: 5px;">
        <span>X-axis:</span>
        <Select v-model="selectXaxis" @on-change="selectX()" style="width:80px" size="small">
          <Option v-for="item in variableList" :value="item.value" :key="item.value">{{ item.label }}</Option>
        </Select>
        <span style="margin-left: 4px;">Y-axis:</span>
        <Select v-model="selectYaxis" @on-change="selectY()" style="width:80px" size="small">
          <Option v-for="item in variableList" :value="item.value" :key="item.value">{{ item.label }}</Option>
        </Select>
      </div>
      <div id="cluster_container"></div>
    </Card>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'studentcluster',
  data() {
    return {
      base_url: 'http://127.0.0.1:8420/',
      classList: [
        {
          value: 'G1',
          label: 'G1'
        },
        {
          value: 'G2',
          label: 'G2'
        },
        {
          value: 'G3',
          label: 'G3'
        }
      ],
      selectClass: 'G1',
      variableList: [
        {
          value: 'CR',
          label: 'Correct'
        },
        {
          value: 'ER',
          label: 'Error'
        },
        {
          value: 'TS',
          label: 'Total submissions'
        },
        {
          value: 'EQ',
          label: 'Easy questions'
        },
        {
          value: 'MQ',
          label: 'Medium questions'
        },
        {
          value: 'HQ',
          label: 'Hard questions'
        }
      ],
      selectXaxis: 'TS',
      selectYaxis: 'CR'
    }
  },
  watch: {},
  computed: {},
  created() {
  },
  mounted() {
    this.getClusterData();
  },
  methods: {
    getClusterData() {
      axios.get(this.base_url + 'getCluster/?selectX=' + this.selectXaxis + '&selectY=' + this.selectYaxis)
        .then(res => {
          this.drawCluster(res.data);

        });
    },
    selectX() {
      this.getClusterData();
    },
    selectY() {
      this.getClusterData();
    },
    drawCluster(data) {
      $('#cluster_container').empty();

      //获取画布
      const margin = {top: 8, left: 4, right: 5, bottom: 5};
      const container = d3.select("#cluster_container")
        .append('svg')
        .attr('id', 'clusterInfo');

      const svg = d3.select("#clusterInfo");
      const height = d3.select("#cluster_container")._groups[0][0].clientHeight - 7 * margin.top;
      const width = d3.select("#clusterInfo")._groups[0][0].clientWidth - 5 * margin.left;
      const g = svg.append("g")
        .attr("id", "maingroup")
        .attr('transform', `translate(${margin.left},${margin.top})`);

      var xValues = data.clusterInfo.map(function (d) {
        return d.x;
      });
      var yValues = data.clusterInfo.map(function (d) {
        return d.y;
      });

      var scatter_xScale = d3.scaleLinear()
        .domain([d3.min(xValues), d3.max(xValues)])
        .range([10 * margin.left, width])
        .nice();

      var scatter_yScale = d3.scaleLinear()
        .domain([d3.min(yValues), d3.max(yValues)])
        .range([height, margin.top * 5])
        .nice();

      const colorList = ['#e9c46b', '#C07A92', '#287271', '#834026', '#354e87', '#EDDDC3', '#8ab07d', '#e2c3c9', '#E66F51', '#2a9d8c'];

      const scatter_xAxis = d3.axisBottom(scatter_xScale);
      const scatter_yAxis = d3.axisLeft(scatter_yScale);


      const circles = g.selectAll("circle")
        .data(data.clusterInfo)
        .enter()
        .append("circle")
        .attr("class",d=>'cluster'+d.cluster)
        .attr("cx", d => scatter_xScale(d.x))
        .attr("cy", d => scatter_yScale(d.y))
        .attr("r", 3.5)
        .attr("fill", d => colorList[d.cluster])
        .attr("opacity", '0.7');

      const xAxis = d3
        .axisBottom()
        .scale(scatter_xScale)
        .ticks(8);

      const yAxis = d3
        .axisLeft()
        .scale(scatter_yScale)
        .ticks(10);

      g.append('g')
        .attr('transform', `translate(0,${height})`)
        .call(xAxis);

      g.append('g')
        .attr('transform', `translate(${10 * margin.left}, 0)`)
        .call(yAxis);

      g.append("g")
        .append("text")
        .attr("x", width / 3)
        .attr("y", height + 4 * margin.top)
        .text(data.xname)
        .attr("font-size", 12)
        .attr("font-weight", 'bold');

      g.append("g")
        .attr("transform", `translate(${2 * margin.left},${height / 4 * 2.8}) rotate(-90)`)
        .append("text")
        .text(data.yname)
        .attr("font-size", 12)
        .attr("font-weight", 'bold');


      //图例
      const legend_data = new Set(data.clusterInfo.map(d => d.cluster));

      const legend_array = Array.from(legend_data);
      legend_array.sort((a, b) => a - b);

      g.append("g")
        .append("rect")
        .attr("x", 15 * margin.left)
        .attr("y", margin.top)
        .attr("fill", 'none')
        .attr("stroke", 'gray')
        .attr("width", legend_data.size * 38)
        .attr("height", 20)
        .attr("stroke-width", 1)
        .attr("rx", 4)
        .attr("ry", 4)
        .attr("stroke-dasharray", 2);

      g.append("g")
        .selectAll("text")
        .data(legend_array)
        .enter()
        .append("text")
        .attr("x", (d, i) => 15 * margin.left + 24 + i * 30)
        .attr("y", margin.top + 13)
        .attr("font-size", '8px')
        .style("cursor", "pointer")
        .text(d=>{
          if((d+1)==legend_array.length)
            return 'Abnormal';
          else
             return 'C' + d;
        })
        .on("click", (event, d, i) => {
          // 点击时高亮当前类，其他类减淡至15%
          d3.selectAll(".cluster"+d).attr("opacity",1);
          legend_array.forEach(cluster => {
            if(cluster !== d) {
              d3.selectAll(".cluster"+cluster).attr("opacity",0.0001);
            }
          });
        })
        .on("dblclick", (event, d, i) => {
          // 双击恢复所有类的原始状态
          d3.selectAll("circle").attr("opacity",0.7);
        });

      g.append("g")
        .selectAll("circle")
        .data(legend_array)
        .enter()
        .append("circle")
        .attr("class",d=>'cluster'+d.cluster)
        .attr("cx", (d, i) => 15 * margin.left + 16 + i * 30)
        .attr("cy", margin.top + 10)
        .attr("r", 4)
        .attr("fill", d => colorList[d])
        .attr("font-size", '8px')
        .on("click", (event, d, i) => {
          // 点击时高亮当前类，其他类减淡至30%
          d3.selectAll(".cluster"+d).attr("opacity",1);
          legend_array.forEach(cluster => {
            if(cluster !== d) {
              d3.selectAll(".cluster"+cluster).attr("opacity",0.3);
            }
          });
        })
        .on("dblclick", (event, d, i) => {
          // 双击恢复所有类的原始状态
          d3.selectAll("circle").attr("opacity",0.7);
        });

      g.append("g")
        .append("line")
        .attr("x1", 5 * margin.left + width / 2)
        .attr("y1", margin.top * 5)
        .attr("x2", 5 * margin.left + width / 2)
        .attr("y2", height + margin.top * 0.2)
        .attr("stroke", 'gray')
        .attr("stroke-dasharray", 4);

      g.append("g")
        .append("line")
        .attr("x1", 10 * margin.left)
        .attr("y1", height / 2 + margin.top * 2.5)
        .attr("x2", width)
        .attr("y2", height / 2 + margin.top * 2.5)
        .attr("stroke", 'gray')
        .attr("stroke-dasharray", 4);
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
div#cluster_container {
  height: 307px;
  width: 275px;
  overflow-y: auto;
  overflow-x: hidden;
}

svg#clusterInfo {
  height: 294px;
  width: 275px;
}

.ivu-select-small.ivu-select-single .ivu-select-selection {
  height: 20px;
}

.ivu-select-small.ivu-select-single .ivu-select-selection .ivu-select-placeholder, .ivu-select-small.ivu-select-single .ivu-select-selection .ivu-select-selected-value {
  height: 22px;
  font-weight: normal;
}
</style>
