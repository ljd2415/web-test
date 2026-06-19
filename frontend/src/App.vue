<script setup>
import { computed, reactive, ref } from 'vue'

const roleOptions = [
  { key: 'owner', label: '业主', hint: '录入本人及房屋门禁信息' },
  { key: 'tenant', label: '租户', hint: '录入租住人与房屋关联信息' },
  { key: 'admin', label: '管理员', hint: '查看全部住户提交资料' },
]

const relationOptions = ['本人', '配偶', '子女', '父母', '租户', '其他']
const buildingOptions = ['1栋', '2栋', '3栋', '4栋', '5栋', '6栋']
const unitOptions = ['1单元', '2单元', '3单元', '4单元']
const propertyOptions = ['自住', '出租']

const selectedRole = ref('owner')
const currentView = ref('login')
const activeUser = ref(null)
const loginError = ref('')
const notice = ref('')
const loading = ref(false)
const profiles = ref([])
const currentProfile = ref(null)

const loginForm = reactive({
  name: '',
  phone: '',
  username: '',
  password: '',
})

const profileForm = reactive({
  id: '',
  name: '',
  phone: '',
  relationship: '本人',
  building: '1栋',
  unit: '1单元',
  room: '',
  propertyType: '自住',
})

const roleLabel = computed(() => {
  return roleOptions.find((role) => role.key === selectedRole.value)?.label || ''
})

const adminRows = computed(() => profiles.value)

function selectRole(role) {
  selectedRole.value = role
  currentView.value = 'login'
  activeUser.value = null
  currentProfile.value = null
  loginError.value = ''
  notice.value = ''
  resetLogin()
}

function resetLogin() {
  loginForm.name = ''
  loginForm.phone = ''
  loginForm.username = ''
  loginForm.password = ''
}

async function login() {
  loginError.value = ''
  notice.value = ''

  if (selectedRole.value === 'admin') {
    if (loginForm.username === 'ljd' && loginForm.password === 'ljd') {
      activeUser.value = { id: 'admin', role: 'admin', name: 'ho_ok' }
      await loadAllProfiles()
      currentView.value = 'admin'
      return
    }
    loginError.value = '管理员账号或密码不正确'
    return
  }

  if (!loginForm.name.trim() || !/^1\d{10}$/.test(loginForm.phone)) {
    loginError.value = '请输入姓名和 11 位手机号'
    return
  }

  activeUser.value = {
    role: selectedRole.value,
    name: loginForm.name.trim(),
    phone: loginForm.phone,
  }

  const existing = await loadProfileByPhone(loginForm.phone)
  if (existing) {
    fillProfile(existing)
    currentProfile.value = existing
    currentView.value = 'profile'
  } else {
    fillProfile({
      id: '',
      name: loginForm.name.trim(),
      phone: loginForm.phone,
      relationship: selectedRole.value === 'owner' ? '本人' : '租户',
      building: '1栋',
      unit: '1单元',
      room: '',
      propertyType: selectedRole.value === 'owner' ? '自住' : '出租',
    })
    currentView.value = 'form'
  }
}

async function loadProfileByPhone(phone) {
  loading.value = true
  try {
    const response = await fetch(`/api/pi/?phone=${encodeURIComponent(phone)}`)
    const data = await response.json()
    if (!response.ok) {
      throw new Error(data.error || '查询信息失败')
    }
    return data.results?.[0] || null
  } catch (error) {
    loginError.value = error.message
    return null
  } finally {
    loading.value = false
  }
}

async function loadAllProfiles() {
  loading.value = true
  try {
    const response = await fetch('/api/pi/')
    const data = await response.json()
    if (!response.ok) {
      throw new Error(data.error || '查询信息失败')
    }
    profiles.value = data.results || []
  } catch (error) {
    loginError.value = error.message
  } finally {
    loading.value = false
  }
}

function fillProfile(profile) {
  Object.assign(profileForm, {
    id: profile.id || '',
    name: profile.name || '',
    phone: profile.phone || '',
    relationship: profile.relationship || '本人',
    building: profile.building || '1栋',
    unit: profile.unit || '1单元',
    room: profile.room || '',
    propertyType: profile.propertyType || '自住',
  })
}

async function submitProfile() {
  notice.value = ''

  if (!profileForm.name.trim() || !/^1\d{10}$/.test(profileForm.phone)) {
    notice.value = '请检查姓名和手机号'
    return
  }

  if (!profileForm.room.trim()) {
    notice.value = '请填写房号'
    return
  }

  loading.value = true
  try {
    const response = await fetch('/api/pi/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: profileForm.name,
        phone: profileForm.phone,
        relationship: profileForm.relationship,
        building: profileForm.building,
        unit: profileForm.unit,
        room: profileForm.room,
        propertyType: profileForm.propertyType,
      }),
    })
    const data = await response.json()
    if (!response.ok) {
      throw new Error(data.error || '保存失败')
    }

    currentProfile.value = data.result
    fillProfile(data.result)
    currentView.value = 'profile'
    notice.value = '信息已保存到数据库'
  } catch (error) {
    notice.value = error.message
  } finally {
    loading.value = false
  }
}

function editProfile() {
  if (currentProfile.value) {
    fillProfile(currentProfile.value)
  }
  notice.value = ''
  currentView.value = 'form'
}

function logout() {
  activeUser.value = null
  currentProfile.value = null
  currentView.value = 'login'
  notice.value = ''
  loginError.value = ''
  resetLogin()
}
</script>

