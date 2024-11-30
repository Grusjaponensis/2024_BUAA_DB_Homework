/**
 * router/index.ts
 *
 * Automatic routes for `./src/pages/*.vue`
 */

// Composables
import { createRouter, createWebHistory } from 'vue-router/auto'
import { setupLayouts } from 'virtual:generated-layouts'
//import { routes } from 'vue-router/auto-routes'
// pages_import_start
import Index from '../pages/index.vue';
import Home from '../pages/home.vue';
import ForumCenter from '../pages/ForumCenter/forumCenter.vue';
import RescueAction from '../pages/rescueAction.vue';
import CatBase from '../pages/catBase.vue';
import AdoptionPlan from '../pages/adoptionPlan.vue';
import CreatePost from '../pages/ForumCenter/createPost.vue';
import MyPosts from '../pages/ForumCenter/myPosts.vue';
import MyFavorites from '../pages/ForumCenter/myFavorites.vue';
import PostDetails from '../pages/ForumCenter/postDetails.vue';
// ... 导入其他页面组件

const routes = [
  {
    path: '/',
    name: 'Index',
    component: Index
  },
  {
    path: '/home',
    name: 'Home',
    component: Home
  },
  {
    path: '/forum-center',
    name: 'ForumCenter',
    component: ForumCenter
  },
  {
    path: '/forum-center/my-posts',
    name: 'MyPosts',
    component: MyPosts
  },
  {
    path: '/forum-center/my-favorites',
    name: 'MyFavorites',
    component: MyFavorites
  },
  {
    path: '/post/:postId', 
    name: 'PostDetails',
    component: PostDetails,
    props: true 
  },
  {
    path: '/rescue-action',
    name: 'RescueAction',
    component: RescueAction
  },
  {
    path: '/cat-base',
    name: 'CatBase',
    component: CatBase
  },
  {
    path: '/adoption-plan',
    name: 'AdoptionPlan',
    component: AdoptionPlan
  },
  {
    path: '/create-post',
    name: 'CreatePost',
    component: CreatePost
  },
  // 其他路由...
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: setupLayouts(routes),
})

// Workaround for https://github.com/vitejs/vite/issues/11804
router.onError((err, to) => {
  if (err?.message?.includes?.('Failed to fetch dynamically imported module')) {
    if (!localStorage.getItem('vuetify:dynamic-reload')) {
      console.log('Reloading page to fix dynamic import error')
      localStorage.setItem('vuetify:dynamic-reload', 'true')
      location.assign(to.fullPath)
    } else {
      console.error('Dynamic import error, reloading page did not fix it', err)
    }
  } else {
    console.error(err)
  }
})

router.isReady().then(() => {
  localStorage.removeItem('vuetify:dynamic-reload')
})

export default router
