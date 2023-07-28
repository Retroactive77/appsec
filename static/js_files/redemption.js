var minValue = 1;  // Lower limit
var maxValue = 20;   // Upper limit

function increment() {
  var input = document.getElementById('quantity');
  var value = parseInt(input.value, 10);
  if (value < maxValue) {
    input.value = value + 1;
  }
}

function decrement() {
  var input = document.getElementById('quantity');
  var value = parseInt(input.value, 10);
  if (value > minValue) {
    input.value = value - 1;
  }
}


