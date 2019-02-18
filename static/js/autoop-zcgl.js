
window.onload = function() {
    changePage();
};


//模态框
function modal() {
    var modal_lay = document.getElementById('modal-overlay');
    modal_lay.style.display = (modal_lay.style.display == "block") ? "none" : "block";
    var modal_data = modal_lay.getElementsByClassName('modal-data')[0];
    modal_data.style.display = (modal_data.style.display == "block") ? "none" : "block";
    if(modal_data.style.display == "block")
    {
        setTimeout(function () {
            modal_data.className = "modal-data active";
        }, 0);
        document.getElementById('inputIP').value = null;
        document.getElementById('inputhostname').value = null;
        document.getElementById('inputproduct').value = null;
        document.getElementById('inputapplication').value = null;
        document.getElementById('inputjg').value = null;
        document.getElementById('inputstatus').value = null;
        document.getElementById('inputremark').value = null;
        modal_data.getElementsByClassName("submit")[0].onclick = function () {
            var sendData = {
                "operate": "insert",
                "ip": document.getElementById('inputIP').value,
                "hostname": document.getElementById('inputhostname').value,
                "product": document.getElementById('inputproduct').value,
                "application": document.getElementById('inputapplication').value,
                "jg": document.getElementById('inputjg').value,
                "status": document.getElementById('inputstatus').value,
                "remark": document.getElementById('inputremark').value
            };
            console.log(sendData);
            var result = $.ajax({
                url: './dataBase.json',
                data: sendData,
                dataType: 'JSON',
                type: 'post',
                success: function () {
                    document.getElementById('page').click();
                    var jsonData = JSON.parse(result.responseText);
                    var modal_alert = document.getElementsByClassName("modal-alert")[0];
                    if(jsonData.result == "success") {
                        // alert("操作成功");
                        modal_alert.innerText = "添加成功";
                        modal_alert.className = "modal-alert active";
                        setTimeout(function () {
                            modal_alert.className = "modal-alert alert-disappear";
                        }, 3000);
                        document.getElementById('page').click();
                    } else {
                        // alert("操作失败");
                        modal_alert.innerText = "操作失败";
                        modal_alert.className = "modal-alert error";
                        setTimeout(function () {
                            modal_alert.className = "modal-alert error-disappear";
                        }, 3000);
                        document.getElementById('page').click();
                    }
                }
            });
            modal();
        };
    } else {
        modal_data.className = "modal-data";
    }

}

function modalChange(aChange) {
    var grandfather = aChange.parentNode.parentNode;
    var modal_lay = document.getElementById('modal-overlay');
    modal_lay.style.display = "block";
    var modal_data = modal_lay.getElementsByClassName('modal-data')[0];
    modal_data.style.display = "block";
    setTimeout(function () {
        modal_data.className = "modal-data active";
    }, 0);
    var row = grandfather.getElementsByTagName('td');
    var IP = row[0].innerText;
    document.getElementById('inputIP').value = IP;
    document.getElementById('inputhostname').value = row[1].innerText;
    document.getElementById('inputproduct').value = row[2].innerText;
    document.getElementById('inputapplication').value = row[3].innerText;
    document.getElementById('inputjg').value = row[4].innerText;
    document.getElementById('inputstatus').value = row[5].innerText;
    document.getElementById('inputremark').value = row[6].innerText;
    modal_data.getElementsByClassName("submit")[0].onclick = function () {
        var sendData = {
            "operate": "update",
            "updateIP": IP,
            "ip": document.getElementById('inputIP').value,
            "hostname": document.getElementById('inputhostname').value,
            "product": document.getElementById('inputproduct').value,
            "application": document.getElementById('inputapplication').value,
            "jg": document.getElementById('inputjg').value,
            "status": document.getElementById('inputstatus').value,
            "remark": document.getElementById('inputremark').value
        };
        console.log(sendData);
        var result = $.ajax({
            url: './dataBase.json',
            data: sendData,
            dataType: 'JSON',
            type: 'post',
            success: function () {
                document.getElementById('page').click();
                var jsonData = JSON.parse(result.responseText);
                var modal_alert = document.getElementsByClassName("modal-alert")[0];
                if(jsonData.result == "success") {
                    // alert("操作成功");
                    modal_alert.innerText = "修改成功";
                    modal_alert.className = "modal-alert active";
                    setTimeout(function () {
                        modal_alert.className = "modal-alert alert-disappear";
                    }, 3000);
                    document.getElementById('page').click();
                } else {
                    // alert("操作失败");
                    modal_alert.innerText = "操作失败";
                    modal_alert.className = "modal-alert error";
                    setTimeout(function () {
                        modal_alert.className = "modal-alert error-disappear";
                    }, 3000);
                    document.getElementById('page').click();
                }
            }
        });
        modal();
    };
}


