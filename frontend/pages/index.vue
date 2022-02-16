<template>
	<div class="container index">
		<h1>search.dn42</h1>
		<p class="small" v-if="data">Search {{ data.index_size }} indexed documents on dn42 sites</p>

		<div>
			<form type="GET" action="/search">
				<div class="form-floating">
					<input type="text" name="q" placeholder="Search query" class="form-control" id="query" autofocus>
					<label for="query"><i class="fa-regular fa-magnifying-glass"></i> Search query</label>
				</div>

				<button class="btn btn-primary" type="submit">Search</button>
			</form>

			<p class="small">Try <router-link to='/search?q=url%3Alg.*+OR+title%3A"*looking+glass*"'><code>url:lg.* OR title:"*looking glass*"</code></router-link></p>
		</div>
	</div>
</template>

<script setup>
const { data } = await useAsyncData('index_size', () => $fetch('http://localhost:8000'), { server: false })
</script>
