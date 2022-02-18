<template>
	<div class="container index">
		<h1>search.dn42</h1>
		<p class="small">Search <span v-if="data">{{ data.index_size }}</span><span v-else>...</span> indexed documents on dn42 sites</p>

		<div>
			<SearchForm autofocus />

			<p class="small">Try <router-link to='/search?q=url%3Alg.*+OR+title%3A"*looking+glass*"'><code>url:lg.* OR title:"*looking glass*"</code></router-link></p>
		</div>
	</div>
</template>

<script>
import SearchForm from '~/components/SearchForm.vue'

export default {
	components: {
		SearchForm
	}
}
</script>

<script setup>
useMeta({ title: 'DN42 search' })

const config = useRuntimeConfig()
const { data } = await useAsyncData('index_size', () => $fetch(config.API_BASE), { server: false })
</script>

<style lang="scss">
.index {
	display: flex;
	flex-direction: column;
	align-items: center;

	h1 {
		font-weight: 200;
		font-size: 5rem;
		margin-top: 10rem;
		margin-bottom: 1rem;
	}

	.search-form {
		margin-top: 4rem;
		margin-bottom: .5rem;
		width: 700px;
		max-width: 95vw;
	}
}
</style>
