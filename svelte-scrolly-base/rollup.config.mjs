import svelte from 'rollup-plugin-svelte';
import sveltePreprocess from 'svelte-preprocess';
import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import terser from '@rollup/plugin-terser';

export default [
	{
		input: 'src/main.js',
		output: {
			sourcemap: false,
			format: 'iife',
			file: '/projects/temp.dist.js',
			name: 'scrolly'
		},
		plugins: [
			svelte({
				emitCss: false,
				preprocess: sveltePreprocess()
			}),
			resolve({
				browser: true,
				dedupe: ['svelte'],
				exportConditions: ['svelte']
			}),
			commonjs(),
			terser()
		],
	}
];