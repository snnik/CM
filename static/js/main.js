var headertext = [],
    headers = document.querySelectorAll(".responce-table th"),
    tablerows = document.querySelectorAll(".responce-table th"),
    tablebody = document.querySelector(".responce-table tbody");

for (var i = 0; i < headers.length; i++) {
    var current = headers[i];
    headertext.push(current.textContent.replace(/\r?\n|\r/, ""));
}
for (var i = 0, row; row = tablebody.rows[i]; i++) {
    for (var j = 0, col; col = row.cells[j]; j++) {
        col.setAttribute("data-th", headertext[j]);
    }
}

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
};

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

$(document).ready(function() {
    $('.nav-link-collapse').on('click', function() {
            $('.nav-link-collapse').not(this).removeClass('nav-link-show');
            $(this).toggleClass('nav-link-show');
        });
});

