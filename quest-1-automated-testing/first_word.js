// Checks on the first word of a reply, used by promptfoo-v3-a1.yaml
const firstWord = (output) => (output.trim().match(/[A-Za-z]+/) || [''])[0].toLowerCase();

module.exports.notYes = (output) => firstWord(output) !== 'yes';
module.exports.isYes = (output) => firstWord(output) === 'yes';
