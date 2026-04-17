// Перемикання секцій
function showSection(id) {
    document.querySelectorAll(".section").forEach(s => s.classList.remove("active"));
    document.getElementById(id).classList.add("active");
}

// Пошук
function filterDiseases() {
    const input = document.getElementById('searchInput').value.toLowerCase();
    const cards = document.querySelectorAll('.disease-card');

    cards.forEach(card => {
        const name = card.dataset.name;
        card.style.display = name.includes(input) ? "block" : "none";
    });
}

// Модалка (додали нормальну)
function showDiseaseDetails(id) {
    const modal = document.getElementById("modal");
    const body = document.getElementById("modalBody");

    body.innerHTML = `
        <h2>DATA_ACCESS</h2>
        <p>Деталі для ID: ${id}</p>
    `;

    modal.style.display = "flex";
}

function closeModal() {
    document.getElementById("modal").style.display = "none";
}

function showDiseaseDetails(id) {
    const modal = document.getElementById("modal");
    const body = document.getElementById("modalBody");

    body.innerHTML = ">>> LOADING...";

    fetch(`/api/disease/${id}/`)
        .then(response => response.json())
        .then(data => {

            if (data.error) {
                body.innerHTML = "ERROR";
                return;
            }

            body.innerHTML = `
                <h2>${data.name}</h2>

                ${data.image ? `<img src="${data.image}" style="width:100%; margin:10px 0;">` : ""}

                <p>${data.description}</p>
            `;
        })
        .catch(() => {
            body.innerHTML = "SERVER ERROR";
        });

    modal.style.display = "flex";
}