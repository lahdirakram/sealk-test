export class DummyAI {
    static async getCompanyAttractiveness(companyId: string): Promise<{ id: string; score: number }> {
        return new Promise((r) => {
            setTimeout(() => {
                r({
                    id: companyId,
                    score: Math.round(Math.random() * 100) / 100,
                });
            }, 1000);
        });
    }
}