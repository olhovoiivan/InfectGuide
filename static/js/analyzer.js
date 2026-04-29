document.addEventListener('DOMContentLoaded', function() {
    const diagBtn = document.getElementById('run-diagnosis'); // Твоя кнопка
    const resultsContainer = document.getElementById('diagnosis-results'); // Куди виводити результат

    diagBtn.addEventListener('click', function(e) {
        e.preventDefault(); // Зупиняємо перезавантаження сторінки

        // 1. Збираємо вибрані симптоми
        const selected = Array.from(document.querySelectorAll('input[name="symptoms"]:checked'))
                              .map(cb => cb.value);

        if (selected.length === 0) {
            resultsContainer.innerHTML = "<p style='color: #ff4d6d;'>[ ERROR: NO_SYMPTOMS_SELECTED ]</p>";
            return;
        }

        // 2. Відправляємо асинхронний запит (Fetch API)
        const params = new URLSearchParams();
        selected.forEach(id => params.append('symptoms', id));

        fetch(`/api/check_symptoms/?${params.toString()}`)
            .then(response => response.json())
            .then(data => {
                // 3. Обробляємо результат і вставляємо в HTML
                renderResults(data.diseases);
            });
    });

    function renderResults(diseases) {
        if (diseases.length === 0) {
            resultsContainer.innerHTML = "<p>[ NO_MATCHES_FOUND_IN_DATABASE ]</p>";
            return;
        }

        let html = "<h3>_ANALYSIS_COMPLETED:</h3>";
        diseases.forEach(d => {
            html += `
                <div class="result-item" style="border-left: 3px solid #00ff9c; padding-left: 10px; margin-bottom: 10px;">
                    <strong style="color: #00ff9c;">${d.name}</strong>
                    <span style="color: #6fa3c7;">(Збігів: ${d.match_count})</span>
                </div>
            `;
        });
        resultsContainer.innerHTML = html;
    }
});