//下架主机
function remove(aDelete) {
    var modal_lay = document.getElementById('modal-overlay');
    modal_lay.style.display = (modal_lay.style.display == "block") ? "none" : "block";
    var modal_confirm = modal_lay.getElementsByClassName('modal-confirm')[0];
    modal_confirm.style.display = (modal_confirm.style.display == "block") ? "none" : "block";
    if(modal_confirm.style.display == "block")
    {
        setTimeout(function () {
            modal_confirm.className = "modal-confirm confirm-active";
        }, 0);
        modal_confirm.getElementsByClassName("submit")[0].onclick = function() {
            var grandfather = aDelete.parentNode.parentNode;
            var row = grandfather.getElementsByTagName('td');
            var IP = grandfather.getElementsByTagName('td')[1].innerText;
            var sendData = {
                "operate": "delete",
                "deleteIP": IP,
                "ip": row[1].innerText,
                "hostname": row[2].innerText,
                "product": row[3].innerText,
                "application": row[4].innerText,
                "jg": row[5].innerText,
                "status": row[6].innerText,
                "remark": row[7].innerText
            };
            var result = $.ajax({
                url: './dataBase.json',
                data: sendData,
                dataType: 'JSON',
                type: 'post',
                success: function () {
                    var jsonData = JSON.parse(result.responseText);
                    var modal_alert = document.getElementsByClassName("modal-alert")[0];
                    if(jsonData.result == "success") {
                        // alert("操作成功");
                        modal_alert.innerText = "下架成功";
                        modal_alert.className = "modal-alert active";
                        setTimeout(function () {
                            modal_alert.className = "modal-alert alert-disappear";
                        }, 3000);
                        document.getElementById('page').click();
                    } else {
                        // alert("操作失败");
                        modal_alert.innerText = "操作失败";
                        modal_alert.className = "modal-alert error";
                        setTimeout(function () {
                            modal_alert.className = "modal-alert error-disappear";
                        }, 3000);
                        document.getElementById('page').click();
                    }
                    console.log(IP);
                }
            });
            modal_confirm.className = "modal-confirm confirm-disappear";
            setTimeout(function () {
                modal_lay.style.display = "none";
                modal_confirm.style.display = "none";
                modal_confirm.className = "modal-confirm";
            }, 200);
        };
    } else {
        modal_confirm.className = "modal-confirm";
    }
}


