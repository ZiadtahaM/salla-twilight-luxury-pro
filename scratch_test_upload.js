const fs = require('fs');
const FormData = require('form-data');
const axios = require('axios');

async function testUpload() {
    const cliCache = JSON.parse(fs.readFileSync('./node_modules/.salla-cli', 'utf8'));
    console.log('Cache:', cliCache);

    const form = new FormData();
    form.append('file', fs.createReadStream('src/views/layouts/master.twig'), 'master.twig');
    form.append('path', 'src/views/layouts');
    form.append('draft_id', cliCache.draft_id);

    try {
        const response = await axios.post(cliCache.upload_url, form, {
            headers: {
                ...form.getHeaders(),
                'Store-Identifier': cliCache.store_id
            }
        });
        console.log('Upload response status:', response.status);
        console.log('Upload response data:', response.data);
    } catch (err) {
        console.error('Upload failed with status:', err.response?.status);
        console.error('Upload response headers:', err.response?.headers);
        console.error('Upload response data:', JSON.stringify(err.response?.data, null, 2));
    }
}

testUpload();
