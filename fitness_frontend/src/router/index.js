import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../store/auth'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../components/auth/Login.vue'),
    meta: { requiresAuth: false, hideNavbar: true, hideFooter: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../components/auth/Register.vue'),
    meta: { requiresAuth: false, hideNavbar: true, hideFooter: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../components/client/Profile.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/centers',
    name: 'FitnessCenters',
    component: () => import('../components/client/FitnessCenters.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/services',
    name: 'Services',
    component: () => import('../components/client/Services.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/subscriptions',
    name: 'Subscriptions',
    component: () => import('../components/client/Subscriptions.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/schedule',
    name: 'Schedule',
    component: () => import('../components/client/Schedule.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register-workout/:id',
    name: 'WorkoutRegistration',
    component: () => import('../components/client/WorkoutRegistration.vue'),
    meta: { requiresAuth: true, isClient: true }
  },
  {
    path: '/feedback/:trainerId',
    name: 'FeedbackForm',
    component: () => import('../components/client/FeedbackForm.vue'),
    meta: { requiresAuth: true, isClient: true }
  },
  // Admin routes
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: () => import('../components/admin/AdminDashboard.vue'),
    meta: { requiresAuth: true, isEmployee: true }
  },
  {
    path: '/admin/workouts',
    name: 'WorkoutManagement',
    component: () => import('../components/admin/WorkoutManagement.vue'),
    meta: { requiresAuth: true, isEmployee: true }
  },
  {
    path: '/admin/trainers',
    name: 'TrainerManagement',
    component: () => import('../components/admin/TrainerManagement.vue'),
    meta: { requiresAuth: true, isEmployee: true }
  },
  {
    path: '/admin/services',
    name: 'ServiceManagement',
    component: () => import('../components/admin/ServiceManagement.vue'),
    meta: { requiresAuth: true, isEmployee: true }
  },
  {
    path: '/admin/subscriptions',
    name: 'SubscriptionManagement',
    component: () => import('../components/admin/SubscriptionManagement.vue'),
    meta: { requiresAuth: true, isEmployee: true }
  },
  {
    path: '/admin/reports',
    name: 'ReportGeneration',
    component: () => import('../components/admin/ReportGeneration.vue'),
    meta: { requiresAuth: true, isEmployee: true }
  },
  // Добавьте эти маршруты в массив routes
  {
    path: '/trainers',
    name: 'Trainers',
    component: () => import('../components/client/Trainers.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/trainers/:id',
    name: 'TrainerDetails',
    component: () => import('../components/client/TrainerDetails.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/workout/:id',
    name: 'WorkoutDetails',
    component: () => import('../components/client/WorkoutDetails.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../components/client/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/About.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue'),
    meta: { requiresAuth: false }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // Для отладки
  console.log('Navigation guard triggered:', {
    to: to.name,
    from: from.name,
    isAuthenticated: authStore.isAuthenticated,
    user: authStore.user,
    token: authStore.token ? 'exists' : 'none'
  })
  
  const isAuthenticated = authStore.isAuthenticated
  const user = authStore.user

  // Если пытаемся зайти на страницы входа/регистрации уже авторизованными
  if ((to.name === 'Login' || to.name === 'Register') && isAuthenticated) {
    console.log('Already authenticated, redirecting to home')
    next('/')
    return
  }

  // Проверка защищенных маршрутов
  if (to.meta.requiresAuth && !isAuthenticated) {
    console.log('Route requires auth, redirecting to login')
    next('/login')
    return
  }

  // Проверка ролей
  if (to.meta.isEmployee && (!user || !user.is_employee)) {
    console.log('Route requires employee role')
    next('/')
    return
  }
  
  if (to.meta.isClient && (!user || user.is_employee)) {
    console.log('Route requires client role')
    next('/')
    return
  }

  console.log('Navigation allowed')
  next()
})

export default router