<template>
	<div class="container search-results">
		<router-link to="/"><h1>search.dn42</h1></router-link>

		<SearchForm :value="query" />

		<i class="fa-regular fa-spinner fa-spin fa-2x mt-5" v-if="!data"></i>

		<p class="mt-3" v-if="data && data.error">{{ data.error }}</p>

		<div class="results-main" v-if="data && !data.error">
			<p class="small">Results {{ (page-1) * 15 + 1 }} to {{ Math.min((page-1) * 15 + 16, data.count) }} of {{ data.count }}</p>

			<div class="results">
				<SearchResult
					v-for="result of data.results"
					:key="result.url"
					:result="result"
					:query="query"
					:more="'more' in data && result.domain in data.more && data.more[result.domain].numFound > 1 ? data.more[result.domain] : null" />
			</div>

			<nav v-if="data.pages > 1" aria-label="Search results pagination">
				<ul class="pagination justify-content-center">
					<li v-if="page != 1" class="page-item">
						<router-link class="page-link" :to="{ path: '/search', query: { q: query, page: page-1, group_domains: group_domains } }">Previous</router-link>
					</li>
					<li v-for="(n, index) in data.pages" :key="index" :class="{ 'page-item': true, disabled: page == n }">
						<router-link class="page-link" :to="{ path: '/search', query: { q: query, page: n, group_domains: group_domains } }">{{ n }}</router-link>
					</li>
					<li v-if="page < data.pages" class="page-item">
						<router-link class="page-link" :to="{ path: '/search', query: { q: query, page: page+1, group_domains: group_domains } }">Next</router-link>
					</li>
				</ul>
			</nav>
		</div>
	</div>
</template>

<script>
import SearchForm from '~/components/SearchForm.vue'
import SearchResult from '~/components/SearchResult.vue'

export default {
	components: {
		SearchForm,
		SearchResult
	},

	created() {
		this.$watch(
			() => this.$route.query, (toQuery, previousQuery) => {
				this.data = null
				this.page = Number(toQuery.page) || 1
				this.query = toQuery.q
				this.group_domains = toQuery.group_domains || true

				const config = useRuntimeConfig()
				$fetch(`${config.API_BASE}/search?q=${this.query}&page=${this.page}&group_domains=${this.group_domains}`).then((data) => {
					this.data = data
				})
			}
		)
	},
}
</script>

<script setup>
import { ref } from 'vue'

const config = useRuntimeConfig()
const route = useRoute()
const router = useRouter()

if(route.query.q) {
	useMeta({ title: `${route.query.q} — DN42 search` })
} else {
	useMeta({ title: `DN42 search` })
}

let query = ref(route.query.q || '')
let page = ref(route.query.page ? Number(route.query.page) : 1)
let group_domains = ref(route.query.group_domains || true)

let { data } = await useAsyncData('searchResults', () => $fetch(`${config.API_BASE}/search?q=${route.query.q}&page=${route.query.page || 1}&group_domains=${route.query.group_domains || true}`), { server: false })
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
		}
	}
}
</style>
