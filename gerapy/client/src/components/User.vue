<template>
    <div id="user">
        <el-dropdown size="mini" split-button type="primary">
            <span class="el-icon-info"></span>
            <el-dropdown-menu slot="dropdown">
                <el-dropdown-item><span @click="singOut">{{$lang.buttons.logout}}</span></el-dropdown-item>
            </el-dropdown-menu>
        </el-dropdown>
    </div>
</template>

<script>

    import { removeToken } from '../utils/auth'

    export default {
        name: "User",

        methods: {
            singOut() {
                removeToken()
                this.$router.push({path: '/login'})
            }
        }
    }
</script>

<style scoped>
    #user {
        float: right;
        margin-top: 15px;
        margin-right: 240px;
        cursor: pointer;
    }
</style>