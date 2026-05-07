const num1Input = document.getElementById("num1");
const num2Input = document.getElementById("num2");
const resultDiv = document.getElementById("result");

function parseInputs() {
    const a = Number(num1Input.value.replace(",", "."));
    const b = Number(num2Input.value.replace(",", "."));

    if (Number.isNaN(a) || Number.isNaN(b) || num1Input.value === "" || num2Input.value === "") {
        return null;
    }
    return { a, b };
}

function showResult(text, type = "success") {
    resultDiv.textContent = text;
    resultDiv.className = "result " + type;
}

function showError(message) {
    showResult(message, "error");
}

function calculate(operation) {
    const inputs = parseInputs();
    if (inputs === null) {
        showError("Palun sisesta mõlemasse välja arv");
        return;
    }

    const { a, b } = inputs;
    let result;

    switch (operation) {
        case "add":
            result = a + b;
            break;
        case "subtract":
            result = a - b;
            break;
        case "multiply":
            result = a * b;
            break;
        case "divide":
            if (b === 0) {
                showError("Nulliga jagada ei saa");
                return;
            }
            result = a / b;
            break;
        default:
            showError("Tundmatu tehe");
            return;
    }

    showResult("Tulemus: " + result);
}

document.getElementById("add").addEventListener("click", () => calculate("add"));
document.getElementById("subtract").addEventListener("click", () => calculate("subtract"));
document.getElementById("multiply").addEventListener("click", () => calculate("multiply"));
document.getElementById("divide").addEventListener("click", () => calculate("divide"));
