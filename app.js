const diseases=[

{name:"Грип",type:"virus",symptoms:["температура","кашель","біль у горлі"],info:"Гостра вірусна інфекція дихальних шляхів."},

{name:"COVID-19",type:"virus",symptoms:["температура","кашель","втрата нюху"],info:"Коронавірусна інфекція SARS-CoV-2."},

{name:"Туберкульоз",type:"bacteria",symptoms:["кашель","слабкість","схуднення"],info:"Хронічна бактеріальна інфекція легень."},

{name:"Черевний тиф",type:"bacteria",symptoms:["температура","біль у животі","слабкість"],info:"Системна інфекція Salmonella Typhi."},

{name:"Дифтерія",type:"bacteria",symptoms:["біль у горлі","температура","слабкість"],info:"Бактеріальна інфекція дихальних шляхів."},

{name:"Холера",type:"bacteria",symptoms:["діарея","слабкість"],info:"Гостра кишкова інфекція Vibrio cholerae."},

{name:"Шигельоз",type:"bacteria",symptoms:["діарея","температура","біль у животі"],info:"Бактеріальна дизентерія."},

{name:"Малярія",type:"parasite",symptoms:["лихоманка","озноб","слабкість"],info:"Паразитарна інфекція плазмодіями."},

{name:"Лептоспіроз",type:"bacteria",symptoms:["температура","слабкість"],info:"Зоонозна бактеріальна інфекція."},

{name:"Ботулізм",type:"bacteria",symptoms:["слабкість"],info:"Токсикоінфекція Clostridium botulinum."}

]

const allSymptoms=[
"температура",
"кашель",
"біль у горлі",
"слабкість",
"озноб",
"діарея",
"біль у животі",
"втрата нюху",
"лихоманка"
]

// [Завдання 1.1 + 1.3] Реєстрація та Валідація

const registerForm = document.getElementById("registerForm");

if (registerForm) {
    registerForm.addEventListener("submit", function(e) {
        e.preventDefault();

        const firstName = document.getElementById("firstName").value.trim();
        const lastName  = document.getElementById("lastName").value.trim();
        const email     = document.getElementById("email").value.trim();
        const password  = document.getElementById("password").value;
        const msg       = document.getElementById("formMessage");

        // Очищаємо попереднє повідомлення
        msg.innerHTML = "";

        // ========== ВАЛІДАЦІЯ ==========

        if (!firstName) {
            msg.innerHTML = ">>> ERROR: Введіть ім'я (F_NAME)";
            msg.style.color = "#ff4444";
            return;
        }

        if (!lastName) {
            msg.innerHTML = ">>> ERROR: Введіть прізвище (L_NAME)";
            msg.style.color = "#ff4444";
            return;
        }

        if (!email) {
            msg.innerHTML = ">>> ERROR: EMAIL_ADDR не може бути порожнім";
            msg.style.color = "#ff4444";
            return;
        }

        // === ОСНОВНА ВАЛІДАЦІЯ EMAIL ===
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailRegex.test(email)) {
            msg.innerHTML = ">>> ERROR: НЕКОРЕКТНИЙ EMAIL_ADDR";
            msg.style.color = "#ff4444";
            return;
        }

        if (!password) {
            msg.innerHTML = ">>> ERROR: Введіть пароль (PASS_HASH)";
            msg.style.color = "#ff4444";
            return;
        }

        if (password.length < 6) {
            msg.innerHTML = ">>> ERROR: PASS_HASH повинен бути не менше 6 символів";
            msg.style.color = "#ff4444";
            return;
        }

        // ========== УСПІХ ==========
        msg.innerHTML = `>>> SUCCESS: USER ${firstName.toUpperCase()} ${lastName.toUpperCase()} ЗАРЕЄСТРОВАНИЙ<br>
                         >>> EMAIL: ${email}<br>
                         >>> STATUS: ENCRYPTED_AND_SAVED`;
        msg.style.color = "#00ff41";

        // Очищаємо форму після успішної реєстрації
        registerForm.reset();
    });
}
// Рендер бази даних
function renderDiseases(list, target = "diseasesGrid") {
    const grid = document.getElementById(target);
    grid.innerHTML = "";
    list.forEach(d => {
        const card = document.createElement("div");
        card.className = "card";
        card.innerHTML = `<h3>${d.name}</h3><p>${d.info}</p>`;
        card.onclick = () => showDetail(d);
        grid.appendChild(card);
    });
}

// Перемикання розділів (SPA Логіка)
function showSection(id) {
    document.querySelectorAll(".section").forEach(s => s.classList.remove("active"));
    document.getElementById(id).classList.add("active");
}

// Ініціалізація симптомів
function renderSymptoms() {
    const container = document.getElementById("symptomsList");
    container.innerHTML = ""; // Очищуємо перед рендером

    allSymptoms.forEach(s => {
        const label = document.createElement("label");
        label.className = "symptom-item"; // Новий клас для стилів
        label.innerHTML = `
            <input type="checkbox" value="${s}">
            <span>${s}</span>
        `;
        container.appendChild(label);
    });
}

function checkSymptoms() {
    const checked = [...document.querySelectorAll("#symptomsList input:checked")].map(c => c.value);
    const matches = diseases.filter(d => checked.some(s => d.symptoms.includes(s)));
    renderDiseases(matches, "resultCards");
}

function showDetail(d) {
    document.getElementById("modalBody").innerHTML = `<h2>${d.name}</h2><p>${d.info}</p>`;
    document.getElementById("modal").style.display = "flex";
}

function closeModal() { document.getElementById("modal").style.display = "none"; }

window.onload = () => {
    renderDiseases(diseases);
    renderSymptoms();
};



