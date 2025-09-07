<template>
  <div class="content">
    <Card :bordered="false" class="myCard">
      <p slot="title" style="text-align: left;  margin-top: 3px;">Pattern Overview</p>
      <div>
        <Button @click="rankNormalByAscending" icon="ios-trending-up"
                style="color: black; font-size: 13px; padding: 0px 0px; width: 20px; height: 20px; position: absolute; top: 10px; left: 140px;"></Button>
        <Button @click="rankNormalByDescending" icon="ios-trending-down"
                style="color: black; font-size: 13px; padding: 0px 0px; width: 20px; height: 20px; position: absolute; top: 10px; left: 165px;"></Button>
      </div>
      <div>
        <Button @click="rankAbnormalByAscending" icon="ios-trending-up"
                style="color: black; font-size: 13px; padding: 0px 0px; width: 20px; height: 20px; position: absolute; top: 10px; left: 210px;"></Button>
        <Button @click="rankAbnormalByDescending" icon="ios-trending-down"
                style="color: black; font-size: 13px; padding: 0px 0px; width: 20px; height: 20px; position: absolute; top: 10px; left: 235px;"></Button>
      </div>
      <div id="overview_container"></div>
    </Card>
  </div>
</template>
<script>
import axios from "axios";

export default {
  name: 'patternoverview',
  data() {
    return {
      base_url: 'http://127.0.0.1:8420/'
    }
  },
  watch: {},
  computed: {},
  created() {
  },
  mounted() {
    this.getPatternoverdata();
  },
  methods: {
    getPatternoverdata() {
      axios.get(this.base_url + 'getPatternOverview')
        .then(res => {
          this.drawFeature(res.data);
          this.$store.state.selectPat = res.data;
        });
    },
    rankNormalByAscending() {
      this.$store.state.selectPat.patternList.sort(function (a, b) {
        return b.value[0] - a.value[0]; // 从大到小排序
      });
      this.drawFeature(this.$store.state.selectPat);
    },
    rankNormalByDescending() {
      this.$store.state.selectPat.patternList.sort(function (a, b) {
        return a.value[0] - b.value[0]; // 从大到小排序
      });
      this.drawFeature(this.$store.state.selectPat);
    },
    rankAbnormalByAscending() {
      this.$store.state.selectPat.patternList.sort(function (a, b) {
        return b.value[1] - a.value[1]; // 从大到小排序
      });
      this.drawFeature(this.$store.state.selectPat);
    },
    rankAbnormalByDescending() {
      this.$store.state.selectPat.patternList.sort(function (a, b) {
        return a.value[1] - b.value[1]; // 从大到小排序
      });
      this.drawFeature(this.$store.state.selectPat);
    },
    handleContainerScroll() {
      // 获取画布容器和跟随的div元素的引用
      const container = this.$refs.overview_container;
      const followingDiv = this.$refs.followingDiv;

      // 获取当前画布容器的滚动位置
      const scrollTop = container.scrollTop;
      const scrollLeft = container.scrollLeft;

      // 根据滚动位置调整followingDiv元素的位置
      followingDiv.style.top = (20 + scrollTop) + 'px';
      followingDiv.style.left = (20 + scrollLeft) + 'px';
    },
    drawFeature(data) {
      console.log(data);
      $("#overview_container").empty();
      //获取画布
      const margin = {top: 5, left: 5, right: 5, bottom: 5};
      const container = d3.select("#overview_container")
        .append('svg')
        .attr('id', 'overviewInfo');

      const svg = d3.select("#overviewInfo");
      const height = 545 + 35.14 * data.total - margin.top - margin.bottom;
      const width = d3.select("#overviewInfo")._groups[0][0].clientWidth;
      const g = svg.append("g")
        .attr("id", "maingroup")
        .attr('transform', `translate(${margin.left},${margin.top})`);

      let containerA = document.getElementById("overviewInfo").setAttribute('height', height + 'px');

      g.append("g")
        .append("text")
        .attr("x", margin.left * 2)
        .attr("y", margin.top * 5)
        .attr("font-size", 14)
        .text('Number of patterns: ');

      g.append("g")
        .append("text")
        .attr("x", margin.left * 2 + 130)
        .attr("y", margin.top * 5)
        .attr("font-size", 14)
        .attr("font-weight", "bold")
        .text(data.total);


      // const Piecolor = ["#A9D18E", "#9DC3E6"];
      const Piecolor = ["#62B197", "#E18E6D"];

      //图例
      g.append("g")
        .append("rect")
        .attr("x", 10)
        .attr("y", 43)
        .attr("width", 25)
        .attr("height", 10)
        .attr("fill", Piecolor[0]);

      g.append("g")
        .append("text")
        .attr("x", 38)
        .attr("y", 53)
        .attr("font-size", 12)
        .text("Normal");

      g.append("g")
        .append("rect")
        .attr("x", 90)
        .attr("y", 43)
        .attr("width", 25)
        .attr("height", 10)
        .attr("fill", Piecolor[1]);

      g.append("g")
        .append("text")
        .attr("x", 118)
        .attr("y", 53)
        .attr("font-size", 12)
        .text("Abnormal");


      const startAngle = 0;
      const endAngle = 7;
      const pie = d3.pie().value(d => d.value)
        .startAngle(startAngle)
        .endAngle(endAngle);

      const arcs = pie(data.ratio);

      const PieRadius = 24;
      const arc = d3.arc()
        .innerRadius(0)
        .outerRadius(PieRadius);

      const arcOuter = d3.arc()
        .innerRadius(PieRadius + 2)
        .outerRadius(PieRadius + 6);

      const arcLabel = d3.arc().innerRadius(0).outerRadius(PieRadius);

      g.append("g")
        .attr("transform", d => `translate(${width - 12 * margin.right},${margin.top * 6.5})`)
        .selectAll("path")
        .data(arcs)
        .enter()
        .append("path")
        .attr("fill", (d, i) => Piecolor[i])
        .attr("stroke", "white")
        .attr("d", arc);

      g.append("g")
        .attr("transform", d => `translate(${width - 12 * margin.right},${margin.top * 6.5})`)
        .selectAll("path")
        .data(arcs)
        .enter()
        .append("path")
        .attr("fill", (d, i) => Piecolor[i])
        .attr("stroke", "white")
        .attr("opacity", '0.6')
        .attr("d", arcOuter);

      g.append("g")
        .attr("transform", d => `translate(${width - 12 * margin.right},${margin.top * 5.5})`)
        .attr("font-family", "sans-serif")
        .attr("font-size", 10)
        .attr("text-anchor", "middle")
        .selectAll("text")
        .data(arcs)
        .join("text")
        .attr("transform", d => `translate(${arcLabel.centroid(d)})`)
        .call(text => text.append("tspan")
          .attr("x", 0)
          .attr("y", "0.7em")
          .attr("fill-opacity", 1)
          .text(d => d.value.toFixed(2).toLocaleString() + "%"));

      var stu_gap = 10;
      var stu_content = 26;
      // 定义箭头
      g.append("defs").append("marker")
        .attr("id", "arrow")
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 5)
        .attr("refY", 0)
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("orient", "auto")
        .append("path")
        .attr("d", "M0,-5L10,0L0,5");

      // 定义直线的起点和终点
      var x_lineData = [{x: margin.left * 10, y: margin.top * 15}, {
        x: width - margin.left - 5 * margin.right,
        y: margin.top * 15
      }];

      // 创建直线
      var line = d3.line()
        .x(function (d) {
          return d.x;
        })
        .y(function (d) {
          return d.y;
        });

      g.append("path")
        .data([x_lineData])
        .attr("d", line)
        .attr("stroke", "black")
        .attr("stroke-width", 1)
        .attr("fill", "none")
        .attr("marker-end", "url(#arrow)");
      var y_lineData = [{x: margin.left * 10, y: margin.top * 15}, {
        x: margin.left * 10,
        y: stu_gap + margin.top * 15 + (stu_gap + stu_content) * data.patternList.length
      }];
      g.append("path")
        .data([y_lineData])
        .attr("d", line)
        .attr("stroke", "black")
        .attr("stroke-width", 1)
        .attr("fill", "none")
        .attr("marker-end", "url(#arrow)");

      //灰色背景
      var bar_width = width - margin.left - 16 * margin.right;
      g.append("g")
        .selectAll("rect")
        .data(data.patternList)
        .join("rect")
        .attr("x", margin.left * 10.2)
        .attr("y", (d, i) => stu_gap + margin.top * 15 + i * (stu_content + stu_gap))
        .attr("width", bar_width)
        .attr("height", stu_content)
        .attr("fill", '#F2F2F2');

      //模式名称
      g.append("g")
        .selectAll("text")
        .data(data.patternList)
        .join("text")
        .attr("x", margin.left * 1.5)
        .attr("y", (d, i) => stu_gap + margin.top * 15 + (i + 0.5) * (stu_content + stu_gap))
        .text(d => d.name)
        .attr("font-size", 10);

      //堆叠柱状
      var stu_bar = 14;
      var rscale = d3.scaleLinear().domain([0, data.patternMax]).range([0, bar_width]);
      g.append("g")
        .selectAll(null)
        .data(data.patternList)
        .join((enter) => {
          let enterg = enter.append("g")
            .attr("transform", `translate(${margin.left},${23})`);

          enterg.append("rect")
            .attr("x", d => margin.left * 9.1)
            .attr("y", (d, i) => stu_gap + margin.top * 15 + i * (stu_content + stu_gap) - 2.8 * (stu_content - stu_bar) / 2)
            .attr("width", d => rscale(d.value[0]))
            .attr("height", stu_bar)
            .attr("fill", Piecolor[0]);

          enterg.append("rect")
            .attr("x", d => margin.left * 9.1 + rscale(d.value[0]))
            .attr("y", (d, i) => stu_gap + margin.top * 15 + i * (stu_content + stu_gap) - 2.8 * (stu_content - stu_bar) / 2)
            .attr("width", d => rscale(d.value[1]))
            .attr("height", stu_bar)
            .attr("fill", Piecolor[1]);
        });
    }
  }
}
</script>

<style>
div#overview_container {
  height: 536px;
  width: 275px;
  overflow-y: auto;
  overflow-x: hidden;

}

svg#overviewInfo {
  width: 270px;
}

.ivu-card-body {
  padding: 1px;
}
</style>
