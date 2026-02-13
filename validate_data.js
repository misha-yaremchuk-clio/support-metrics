
const fs = require('fs');

try {
    const data = JSON.parse(fs.readFileSync('/Users/mishayaremchuk/swarm-analysis/swarm-data.json', 'utf8'));
    console.log("Successfully parsed JSON.");

    let errorCount = 0;
    const maxErrors = 10;

    data.forEach((d, i) => {
        if (!d.start_date) {
            console.error(`Index ${i}: Missing start_date`);
            errorCount++;
        }

        // Simulate getDifficultyLabel
        const score = d.consult_complexity;
        if (score !== undefined && score !== null && typeof score !== 'number' && typeof score !== 'string') {
            console.error(`Index ${i}: consult_complexity is ${typeof score}: ${score}`);
            errorCount++;
        }

        // Simulate getPrereqScore
        const score2 = d.initial_consult_quality;
        if (score2 !== undefined && score2 !== null && typeof score2 !== 'number' && typeof score2 !== 'string') {
            console.error(`Index ${i}: initial_consult_quality is ${typeof score2}: ${score2}`);
            errorCount++;
        }

        // Check for double quotes in descriptions that might break tooltip if not escaped properly
        // Actually, replace(/"/g, '&quot;') handles this, but let's check if anything weird happens.
    });

    if (errorCount === 0) {
        console.log("No critical data errors found.");
    }

} catch (e) {
    console.error("JSON Parse Error:", e);
}
