<template>
  <div id="app">
    <i-col span="4">
      <Row style="height: 40%;">
        <studentcluster></studentcluster>
      </Row>
      <Row style="height: 60%;">
        <patternoverview></patternoverview>
      </Row>
    </i-col>

    <i-col span="20">
      <Row style="height: 40%;">
        <i-col span="19">
          <abnoramlscore></abnoramlscore>
        </i-col>
        <i-col span="5">
          <patterncompare></patterncompare>
        </i-col>

      </Row>
      <Row style="height: 60%;">
        <patternexplore></patternexplore>
      </Row>
    </i-col>

  </div>
</template>

<script>
import Row from '../node_modules/iview/src/components/grid/row.vue'
import ICol from '../node_modules/iview/src/components/grid/col.vue'
import patternoverview from './components/1.patternOverview'
import patternexplore from './components/2.patternExplore'
import studentcluster from './components/4.studentCluster'
import abnoramlscore from './components/5.abnormalScore'
import patterncompare from './components/6.patternCompare'

export default {
  name: 'App',
  components: {
    Row,
    ICol,
    patternoverview,
    patternexplore,
    studentcluster,
    abnoramlscore,
    patterncompare
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  overflow: hidden;
}

html, body, #app {
  height: 100%;
}

.myCard {
  height: 100%;
}

.content {
  background: #eee;
  padding: 2px;
  height: 100%;
}

.ivu-card-head {
  border-bottom: 1px solid #e8eaec;
  padding: 4px 10px;
  line-height: 1;
}
.ivu-col-span-4 .ivu-col-span-16 {
  height: 100%;
}
.ivu-card-body {
    padding: 4px;
}
</style>
