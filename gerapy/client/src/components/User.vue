<template>
	<div id="user">
		<el-dropdown size="mini" split-button type="primary">
			<el-dropdown-menu slot="dropdown">
				<el-dropdown-item><span @click="singOut">{{ $lang.buttons.logout }}</span></el-dropdown-item>
			</el-dropdown-menu>
		</el-dropdown>
	</div>
</template>

<script>


	export default {
		name: 'User',
		methods: {
			singOut() {
				this.$store.commit('clearToken')
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