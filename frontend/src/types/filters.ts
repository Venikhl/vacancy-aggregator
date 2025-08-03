export type Filters = {
    title: string | null;
    salary_min: number | null;
    salary_max: number | null;
    experience_categories: {
        name: string;
        years_of_experience: number | null;
    }[];
    location: { region: string } | null;
    date_published_from: null;
    date_published_to: null;
};

export type ResumeFilters = {
    title: string | null;
    location: { region: string } | null;
    salary_min: number | null;
    salary_max: number | null;
    experience_categories: {
        name: string;
        years_of_experience: number | null;
    }[];
    skills: string[];
};
