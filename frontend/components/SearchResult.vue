<template>
	<div class="result">
		<div class="primary">
			<div class="small text-muted text-truncate"><a :href="result.url" rel="nofollow noopener" target="_blank" class="text-muted">{{ prettyPath(result.url) }}</a></div>
			<h5><a :href="result.url" rel="nofollow noopener" target="_blank">
				<template v-if="result.title">{{ result.title }}</template>
				<em v-else>No page title</em>
			</a></h5>
			<p class="excerpt" v-if="result.excerpt">{{ result.excerpt }}</p>
		</div>

		<div class="more" v-if="more">
			<p v-for="mresult of more.docs" :key="mresult.url">
				<a :href="mresult.url" rel="nofollow noopener" target="_blank">{{ mresult.title }}</a>
				<p class="small">{{ mresult.excerpt }}</p>
			</p>

			<p v-if="more.numFound > more.docs.length" class="small">
				<router-link :to="{ path: '/search', query: {q: `${query} AND hostname:${result.hostname}`, group_hostnames: false } }">Show all {{ more.numFound }} results from {{ result.hostname }}</router-link>
			</p>
		</div>
	</div>
</template>

<script>
export default {
	props: ['query', 'result', 'more'],

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
	}
}
</script>

<style lang="scss">
 .result {
 	margin-bottom: 2rem;

	h5 {
		margin-top: .3rem;
		margin-bottom: .3rem;
	}

	.excerpt {
		font-size: 0.95rem;
	}

	.more {
		margin-top: .5rem;
		padding-left: 1rem;
	}
}
</style>
