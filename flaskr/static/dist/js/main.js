'use strict'

window.addEventListener('load', ()=>{
    const date = new Date().toLocaleString();
    const date_time = document.querySelector('.date-time');
    date_time.innerHTML = `${date}`;
})

document.addEventListener('click', (event) => {

    // Validate if was click on menu and show menu option in header.
    menu_click(event.target);
});

function menu_click(target){
    const menu = document.querySelectorAll('.menu-option');
    const icons = document.querySelectorAll('.icon-option');
    const header = document.querySelector('.title-header')
    const icon_header = document.querySelector('.icon-header i')

    const elements = [];
    for(let i=0; i<(menu.length); i++){

        if (target.innerText === menu[i].innerText) {
            console.log(target.innerText);
            console.log(icons[i].className)
            header.innerHTML =  target.innerText
            icon_header.className = icons[i].className;          
        }

    }
}

function close_modal(){
    const modal = document.querySelector(".modal");
    modal.style.setProperty('Display', 'None');
}