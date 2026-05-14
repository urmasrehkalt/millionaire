import { renderMenu } from "./ui/menu.js";
import { startNewGame } from "./ui/game.js";
import { renderResult } from "./ui/result.js";

const app = document.getElementById("app");

function showMenu() {
    renderMenu(app, showGame);
}

function showGame(assignment) {
    startNewGame(app, assignment, showResult);
}

function showResult(result) {
    renderResult(app, result, {
        onPlayAgain: (assignment) => startNewGame(app, assignment, showResult),
        onBackToMenu: showMenu,
    });
}

showMenu();