<template>
  <main class="app-shell">
    <aside class="sidebar">
      <div class="brand">
        <span class="brand-mark">门</span>
        <div>
          <strong>小区物业门禁</strong>
          <small>信息录入系统</small>
        </div>
      </div>

      <nav class="role-list" aria-label="身份选择">
        <button
          v-for="role in roleOptions"
          :key="role.key"
          type="button"
          :class="['role-card', { active: selectedRole === role.key }]"
          @click="selectRole(role.key)"
        >
          <span>{{ role.label }}</span>
          <small>{{ role.hint }}</small>
        </button>
      </nav>

      <a class="admin-link" href="/admin/">Django 后台</a>
    </aside>

    <section class="workspace">
      <header class="topbar">
        <div>
          <p class="eyebrow">Access Registration</p>
          <h1>{{ roleLabel }}身份验证</h1>
        </div>
        <button v-if="activeUser" class="ghost-button" type="button" @click="logout">
          退出登录
        </button>
      </header>

      <section v-if="currentView === 'login'" class="panel login-panel">
        <div class="panel-heading">
          <h2>请选择身份并登录</h2>
          <p>业主和租户使用姓名及手机号验证，管理员使用账号密码验证。</p>
        </div>

        <form class="form-grid" @submit.prevent="login">
          <template v-if="selectedRole === 'admin'">
            <label>
              管理员账号
              <input v-model.trim="loginForm.username" autocomplete="username" placeholder="请输入账号" />
            </label>
            <label>
              管理员密码
              <input
                v-model="loginForm.password"
                autocomplete="current-password"
                placeholder="请输入密码"
                type="password"
              />
            </label>
          </template>

          <template v-else>
            <label>
              姓名
              <input v-model.trim="loginForm.name" autocomplete="name" placeholder="请输入真实姓名" />
            </label>
            <label>
              手机号
              <input
                v-model.trim="loginForm.phone"
                autocomplete="tel"
                maxlength="11"
                placeholder="请输入 11 位手机号"
              />
            </label>
          </template>

          <p v-if="loginError" class="error">{{ loginError }}</p>
          <button class="primary-button" type="submit" :disabled="loading">
            {{ loading ? '处理中...' : '进入系统' }}
          </button>
        </form>
      </section>

      <section v-if="currentView === 'form'" class="panel">
        <div class="panel-heading">
          <h2>个人信息录入</h2>
          <p>请确认住户身份、联系方式和房屋门禁关联信息。</p>
        </div>

        <form class="form-grid two-columns" @submit.prevent="submitProfile">
          <label>
            姓名
            <input v-model.trim="profileForm.name" placeholder="请输入姓名" />
          </label>
          <label>
            手机号
            <input v-model.trim="profileForm.phone" maxlength="11" placeholder="请输入手机号" />
          </label>
          <label>
            与业主身份关系
            <select v-model="profileForm.relationship">
              <option v-for="item in relationOptions" :key="item">{{ item }}</option>
            </select>
          </label>
          <label>
            楼栋
            <select v-model="profileForm.building">
              <option v-for="item in buildingOptions" :key="item">{{ item }}</option>
            </select>
          </label>
          <label>
            单元
            <select v-model="profileForm.unit">
              <option v-for="item in unitOptions" :key="item">{{ item }}</option>
            </select>
          </label>
          <label>
            房号
            <input v-model.trim="profileForm.room" placeholder="例如 1802" />
          </label>
          <label>
            房屋属性
            <select v-model="profileForm.propertyType">
              <option v-for="item in propertyOptions" :key="item">{{ item }}</option>
            </select>
          </label>

          <p v-if="notice" class="notice">{{ notice }}</p>
          <button class="primary-button span-all" type="submit" :disabled="loading">
            {{ loading ? '保存中...' : '保存信息' }}
          </button>
        </form>
      </section>

      <section v-if="currentView === 'profile'" class="panel">
        <div class="panel-heading horizontal">
          <div>
            <h2>个人主页</h2>
            <p>查看并维护已提交到数据库的门禁信息。</p>
          </div>
          <button class="primary-button compact" type="button" @click="editProfile">修改信息</button>
        </div>

        <dl v-if="currentProfile" class="profile-list">
          <div><dt>姓名</dt><dd>{{ currentProfile.name }}</dd></div>
          <div><dt>手机号</dt><dd>{{ currentProfile.phone }}</dd></div>
          <div><dt>关系</dt><dd>{{ currentProfile.relationship }}</dd></div>
          <div><dt>楼栋</dt><dd>{{ currentProfile.building }}</dd></div>
          <div><dt>单元</dt><dd>{{ currentProfile.unit }}</dd></div>
          <div><dt>房号</dt><dd>{{ currentProfile.room }}</dd></div>
          <div><dt>房屋属性</dt><dd>{{ currentProfile.propertyType }}</dd></div>
        </dl>
      </section>

      <section v-if="currentView === 'admin'" class="panel">
        <div class="panel-heading horizontal">
          <div>
            <h2>住户信息管理</h2>
            <p>管理员可查看 MySQL 数据库中所有业主与租户提交的个人信息。</p>
          </div>
          <span class="count-badge">{{ adminRows.length }} 条记录</span>
        </div>

        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>姓名</th>
                <th>手机号</th>
                <th>关系</th>
                <th>楼栋</th>
                <th>单元</th>
                <th>房号</th>
                <th>房屋属性</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in adminRows" :key="item.id">
                <td>{{ item.name }}</td>
                <td>{{ item.phone }}</td>
                <td>{{ item.relationship }}</td>
                <td>{{ item.building }}</td>
                <td>{{ item.unit }}</td>
                <td>{{ item.room }}</td>
                <td>{{ item.propertyType }}</td>
              </tr>
              <tr v-if="adminRows.length === 0">
                <td class="empty" colspan="7">暂无住户提交信息</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </section>
  </main>
</template>