//分页函数
function changePage() {
    var contain = document.getElementsByClassName('main-contain-zijinguanli');
    var theTable = document.getElementsByClassName('theTable');
    var tbody = theTable[0].getElementsByTagName('tbody')[0];
    var btn = contain[0].getElementsByClassName('contain-footer')[0].getElementsByTagName('a');
    var pagesNumber = btn.length - 2;                           //得到总页数
    console.log(pagesNumber);
    var page = 1;                                               //当前页初始化为1

    btn[page].getElementsByTagName('div')[0].id= 'page';       //当前页设置id=page

    btn[0].getElementsByTagName('div')[0].id = 'disable';      //给前一页设置不可选,设置id=disable

    if (pagesNumber == 1) {                                    //如果只有一页，设置后一页也无法被选取id=disable
         btn[btn.length - 1].getElementsByTagName('div')[0].id = "disable";
    }


    //点击页号时发生
     (function whenClick(clickPage){
         page = clickPage;
         //设置样式
         document.getElementById('page').id = null;
         btn[clickPage].getElementsByTagName('div')[0].id= 'page';      //当前页设置id=page

         btn[0].getElementsByTagName('div')[0].id = null;
         btn[btn.length - 1].getElementsByTagName('div')[0].id = null;

         if (clickPage == 1) {
              btn[0].getElementsByTagName('div')[0].id = 'disable';     //给前一页设置不可选,设置id=disable
         }

         if (clickPage == pagesNumber) {                                //如果只有一页，设置后一页也无法被选取id=disable
              btn[btn.length - 1].getElementsByTagName('div')[0].id = "disable";
         }

         //设置连接
        //  for (var i = 0; i < btn.length; i++) {                         //所有页设置不可选
            //  $(btn[i]).click(function(e){
            //      e = e|| window.event;                                  //使其兼容ie，ie才有window.event
            //      e.preventDefault();
            //   });
        //  }
         //点击页号
         for(let selectPage = 1; selectPage <= pagesNumber; selectPage++ ) {
             if(selectPage != page) {
                 btn[selectPage].onclick = function() {
                     var result = $.ajax({
                         url: './page2.json',                           //  :./asset/host_last
                         data: {"selectPage": selectPage},
                         dataType: 'JSON',
                         type: 'post',
                         success: function(){
                             console.log("success");
                             console.log(result.responseText);
                             console.log("请求的是第" + selectPage + "页");
                             var jsonData = JSON.parse(result.responseText);
                             tbody.innerHTML = null;
                             for (var i=0; i<jsonData.length; i++) {
                                 var row = jsonData[i];
                                 for (var id in row) {
                                     tbody.innerHTML += ('<tr><td>'+id+'</td><td>'+row[id].ip+'</td><td>'+row[id].hostname+'</td><td>'+row[id].product+'</td><td>'+row[id].application+'</td><td>'+row[id].jg+'</td><td>'+row[id].status+'</td><td>'+row[id].remark+'</td><td><a onclick="modalChange(this)" class="fa">&#xf0ad;</a>&emsp;<a onclick="remove(this)" class="fa">&#xf014;</a></td></tr>');
                                 }
                             }
                             whenClick(selectPage);
                         }
                     });
                 };
             }
         }
         //前一页和后一页
         btn[0].onclick = function() {
             if(page != 1) {
                 var selectPage = page - 1;
                 var result = $.ajax({
                     url: './page2.json',                           //  :./asset/host_last
                     data: {"selectPage": selectPage},
                     dataType: 'JSON',
                     type: 'post',
                     success: function(){
                         console.log("success");
                         console.log(result.responseText);
                         console.log("请求的是第" + selectPage + "页");
                         var jsonData = JSON.parse(result.responseText);
                         tbody.innerHTML = null;
                         for (var i=0; i<jsonData.length; i++) {
                             var row = jsonData[i];
                             for (var id in row) {
                                 tbody.innerHTML += ('<tr><td>'+id+'</td><td>'+row[id].ip+'</td><td>'+row[id].hostname+'</td><td>'+row[id].product+'</td><td>'+row[id].application+'</td><td>'+row[id].jg+'</td><td>'+row[id].status+'</td><td>'+row[id].remark+'</td><td><a onclick="modalChange(this)" class="fa">&#xf0ad;</a>&emsp;<a onclick="remove(this)" class="fa">&#xf014;</a></td></tr>');
                             }
                         }
                         whenClick(selectPage);
                     }
                 });
             }
         };
         btn[pagesNumber + 1].onclick = function() {
             if(page != pagesNumber) {
                 var selectPage = page + 1;
                 var result = $.ajax({
                     url: './page2.json',                           //  :./asset/host_last
                     data: {"selectPage": selectPage},
                     dataType: 'JSON',
                     type: 'post',
                     success: function(){
                         console.log("success");
                         console.log(result.responseText);
                         console.log("请求的是第" + selectPage + "页");
                         var jsonData = JSON.parse(result.responseText);
                         tbody.innerHTML = null;
                         for (var i=0; i<jsonData.length; i++) {
                             var row = jsonData[i];
                             for (var id in row) {
                                 tbody.innerHTML += ('<tr><td>'+id+'</td><td>'+row[id].ip+'</td><td>'+row[id].hostname+'</td><td>'+row[id].product+'</td><td>'+row[id].application+'</td><td>'+row[id].jg+'</td><td>'+row[id].status+'</td><td>'+row[id].remark+'</td><td><a onclick="modalChange(this)" class="fa">&#xf0ad;</a>&emsp;<a onclick="remove(this)" class="fa">&#xf014;</a></td></tr>');
                             }
                         }
                         whenClick(selectPage);
                     }
                 });
             }
         };
     })(page);
}
