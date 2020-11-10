
var myblock = document.querySelectorAll('.del_btn_active');
myblock.forEach(block => block.addEventListener('click', removeBlock));
var choice_counter = 2;
function removeBlock() {
  let block = this;
  block.parentNode.style.opacity = 1;

  let blockId = setInterval(function() {
    if (block.parentNode.style.opacity > 0) block.parentNode.style.opacity -= .1;
    else {
  	clearInterval(blockId);
  	block.parentNode.remove();
    }
  }, 50)
}

document.getElementById('add_btn').addEventListener('click', addBlock);
function addBlock() {
choice_counter ++;

let counter_field = document.getElementById('counter_field');
counter_field.value ++; 

let elems = document.getElementsByClassName('inpdiv');
console.log(elems.length);

let inpdiv = document.createElement('div');
inpdiv.className = "inpdiv";

let inpfield = document.createElement('input');
inpfield.className = "inpfield";
inpfield.type="text";
inpfield.placeholder="Вариант ответа";
inpfield.name = 'choice' + choice_counter;

let delbtn = document.createElement('div');
delbtn.className = "del_btn_active";

inpdiv.appendChild(inpfield);
inpdiv.appendChild(delbtn);

document.getElementById("polls").appendChild(inpdiv);

myblock = document.querySelectorAll('.del_btn_active');
myblock.forEach(block => block.addEventListener('click', removeBlock));
}