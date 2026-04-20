(function(){
  function messageFor(input){
    const label = input.dataset.label || input.name || 'Trường này';
    const validity = input.validity || {};
    if (validity.valueMissing) return `${label} không được để trống.`;
    if (validity.typeMismatch && input.type === 'email') return 'Email không đúng định dạng.';
    if (validity.patternMismatch && input.name === 'phone') return 'Số điện thoại không hợp lệ.';
    if (validity.tooShort) return `${label} phải có ít nhất ${input.getAttribute('minlength')} ký tự.`;
    if (input.name && input.name.includes('password') && input.value && input.value.length < 8) return 'Mật khẩu phải có ít nhất 8 ký tự.';
    return input.validationMessage || '';
  }
  function errorNode(input){
    const id = input.id;
    if (!id) return null;
    return document.querySelector(`[data-error-for="${id}"]`);
  }
  function show(input){
    const node = errorNode(input);
    if (!node) return;
    if (input.checkValidity()) {
      node.textContent = '';
      input.classList.remove('is-invalid');
      return;
    }
    node.textContent = messageFor(input);
    input.classList.add('is-invalid');
  }
  document.querySelectorAll('form.live-validate-form input, form.live-validate-form select, form.live-validate-form textarea').forEach((input) => {
    input.addEventListener('input', ()=>show(input));
    input.addEventListener('change', ()=>show(input));
    input.addEventListener('blur', ()=>show(input));
    input.addEventListener('invalid', (e)=>{e.preventDefault(); show(input);});
  });
})();
