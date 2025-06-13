import { IntroInfo } from './components/IntroInfo';
import { Vacancies } from './components/Vacancies';

export default function Root() {
    return (
        <div className="min-h-screen bg-background text-on-background flex flex-col relative overflow-hidden">
            <div className="flex-1 flex flex-col z-10 relative">
                <IntroInfo />
                <Vacancies />
            </div>
        </div>
    );
}
