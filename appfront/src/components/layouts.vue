<template>
  <!-- 最外层容器 -->
  <el-container>

    <!-- 顶栏容器 -->
    <el-header>
      <el-menu :default-active="activeIndex" mode="horizontal" :router="true">
        <el-menu-item index="/basic">基础模板</el-menu-item>
        <el-submenu index="workspace">
          <template slot="title">我的工作台</template>
          <el-menu-item index="2-1">选项1</el-menu-item>
          <el-menu-item index="2-2">选项2</el-menu-item>
          <el-menu-item index="2-3">选项3</el-menu-item>
        </el-submenu>
      </el-menu>
    </el-header>

    <el-container>
      <!-- 侧栏容器 -->
      <el-aside style="width: 18%;">
        <h4>基础模板</h4>
        <el-menu
          :router="true"
          default-active="/basic">
          <el-menu-item index="/basic">
            <template slot="title">
              <i class="el-icon-menu"></i>
              <span>基础功能</span>
            </template>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- 内容容器 -->
      <el-main>
        <router-view></router-view>
      </el-main>

    </el-container>

  </el-container>
</template>

<script>
export default {
  data () {
    return {
      activeIndex: 'crud'
    }
  }
}
</script>
