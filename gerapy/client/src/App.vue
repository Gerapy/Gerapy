<template>
	<section class="body-wrap">
		<transition name="fade" mode="out-in">
			<div class="view-page">
				<left></left>
				<wrapper>
					<router-view></router-view>
				</wrapper>
			</div>
		</transition>
	</section>
</template>

<script>
	import Wrapper from './components/Wrapper'
	import Left from './components/Left'

	export default {
		name: 'app',
		components: {
			Wrapper,
			Left
		}
	}
</script>

<style>
	#app {
		font-family: 'Avenir', Helvetica, Arial, sans-serif;
		-webkit-font-smoothing: antialiased;
		-moz-osx-font-smoothing: grayscale;
		text-align: center;
		color: #2c3e50;
		margin-top: 60px;
	}
</style>
