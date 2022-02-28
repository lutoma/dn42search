<template>
	<div class="pt-0 d-flex flex-column h-100">
		<main class="flex-shrink-0">
			<NuxtLayout>
				<NuxtPage/>
			</NuxtLayout>
		</main>

		<footer class="footer mt-auto pt-5 pb-4">
			<div class="container">
				<span class="text-muted small"><a href="https://lutoma.org/contact">Contact</a> / <a href="https://github.com/lutoma/dn42search">Source code</a></span>
			</div>
		</footer>
	</div>
</template>

<style lang="scss">
@import 'typeface-fira-sans/index';
@import '@fortawesome/fontawesome-pro/css/fontawesome';
@import '@fortawesome/fontawesome-pro/css/regular';

$font-family-sans-serif: 'Fira Sans', system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", "Liberation Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji" !default;

@import 'bootstrap/scss/functions';
@import 'bootstrap/scss/variables';
@import 'bootstrap/scss/mixins';
@import 'bootstrap/scss/utilities';
@import 'bootstrap/scss/root';
@import 'bootstrap/scss/reboot';
@import 'bootstrap/scss/type';
@import 'bootstrap/scss/containers';
@import 'bootstrap/scss/grid';
@import 'bootstrap/scss/forms';
@import 'bootstrap/scss/buttons';
@import 'bootstrap/scss/pagination';
@import 'bootstrap/scss/helpers';
@import 'bootstrap/scss/utilities/api';

html, body, #__nuxt {
	width: 100%;
	height: 100%;
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
</style>
