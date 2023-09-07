import path from "path";
import { build } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";
import cssInjectedByJsPlugin from "vite-plugin-css-injected-by-js";
import { fileURLToPath } from "url";
import { readdirSync } from "fs";

// component argument, if there is one
const componentName = process.argv[2];

// name of needed directories (also used in path_utils.py)
const COMPONENTS = "components";
const COMPILED = "compiled";

// resolve dir paths
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const componentsDir = path.resolve(path.join(__dirname, COMPONENTS));

// get names of local svelte components
const localSvelteComponents = readdirSync(componentsDir, {
  withFileTypes: true,
})
  .filter((item) => !item.isDirectory())
  .map((item) => {
    return item.name;
  });

// create build component config for vite build

let localComponentBuilds = localSvelteComponents.map((d) => {
  // if receive component argument, only build that component
  if (componentName && d !== componentName) {
    return;
  }
  // otherwise, build all components
  const fileBase = d.split(".svelte")[0];
  return {
    entry: `${COMPONENTS}/${d}`,
    fileName: fileBase,
    name: fileBase,
    formats: ["iife"],
  };
});

// filter to existing components (in case of building single component, many nulls may exist)
localComponentBuilds = localComponentBuilds.filter(Boolean);

// build each component
localComponentBuilds.forEach((lib) => {
  build({
    build: {
      rollupOptions: {
        output: {
          manualChunks: undefined,
        },
      },
      cssCodeSplit: true,
      outDir: `./${COMPILED}`,
      lib: {
        ...lib,
      },
      emptyOutDir: false,
      plugins: [svelte(), cssInjectedByJsPlugin()],
    },
  });
});
