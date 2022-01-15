'use strict'


var modalWrap = null;



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


function delete_item(id, table, field_id, url_return, message){

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
                Are you shure to delete this: ${message} ?
                </div>
                <div class="modal-footer">
                <a class="btns btn-submit" data-bs-dismiss="modal">Cancel</a>
                <a class="btns btn-delete modal-success-btn" data-bs-dismiss="modal">Delete</a>
                </div>
            </div>
            </div>
        </div>
    `
    modalWrap.querySelector('.modal-success-btn').onclick = ()=>{
        
        var data = JSON;

        data = {
            "id" : id,
            "table" : table,
            "field_id" : field_id,
            "url_return" : url_return
        }
        // Server Request
        var client = new XMLHttpRequest();

        client.open("POST", "/delete")
        client.setRequestHeader("Content-Type", "application/json")
        client.setRequestHeader("Location", `/${data['url_return']}`)
        
        client.onreadystatechange = function() {
            location.reload()
        }
        client.send(JSON.stringify(data))

    };

    document.body.append(modalWrap)
    var modal = new bootstrap.Modal(modalWrap.querySelector('.modal'));
    modal.show();

/* 



    var myModalEl = document.getElementById('exampleModal')

    var modal = new bootstrap.Modal(myModalEl) // initialized with defaults

    modal.show()

    myModalEl.addEventListener('hidden.bs.modal', function (event) {
        console.log(event.currentTarget) 
        })
 */}


