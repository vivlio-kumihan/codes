// const select = document.getElementById('select');
// select.addEventListener('change', (e) => {
//   const selectValue = document.getElementById('selectValue');
//   selectValue.innerHTML = e.target.value;
// });

const hash = {};
hash.name = "hello"
console.log(hash);

const input = document.getElementById('input');
input.addEventListener('input', () => {
  const inputValue = document.getElementById('inputValue');
  inputValue.innerHTML = input.value;
});

const select = document.getElementById('select');
select.addEventListener('change', () => {
  const selectValue = document.getElementById('selectValue');
  selectValue.innerHTML = select.value;
});


// const select = document.getElementById('select');
// select.addEventListener('change', () => {
//   const selectValue = document.getElementById('selectValue');
//   selectValue.innerHTML = select.options[select.selectedIndex].innerHTML;
// });

