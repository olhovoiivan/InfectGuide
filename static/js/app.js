// ===== 1. НАВІГАЦІЯ МІЖ РОЗДІЛАМИ =====
function navigateToSection(id) {
    const target = document.getElementById(id);
    const menu = document.getElementById("main-nav");

    if (target) {
        // Приховуємо всі секції
        document.querySelectorAll('.section').forEach(s => {
            s.style.display = 'none';
            s.classList.remove('active');
        });

        // Показуємо потрібну
        target.style.display = 'block';
        target.classList.add('active');

        // Закриваємо мобільне меню (якщо воно відкрите)
        if (menu) menu.classList.remove('active');

        // Скролимо вгору сторінки для зручності
        window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
        // Якщо ми на іншій сторінці (напр. login), переходимо на головну з якорем
        window.location.href = "/#" + id;
    }
}

// ===== 2. ПОШУК ІНФЕКЦІЙ (DB) =====
function filterDiseases() {
    const input = document.getElementById('searchInput').value.toLowerCase();
    const cards = document.querySelectorAll('.disease-card');

    cards.forEach(card => {
        const name = card.dataset.name || "";
        if (name.includes(input)) {
            card.style.display = "block";
        } else {
            card.style.display = "none";
        }
    });
}

// ===== 3. МОДАЛЬНЕ ВІКНО (ДЕТАЛІ) =====
function openModal() {
    const modal = document.getElementById("modal");
    if (modal) {
        modal.style.display = "flex";
        document.body.style.overflow = "hidden"; // Забороняємо скрол фону
    }
}

function closeModal() {
    const modal = document.getElementById("modal");
    if (modal) {
        modal.style.display = "none";
        document.body.style.overflow = "auto"; // Повертаємо скрол
    }
}

// Закриття модалки при кліку на фон
window.onclick = function(e) {
    const modal = document.getElementById("modal");
    if (e.target === modal) {
        closeModal();
    }
};

// Завантаження даних про хворобу через API
function showDiseaseDetails(id) {
    const modalBody = document.getElementById("modalBody");
    if (!modalBody) return;

    openModal();
    modalBody.innerHTML = `
        <div style="text-align: center; padding: 20px;">
            <p style="color: var(--blue); font-family: 'JetBrains Mono';">>>> ACCESSING ENCRYPTED DATA...</p>
        </div>
    `;

    fetch(`/api/disease/${id}/`)
        .then(res => {
            if (!res.ok) throw new Error("Not found");
            return res.json();
        })
        .then(data => {
            modalBody.innerHTML = `
                <h2 style="color: var(--green); margin-bottom: 15px; text-transform: uppercase;">${data.name}</h2>

                ${data.image ? `
                    <div style="border: 1px solid var(--blue); margin-bottom: 20px;">
                        <img src="${data.image}" style="width:100%; display:block; max-height: 400px; object-fit: contain;">
                    </div>
                ` : ""}

                <div style="background: rgba(0, 212, 255, 0.05); padding: 15px; border-left: 3px solid var(--blue); margin-bottom: 20px;">
                    <p style="font-size: 14px; line-height: 1.6; color: #fff;">${data.description}</p>
                </div>

                <div class="tags" style="display: flex; flex-wrap: wrap; gap: 8px;">
                    ${data.symptoms.map(s => `
                        <span style="border: 1px solid var(--green); color: var(--green); padding: 4px 8px; font-size: 11px;">
                            #${s.toUpperCase()}
                        </span>
                    `).join("")}
                </div>
            `;
        })
        .catch(err => {
            console.error(err);
            modalBody.innerHTML = "<p style='color: red; text-align: center;'>[ ERROR: DATA_CORRUPTION_OR_SERVER_OFFLINE ]</p>";
        });
}

// ===== 4. АНАЛІЗАТОР СИМПТОМІВ =====
function checkSymptoms() {
    console.log("Функція checkSymptoms викликана успішно!");
    const selected = Array.from(document.querySelectorAll('input[name="symptom"]:checked'))
                          .map(cb => cb.value);
    const resultContainer = document.getElementById("resultCards");

    if (!resultContainer) return;

    if (selected.length === 0) {
        resultContainer.innerHTML = "<p style='grid-column: 1/-1; text-align: center; color: var(--blue);'>[ STATUS: ОБЕРІТЬ СИМПТОМИ ДЛЯ СКАНУВАННЯ ]</p>";
        return;
    }

    resultContainer.innerHTML = "<p style='grid-column: 1/-1; text-align: center; color: var(--green);'>>>> RUNNING BIO-SCAN...</p>";

    // Формуємо GET запит до Django API
    const params = new URLSearchParams();
    selected.forEach(id => params.append('symptoms[]', id));

    fetch(`/api/check_symptoms/?${params.toString()}`)
        .then(res => res.json())
        .then(data => {
            resultContainer.innerHTML = "";

            if (!data.diseases || data.diseases.length === 0) {
                resultContainer.innerHTML = "<p style='grid-column: 1/-1; text-align: center; color: #fff;'>Збігів не знайдено. Спробуйте змінити критерії пошуку.</p>";
                return;
            }

            // Виведення карток результатів
            data.diseases.forEach(d => {
                resultContainer.innerHTML += `
                    <div class="disease-card">
                        <div class="card-content">
                            <h3 style="color: var(--green)">${d.name}</h3>
                            <div style="margin: 10px 0;">
                                <span style="font-size: 10px; background: rgba(0,255,156,0.1); color: var(--green); padding: 2px 5px; border: 1px solid var(--green);">
                                    MATCH: ${d.match_count} SYMPTOMS
                                </span>
                            </div>
                            <p style="font-size: 13px; color: #9fdfff;">${d.description}</p>
                            <button class="btn-cyber-small" style="margin-top:15px;" onclick="showDiseaseDetails('${d.id}')">
                                OPEN_DATA_FILE
                            </button>
                        </div>
                    </div>`;
            });
        })
        .catch(err => {
            console.error(err);
            resultContainer.innerHTML = "<p style='grid-column: 1/-1; text-align: center; color: red;'>SYSTEM FAILURE: API UNREACHABLE</p>";
        });
}

// ===== 5. ІНІЦІАЛІЗАЦІЯ ПРИ ЗАВАНТАЖЕННІ =====
document.addEventListener("DOMContentLoaded", function() {
    // Обробка хешу в URL (якщо прийшли з іншої сторінки на #checker)
    const hash = window.location.hash.replace('#', '');
    if (hash === 'home' || hash === 'checker') {
        navigateToSection(hash);
    }
});