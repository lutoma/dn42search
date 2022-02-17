<template>
	<div class="container search-results">
		<router-link to="/"><h1>search.dn42</h1></router-link>

		<SearchForm :value="query" />

		<i class="fa-regular fa-spinner fa-spin fa-2x mt-5" v-if="!data"></i>

		<p class="mt-3" v-if="data && data.error">{{ data.error }}</p>

		<template v-if="data && !data.error">
			<p class="small results-count">{{ data.count }} results</p>

			<div class="results">
				<div class="result" v-for="result of data.results">
					<small class="text-muted"><a :href="result.url" rel="nofollow noopener" target="_blank" class="text-muted">{{ result.url }}</a></small>
					<!--<small class="text-muted"><a href="{{ result.url }}" rel="nofollow noopener" target="_blank" class="text-muted">{{ result.url }}</a> - Size: {{ result.size }} / Last indexed: {{ result.last_indexed }}</small>-->
					<h5><a :href="result.url" rel="nofollow noopener" target="_blank">
						<template v-if="result.title">{{ result.title }}</template>
						<em v-else>No page title</em>
					</a></h5>
					<p class="excerpt" v-if="result.excerpt">{{ result.excerpt }}</p>
				</div>
			</div>
		</template>
	</div>
</template>

<script>
import SearchForm from '~/components/SearchForm.vue'

export default {
	components: {
		SearchForm
	},

	data() {
		return {
			'data': [],
			'query': 'lutoma'
		}
	},

	created() {
		this.$watch(
			() => this.$route.query, (toQuery, previousQuery) => {
				this.data = null

				const config = useRuntimeConfig()
				$fetch(`${config.API_BASE}/search/?q=${toQuery.q}`).then((data) => {
					this.data = data
				})
			}
		)
	},
}
</script>

<script setup>
const config = useRuntimeConfig()
const route = useRoute()
const router = useRouter()

const _query = route.query.q ? route.query.q : ''
const query = ref(_query)

const { data } = await useAsyncData('searchResults', () => $fetch(`${config.API_BASE}/search/?q=${_query}`), { server: false })
</script>

<style lang="scss">
@import 'bootstrap/scss/functions';
@import 'bootstrap/scss/variables';

.search-results {
	h1 {
		font-weight: 200;
		font-size: 2rem;
		margin-top: 1rem;
		margin-bottom: 1rem;
		color: $body-color;
	}

	form {
		display: flex;
		flex-direction: row;

		input {
			max-width: 100vw;
			width: 30rem;
		}

		button {
			margin-left: 1rem;
			padding-left: 1.5rem;
			padding-right: 1.5rem;
		}
	}

	.results-count {
		margin-top: .5rem;
	}

	.results {
		 max-width: 700px;
		 margin-top: 2rem;

		 .result {
		 	margin-bottom: 2rem;

			h5 {
				margin-top: .3rem;
				margin-bottom: .3rem;
			}

			.excerpt {
				font-size: 0.95rem;
			}
		}
	}
}
</style>
