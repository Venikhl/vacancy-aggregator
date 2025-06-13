import { useState } from 'react';
import { FaChevronRight } from 'react-icons/fa';

const fields = [
    { label: 'Имя', key: 'name', value: 'Вера Неттор' },
    { label: 'Дата рождения', key: 'dob', value: '15.03.2002' },
    { label: 'Пол', key: 'gender', value: 'Женский' },
    { label: 'Почта', key: 'email', value: 'VeraNettor2002@gmail.com' },
    { label: 'Никнейм', key: 'nickname', value: 'Virus' },
    { label: 'Пароль', key: 'password', value: '********' },
];

const Settings = () => {
    const [editField, setEditField] = useState<null | { key: string; label: string; value: string }>(null);
    const [inputValue, setInputValue] = useState('');
    const [avatarUrl, setAvatarUrl] = useState('/user-avatar.png');

    const openModal = (field: typeof editField) => {
        setEditField(field);
        setInputValue(field?.value || '');
    };

    const closeModal = () => {
        setEditField(null);
    };

    const saveChange = () => {
        // TODO как будет готов бэк - написать логику обновления полей
        closeModal();
    };

    const handleAvatarChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            const imageUrl = URL.createObjectURL(file);
            setAvatarUrl(imageUrl);
        }
    };

    return (
        <div className="bg-[#1e1e1e] min-h-screen text-white p-8">
            <h1 className="text-3xl font-bold text-right mb-12">Настройки аккаунта</h1>

            <section className="mb-12">
                <h2 className="text-2xl font-semibold mb-6">Общая информация</h2>

                <div className="flex items-center gap-6 mb-8">
                    <img
                        src={avatarUrl}
                        alt="Profile"
                        className="w-20 h-20 rounded-full object-cover border-2 border-orange-400"
                    />
                    <label className="cursor-pointer text-sm text-gray-400 hover:text-orange-400 transition">
                        Загрузить с <br /> локального хранилища
                        <input
                            type="file"
                            accept="image/*"
                            className="hidden"
                            onChange={handleAvatarChange}
                        />
                    </label>
                </div>

                {fields.slice(0, 4).map((field) => (
                    <button
                        key={field.key}
                        onClick={() => openModal(field)}
                        className="w-full flex justify-between items-center py-3 border-b border-gray-700 text-left hover:bg-[#2a2a2a] transition"
                    >
                        <div>
                            <div className="text-gray-400 text-sm">{field.label}</div>
                            <div className="font-medium">{field.value}</div>
                        </div>
                        <FaChevronRight className="text-gray-400" />
                    </button>
                ))}
            </section>

            <section>
                <h2 className="text-2xl font-semibold mb-6">Информация Аккаунта</h2>

                {fields.slice(4).map((field) => (
                    <button
                        key={field.key}
                        onClick={() => openModal(field)}
                        className="w-full flex justify-between items-center py-3 border-b border-gray-700 text-left hover:bg-[#2a2a2a] transition"
                    >
                        <div>
                            <div className="text-gray-400 text-sm">{field.label}</div>
                            <div className="font-medium">{field.value}</div>
                        </div>
                        <FaChevronRight className="text-gray-400" />
                    </button>
                ))}
            </section>

            {/* ===== Modal ===== */}
            {editField && (
                <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
                    <div className="bg-[#1a1a1a] p-6 rounded-xl w-full max-w-md shadow-xl">
                        <h2 className="text-xl font-semibold mb-4">Изменить {editField.label}</h2>
                        <input
                            type="text"
                            className="w-full p-2 rounded bg-[#262626] border border-gray-600 text-white mb-4"
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                        />
                        <div className="flex justify-end gap-4">
                            <button
                                onClick={closeModal}
                                className="px-4 py-2 rounded bg-gray-600 hover:bg-gray-700 transition"
                            >
                                Отмена
                            </button>
                            <button
                                onClick={saveChange}
                                className="px-4 py-2 rounded bg-orange-500 hover:bg-orange-600 transition font-semibold"
                            >
                                Сохранить
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Settings;
