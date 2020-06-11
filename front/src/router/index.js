import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/Login.vue'
import Home from '../views/Home.vue'
Vue.use(VueRouter)
console.log('router',localStorage.getItem('isAuth'))
const ifNotAuthenticated = (to, from, next) => {
  if (localStorage.getItem('isAuth')) {
    next()
    return
  }
  next('/')
}

const ifAuthenticated = (to, from, next) => {
  if (!localStorage.getItem('isAuth')) {
    next()
    return
  }
  next('/login')
}
  const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    beforeEnter: ifNotAuthenticated,

  },
  {
    path: '/register',
    name: 'Register',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/Register.vue'),
    beforeEnter: ifNotAuthenticated,
  },
  {
      path: '/',
      name: 'Home',
      component: Home,
      beforeEnter: ifAuthenticated,
  }

]

const router = new VueRouter({
  routes
})

export default router
