<template>
	<div class="container search-results">
		<router-link to="/"><h1>search.dn42</h1></router-link>

		<SearchForm :value="query" />

		<i class="fa-regular fa-spinner fa-spin fa-2x mt-5" v-if="!data"></i>

		<p class="mt-3" v-if="data && data.error">{{ data.error }}</p>

		<div class="results-main" v-if="data && !data.error">
			<p class="small">Results {{ (page-1) * 15 + 1 }} to {{ Math.min((page-1) * 15 + 16, data.count) }} of {{ data.count }}</p>

			<div class="results">
				<div class="result" v-for="result of data.results">
					<div class="small text-muted text-truncate"><a :href="result.url" rel="nofollow noopener" target="_blank" class="text-muted">{{ prettyPath(result.url) }}</a></div>
					<!--<small class="text-muted"><a href="{{ result.url }}" rel="nofollow noopener" target="_blank" class="text-muted">{{ result.url }}</a> - Size: {{ result.size }} / Last indexed: {{ result.last_indexed }}</small>-->
					<h5><a :href="result.url" rel="nofollow noopener" target="_blank">
						<template v-if="result.title">{{ result.title }}</template>
						<em v-else>No page title</em>
					</a></h5>
					<p class="excerpt" v-if="result.excerpt">{{ result.excerpt }}</p>
				</div>
			</div>

			<nav v-if="data.pages > 1" aria-label="Search results pagination">
				<ul class="pagination justify-content-center">
					<li v-if="page != 1" class="page-item">
						<a class="page-link" href="#" tabindex="-1" aria-disabled="true">Previous</a>
					</li>
					<li v-for="(n, index) in data.pages" :key="index" :class="{ 'page-item': true, disabled: page == n }">
						<router-link class="page-link" :to="{ path: '/search', query: { q: query, page: n } }">{{ n }}</router-link>
					</li>
					<li v-if="page < data.pages" class="page-item">
						<a class="page-link" href="#">Next</a>
					</li>
				</ul>
			</nav>
		</div>
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
			'page': 1
		}
	},

	methods: {
		prettyPath(_url) {
			const url = new URL(_url)
			let path = url.pathname.split('/').filter(n => n)
			if(!path.length) {
				return url.origin
			} else {
				path = path.map(decodeURI)
				return `${url.origin} › ${path.join(' › ')}`
			}
		}
	},

	created() {
		this.$watch(
			() => this.$route.query, (toQuery, previousQuery) => {
				this.data = null
				this.page = toQuery.page || 1

				const config = useRuntimeConfig()
				$fetch(`${config.API_BASE}/search/?q=${toQuery.q}&page=${toQuery.page || 1}`).then((data) => {
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

if(route.query.q) {
	useMeta({ title: `${route.query.q} — DN42 search` })
} else {
	useMeta({ title: `DN42 search` })
}

const query = ref(route.query.q || '')
const page = ref(route.query.page ? route.query.page : 1)

const { data } = await useAsyncData('searchResults', () => $fetch(`${config.API_BASE}/search/?q=${route.query.q }&page=${route.query.page || 1}`), { server: false })
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

	.search-form {
		max-width: 700px;
	}

	.results-main {
		max-width: 700px;
		margin-top: .5rem;

		.results {
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
}
</style>
