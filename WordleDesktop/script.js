console.log("Script!");

let rowNum = 0;
let colNum = 0;
let isGameDone = false;

const test = () => {
    console.log("test func!!!");
};

// detect keypresses
// if letter, update guess
// if backspace, go back
// if other, do nothing?
document.addEventListener('keydown', keyDownFunc);
function keyDownFunc(e) {
    if (isGameDone) {
        console.log("Sorry, the game is over!")
        return;
    }
    let key = e.key.toUpperCase();
    console.log(key);
    if (key.length === 1 && key.match(/[A-Z]/i)) {
        console.log("Key is letter")
        if (colNum === 5) {
            console.log("Press Enter to make a guess!")
            return;
        } 
        addLetterToGuess(key);
        colNum++;
    }
    else if (key === "ENTER") {
        console.log("Made guess!")
        colNum = 0;
        rowNum++;
        if (rowNum === 6) {
            isGameDone = true;
            console.log("gameover");
        }
    }
    else if (key === "BACKSPACE") {
        console.log("Key is backspace!")
        resetTile();
        if (colNum === 0) {
            return;
        }
        colNum -= 1;
    }
    else {
        console.log("Not a letter or backspace");
    }
}

function resetTile() {
    console.log("Resetting tile")
    var tile = document.getElementById("row_" + rowNum + "_tile_" + colNum);
    tile.innerHTML = "";
}

function addLetterToGuess(key) {
    console.log("Adding: " + key + " to tile: " + rowNum + " " + colNum);
    var tile = document.getElementById("row_" + rowNum + "_tile_" + colNum);
    console.log(tile)
    tile.innerHTML = key;
}