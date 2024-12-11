document.addEventListener('DOMContentLoaded', () => {
    const submitButton = document.getElementById('submitButton');
    const blocks = document.querySelectorAll('.block');
    let selectedBlock = null;

    // Обробка кліку на блок
    blocks.forEach(block => {
        block.addEventListener('click', () => {
            // Якщо вже вибраний блок, скидаємо стиль
            if (selectedBlock) {
                selectedBlock.classList.remove('selected');
            }

            // Позначаємо новий вибраний блок
            selectedBlock = block;
            block.classList.add('selected');
        });
    });

    // Надсилання даних
    submitButton.addEventListener('click', () => {
        const phone = document.getElementById('phone').value;
        const name = document.getElementById('name').value;

        // Перевірка вибраного блоку
        if (!selectedBlock) {
            alert('Будь ласка, виберіть час запису.');
            return;
        }

        // Отримання дати та часу з вибраного блоку
        const date = selectedBlock.querySelector('.date').textContent.trim();
        const time = selectedBlock.querySelector('.time').textContent.trim();

        // Перевірка заповнення полів
        if (!phone || !name) {
            alert('Будь ласка, заповніть всі поля.');
            return;
        }

        const houseId = window.location.pathname.split('/')[2]; // Отримаємо ID з URL, наприклад, "1"

        const data = {
            phone: phone,
            name: name,
            datetime: `${date} ${time}`,
            houseId: houseId  // Додаємо ID будинку
        };

        // Надсилання даних на сервер
        fetch('/appointment/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                alert(response);
                window.location.reload();
                throw new Error('Помилка');
            }
            return response.json();
        })
        .then(data => {
            alert('Вас успішно записано!');
            window.history.back();
        })
        .catch(error => {
            console.error('Помилка:', error);
            alert(error);
            if(error == 'Немає вільних ріелторів на цей час. Спробуйте інший час'){
                window.location.reload();
            }
        });
    });
});
