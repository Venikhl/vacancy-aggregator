import { Badge } from '@/components/ui/badge.tsx';

interface VacancyProps {
    company: string;
    title: string;
    description: string;
    tags: string[];
    url: string;
}

const Vacancy = ({ company, title, description, tags, url }: VacancyProps) => {
    return (
        <a
            href={url}
            target="_blank"
            rel="noopener noreferrer"
            className="h-full"
        >
            <div className="bg-fore border border-primary text-on-foreground rounded-xl p-4 flex flex-col gap-2 shadow-md hover:shadow-primary/30 transition-shadow h-full">
                <div className="flex items-center gap-2">
                    <span className="bg-primary text-on-primary text-xs px-2 py-1 rounded-full font-semibold">
                        {company}
                    </span>
                </div>
                <h3 className="text-lg font-semibold">{title}</h3>
                <p className="text-sm text-secondary flex-1 overflow-hidden text-ellipsis">
                    <span className="line-clamp-[10] block">{description}</span>
                </p>
                <div className="flex flex-wrap gap-2 mt-2 text-xs">
                    {tags.map((tag, index) => (
                        <Badge
                            key={index}
                            className="bg-primary/90 rounded-full"
                        >
                            {tag}
                        </Badge>
                    ))}
                </div>
            </div>
        </a>
    );
};

export default Vacancy;
