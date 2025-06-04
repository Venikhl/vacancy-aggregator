import React from 'react';

const Resume: React.FC = () => {
    return (
        <div>
            <h1>Резюме</h1>
            <p>Это страница с информацией о резюме.</p>

            {/* Добавим много параграфов, чтобы страница была длинной */}
            {[...Array(30)].map((_, i) => (
                <p key={i}>
                    Пункт резюме #{i + 1}: Lorem ipsum dolor sit amet,
                    consectetur adipiscing elit. Sed do eiusmod tempor
                    incididunt ut labore et dolore magna aliqua.
                </p>
            ))}
        </div>
    );
};

export default Resume;
