export class DummyAI {
    static async getCompanyAttractiveness(companySymbol: string): Promise<{ id: string; score: number }> {
        return new Promise((r) => {
            setTimeout(() => {
                r({
                    id: companySymbol,
                    score: Math.round(Math.random() * 100) / 100,
                });
            }, 1000);
        });
    }
}