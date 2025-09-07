import Vue from 'vue'
import Router from 'vue-router'
import patternOverview from '@/components/1.patternOverview'
import patternExplore from '@/components/2.patternExplore'
import studentCluster from '@/components/4.studentCluster'
import abnormalScore from '@/components/5.abnormalScore'
import patternCompare from '@/components/6.patternCompare'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'patternoverview',
      component: patternOverview
    },
    {
      path: '/',
      name: 'patternexplore',
      component: patternExplore
    },
    {
      path: '/',
      name: 'studentcluster',
      component: studentCluster
    },
    {
      path: '/',
      name: 'abnormalscore',
      component: abnormalScore
    },
    {
      path: '/',
      name: 'patterncompare',
      component: patternCompare
    }
  ]
})
