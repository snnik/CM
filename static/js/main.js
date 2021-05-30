function escape(string) {
    var htmlEscapes = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;'
    };

    return string.replace(/[&<>"']/g, function(match) {
        return htmlEscapes[match];
    });
}

function idvalue(){
  var elem = event.target;
  var url = "/";
  var pk;
  url = window.location.origin + elem.parentElement.cells[0].textContent;
  $('#person-content').load(url);
}

function loadForList(url){
  $('#person-content').load(window.location.origin + url);
}

function LoadEvent(obj, uri){
    let listItems = document.querySelectorAll('.list-rectangle .active');
    for (let item of listItems) {
        item.classList.toggle("active");
    }
    obj.classList.add("active");
    loadForList(uri);
}

function getTblElem(id, table){
    let idArray = [];
    let elem;
    let i = 0;
    $('#'+ table +'-table th').each(function(){
        elem = $(this).text();
        if (id != elem){
            idArray[i] = elem;
            i++;
        }
    });
    return idArray;
}

function refreshTables(d){
    let idArray = [];
    let content;
    idArray = getTblElem(d['pk'], d['cname']);
    content = '?';
    idArray.forEach(function(item, i, arr){
        content += 'id=' + item + '&';
    });
    $('#'+ d['cname'] + '-table').load(window.location.origin + d['cname'] + '/ajax/' + content + '/');
}

function modalid(){
    var elem = event.target;
    var url = "/";
    url = elem.parentElement.cells[1].textContent;
    $('#exampleModalCenter').modal('show');
    loadContent(url);
}

function loadContent(uri){
    $("#modal-body").load(window.location.origin + uri);
    chanelBtn = '<button type="button" class="btn btn-icon btn-secondary" data-dismiss="modal"><span class="icon"><i class="fas fa-window-close"></i></i></span>Закрыть</button>';
    submitBtn = '<button id="submitModal" type="button" class="btn btn-icon btn-primary" onclick="ServerQuery('+ "'"+ uri +"'"+')"> <span class="icon"><i class="far fa-save"></i></span> Сохранить </button>';
    $('#submitBlock').html(chanelBtn);
    $(submitBtn).appendTo('#submitBlock');
}

function unblockedInputField(e){
    e.readOnly = false;
}

function blockedInputField(e){
    e.readOnly = true;
    e.value = '';
}

function onChangeEventSelect(e){
    var sIndex = e.selectedIndex;
    if (sIndex === 0){
        blockedObjectId = '#id_locality';
        unblockedObjectId = '#id_city';
    } else if (sIndex === 1){
        blockedObjectId = '#id_city';
        unblockedObjectId = '#id_locality';
    }
    blockedInputField(document.querySelector(blockedObjectId));
    unblockedInputField(document.querySelector(unblockedObjectId));
}

function onChangeEventInput(e){
    if (!e.readOnly){

        if (e.id === 'id_locality') {
            blockedObjectId = '#id_city';
            sIndex = 1;
        } else if (e.id === 'id_city') {
            blockedObjectId = '#id_locality';
            sIndex = 0;
        }
        blockedInputField(document.querySelector(blockedObjectId));
        selectObject = document.querySelector('#id_terrain');
        selectObject.selectedIndex = sIndex;
    }
}

$(document).ready(function() {
    $('.nav-link-collapse').on('click', function() {
            $('.nav-link-collapse').not(this).removeClass('nav-link-show');
            $(this).toggleClass('nav-link-show');
        });



});
