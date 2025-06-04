import { Badge } from '@/components/ui/badge.tsx';
import { PhoneIcon } from 'lucide-react';

interface VacancyProps {
    company: string;
    title: string;
    description: string;
    tags: string[];
    phone: string;
}

const Vacancy = ({
    company,
    title,
    description,
    tags,
    phone,
}: VacancyProps) => {
    return (
        <div className="bg-fore border border-primary-active text-on-primary rounded-xl p-4 flex flex-col gap-2 shadow-md hover:shadow-orange-500/30 transition-shadow">
            <div className="flex items-center gap-2">
                <span className="bg-primary text-on-primary text-xs px-2 py-1 rounded-full font-semibold">
                    {company}
                </span>
            </div>
            <h3 className="text-lg font-semibold">{title}</h3>
            <p className="text-sm text-gray-400">{description}</p>
            <div className="flex flex-wrap gap-2 mt-2 text-xs">
                {tags.map((tag, index) => (
                    // <span className="bg-black border border-gray-500 px-2 py-1 rounded-full" key={index}>{tag}</span>
                    <Badge key={index} className="bg-primary/50 rounded-full">
                        {tag}
                    </Badge>
                ))}
            </div>
            <div className="flex items-center gap-x-2 mt-2 ">
                <PhoneIcon size={12} className="text-secondary" />
                <span className="text-xs font-semibold text-secondary">
                    {phone}
                </span>
            </div>
        </div>
    );
};

export default Vacancy;
