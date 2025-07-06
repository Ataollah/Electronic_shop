document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.qty-container').forEach(function (container) {
        const minusBtn = container.querySelector('.qty-btn-minus');
        const plusBtn = container.querySelector('.qty-btn-plus');
        const qtyInput = container.querySelector('.input-qty');
        const maxQty = parseInt(qtyInput.getAttribute('data-inventory'), 10) || 99;

        plusBtn.addEventListener('click', function () {
            let current = parseInt(qtyInput.value, 10) || 1;
            //    if (current < maxQty) {
            //        qtyInput.value = current + 1;
            //  }
            plusBtn.disabled = parseInt(qtyInput.value, 10) >= maxQty;
            minusBtn.disabled = parseInt(qtyInput.value, 10) <= 1;
        });

        minusBtn.addEventListener('click', function () {
            let current = parseInt(qtyInput.value, 10) || 1;
            //     if (current > 1) {
            //         qtyInput.value = current - 1;
            //     }
            minusBtn.disabled = parseInt(qtyInput.value, 10) <= 1;
            plusBtn.disabled = parseInt(qtyInput.value, 10) >= maxQty;
        });

        qtyInput.addEventListener('input', function () {
            let value = parseInt(qtyInput.value, 10) || 1;
            if (value > maxQty) value = maxQty;
            if (value < 1) value = 1;
            qtyInput.value = value;
            plusBtn.disabled = value >= maxQty;
            minusBtn.disabled = value <= 1;
        });

        // Initialize button states
        minusBtn.disabled = true;
        plusBtn.disabled = parseInt(qtyInput.value, 10) >= maxQty;
    });
});