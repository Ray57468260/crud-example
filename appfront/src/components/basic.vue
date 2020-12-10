<template>
  <div>
    <el-card>
      <div style="display: flex">
        <el-button type="primary" @click="create">新增</el-button>
        <el-button type="danger" @click="del">删除</el-button>
        <el-button @click="getTemplate">下载模板</el-button>
        <el-button @click="importShow=!importShow">导入</el-button>
        <el-button @click="exportExcel">导出</el-button>
      </div>

      <!-- 条件搜索 -->
      <el-divider><i class="el-icon-search" @click="isSearch=!isSearch" style="cursor: pointer;">条件搜索</i></el-divider>
      <div v-if="isSearch">
        <el-form :inline="true" size="mini" ref="form" :model="searchForm" label-width="auto">
          <el-form-item label="字段1">
            <el-input v-model="searchForm.field1" size="mini" placeholder="精确搜索"></el-input>
          </el-form-item>
          <el-form-item label="字段2">
            <el-input v-model="searchForm.field2" size="mini" placeholder="多条模糊搜索, 逗号分隔"></el-input>
          </el-form-item>
          <el-form-item label="字段3">
            <el-input v-model="searchForm.field3" size="mini" placeholder="模糊搜索"></el-input>
          </el-form-item>
          <el-button size="mini" type="primary" @click="pageLoad">查询</el-button>
        </el-form>
      </div>

      <!-- 功能区域 -->
      <div style="display: flex">
        <el-upload
          v-if="importShow"
          drag
          :http-request="upload"
          action=""
          multiple>
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
        </el-upload>
      </div>

      <!-- 表格区域 -->
      <el-table :data="tableData" v-loading="loading" size="mini"
        @selection-change="handleSelectionChange">
        <el-table-column
          type="selection"
          fixed="left">
        </el-table-column>
        <el-table-column
          prop="id"
          key="id"
          label="ID">
        </el-table-column>
        <el-table-column
          prop="field1"
          key="field1"
          label="字段1">
        </el-table-column>
        <el-table-column
          prop="field2"
          key="field2"
          label="字段2">
        </el-table-column>
        <el-table-column
          prop="field3"
          key="field3"
          label="字段3">
        </el-table-column>
        <el-table-column
          label="操作"
          align="center"
          min-width="100">
          <template slot-scope="scope">
            <div style="display: flex">
              <el-button size="mini" type="primary" icon="el-icon-edit" @click="edit(scope.row)"></el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
      <br>
      <el-pagination
        background
        @size-change="sizeChange"
        @current-change="currentChange"
        :current-page="pageNum"
        :page-sizes="[10,20,100,200]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="itemCount">
      </el-pagination>
    </el-card>

    <!-- 弹窗 -->
    <el-dialog
        :title="editMode? '修改':'新增'"
        :visible.sync="dialogVisible"
        width="40%"
        center
        append-to-body>
      <el-form label-width="auto" :model="form" ref="form" size="mini">
        <el-row :gutter="20">
          <el-form-item label="字段1" prop="field1" style="margin-bottom: 15px">
            <el-input size="mini" v-model="form.field1" style="width: 100%"></el-input>
          </el-form-item>
          <el-form-item label="字段2" prop="field2" style="margin-bottom: 15px">
            <el-input size="mini" v-model="form.field2" style="width: 100%"></el-input>
          </el-form-item>
          <el-form-item label="字段3" prop="field3" style="margin-bottom: 15px">
            <el-input size="mini" v-model="form.field3" style="width: 100%"></el-input>
          </el-form-item>
        </el-row>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button size="mini" type="primary" @click="editMode?editSubmit():createSubmit()">确 定</el-button>
        <el-button size="mini" @click="dialogVisible = false">取 消</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data () {
    return {
      tableData: [],
      pageNum: 1,
      pageSize: 10,
      itemCount: 0,
      loading: false,
      selectedId: 0,
      dialogVisible: false,
      editMode: false,
      importShow: false,
      multipleSelection: [],
      form: {
        field1: '',
        field2: '',
        field3: ''
      },
      isSearch: true,
      searchForm: {
        field1: '',
        field2: '',
        field3: ''
      }
    }
  },
  methods: {
    // 表格多选相关
    handleSelectionChange (val) {
      this.multipleSelection = val
    },
    // 分页相关
    sizeChange (val) {
      this.pageSize = val
      this.pageLoad()
    },
    currentChange (val) {
      this.pageNum = val
      this.pageLoad()
    },
    pageLoad () {
      const that = this
      this.loading = true
      this.$axios.get('crud/', {
        params: {
          action: 'GetData',
          pageSize: this.pageSize,
          pageNum: this.pageNum,
          search: this.searchForm
        }
      }).then((response) => {
        that.loading = false
        if (response.data.state === 'success') {
          that.tableData = response.data.data
          that.itemCount = response.data.allCount
        } else {
          console.log(response.data)
        }
      })
    },
    // 删除相关
    del () {
      const that = this
      this.$confirm('确认删除?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        that.delSubmit()
      }).catch(() => {})
    },
    delSubmit () {
      const that = this
      const ids = this.multipleSelection.map(x => x.id)
      this.$axios({
        method: 'post',
        url: 'crud/',
        data: {
          action: 'Delete',
          ids: ids
        }
      }).then((response) => {
        if (response.data.state === 'success') {
          that.$message.success('操作成功')
          that.pageLoad()
        }
      })
    },
    // 修改相关
    edit (row) {
      this.editMode = true
      this.selectedId = row.id
      this.form = row
      this.dialogVisible = true
    },
    editSubmit () {
      const that = this
      this.$axios({
        method: 'post',
        url: 'crud/',
        data: {
          action: 'Update',
          id: this.selectedId,
          form: this.form
        }
      }).then((response) => {
        if (response.data.state === 'success') {
          this.dialogVisible = false
          that.$message.success('操作成功')
          that.pageLoad()
        }
      })
    },
    // 新增相关
    create () {
      this.editMode = false
      this.form = JSON.parse(JSON.stringify(this.formBak))
      this.dialogVisible = true
    },
    createSubmit () {
      const that = this
      this.$axios({
        method: 'post',
        url: 'crud/',
        data: {
          action: 'Create',
          id: this.selectedId,
          form: this.form
        }
      }).then((response) => {
        if (response.data.state === 'success') {
          this.dialogVisible = false
          that.$message.success('操作成功')
          that.pageLoad()
        }
      })
    },
    // 导出相关
    exportExcel () {
      const that = this
      this.$axios.get('crud/', {
        params: {
          action: 'DownloadFile'
        },
        responseType: 'blob'
      }).then((response) => {
        if (response.data.status === 'error') {
          that.$message.warning('模板不存在!')
        } else {
          const url = window.URL.createObjectURL(new Blob([response.data]))
          const link = document.createElement('a')
          link.style.display = 'none'
          link.href = url
          link.setAttribute('download', JSON.parse(response.headers.filename))
          document.body.appendChild(link)
          link.click()
          document.body.removeChild(link) // 下载完成移除元素
          window.URL.revokeObjectURL(url) // 释放掉blob对象
        }
      }).catch((err) => {
        console.log('错误:', err)
        that.$message.error('请求运维接口出错，请联系开发人员！')
      })
    },
    // 上传相关
    getTemplate () {
      const that = this
      this.$axios.get('crud/', {
        params: {
          action: 'DownloadTemplate'
        },
        responseType: 'blob'
      }).then((response) => {
        if (response.data.status === 'error') {
          that.$message.warning('模板不存在!')
        } else {
          const url = window.URL.createObjectURL(new Blob([response.data]))
          const link = document.createElement('a')
          link.style.display = 'none'
          link.href = url
          link.setAttribute('download', JSON.parse(response.headers.filename))
          document.body.appendChild(link)
          link.click()
          document.body.removeChild(link) // 下载完成移除元素
          window.URL.revokeObjectURL(url) // 释放掉blob对象
        }
      }).catch((err) => {
        console.log('错误:', err)
        that.$message.error('请求运维接口出错，请联系开发人员！')
      })
    },
    upload (fileObj) {
      const that = this
      const formData = new FormData()
      formData.append('file', fileObj.file)
      formData.append('type', fileObj.file.type)
      formData.append('action', 'Upload')
      this.$message.info('正在上传, 请稍等')
      return this.$axios.request({
        url: 'crud/',
        method: 'post',
        data: formData
      }).then((response) => {
        if (response.data.state === 'success') {
          that.$message.success('上传成功')
          that.pageLoad()
        } else {
          this.$message.error(response.data.message)
        }
      }).catch((err) => {
        window.console.log(err)
        that.$message.error('请求运维接口出错，请联系开发人员！')
      })
    }
  },
  mounted () {
    this.pageLoad()
    this.formBak = JSON.parse(JSON.stringify(this.form))
  }
}
</script>
