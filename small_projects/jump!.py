var teagan;
var SIZE_OF_BOARD_X = 13;//13
var SIZE_OF_BOARD_Y = 15;//15
var allowKeyPress = true;
var TICK_DELAY = 175;
var jumpOff = true;
var board = new Grid(SIZE_OF_BOARD_Y, SIZE_OF_BOARD_X);
var SIZE_OF_OBJECTS_X = getWidth() / SIZE_OF_BOARD_X;
var SIZE_OF_OBJECTS_Y = getHeight() / SIZE_OF_BOARD_Y;
var PLAYER_W = SIZE_OF_OBJECTS_X;
var PLAYER_H = SIZE_OF_OBJECTS_Y;
var MAX_JUMP_HEIGHT = (SIZE_OF_OBJECTS_Y * 2.5);
var jumpCounter = 0;
var gravityAlow = true;
var winer = false;
//-----------------MAP1
// c = middle block, p = player, l = lava
board.initFromArray([
    ["c","p","a","a","a","a","a","a","a","a","a","a","a"],
    ["c","a","a","a","a","c","c","c","a","a","a","a","l"],
    ["c","c","c","c","l","a","a","a","l","c","l","a","a"],
    ["c","a","a","a","a","a","a","a","a","a","c","a","a"],
    ["l","a","a","c","a","a","l","a","a","a","a","l","a"],
    ["a","a","l","c","a","l","c","l","c","a","a","a","a"],
    ["a","c","c","c","c","c","c","l","c","l","c","c","c"],
    ["a","a","a","a","a","c","a","a","c","c","a","a","a"],
    ["a","a","a","a","a","a","a","a","a","a","a","a","a"],
    ["l","l","c","l","a","a","c","a","a","a","a","l","a"],
    ["a","a","a","a","c","l","c","c","l","c","a","a","a"],
    ["a","a","a","a","a","a","a","a","c","a","l","a","c"],
    ["a","l","a","a","a","a","c","a","a","a","a","a","a"],
    ["w","c","a","a","a","a","c","c","a","a","c","a","a"],
    ["c","c","c","l","l","l","c","c","c","l","c","l","c"]
]);
/*board.initFromArray([
    ["c","c","c","c","c","c","c","c","c","c","c","c","c"],
    ["c","c","c","c","c","c","c","c","c","c","c","c","c"],
    ["c","c","c","c","c","c","c","c","c","c","c","c","c"],
    ["c","c","c","c","c","c","c","c","c","c","c","c","c"],
    ["c","c","c","c","c","c","c","c","c","c","c","c","c"],
    ["c","c","c","c","c","c","c","c","c","c","c","c","c"],
    ["c","c","c","c","c","c","c","c","c","c","c","c","c"],
    ["c","c","c","c","c","c","c","c","c","c","c","c","c"],
    ["c","c","c","c","c","c","c","c","c","c","c","c","c"],
    ["c","c","c","c","c","c","c","c","c","c","c","c","c"],
    ["c","c","c","c","c","c","c","c","c","c","c","c","c"],
    ["c","c","c","c","c","c","c","c","c","c","c","c","c"],
    ["c","c","c","c","c","c","c","c","c","c","c","c","c"],
    ["c","c","c","c","c","c","c","c","c","c","c","c","c"],
    ["c","c","c","c","c","c","c","c","c","c","c","c","c"]
]);*/
function start(){
    setBoard();
    //println(SIZE_OF_OBJECTS_X + ","  + SIZE_OF_OBJECTS_Y);
    if(gravityAlow == true){
        //music();
        setTimer(gravity, TICK_DELAY);
        setTimer(lavaCheck, TICK_DELAY);
        setTimer(topCheck,TICK_DELAY);
        setTimer(winCheck, TICK_DELAY);
    }
}
//------------------------SET BOARD
function setBoard(){
    for(var y = 0; y < SIZE_OF_BOARD_Y; y++){
        for(var x = 0; x < SIZE_OF_BOARD_X; x++){
            var position =  board.get(y, x);
            if(position == "a"){
            }else if(position == "c"){
                blockCenterSet(x,y);
            }else if(position == "p"){
                playerSet(x,y);
            }else if(position == "l"){
                lavaSet(x,y);
            }else if(position == "w"){
                winSet(x,y);
            }else if(position == ""){
                
            }
        }
    }
}
//------------------------Add BOARD
//Block
var blockCenter;
function blockCenterSet(x, y){
    blockCenter = new Rectangle( 10, 10);
    blockCenter.setColor(Color.gray);
    blockCenter.setSize(30.76923076923077, 32);
    blockCenter.setPosition((x * SIZE_OF_OBJECTS_X), (y * SIZE_OF_OBJECTS_Y));
    add(blockCenter);
}
//Player
function playerSet(x, y){
    var randomCari = ["https://static.codehs.com/img/library/characters/penguin.png",
    "https://static.codehs.com/img/library/characters/monkey.jpg",
    "https://static.codehs.com/img/library/characters/leopard.jpg",
    "https://static.codehs.com/img/library/characters/chameleon.jpg",
    "https://static.codehs.com/img/library/characters/lizard.jpg",
    "https://static.codehs.com/img/library/characters/butterfly.jpg",
    "https://static.codehs.com/img/library/objects/icicle.png",
    "https://static.codehs.com/img/library/objects/helicopter.png",
    "https://static.codehs.com/img/library/objects/asteroid.png",
    "https://static.codehs.com/img/library/objects/soccerBall.png",
    "https://static.codehs.com/img/library/landscapes/flowers.jpg"]
    teagan = new WebImage(randomCari[Randomizer.nextInt(0, 10)]);
    teagan.setSize(30.76923076923077, 32);
    teagan.setPosition(x * SIZE_OF_OBJECTS_X, y * SIZE_OF_OBJECTS_Y);
    teagan.setColor("pink");
    add(teagan);
}
//Lava
let lava;
function lavaSet(x, y){
    lava = new Rectangle(PLAYER_W, PLAYER_H);
    lava.setPosition(x * SIZE_OF_OBJECTS_X, y * SIZE_OF_OBJECTS_Y);
    lava.setColor("red");
    add(lava);
}
//Win
var win;
function winSet(x, y){
    win = new Rectangle(PLAYER_W, PLAYER_H);
    win.setPosition(x * SIZE_OF_OBJECTS_X, y * SIZE_OF_OBJECTS_Y);
    win.setColor(Color.CYAN);
    add(win);
}

