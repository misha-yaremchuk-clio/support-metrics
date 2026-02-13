
const fs = require('fs');

try {
    const data = JSON.parse(fs.readFileSync('/Users/mishayaremchuk/swarm-analysis/swarm-data.json', 'utf8'));
    console.log("Successfully parsed JSON.");

    let errorCount = 0;
    const fieldsToSanitize = ['swarm_type', 'specialist_asking'];

    data.forEach((d, i) => {
        fieldsToSanitize.forEach(field => {
            const val = d[field];
            if (val && typeof val === 'string' && val.includes('"')) {
                console.error(`Index ${i}: ${field} contains double quote: ${val}`);
                errorCount++;
            }
        });

        // Also check if any string ends with unescaped quote that might break attribute parsing
    });

    if (errorCount === 0) {
        console.log("No issues with quotes in critical fields.");
    } else {
        console.log(`Found ${errorCount} data validation errors.`);
    }

} catch (e) {
    console.error("JSON Parse Error:", e);
}
