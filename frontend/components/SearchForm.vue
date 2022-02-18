<template>
	<form type="GET" action="/search" class="search-form">
		<div class="form-floating">
			<input type="text" name="q" placeholder="Search query" class="form-control" id="query" v-model="int_value" :autofocus="autofocus">
			<label for="query"><i class="fa-regular fa-magnifying-glass"></i> Search query</label>
		</div>

		<button class="btn btn-primary" type="submit" @click.stop.prevent="submit()">Search</button>
	</form>
</template>

<script>
export default {
	props: ['value', 'autofocus'],
	emits: ['searched'],

	data() {
		return {
			int_value: this.value || ''
		}
	},

	methods: {
		submit() {
			this.$router.push({ path: '/search', query: { q: this.int_value } })
			this.$emit('searched', this.int_value)
		}
	}
}
</script>

<style lang="scss">
.search-form {
	display: flex;
	flex-direction: row;

	.form-floating {
		flex-grow: 1;

		input {
			width: 100%;
		}
	}

	button {
		margin-left: 1rem;
		padding-left: 1.5rem;
		padding-right: 1.5rem;
	}
}
</style>
