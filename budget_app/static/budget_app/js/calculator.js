document.addEventListener("DOMContentLoaded", function () {

    const resultEl = document.getElementById('result');
    const historyEl = document.getElementById('history');
    const clearBtn = document.getElementById('clear');
    const deleteBtn = document.getElementById('delete_single_num');
    const equalBtn = document.getElementById('equalTo');


    const inputButtons = document.querySelectorAll('[data-btn="normal"]');

    let expr = "";


    inputButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            expr += btn.textContent.trim();
            resultEl.textContent = expr;
        });
    });

    equalBtn.addEventListener('click', () => {
        try {
            if (expr.trim() === "") {
                alert("Please enter a number");
                return;
            }
            historyEl.textContent = expr;

            const value = eval(expr);
            expr = String(value);
            resultEl.textContent = expr;
        } catch (e) {
            alert("Invalid expression");
        }
    });


    clearBtn.addEventListener('click', () => {
        expr = "";
        resultEl.textContent = "";
        historyEl.textContent = "History";
    });

    deleteBtn.addEventListener('click', () => {
        expr = expr.slice(0, -1);
        resultEl.textContent = expr;
    });

});
