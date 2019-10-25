var curlist = $('#active-list');
var tasklist = $("#task-list");
var lists =$('.list-name');
var listname = $("#new-list");
var tskcounter = 0;
function load_list(listname) {
  var xhr = new XMLHttpRequest()
  tskcounter = 0;
  $('.task').remove();
  xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
       // Typical action to be performed when the document is ready:
       data = JSON.parse(xhr.responseText)
       for(var i=0;i < data.length;i++) {
        newtask(data[i].text,data[i].checked);
       }
    }
  }
  xhr.open('GET','/todolists/'+listname+'/tasks',true)
  xhr.send()
  var xhr2 = new XMLHttpRequest()
  xhr2.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
       // Typical action to be performed when the document is ready:
       $('.task-count').text((JSON.parse(xhr2.responseText)['todo']).toString()+' tasks remaining')
       }
    }
  xhr2.open("GET","/todolists/"+curlist.text()+'/tasks/count/',true)
  xhr2.send();
}
function update_todo_lists(text) {
  $('.list-name').remove()
  arr = JSON.parse(text)
 for (var i = 0;i < arr.length; i++) {
    createList(arr[i])
 }
 tskcounter = 0;
  $('.task').remove();
  load_list($('#active-list').text())
}
var xhr = new XMLHttpRequest();
xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
       // Typical action to be performed when the document is ready:
       update_todo_lists(xhr.responseText);
       }
};
xhr.open('GET',"/todolists/")
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
        load_list(t.text())
      }

  })
  tasklist.append(ndom);
  curlist = $('#active-list');
  lists = $('.list-name')
  $('#list-title').text(curlist.text())
  updateDeleteButton();
}
}
$('#btn-newlist').on("click", function () {
var xhr = new XMLHttpRequest()
xhr.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
       // Typical action to be performed when the document is ready:
        update_todo_lists(xhr.responseText);
        listname.val('');
    }
  }

  xhr.open('POST','/todolists/',true)
    xhr.send(listname.val())
})
$('#list-creator').on("submit",function (event) {
  event.preventDefault();
  var xhr = new XMLHttpRequest()
  xhr.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
       // Typical action to be performed when the document is ready:
        update_todo_lists(xhr.responseText);
        listname.val('')
      }
  }
    xhr.open('POST','/todolists/',true)
    xhr.send(listname.val())
})
function list_delete_net() {
  var xhr = new XMLHttpRequest()
  xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
     update_todo_lists(xhr.responseText);
    }
  }
  xhr.open('DELETE','/todolists/',true)
  xhr.send(curlist.text())
}
$("#btn-dl").on("click", list_delete_net )
function newtask(text,checked) {
  var div = $('<div>')
  var input = $('<input>')
  var label= $("<label>")
  var span_cc = $("<span>")
  var span_txt = $("<span>")
  div.addClass("task")
  input.attr('type','checkbox')
  input.change(function() {
    var xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
       // Typical action to be performed when the document is ready:
       $('.task-count').text((JSON.parse(xhr.responseText)['todo']).toString()+' tasks remaining')
    }
  }
    xhr.open('POST','/todolists/'+curlist.text()+'/'+$(this).attr('id')+'/toggleChecked/',true)
    xhr.send()
  })
  if (checked) {input.attr('checked','true')}
  var taskid = tskcounter.toString()
  input.attr('id', taskid)
  div.append(input)
  label.attr('for',taskid)
  span_cc.addClass('custom-checkbox')
  label.append(span_cc)
  label.append(span_txt.text(text))
  div.append(label);
  $('.tasks').append(div);
  tskcounter++;
}
$('#btn-newtask').on('click', function() {
  var xhr = new XMLHttpRequest()
  xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
       // Typical action to be performed when the document is ready:
       tskcounter = 0;
  $('.task').remove();
       data = JSON.parse(xhr.responseText)
       for(var i=0;i < data.length;i++) {
        newtask(data[i].text,data[i].checked);
       }
    }
  }
  xhr.open("POST","/todolists/"+curlist.text()+'/tasks',true)
  xhr.send(JSON.stringify({text:$('#new-task').val(),checked:false}))
  $("#new-task").val('')
  var xhr2 = new XMLHttpRequest()
  xhr2.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
       // Typical action to be performed when the document is ready:
       $('.task-count').text((JSON.parse(xhr2.responseText)['todo']).toString()+' tasks remaining')
       }
    }
  xhr2.open("GET","/todolists/"+curlist.text()+'/tasks/count/',true)
  xhr2.send();
})
$("#task-creator").on('submit',function(event) {
  event.preventDefault();
  var xhr = new XMLHttpRequest()
  xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
       // Typical action to be performed when the document is ready:
       tskcounter = 0;
  $('.task').remove();
       data = JSON.parse(xhr.responseText)
       for(var i=0;i < data.length;i++) {
        newtask(data[i].text,data[i].checked);
       }
    }
  }
  xhr.open("POST","/todolists/"+curlist.text()+'/tasks',true)
  xhr.send(JSON.stringify({text:$('#new-task').val(),checked:false}))
  $("#new-task").val('')
  var xhr2 = new XMLHttpRequest()
  xhr2.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
       // Typical action to be performed when the document is ready:
       $('.task-count').text((JSON.parse(xhr2.responseText)['todo']).toString()+' tasks remaining')
       }
    }
  xhr2.open("GET","/todolists/"+curlist.text()+'/tasks/count/',true)
  xhr2.send();
})
$("#btn-cct").on('click', function() {
var xhr = new XMLHttpRequest()
  xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
       // Typical action to be performed when the document is ready:
       tskcounter = 0;
  $('.task').remove();
       data = JSON.parse(xhr.responseText)
       for(var i=0;i < data.length;i++) {
        newtask(data[i].text,data[i].checked);
       }
    }
  }
  xhr.open("POST","/todolists/"+curlist.text()+'/cct',true)
  xhr.send();

})