//---------------------------- move ment
keyDownMethod(keyDown);
function keyDown(kea){
    var pX = teagan.getX();
    var pY = teagan.getY();
    var elem = getElementAt(pX, pY);
    if(kea.key == "w" && jumpOff == true){
        setTimer(jumpUp, TICK_DELAY);
        jumpOff = false;
    }
    if(kea.key == "a"){ 
        if(getElementAt(pX - (SIZE_OF_OBJECTS_X / 4), pY + 1) == null 
        && getElementAt(pX - (SIZE_OF_OBJECTS_X / 4), pY + (PLAYER_H / 2)) == null 
        && getElementAt(pX - (SIZE_OF_OBJECTS_X / 4), (pY + PLAYER_H) - 1) == null
        && pX >= 0){
            teagan.move(- SIZE_OF_OBJECTS_X,0);
        }
    }
    if(kea.key == "d"){
        if(getElementAt((pX + PLAYER_W) + (SIZE_OF_OBJECTS_X / 4), pY + 1) == null 
        && getElementAt((pX + PLAYER_W) + (SIZE_OF_OBJECTS_X / 4), pY + (PLAYER_H / 2)) == null 
        && getElementAt((pX + PLAYER_W) + (SIZE_OF_OBJECTS_X / 4), (pY + PLAYER_H) - 1) == null
        && pX + PLAYER_W <= getWidth() - PLAYER_W){
            teagan.move(+ SIZE_OF_OBJECTS_X,0);
        }
    }
}
//var rect;
//mouseClickMethod(test);
/*function test(e) {
    rect = new Rectangle(SIZE_OF_OBJECTS_X, SIZE_OF_OBJECTS_Y);
    rect.setPosition(e.getX(), e.getY());
    rect.setColor("blue");
    add(rect);
}*/

