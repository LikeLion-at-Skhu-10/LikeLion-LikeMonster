let modal = document.querySelector('#modal-notice'),
    modalActive = document.querySelector('#modal-active'),
    modalClose = document.querySelector('#modal-close');

function openModal() {
    modal.classList.add('active');
    document.querySelector('body').style.overflow = 'hidden';
}

function closeModal() {
    modal.classList.remove('active');
    document.querySelector('body').style.overflow = 'visible';
}

modalActive.addEventListener('click', openModal)
modalClose.addEventListener('click', closeModal)