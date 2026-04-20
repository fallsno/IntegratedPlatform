<template>
  <div class="family-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>产品型号列表</span>
          <el-button type="primary" @click="showAddDialog = true">
            <el-icon><Plus /></el-icon>新增型号
          </el-button>
        </div>
      </template>

      <el-table :data="families" v-loading="loading" stripe>
        <el-table-column prop="family_code" label="主代号" width="150" />
        <el-table-column prop="family_name" label="名称" width="180" />
        <el-table-column label="旧代号" width="250">
          <template #default="{ row }">
            <el-tag v-for="alias in row.aliases" :key="alias.id" size="small" style="margin-right: 5px">
              {{ alias.alias_code }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="category" label="分类" width="150" />
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button type="primary" link @click="goToVersions(row.id)">版本管理</el-button>
            <el-button type="success" link @click="editFamily(row)">编辑</el-button>
            <el-button type="danger" link @click="deleteFamily(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新增/编辑型号对话框 -->
    <el-dialog v-model="showAddDialog" :title="editingFamily ? '编辑型号' : '新增型号'" width="500px">
      <el-form :model="familyForm" label-width="100px">
        <el-form-item label="主代号" required>
          <el-input v-model="familyForm.family_code" placeholder="例如 AT240R.0" />
        </el-form-item>
        <el-form-item label="名称" required>
          <el-input v-model="familyForm.family_name" placeholder="例如 干燥滚筒" />
        </el-form-item>
        <el-form-item label="分类">
          <el-input v-model="familyForm.category" placeholder="例如 干燥滚筒" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="familyForm.description" type="textarea" />
        </el-form-item>
        <el-form-item label="旧代号（多个用逗号分隔）">
          <el-input v-model="aliasInput" placeholder="例如 GT240GF1.0, GTRS200B.0" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="saveFamily">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const families = ref([])
const loading = ref(false)
const showAddDialog = ref(false)
const editingFamily = ref(null)
const familyForm = ref({ family_code: '', family_name: '', category: '', description: '' })
const aliasInput = ref('')

const fetchFamilies = async () => {
  loading.value = true
  try {
    const res = await axios.get('/families/')
    families.value = res.data
  } catch (e) {
    ElMessage.error('获取型号列表失败')
  } finally {
    loading.value = false
  }
}

const saveFamily = async () => {
  try {
    // ✅ 前端拦截空值
    if (!familyForm.value.family_code?.trim()) {
      ElMessage.warning('主代号不能为空')
      return
    }
    if (!familyForm.value.family_name?.trim()) {
      ElMessage.warning('名称不能为空')
      return
    }
    if (editingFamily.value) {
      // 编辑（简化处理，仅更新基本信息，别名单独维护）
      await axios.put(`/families/${editingFamily.value.id}`, familyForm.value)
      ElMessage.success('更新成功')
    } else {
      const res = await axios.post('/families/', familyForm.value)
      const familyId = res.data.id
      // 添加别名
      if (aliasInput.value.trim()) {
        const aliases = aliasInput.value.split(',').map(s => s.trim()).filter(s => s)
        for (const code of aliases) {
          await axios.post(`/families/${familyId}/aliases?alias_code=${code}&alias_type=old`)
        }
      }
      ElMessage.success('创建成功')
    }
    showAddDialog.value = false
    editingFamily.value = null
    familyForm.value = { family_code: '', family_name: '', category: '', description: '' }
    aliasInput.value = ''
    fetchFamilies()
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

const editFamily = (row) => {
  editingFamily.value = row
  familyForm.value = { ...row }
  aliasInput.value = row.aliases.map(a => a.alias_code).join(', ')
  showAddDialog.value = true
}

const deleteFamily = async (id) => {
  await ElMessageBox.confirm('确定删除该型号及其所有版本和部件吗？', '警告', { type: 'warning' })
  try {
    await axios.delete(`/families/${id}`)
    ElMessage.success('删除成功')
    fetchFamilies()
  } catch (e) {
    ElMessage.error('删除失败')
  }
}

const goToVersions = (familyId) => {
  router.push({ name: 'Versions', params: { familyId } })
}

onMounted(fetchFamilies)
</script>

<style scoped>
.family-list { padding: 20px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>