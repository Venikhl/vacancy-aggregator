export type Filters = {
  title: string;
  salary_min: number;
  salary_max: number;
  experience_categories: { name: string }[];
  location: { region: string } | null;
};
