import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router';
import LandingPage from '../components/LandingPage.vue';
import CharactersPage from '../components/CharactersPage.vue';
import ChatWindow from '@/components/ChatWindow.vue';
import ProfileComponent from '../components/ProfileComponent.vue';
import AuthPage from '../components/AuthPage.vue';
import { useUserStore } from '@/store';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: LandingPage
  },
  {
    path: '/characters',
    name: 'Characters',
    component: CharactersPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/chat/:characterId?',
    name: 'Chat',
    component: ChatWindow,
    meta: { requiresAuth: true },
    props: true
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfileComponent,
    meta: { requiresAuth: true }
  },
  {
    path: '/auth',
    name: 'Auth',
    component: AuthPage
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, _from, next) => {
  const userStore = useUserStore();
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);

  if (requiresAuth && !userStore.user) {
    next('/auth');
  } else {
    next();
  }
});

export default router;