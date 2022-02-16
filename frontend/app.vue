<template>
	<div class="pt-0 d-flex flex-column h-100">
		<main class="flex-shrink-0">
			<NuxtLayout>
				<NuxtPage/>
			</NuxtLayout>
		</main>

		<footer class="footer mt-auto pt-5 pb-4">
			<div class="container">
				<span class="text-muted small"><a href="https://lutoma.org/contact">Contact</a></span>
			</div>
		</footer>
	</div>
</template>

<style lang="scss">
@import 'typeface-fira-sans/index';
@import '@fortawesome/fontawesome-pro/css/fontawesome';
@import '@fortawesome/fontawesome-pro/css/light';
@import '@fortawesome/fontawesome-pro/css/thin';
@import '@fortawesome/fontawesome-pro/css/regular';

$font-family-sans-serif: 'Fira Sans', system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", "Liberation Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji" !default;
@import 'bootstrap/scss/bootstrap';

html, body, #__nuxt {
	width: 100%;
	height: 100%;
}

body {
	//padding: 2rem 0;
}

a {
	text-decoration: none;

	&:hover {
		text-decoration: underline;
	}
}


footer {
	a {
		color: $text-muted;
	}
}

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

	form {
		display: flex;
		flex-direction: row;
		margin-top: 4rem;
		margin-bottom: .5rem;

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
}

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
