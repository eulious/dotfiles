import { readdir, readFile, writeFile } from 'fs/promises';
import { promisify } from 'util';
import { exec } from 'child_process';
import { join } from 'path';
(async () => {
  await promisify(exec)('npx vite build');
  const fns = await readdir('dist/assets');
  const lines = (await readFile(join('dist/index.html'))).toString().split('\n');
  for (const [pattern, tag] of [
    [/index.*.js/, 'script'],
    [/index.*.css/, 'style']
  ]) {
    const fn = fns.filter((fn) => fn.match(pattern)).pop() ?? '';
    const script = await readFile(join('dist/assets', fn));
    for (let i = 0; i < lines.length; i++) {
      if (lines[i].match(fn)) lines[i] = `<${tag}>${script}</${tag}>`;
      else lines[i] = lines[i].trim();
    }
  }
  const html = lines.reduce((a, b) => a + b.trim());
  await writeFile(`compat.html`, html);
})();
