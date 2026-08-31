/**
 * Use decodeURI() to decode the instruction prior to posting to PR
 * (URI Encoding was applied in create-instruction.js to handle the backtick character)
 * @param {Object} github - github object
 * @param {Object} context - context object
 * @param {Number} issueNum - the number of the issue where the post will be made
 * @param {String} instruction - commandline instructions
 */
async function main({ github, context }, { issueNum, instruction }) {
    try {
        await github.rest.issues.createComment({
            owner: context.repo.owner,
            repo: context.repo.repo,
            issue_number: issueNum,
            body: decodeURI(instruction),
        });
        return true;
    } catch (err) {
        throw new Error(err);
    }
}

module.exports = main
