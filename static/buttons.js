function moveUp() {
    console.log("moveUp");
    fetch('/move_up')
        .then(response => response.text())
        .then(data => console.log(`recv: ${data}`));
}
function moveDown() {
    console.log("moveDown");
    fetch('/move_down')
        .then(response => response.text())
        .then(data => console.log(`recv: ${data}`));
}
function moveLeft() {
    console.log("moveLeft");
    fetch('/move_left')
        .then(response => response.text())
        .then(data => console.log(`recv: ${data}`));
}

function moveRight() {
    console.log("moveRight");
    fetch('/move_right')
        .then(response => response.text())
        .then(data => console.log(`recv: ${data}`));

}        