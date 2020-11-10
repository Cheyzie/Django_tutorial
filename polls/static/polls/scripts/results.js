
var elements = document.getElementById('ul1').getElementsByTagName('li').length;
var values = [];
for (let i = 1; i <= elements; i++) {
  values[i-1] = document.getElementById("res"+i).value;
}
Array.prototype.max = function() {
  return Math.max.apply(null, this);
};

var sum = 0;
for (let i = 0; i < values.length; i++) {
  sum = sum + values[i];
}
for (let i = 1; i <= values.length; i++) {
  let percent = (values[i-1]/sum)*100;
  let width_percent = (values[i-1]/(values.max()))*85
  document.getElementById("div"+i).style.width = width_percent +"%";
  document.getElementById("per"+i).innerHTML = Math.round(percent) +"%";
}