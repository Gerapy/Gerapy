<template>
	<div class="panel">
		<el-dialog :visible.sync="createProjectDialog" size="tiny">
			<el-form>
				<el-form-item :label="$lang.columns.name">
					<el-input
						v-model="projectName" class="inline" :placeholder="$lang.columns.name"
						size="small">
					</el-input>
				</el-form-item>
			</el-form>
			<div slot="footer">
				<el-button @click="createProjectDialog=false" size="small">{{ $lang.buttons.cancel }}
				</el-button>
				<el-button @click="onCreateProject()"
									 type="primary" size="small">{{ $lang.buttons.create }}
				</el-button>
			</div>
		</el-dialog>
		<panel-title :title="$lang.objects.project">
			<el-button @click.stop="onRefresh" size="mini">
				<i class="fa fa-refresh"></i>
				刷新
			</el-button>
			<el-button type="primary" size="mini" @click="createProjectDialog=true">
				<i class="fa fa-plus"></i>
				{{ $lang.buttons.create }}
			</el-button>
		</panel-title>
		<div class="panel-body">
			<el-table
				:data="projects"
				:empty-text="$lang.messages.noData"
				v-loading="loading"
				:element-loading-text="$lang.messages.loading"
				:style="{width: '100%;'}">
				<el-table-column
					align="center"
					prop="name"
					:label="$lang.columns.name"
					width="150">
				</el-table-column>
				<el-table-column
					align="center"
					:label="$lang.columns.configurable"
					width="150">
					<template slot-scope="props" v-if="buildInfos[props.row.name]">
						<span v-if="buildInfos[props.row.name]['configurable']">
							<el-button type="primary" icon="el-icon-check" size="mini" round></el-button>
            </span>
						<span v-else>
							<el-button type="primary" icon="el-icon-close" size="mini" round></el-button>
            </span>
					</template>
				</el-table-column>
				<el-table-column
					align="center"
					:label="$lang.columns.built"
					width="80">
					<template slot-scope="props" v-if="buildInfos[props.row.name]">
						<span v-if="buildInfos[props.row.name]['egg']">
							<el-button type="primary" icon="el-icon-check" size="mini" round></el-button>
            </span>
						<span v-else>
							<el-button type="primary" icon="el-icon-close" size="mini" round></el-button>
            </span>
					</template>
				</el-table-column>
				<el-table-column
					align="center"
					:label="$lang.columns.builtAt"
					width="200">
					<template slot-scope="props">
            <span v-if="buildInfos[props.row.name]">
              {{ buildInfos[props.row.name]['built_at'] }}
            </span>
					</template>
				</el-table-column>
				<el-table-column
					align="center"
					:label="$lang.columns.description"
					width="200">
					<template slot-scope="props">
            <span v-if="buildInfos[props.row.name]">
              {{ buildInfos[props.row.name]['description'] }}
            </span>
					</template>
				</el-table-column>
				<el-table-column
					align="center"
					:label="$lang.columns.operations">
					<template slot-scope="props">
						<router-link :to="{name: 'projectConfigure', params: {name: props.row.name}}" tag="span"
												 v-if="buildInfos[props.row.name] && buildInfos[props.row.name]['configurable']">
							<el-button type="warning" size="mini">
								<i class="fa fa-edit"></i>
								{{ $lang.buttons.configure }}
							</el-button>
						</router-link>
						<router-link :to="{name: 'projectEdit', params: {name: props.row.name}}" tag="span" v-else>
							<el-button type="warning" size="mini">
								<i class="fa fa-edit"></i>
								{{ $lang.buttons.edit }}
							</el-button>
						</router-link>
						<router-link :to="{name: 'projectDeploy', params: {name: props.row.name}}" tag="span">
							<el-button type="success" size="mini">
								<i class="fa fa-cloud-upload"></i>
								{{ $lang.buttons.deploy }}
							</el-button>
						</router-link>
						<!--<router-link :to="{name: 'projectMonitor', params: {name: props.row.name}}" tag="span">-->
						<!--<el-button type="info" size="mini">-->
						<!--<i class="fa fa-podcast"></i>-->
						<!--监控-->
						<!--</el-button>-->
						<!--</router-link>-->
						<el-button type="danger" size="mini" @click="onSingleDelete(props.row.name)">
							<i class="fa fa-remove"></i>
							{{ $lang.buttons.delete }}
						</el-button>
					</template>
				</el-table-column>
			</el-table>
		</div>
	</div>
</template>
<script>
	import PanelTitle from '../../components/PanelTitle'

	export default {
		name: 'projectIndex',
		data() {
			return {
				createProjectDialog: false,
				projectName: null,
				projects: [],
				loading: false,
				buildInfos: {}
			}
		},
		components: {
			PanelTitle,
		},
		created() {
			this.getProjectData()
		},
		methods: {
			getBuildInfo(name) {
				this.$http.get(this.format(this.$store.state.url.project.build, {
					name: name
				})).then(({data: data}) => {
					this.$set(this.buildInfos, name, data)
				})
			},
			getProjectData() {
				this.loading = true
				this.$http.get(this.$store.state.url.project.index
				).then(({data: projects}) => {
					this.projects = projects
					this.loading = false
					this.projects.forEach((project) => {
						this.getBuildInfo(project.name)
					})
				}).catch(() => {
					this.loading = false
				})
			},
			onRefresh() {
				this.$message.info(this.$store.getters.$lang.messages.loading)
				this.getProjectData()
			},
			onDeleteProject(name) {
				this.loading = true
				this.$http.post(this.format(this.$store.state.url.project.remove, {
					name: name
				})).then(() => {
					this.$message.success(this.$store.getters.$lang.messages.successDelete)
					this.loading = false
					this.getProjectData()
				}).catch(() => {
					this.loading = false
					this.$message.error(this.$store.getters.$lang.messages.errorDelete)
				})
			},
			onSingleDelete(name) {
				this.$confirm(this.$store.getters.$lang.messages.confirm, this.$store.getters.$lang.buttons.confirm, {
					confirmButtonText: this.$store.getters.$lang.buttons.yes,
					cancelButtonText: this.$store.getters.$lang.buttons.no,
					type: 'warning'
				}).then(() => {
					this.onDeleteProject(name)
				})
			},
			onCreateProject() {
				this.$http.post(this.$store.state.url.project.create, {
					name: this.projectName
				}).then(() => {
					this.$message.success(this.$store.getters.$lang.messages.successSave)
					this.loading = false
					this.$router.push({name: 'projectConfigure', params: {name: this.projectName}})
				}).catch(() => {
					this.loading = false
					this.$message.error(this.$store.getters.$lang.messages.errorSave)
				})
			}
		}
	}
</script>
