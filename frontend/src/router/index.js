import { createRouter, createWebHistory } from 'vue-router'
import FamilyList from '../views/FamilyList.vue'
import VersionManage from '../views/VersionManage.vue'
import SearchResult from '../views/SearchResult.vue'

const routes = [
  { path: '/', redirect: '/families' },
  { path: '/families', component: FamilyList, name: 'Families' },
  { path: '/families/:familyId/versions', component: VersionManage, name: 'Versions', props: true },
  { path: '/search', component: SearchResult, name: 'Search' }
]

export default createRouter({ history: createWebHistory(), routes })
