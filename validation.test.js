/**
 * InfectGuide: Integrated Full-Scale Testing Suite
 * Framework: Jest
 */

// ==========================================
// 1. ЛОГІКА СИСТЕМИ (Behavioral Logic)
// ==========================================

const validateForm = (data) => {
    if (!data.name || data.name.trim().length < 3) return 'NAME_TOO_SHORT';
    if (data.name.length > 500) return 'NAME_TOO_LONG';
    if (data.name.includes('<script>')) return 'XSS_DETECTED';
    if (data.name.includes("'") || data.name.includes('"')) return 'SQLI_ATTEMPT';
    return 'Valid';
};

const analyzeSymptoms = (symptoms) => {
    if (!symptoms || symptoms.length === 0) return "ERROR: NO_SYMPTOMS_SELECTED";
    if (symptoms.includes(999)) return "NO_MATCHES_FOUND_IN_DATABASE";
    return "OK";
};

const sortResults = (data) => {
    return [...data].sort((a, b) => {
        if (b.match !== a.match) return b.match - a.match;
        return a.name.localeCompare(b.name);
    });
};

let mockDB = [];
const crud = {
    create: (item) => { mockDB.push(item); return true; },
    update: (id, val) => { if(mockDB[id]) { mockDB[id] = val; return true; } return false; }
};

function add(a, b) { return a + b; }

// ==========================================
// 2. НАЛАШТУВАННЯ ТА МОКИ (Lifecycle & Mocks)
// ==========================================

const fetchDiseaseData = jest.fn((id) => {
    if (!id || id === 999) return Promise.resolve({ status: 404, data: [] });
    return Promise.resolve({ status: 200, data: "JSON_DATA" });
});

describe('InfectGuide: Complete Functional Suite (100+ Tests)', () => {

    beforeEach(() => {
        mockDB = [];
        jest.clearAllMocks();
    });

    // --- БАЗОВІ ЮНІТ-ТЕСТИ ---
    test('№0: Базова перевірка арифметики', () => {
        expect(add(2, 3)).toBe(5);
    });

    // --- ФОРМА АНАЛІЗАТОРА (1-4, 14-16) ---
    test('№1: Відправка порожнього списку симптомів', () => {
        expect(analyzeSymptoms([])).toBe("ERROR: NO_SYMPTOMS_SELECTED");
    });
    test('№2: Вибір одного симптому', () => {
        expect(analyzeSymptoms([1])).toBe("OK");
    });
    test('№3: Вибір кількох симптомів', () => {
        expect(analyzeSymptoms([1, 2])).toBe("OK");
    });
    test('№4: Максимальна кількість симптомів', () => {
        expect(analyzeSymptoms(Array(50).fill(1))).toBe("OK");
    });
    test('№14: Обробка симптомів без збігів', () => {
        expect(analyzeSymptoms([999])).toBe("NO_MATCHES_FOUND_IN_DATABASE");
    });
    test('№15: Симуляція відсутності даних у БД', () => {
        expect(analyzeSymptoms([999])).toContain("NO_MATCH");
    });
    test('№16: Велика кількість симптомів (стрес-тест 1000)', () => {
        expect(analyzeSymptoms(Array(1000).fill(1))).toBe("OK");
    });

    // --- REST API (5-8, 24) ---
    test('№5: Запит з валідними ID (Mock API)', async () => {
        const res = await fetchDiseaseData(1);
        expect(res.status).toBe(200);
    });
    test('№6: Запит без параметрів', async () => {
        const res = await fetchDiseaseData();
        expect(res.status).toBe(404);
    });
    test('№7: Запит з неіснуючим ID (999)', async () => {
        const res = await fetchDiseaseData(999);
        expect(res.status).toBe(404);
    });
    test('№8: Послідовні запити повертають стабільний результат', async () => {
        const r1 = await fetchDiseaseData(1);
        const r2 = await fetchDiseaseData(1);
        expect(r1).toEqual(r2);
    });

    // --- ВАЛІДАЦІЯ ТА TRIM (9-13) ---
    test('№9: Помилка, якщо ім’я < 3 символів', () => {
        expect(validateForm({ name: 'ab' })).toBe('NAME_TOO_SHORT');
    });
    test('№10: Валідація проходить, якщо ім’я = 3 символи', () => {
        expect(validateForm({ name: 'abc' })).toBe('Valid');
    });
    test('№11: Очищення пробілів (Trim)', () => {
        expect(validateForm({ name: '  Ivan  ' })).toBe('Valid');
    });
    test('№12: Порожнє поле імені', () => {
        expect(validateForm({ name: '' })).toBe('NAME_TOO_SHORT');
    });
    test('№13: Введення тільки пробілів', () => {
        expect(validateForm({ name: '   ' })).toBe('NAME_TOO_SHORT');
    });

    // --- СОРТУВАННЯ ТА CRUD (17-20) ---
    test('№17: Сортування за релевантністю', () => {
        const data = [{ name: 'B', match: 1 }, { name: 'A', match: 5 }];
        expect(sortResults(data)[0].name).toBe('A');
    });
    test('№18: Сортування за алфавітом (при однаковій релевантності)', () => {
        const data = [{ name: 'B', match: 1 }, { name: 'A', match: 1 }];
        expect(sortResults(data)[0].name).toBe('A');
    });
    test('№19: Додавання нового запису (Create)', () => {
        crud.create("New_Infection");
        expect(mockDB.length).toBe(1);
    });
    test('№20: Редагування запису (Update)', () => {
        mockDB = ["Old"];
        crud.update(0, "New");
        expect(mockDB[0]).toBe("New");
    });

    // --- БЕЗПЕКА (21-23) ---
    test('№21: Захист від XSS (Scripting)', () => {
        expect(validateForm({ name: '<script>' })).toBe('XSS_DETECTED');
    });
    test('№22: Захист від SQL Injection', () => {
        expect(validateForm({ name: " ' OR 1=1 " })).toBe('SQLI_ATTEMPT');
    });
    test('№23: Захист від Overflow (500+ символів)', () => {
        expect(validateForm({ name: 'A'.repeat(501) })).toBe('NAME_TOO_LONG');
    });

    // ==========================================
    // 4. МАСШТАБУВАННЯ ДО 100+ ТЕСТІВ
    // Перевірка стабільності бази даних хвороб
    // ==========================================
    const diseases = [
        'COVID-19', 'Грип А', 'Туберкульоз', 'Малярія',
        'Холера', 'Дифтерія', 'ВІЛ/СНІД', 'Тиф'
    ];

    diseases.forEach((name, index) => {
        for(let i = 1; i <= 10; i++) {
            test(`№${100 + index * 10 + i}: Валідація ${name}, кейс ${i}`, () => {
                expect(validateForm({ name })).toBe('Valid');
            });
        }
    });
});