//----------------------------Jump
function jumpUp(){
    if(getElementAt(teagan.getX() + 1, teagan.getY() - (SIZE_OF_OBJECTS_Y / 4)) == null 
        && getElementAt(teagan.getX() + (PLAYER_W / 2), teagan.getY() - (SIZE_OF_OBJECTS_Y / 4)) == null 
        && getElementAt(teagan.getX() + PLAYER_W - 1, teagan.getY() - (SIZE_OF_OBJECTS_Y / 4)) == null){
            if(jumpCounter < MAX_JUMP_HEIGHT){
                teagan.move(0, - (SIZE_OF_OBJECTS_Y / 2));
                jumpCounter += (SIZE_OF_OBJECTS_Y / 2);
            }else if(jumpCounter == MAX_JUMP_HEIGHT){
                jumpOff = true;
                jumpCounter = 0;
                stopTimer(jumpUp);
            }
    }else{
        jumpOff = true;
        jumpCounter = 0;
        stopTimer(jumpUp);
    }
}
//----------------------------Gravity
function gravity(){
    if(getElementAt(teagan.getX() + 1, (teagan.getY() + PLAYER_H) + (SIZE_OF_OBJECTS_Y / 4)) == null 
        && getElementAt(teagan.getX() + (PLAYER_W / 2), (teagan.getY() + PLAYER_H) + (SIZE_OF_OBJECTS_Y / 4)) == null 
        && getElementAt(teagan.getX() - 1 + PLAYER_W, (teagan.getY() + PLAYER_H) + (SIZE_OF_OBJECTS_Y / 4)) == null
        && jumpOff == true){
            teagan.move(0, +  (SIZE_OF_OBJECTS_Y / 2));
    }
}
/*
function lavaCheck(){
    if(getElementAt(teagan.getX() + 1, (teagan.getY() + PLAYER_H) + (SIZE_OF_OBJECTS_Y / 4)) == lava 
        && getElementAt(teagan.getX() + (PLAYER_W / 2), (teagan.getY() + PLAYER_H) + (SIZE_OF_OBJECTS_Y / 4)) == lava 
        && getElementAt(teagan.getX() - 1 + PLAYER_W, (teagan.getY() + PLAYER_H) + (SIZE_OF_OBJECTS_Y / 4)) == lava){
            removeAll();
    }
}
*/
function topCheck(){
    if(teagan.getY() <= 0){
        jumpOff = true;
        jumpCounter = 0;
        stopTimer(jumpUp);
    }
    
}

function lavaCheck(){
    let elmO = getElementAt(teagan.getX() + 1, (teagan.getY() + PLAYER_H) + (SIZE_OF_OBJECTS_Y / 4));
    let elmT = getElementAt(teagan.getX() + (PLAYER_W / 2), (teagan.getY() + PLAYER_H) + (SIZE_OF_OBJECTS_Y / 4));
    let elmTh = getElementAt(teagan.getX() - 1 + PLAYER_W, (teagan.getY() + PLAYER_H) + (SIZE_OF_OBJECTS_Y / 4));
    if(elmO != null && elmT != null && elmTh != null 
        && elmO.getColor() == "red"
        &&  elmT.getColor() == "red" 
        &&  elmTh.getColor() == "red"){
            removeAll();
            superLose();
    }
}

function winCheck(){
    let elmO = getElementAt(teagan.getX() + 1, (teagan.getY() + PLAYER_H) + (SIZE_OF_OBJECTS_Y / 4));
    let elmT = getElementAt(teagan.getX() + (PLAYER_W / 2), (teagan.getY() + PLAYER_H) + (SIZE_OF_OBJECTS_Y / 4));
    let elmTh = getElementAt(teagan.getX() - 1 + PLAYER_W, (teagan.getY() + PLAYER_H) + (SIZE_OF_OBJECTS_Y / 4));
    if(elmO != null && elmT != null && elmTh != null 
        && elmO.getColor() == Color.CYAN
        &&  elmT.getColor() == Color.CYAN
        &&  elmTh.getColor() == Color.CYAN){
            removeAll();
            winer = true;
            superWin();
    }
}
function superLose(){
    println("you lose");
}
function superWin(){
    println("you win");
}

async function music(){
    var soundA = new Sound("C2", "drum");
    var soundB = new Sound("A4", "triangle");
    var soundC = new Sound("B4", "triangle");
    var soundD = new Sound("C4", "triangle");
    var soundE = new Sound("D4", "triangle");
    var soundF = new Sound("E4", "triangle");
    setInterval(beat, 1000);
    function beat(){
        soundA.playFor(1);
    }
    setInterval(melidy, 2000);
    function melidy(){
        soundB.playFor(0.25);
        setTimeout(1);
        soundB.playFor(0.25);
    }
}
