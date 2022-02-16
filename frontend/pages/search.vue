<template>
	<div class="container search-results">
		<router-link to="/"><h1>search.dn42</h1></router-link>

		<form type="GET" action="/search">
			<input type="text" name="q" placeholder="Search query" :value="query" class="form-control" id="query">
			<button class="btn btn-primary" type="submit">Search</button>
		</form>

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


<script setup>
const config = useRuntimeConfig()
const route = useRoute()
const router = useRouter()

const _query = route.query.q ? route.query.q : ''
const query = ref(_query)

const { data } = await useAsyncData('searchResults', () => $fetch(`${config.API_BASE}/search/?q=${_query}`), { server: false })
</script>
