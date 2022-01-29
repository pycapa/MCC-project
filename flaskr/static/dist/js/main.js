'use strict'


var modalWrap = null;

const btnSubmit = document.querySelector('#btn-submit')
btnSubmit.addEventListener('click', (e)=>{
    e.preventDefault()

    const $form = document.querySelector('form') 
    console.log($form);
    fetch($form.action,{
        method: $form.method,
        body: new FormData($form)
    }, 
    spin())
    .then(res => res.json())
    .then(()=>location.reload())
    .catch(err => alert(err))
    /* 


    e.preventDefault()
    spin()
    location.reload()
 */})

window.addEventListener('load', ()=>{
    const date = new Date().toLocaleString();
    const date_time = document.querySelector('.date-time');
    date_time.innerHTML = `${date}`;

})

document.addEventListener('click', (event) => {

    // Validate if was click on menu and show menu option in header.
    menu_click(event, event.target);

});

function menu_click(event, target){
    const menu = document.getElementsByClassName('menu-option');
    const icons = document.querySelectorAll('.icon-option');
    const header = document.querySelector('.title-header')
    const icon_header = document.querySelector('.icon-header i')
    for(let i=0; i<(menu.length); i++){
        menu[i].classList.remove('active')
        if (target.innerText === menu[i].innerText) {
            header.innerHTML =  target.innerText
            icon_header.className = icons[i].className;   
            menu[i].classList.add('active')      
        }
    }

}

function createModalWindow(){

    // Creatting modal window for validation.
    if (modalWrap !== null){
        modalWrap.remove()
    }

    modalWrap = document.createElement('div');
    modalWrap.innerHTML = `
            <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true" data-bs-backdrop='static'>
            <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">CONFIRMATION</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                Are you shure to delete this:?
                </div>
                <div class="modal-footer">
                <a class="btns btn-submit" data-bs-dismiss="modal" data-response='cancel'>Cancel</a>
                <a class="btns btn-delete modal-success-btn" data-bs-dismiss="modal" data-response = 'delete'>Delete</a>
                </div>
            </div>
            </div>
        </div>
    `
    document.body.append(modalWrap)
    const modal = new bootstrap.Modal(modalWrap.querySelector('.modal'));
    return modal
}

// Delete records.
const $btnDelete = document.querySelectorAll('#btn-delete') 

$btnDelete.forEach(btn => {
    btn.addEventListener('click', ()=>{
        var id = btn.parentElement.id
        var dataset = btn.parentElement.dataset.table
        var key = btn.parentElement.dataset.key

        const modal = createModalWindow()
        const modalresponse = document.querySelector('.modal')


        modalresponse.addEventListener('hide.bs.modal', function(event){
            const confirm = event.explicitOriginalTarget.dataset.response
            if (confirm=='delete'){
                fetch(`/delete/${id},${dataset},${key}`,{
                    method:'POST'
                }, spin())
                .then(res => res.json())
                .then(data => {
                    console.log(data)
                    location.reload()})
                .catch(err => console.log(err))
            }

        })
        
        modal.show()

    })
});


// spin function

function spin(loadding=true){
    
    const spinDiv = document.createElement('div')
    spinDiv.innerHTML = '<div id="circle"></div>'
    document.body.append(spinDiv)
    const spin = document.querySelector('#circle')
    spin.classList.add('circle')
    
}
