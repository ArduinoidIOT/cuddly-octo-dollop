var new_list = $('#btn-newlist');
var curlist = $('#active-list');
var form = $('#list-creator');
var tasklist = $("#task-list");
var lists =$('.list-name');
var listname = $("#new-list");
var delete_list = $("#btn-dl");
var xhr = new XMLHttpRequest();
xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
       // Typical action to be performed when the document is ready:
       arr = JSON.parse(xhr.responseText)
       for (var i = 0;i < arr.length; i++) {
          createList(arr[i])
       }
    }
};
xhr.open('GET',"/todolists")
xhr.send();
function updateDeleteButton() {
lists =$('.list-name');
 if (lists.length < 2) {
    $("#btn-dl").hide()
  } else {
    $("#btn-dl").show()
  }
}

function createList(listname_new) {
  if( listname_new != '') {
  curlist.attr('id','')
  var ndom = $('<li>');
  ndom.text(listname_new)
  ndom.addClass('list-name');
  ndom.attr('id','active-list');
  ndom.on('click', function () {
      var t = $(this)
      if (curlist != t ) {
        curlist.attr('id','')
        t.attr('id','active-list');
        curlist = t;
        $('#list-title').text(curlist.text())
      }
  })
  tasklist.append(ndom);
  curlist = $('#active-list');
  lists = $('.list-name')
  updateDeleteButton();
  $('#list-title').text(curlist.text())
  return 0;
}
}
new_list.on("click", function () {
var xhr = new XMLHttpRequest()
xhr.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
       // Typical action to be performed when the document is ready:
      if (xhr.responseText == 'Success') {
        createList(listname.val());
        listname.val('');
      }
    }
  }
  console.log('/todolists/create/'+listname.val())
  xhr.open('POST','/todolists/create/'+listname.val(),true)
    xhr.send()
})
form.on("submit",function (event) {
  event.preventDefault();
  var xhr = new XMLHttpRequest()
  xhr.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
       // Typical action to be performed when the document is ready:
        if (xhr.responseText == 'Success') {
          createList(listname.val());
          listname.val('');
        }
      }
  }
    xhr.open('POST','/todolists/create/'+listname.val(),true)
    xhr.send()
})
delete_list.on("click", function() {
var xhr = new XMLHttpRequest()
  xhr.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
       // Typical action to be performed when the document is ready:
          curlist.remove();
          lists =$('.list-name');
          lists.first().attr('id','active-list')
          curlist = lists.first();
          updateDeleteButton();
           $('#list-title').text(curlist.text())
      }
  }
    xhr.open('POST','/todolists/delete/'+curlist.text(),true)
    xhr.send()
})
