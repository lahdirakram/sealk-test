import { DummyAI } from '../common/dummy-ai';

async function main() {
    const score = await DummyAI.getCompanyAttractiveness('123');
    console.log(score);
}

main()
    .then(() => {
        console.log('Done');
    })
    .catch((err) => {
        console.log('Error', err);
    });