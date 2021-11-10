var fs = require('fs').promises;
var parse = require('csv-parse/lib/sync');
var stringify = require('csv-stringify');
    

(async function () {
    const fileContent = await fs.readFile('../PRs_dataset/project_list.csv');
    const records = parse(fileContent, {columns: true});
    let index = 0;
    const cleanedData = records.reduce((acc, item) => {
        if (!item['PR Number'] || item['PR Number'] === '0' || item['PR Number'] === 0) {
            return acc;
        }
        const endDate = item['Project Enddate'].split('/');
        const endYear = parseInt(endDate[2]);
        const endMonth = parseInt(endDate[1]);
        const endDay = parseInt(endDate[0]);
        const prDate = item['First PR Created Time'].split(' ')[0].split('-');
        const prYear = parseInt(prDate[0]);
        const prMonth = parseInt(prDate[1]);
        const prDay = parseInt(prDate[2]);
        if (prYear < endYear || (prYear === endYear && prMonth < endMonth) ||
        (prYear === endYear && prMonth === endMonth && prDay < endDay)) {
            index++;
            item[''] = index;
            return [...acc, item];
        }
        return acc;
    }, []);

    stringify(cleanedData, {
        header: true
    }, function (err, output) {
        fs.writeFile('../PRs_dataset/cleaned_project_list.csv', output);
    })
})();