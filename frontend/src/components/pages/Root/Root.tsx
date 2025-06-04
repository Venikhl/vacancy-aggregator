import { TopPanel } from './components/TopPanel';
import { IntroInfo } from './components/IntroInfo';
import { Vacancies } from './components/Vacancies';

export default function Root() {
    return (
        <div className="min-h-screen bg-black text-white flex flex-col relative overflow-hidden">
            <TopPanel />

            <div className="flex-1 flex flex-col z-10 relative">
                <IntroInfo />
                <Vacancies />
            </div>
        </div>
    );
}
