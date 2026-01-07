/**
 * @prop {event} event
 */
function addProfileListItem(event) {
    let listContainer = event.target.closest('.scrollable-container');
    let list = listContainer.querySelector('.scrollable-list');
    let newItem = document.createElement('li');
    let itemInput = document.createElement('input');
    let saveItemButton = document.createElement('button');
    
    saveItemButton.classList.add('accent');
    saveItemButton.classList.add('save-item-btn');
    saveItemButton.type = 'button';
    saveItemButton.textContent = 'Сохранить';
    saveItemButton.addEventListener('mousedown', function(event) {
        saveNewItem(event, newItem, list);
    });

    newItem.classList.add('new-list-item');

    newItem.appendChild(itemInput);
    newItem.appendChild(saveItemButton);

    list.prepend(newItem);

    itemInput.focus();
    itemInput.addEventListener('blur', newItemLostFocus)
}


/**
 * @param {event} event 
 */
function newItemLostFocus(event) {
    let item = this.parentElement;
    item.remove();
}


/**
 * @param {event} event
 * @param {HTMLInputElement} itemInput
 * @param {HTMLUListElement} list
 */
function saveNewItem(event, newItem, list) {
    content = newItem.querySelector('input').value;
    newItem.remove();
    
    if (content === undefined || content === null || content === '') {
        return;
    }

    item = document.createElement('li');
    item.dataset.content = content;
    
    list.prepend(item);

    submitProfileForm(form, hiddenInputsContainer);
}