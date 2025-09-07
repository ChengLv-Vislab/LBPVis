<template>
  <div class="content">
    <Card :bordered="false" class="myCard">
      <p slot="title" style="text-align: left;  margin-top: 3px;">Patter Explore</p>
      <div id="explore_container"></div>
    </Card>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: 'patternexplore',
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
    this.getPatternexploredata();
  },
  methods: {
    getPatternexploredata() {
      axios.get(this.base_url + 'getPatternExplore/')
        .then(res => {
          console.log(res.data);
          this.drawExplore(res.data);
        });
    },
    drawExplore(data) {
      //获取画布
      const margin = {top: 5, left: 2, right: 5, bottom: 5};
      const container = d3.select("#explore_container")
        .append('svg')
        .attr('id', 'exploreInfo');

      const svg = d3.select("#exploreInfo");
      const height = d3.select("#explore_container")._groups[0][0].clientHeight - margin.top - margin.bottom;
      const width = d3.select("#exploreInfo")._groups[0][0].clientWidth;

      const g = svg.append("g")
        .attr("id", "maingroup")
        .attr('transform', `translate(${margin.left},${margin.top})`);

      //中间矩形大小
      const pat_rect_width = 28;
      const pat_rect_height = 28;
      const pat_each_row = 26;
      const pat_margin_top = 50;
      const pat_middle = (data.PatList.length / pat_each_row * pat_rect_height) / 2 - 10;

      const pat_rscale = d3.scaleLinear().domain([d3.min(data.PatList.map(d => d.value)), d3.max(data.PatList.map(d => d.value))]).range(['#c4cfd9', '#004c6d']);

      // const pat_rscale = d3.scaleLinear().domain([d3.min(data.PatList.map(d => d.value)), d3.max(data.PatList.map(d => d.value))]).range(['#BFD9EC', '#094285']);

      // const pat_rscale = d3.scaleSequential()
      // .interpolator(d3.interpolateBlues)
      // .domain([d3.min(data.PatList.map(d => d.value))-0.3, d3.max(data.PatList.map(d => d.value))]);

      const detail_rect_width = 30;
      const detail_rect_height = 30;
      const detail_rect_margin_top = 4;

      var border_y_array = [];
      var border_y_height = [];
      var border_y = 4 * margin.top;
      var before_border_y = 0;
      var stu_each_row = 23;
      var stu_rect_height = 20;
      var stu_margin_border = 5;

      var total_margin_left = 43 * margin.left;
      const stu_r_scale = d3.scaleLinear().domain([0, data.max_occurence]).range([0,12]);


      // 使用line生成器创建曲线函数
      var line = d3.line()
        .x(function (d) {
          return d.x;
        })
        .y(function (d) {
          return d.y;
        })
        .curve(d3.curveBasis); // 使用贝塞尔曲线插值

      g.append("g")
        .append("text")
        .attr("x", margin.left * 10 + (pat_each_row / 2) * pat_rect_width)
        .attr("y", pat_margin_top + margin.top * 2)
        .attr("font-weight", "bold")
        .text("Learning Behavior Patterns");

      g.append("g")
        .selectAll("rect")
        .data(data.PatList)
        .join("rect")
        .attr("x", (d, i) => total_margin_left + (i % pat_each_row) * (pat_rect_width + 2))
        .attr("y", (d, i) => pat_margin_top + 4 * margin.top + Math.floor(i / pat_each_row) * (pat_rect_height + 2))
        .attr("rx", 2)
        .attr("ry", 2)
        .attr("class", "pat")
        .attr("width", pat_rect_width)
        .attr("height", pat_rect_height)
        .attr("fill", d => pat_rscale(d.value))
        .attr("stroke", "white")
        .attr("stroke-width", 2)
        .on("click", function (event, element) {

          d3.selectAll(".pat").attr("stroke", "white");

          d3.select(this)
            .attr("stroke", '#800000')
            .attr("stroke-width", 4);

          d3.selectAll(".patborder").remove();
          d3.selectAll(".patdetail").remove();
          d3.selectAll(".pat_line").remove();
          d3.selectAll(".stu_line").remove();
          d3.selectAll(".pat_circle").remove();
          d3.selectAll(".eventname").remove();
          d3.selectAll(".patname_Rect").remove();
          d3.selectAll(".patname").remove();
          d3.selectAll(".patname_x").remove();

          //选择的模式名称
          g.append("g")
            .append("text")
            .attr("class", "patname_x")
            .attr("x", 80)
            .attr("y", 20)
            .text('Selected Pattern:');

          g.append("g")
            .append("rect")
            .attr("class", "patname_Rect")
            .attr("x", 195)
            .attr("y", 0)
            .attr("rx", 6)
            .attr("ry", 6)
            .attr("width", element.name.length * 9)
            .attr("height", 23)
            .attr("opacity", 0.4)
            .attr("stroke", "#A9A9A9")
            .attr("fill", "#DCDCDC");

          g.append("g")
            .append("text")
            .attr("class", "patname")
            .attr("x", 199)
            .attr("y", 16)
            .attr("font-weight", "bold")
            .text(element.name);

          g.append("g")
            .append("text")
            .attr("class", "patname")
            .attr("x", 118)
            .attr("y", 40)
            .text('Frequency:');

          g.append("g")
            .append("text")
            .attr("class", "patname")
            .attr("x", 192)
            .attr("y", 41)
            .attr("font-weight", "bold")
            .text(element.value);


          //大边框
          g.append("g")
            .append("rect")
            .attr("class", "patborder")
            .attr("x", margin.left * 5)
            .attr("y", pat_margin_top + pat_middle + 8 * margin.top - 2)
            .attr("width", detail_rect_width + 8)
            .attr("height", 4 + (detail_rect_height + detail_rect_margin_top) * element.detail.length)
            .attr("rx", 4)
            .attr("ry", 4)
            .attr("fill", 'none')
            .attr("stroke", "#252525");

          //边框里的元素
          g.append("g")
            .selectAll("rect")
            .data(element.detail)
            .join("rect")
            .attr("class", "patdetail")
            .attr("x", margin.left * 7)
            .attr("y", (d, i) => pat_margin_top + pat_middle + 8.4 * margin.top + i * (detail_rect_height + detail_rect_margin_top))
            .attr("fill", '#96B6D8')
            .attr("width", detail_rect_width)
            .attr("height", detail_rect_height);


          //事件的具体编号
          g.append("g")
            .selectAll("text")
            .data(element.detail)
            .join("text")
            .attr("class", "patdetail")
            .attr("x", d => +d.name < 10 ? margin.left * 12 : margin.left * 10)
            .attr("y", (d, i) => pat_margin_top + pat_middle + 12.4 * margin.top + i * (detail_rect_height + detail_rect_margin_top))
            .text(d => d.name);

          g.append("g")
            .append("text")
            .attr("class", "eventname")
            .attr("x", margin.left * 5)
            .attr("y", pat_margin_top + pat_middle + margin.top * 3)
            .attr("font-weight", "bold")
            .attr("font-size", 12)
            .text("Event");

          g.append("g")
            .append("text")
            .attr("class", "eventname")
            .attr("x", margin.left * 2)
            .attr("y", pat_margin_top + pat_middle + margin.top * 6)
            .attr("font-weight", "bold")
            .attr("font-size", 12)
            .text("Sequence");

          // 给定起始点和结束点
          var startPoint = {
            x: total_margin_left,
            y: pat_margin_top + 4 * margin.top + (pat_rect_height + 2) * (Math.floor(element.id / pat_each_row) + 0.5)
          };
          var endPoint = {
            x: margin.left * 6 + detail_rect_width + 8,
            y: pat_margin_top + pat_middle + (detail_rect_height + detail_rect_margin_top) * (element.detail.length / 2 + 1)
          };

          g.append("g")
            .append("path")
            .attr("class", "pat_line")
            .attr("d", line([startPoint, {
              x: (startPoint.x + endPoint.x) / 2,
              y: startPoint.y
            }, {x: (startPoint.x + endPoint.x) / 2, y: endPoint.y}, endPoint]))
            .attr("stroke", "#d9d9d9")
            .attr("stroke-width", 2)
            .attr("fill", "none");

          g.append("g")
            .append("circle")
            .attr("class", "pat_circle")
            .attr("cx", startPoint.x - 3)
            .attr("cy", startPoint.y)
            .attr("r", 4)
            .attr("fill", "#bdbdbd");

          g.append("g")
            .append("circle")
            .attr("class", "pat_circle")
            .attr("cx", endPoint.x + 3)
            .attr("cy", endPoint.y)
            .attr("r", 4)
            .attr("fill", "#bdbdbd");

          //高亮学习者
          d3.selectAll('.stu_circle').attr("opacity", 0.1);
          d3.selectAll('.stu_rect').attr("opacity", 0.1);
          d3.selectAll('.stu_rect_width').attr("opacity", 0.1).attr("width", 0);


          element.stulist.forEach(function (d) {
            d3.selectAll('.stu_' + d.name).attr("opacity", 1);
            d3.selectAll('.stu_rect_width.x'+d.name)
              .attr("opacity", 1)
              .attr("width", stu_r_scale(d.value));

          });


          //绘制连线
          for (var k = 0; k < element.clusterlist.length; k++) {
            //获取第几簇
            var cluster_num = element.clusterlist[k].slice(1);
            //计算终点坐标

            var startPoint_stu = {
              x: total_margin_left - 2 + pat_each_row * (pat_rect_width + 2),
              y: 14 * margin.top + (pat_rect_height + 2) * (Math.floor(element.id / pat_each_row) + 0.5)
            };
            var endPoint_stu = {
              x: pat_each_row * pat_rect_width + total_margin_left + 105 - 0.5,
              y: border_y_array[cluster_num - 1] + border_y_height[cluster_num - 1] / 2 + margin.top * 4
            };

            g.append("g")
              .append("path")
              .attr("class", "stu_line")
              .attr("d", line([startPoint_stu, {
                x: (startPoint_stu.x + endPoint_stu.x) / 2,
                y: startPoint_stu.y
              }, {x: (startPoint_stu.x + endPoint_stu.x) / 2, y: endPoint_stu.y}, endPoint_stu]))
              .attr("stroke", "#d9d9d9")
              .attr("stroke-width", 2)
              .attr("fill", "none");

            g.append("g")
              .append("circle")
              .attr("class", "pat_circle")
              .attr("cx", startPoint_stu.x + 3)
              .attr("cy", startPoint_stu.y)
              .attr("r", 4)
              .attr("fill", "#bdbdbd");

            g.append("g")
              .append("circle")
              .attr("class", "pat_circle")
              .attr("cx", endPoint_stu.x - 5)
              .attr("cy", endPoint_stu.y)
              .attr("r", 4)
              .attr("fill", "#bdbdbd");

          }

        });

      // 矩形内部白色的背景边框
      g.append("g")
        .selectAll("rect")
        .data(data.PatList)
        .join("rect")
        .attr("x", (d, i) => 30 * margin.left + (i % pat_each_row) * (pat_rect_width + 2) + 28)
        .attr("y", (d, i) => 6 * margin.top + Math.floor(i / pat_each_row) * (pat_rect_height + 2) + 42)
        .attr("class", "pat")
        .attr("stroke", "white")
        .attr("stroke-width", 1)
        .attr("width", pat_rect_width - 7)
        .attr("height", pat_rect_height - 7)
        .attr("fill", 'white');


      //右侧学习者分组子视图
      //边框
      // const colorList = ['#2a9d8c', '#C07A92', '#e9c46b', '#834026', '#287271', '#EDDDC3', '#8ab07d', '#e2c3c9', '#E66F51', '#354e87'];
      const colorList = ['#e9c46b', '#C07A92', '#287271', '#834026', '#354e87', '#EDDDC3', '#8ab07d', '#e2c3c9', '#E66F51', '#2a9d8c'];

      var title_name_height = 20;
      g.append("g")
        .append("text")
        .attr("x", pat_each_row * (pat_rect_width + 2) + stu_each_row * stu_rect_height * 0.8)
        .attr("y", margin.top * 3)
        .attr("font-weight", "bold")
        .attr("font-size", 12)
        .text("Cluster");

      for (var i = 0; i < data.cluster.length; i++) {
        // 绘制大边框
        before_border_y = border_y;
        var num_ele = data.cluster[i].stuInfo.length;
        border_y = border_y + Math.ceil(num_ele / stu_each_row) * stu_rect_height + 9 + 2 * stu_margin_border + title_name_height;

        border_y_array.push(before_border_y);
        border_y_height.push(Math.ceil(data.cluster[i].stuInfo.length / stu_each_row) * stu_rect_height + 2 * stu_margin_border);
        g.append("g")
          .append("rect")
          .attr("x", pat_each_row * pat_rect_width + total_margin_left + 105)
          .attr("y", function () {
            if (i == 0) {
              return title_name_height + before_border_y;
            } else {
              return title_name_height + before_border_y;
            }
          })
          .attr("width", stu_each_row * stu_rect_height + 2 * stu_margin_border)
          .attr("height", Math.ceil(data.cluster[i].stuInfo.length / stu_each_row) * stu_rect_height + 2 * stu_margin_border)
          .attr("rx", 4)
          .attr("ry", 4)
          .attr("fill", 'none')
          .attr("stroke-dasharray", 1)
          .attr("stroke", "#252525");


        //绘制边框里面的学习者
        g.append("g")
          .selectAll("circle")
          .data(data.cluster[i].stuInfo)
          .join("circle")
          .attr("class", d => 'stu_circle ' + 'stu_' + d.name)//为了后续高亮的时候建立索引
          .attr("cx", (d, j) => pat_each_row * pat_rect_width + total_margin_left + 105 + (j % stu_each_row + 0.5) * stu_rect_height + stu_margin_border)
          .attr("cy", (d, j) => margin.top * 2 + title_name_height + before_border_y + Math.floor(j / stu_each_row) * stu_rect_height + stu_margin_border)
          .attr("r", 8)
          .attr("fill", 'none')
          // .attr("stroke", colorList[i])
          .attr("opacity", 1);

        var defs = g.append("defs");
        defs.append("pattern")
          .attr("id", "image-pattern") // 设置图案的ID
          .attr("width", 14) // 图案的宽度
          .attr("height", 14) // 图案的高度
          .append("image")
          .attr("fill", "red")
          .attr("xlink:href", "../static/stu_1.svg") // 图片的路径
          .attr("width", 14) // 图片的宽度
          .attr("height", 14); // 图片的高度

        g.append("g")
          .selectAll("circle")
          .data(data.cluster[i].stuInfo)
          .join("circle")
          .attr("class", d => 'stu_circle ' + 'stu_' + d.name)//为了后续高亮的时候建立索引
          .attr("cx", (d, j) => 1 + pat_each_row * pat_rect_width + total_margin_left + 105 + (j % stu_each_row + 0.5) * stu_rect_height + stu_margin_border)
          .attr("cy", (d, j) => -2 + margin.top * 2 + title_name_height + before_border_y + Math.floor(j / stu_each_row) * stu_rect_height + stu_margin_border)
          .attr("r", 8)
          .attr("fill", "url(#image-pattern)");
        // .attr("stroke", colorList[i]);

        // 图片下面的水平条形
        g.append("g")
          .selectAll("rect")
          .data(data.cluster[i].stuInfo)
          .join("rect")
          .attr("class", d => 'stu_rect ' + 'stu_' + d.name)//为了后续高亮的时候建立索引
          .attr("x", (d, j) => -6 + pat_each_row * pat_rect_width + total_margin_left + 105 + (j % stu_each_row + 0.5) * stu_rect_height + stu_margin_border)
          .attr("y", (d, j) => 5 + margin.top * 2 + title_name_height + before_border_y + Math.floor(j / stu_each_row) * stu_rect_height + stu_margin_border)
          .attr("width", 12)
          .attr("height", 3)
          .attr("fill", "none")
          .attr("stroke", '#b9b9b9')
          .attr("stroke-width", 1);



        g.append("g")
          .selectAll("rect")
          .data(data.cluster[i].stuInfo)
          .join("rect")
          .attr("class", d => 'stu_rect_width ' + 'x' + d.name)//为了后续高亮的时候建立索引
          .attr("x", (d, j) => -6 + pat_each_row * pat_rect_width + total_margin_left + 105 + (j % stu_each_row + 0.5) * stu_rect_height + stu_margin_border)
          .attr("y", (d, j) => 5 + margin.top * 2 + title_name_height + before_border_y + Math.floor(j / stu_each_row) * stu_rect_height + stu_margin_border)
          .attr("width", 0)
          .attr("height", 3)
          .attr("fill", '#3b3b3b');


        g.append("g")
          .append("rect")
          .attr("x", pat_each_row * pat_rect_width + total_margin_left + 105)
          .attr("y", border_y_array[i])
          .attr("width", stu_each_row * stu_rect_height + 10)
          .attr("height", title_name_height)
          .attr("fill", colorList[i])
          .attr("opacity", 0.6);

        var t_name = i == +(data.cluster.length - 1) ? 'Abnormal' : data.cluster[i].name;
        var t_margin_left = i == +(data.cluster.length - 1) ? 115 : 135
        g.append("g")
          .append("text")
          .attr("x", pat_each_row * pat_rect_width + total_margin_left + t_margin_left)
          .attr("y", border_y_array[i] + 15)
          .text(t_name)
          .attr("font-size", 12);

        g.append("g")
          .append("text")
          .attr("x", 70 + pat_each_row * pat_rect_width + total_margin_left + 115)
          .attr("y", border_y_array[i] + 15)
          .text("Number of Learners: ")
          .attr("font-size", 12);

        g.append("g")
          .append("text")
          .attr("x", 70 + pat_each_row * pat_rect_width + total_margin_left + 228)
          .attr("y", border_y_array[i] + 15)
          .text(data.cluster[i].stuInfo.length)
          .attr("font-weight", "bold")
          .attr("font-size", 12);


        // 图例
        const legendRect = g.selectAll("legendRect")
          .data(d3.range(d3.min(data.PatList.map(d => d.value)), d3.max(data.PatList.map(d => d.value)), (d3.max(data.PatList.map(d => d.value)) - d3.min(data.PatList.map(d => d.value))) / 15)) // 使用比例尺范围内的数据创建矩形
          .enter()
          .append("rect")
          .attr("x", (d, i) => 660 + i * 11) // 设置矩形的 x 坐标
          .attr("y", 30) // 设置矩形的 y 坐标
          .attr("width", 8) // 设置矩形的宽度
          .attr("height", 10) // 设置矩形的高度
          .attr("fill", d => pat_rscale(d)); // 根据比例尺填充颜色


        g.append("g")
          .append("text")
          .attr("x", 682)
          .attr("y", 22)
          .text("Degree of frequency")
          .attr("font-size", 12);

        g.append("g")
          .append("text")
          .attr("x", 632)
          .attr("y", 40)
          .text("Low")
          .attr("font-size", 12);

        g.append("g")
          .append("text")
          .attr("x", 826)
          .attr("y", 40)
          .text("High")
          .attr("font-size", 12);


        //模式节点连接图
        const centerX = width / 2;
        const centerY = height / 2;
        const radius = 7; // 中心圆的半径
        const numNodes = data.cluster.length; // 节点数量

        function drawGraph(id) {


          const node_link_chart = g.append("g")
            .attr("transform", `translate(${-568 + ((id % pat_each_row) - 1) * 30},${-185 + Math.floor(id / pat_each_row) * 30})`);

          const nodes = [];
          const angleStep = (2 * Math.PI) / numNodes; // 计算每个节点之间的角度间隔

          // 计算每个节点的位置
          for (let i = 0; i < numNodes; i++) {

             const node_rscale = d3.scaleLinear().domain([results[i].min, results[i].max]).range([0.8, 3]);


            const r_location = Math.floor(id / numNodes) * numNodes + i;
            const angle = (Math.PI / 2) - i * angleStep; // 从12点钟方向开始顺时针排列
            const x = centerX + radius * Math.cos(angle);
            const y = centerY - radius * Math.sin(angle); // 注意sin取负号
            nodes.push({id: i + 1, x: x, y: y, value: node_rscale(data.nodelink[r_location])});
          }

          const links = nodes.map(node => ({source: 0, target: node.id}));


          // 绘制连接线
          const link = node_link_chart.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(links)
            .enter().append("line")
            .attr("stroke", "#252525")
            .attr("stroke-width", 0.3)
            .attr("x1", centerX)
            .attr("y1", centerY)
            .attr("x2", d => nodes[d.target - 1].x)
            .attr("y2", d => nodes[d.target - 1].y);

          // 绘制节点
          const node = node_link_chart.append("g")
            .attr("class", "nodes")
            .selectAll("circle")
            .data(nodes)
            .enter().append("circle")
            .attr("r", d => d.value)
            .attr("fill", "#ECC97F")
            .attr("cx", d => d.x)
            .attr("cy", d => d.y);
        }


        const groups = Array.from({length: numNodes}, () => []);

        // 分组
        for (let i = 0; i < data.nodelink.length; i++) {
          const groupIndex = i % numNodes;
          groups[groupIndex].push(data.nodelink[i]);
        }

        // 计算最大值和最小值的函数
        function getMaxAndMin(group) {
          const max = Math.max(...group);
          const min = Math.min(...group);
          return {max, min};
        }

        // 获取每组的最大值和最小值
        const results = groups.map(group => getMaxAndMin(group));

        for (let i = 0; i < data.PatList.length; i++) {
          drawGraph(i);
        }
      }


    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
div#explore_container {
  height: 545px;
  width: 1397px;
  overflow-y: auto;
}

svg#exploreInfo {
  height: 539px;
  width: 1393px;
}
</style>
