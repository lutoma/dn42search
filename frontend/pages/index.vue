<template>
	<div class="container index">
		<h1 class="display-1 mb-3">search.dn42</h1>
		<p class="small">Search <span v-if="data">{{ data.index_size }}</span><span v-else>...</span> indexed documents on dn42 sites</p>

		<div>
			<SearchForm autofocus />

			<p class="small" v-show="!showOperatorsInfo"><a @click.stop.prevent="showOperatorsInfo = true" role="button" href="#operatorsInfo" :aria-expanded="showOperatorsInfo" aria-controls="operatorsInfo">Show all supported search operators</a></p>

			<div v-show="showOperatorsInfo" id="operatorsInfo" class="mt-5">
				<div class="card card-body">
					<h5>Wildcard matches</h5>
					<p>You can use <code>?</code> to match a single character, and <code>*</code> to match any number of characters.</p>

					<h5>Boolean operators</h5>
					<p>DN42 search supports the <code>AND</code> and <code>OR</code> modifiers for queries. By default, all search terms are OR-ed. In addition, you can prepend search terms with <code>+</code> to require them to be present and with <code>-</code> to require their absence. You can group terms together by enclosing them with <code>"</code>.</p>

					<h5>Fields</h5>
					<p>By default, DN42 search will search the url, title, excerpt and text of pages for a match. However, you can also manually specify a field to search:</p>
					<ul>
						<li><code>url:</code> -  Full URL of the page, e.g. <code>url:wiki.dn42/internal/</code></li>
						<li><code>title:</code> -  Full URL of the page, e.g. <code>tite:"DN42 wiki"</code></li>
						<li><code>excerpt:</code> -  Excerpt of page text, either from the description text or automatically extracted, e.g. <code>excerpt:peering</code></li>
						<li><code>text:</code> -  The full text content of the page, e.g. <code>text:peering</code></li>
						<li><code>mime:</code> -  MIME type sent by the server, e.g. <code>mime:"audio/*"</code></li>
						<li><code>server:</code> -  Server header, e.g. <code>server:caddy</code></li>
						<li><code>links:</code> -  Outgoing links from a page, e.g. <code>links:wiki.dn42 AND -url:wiki.dn42</code></li>
						<li><code>size:</code> -  Size in bytes, e.g. <code>size:[100000 TO 200000]</code></li>
						<li><code>last_indexed:</code> -  Date and time of last indexing, e.g. <code>last_indexed:[NOW-5HOURS TO NOW]</code></li>
					</ul>
				</div>
			</div>
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
			showOperatorsInfo: false
		}
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
		margin-top: 10rem;
	}

	.search-form {
		margin-top: 4rem;
		margin-bottom: .5rem;
		width: 700px;
		max-width: 95vw;
	}

	#operatorsInfo {
		max-width: 700px;
	}
}
</style>
