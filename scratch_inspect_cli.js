const fs = require('fs');
const content = fs.readFileSync('D:/nodejs/node_global/node_modules/@salla.sa/cli/dist/index.js', 'utf8');

console.log('File size:', content.length);

let searchTerms = ['ThemeAPI.preview', 'themeId', 'preview_url', 'draft_id', 'upload_url'];
for (const term of searchTerms) {
    let pos = 0;
    let count = 0;
    while ((pos = content.indexOf(term, pos)) !== -1) {
        count++;
        console.log(`\n=== Found "${term}" #${count} at ${pos} ===`);
        console.log(content.substring(Math.max(0, pos - 150), Math.min(content.length, pos + 350)));
        pos += term.length;
        if (count >= 5) break;
    }
}
