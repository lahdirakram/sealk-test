import { DummyAI } from '../common/dummy-ai';

async function main() {
    const score = await DummyAI.getCompanyAttractiveness('GOOGL');
    console.log(score);
}

main()
    .then(() => {
        console.log('Done');
    })
    .catch((err) => {
        console.log('Error', err);
    });