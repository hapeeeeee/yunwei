// var resultDom = document.getElementsByClassName("return-result")[0];
// var softwaresDom = document.getElementsByClassName("install-softwares")[0];


var mastersData = {
    "targets": ["zhangzhao", "lc"],
    "softwares": []
};

window.onload = loadThePage();

function loadThePage() {
    var mastersDom = document.getElementsByClassName("select-masters")[0];
    mastersDom.innerHTML = "";
    for(var value of mastersData.targets) {
        mastersDom.innerHTML += "<div id=master_" + value + "><div>&nbsp;" + value + "&nbsp;</div><div><a class=\"fa fa-close\" onclick=\"deleteMaster(this)\"></a></div></div>"
    }
    // 判断软件/文件函数
    (function getActive() {
        var active = document.getElementsByClassName("contain-header")[0].children[1].children[0].className;
        if(active == "active") {
            softwarePage();
        } else {
            filePage();
        }
    })();
}

function softwarePage() {
    var theSoftPage = document.getElementsByClassName("part-softwares")[0];
    var theFilesPage = document.getElementsByClassName("part-files")[0];
    theSoftPage.style.display = "block";
    theFilesPage.style.display = "none";
}

function filePage() {
    var theSoftPage = document.getElementsByClassName("part-softwares")[0];
    var theFilesPage = document.getElementsByClassName("part-files")[0];
    theSoftPage.style.display = "none";
    theFilesPage.style.display = "block";
}

function deleteMaster(theTag) {
    var theId = theTag.parentElement.parentElement.id;
    var deleteData = theId.slice(7);
    for (var key in mastersData.targets) {
        if(deleteData == mastersData.targets[key]) {
            mastersData.targets.splice(key, 1);
        }
    }
    var deleteDom = document.getElementById(theId);
    deleteDom.remove();
}

function selectSoftwares(theTag) {
    var parent = theTag.parentElement;
    var theId = parent.parentElement.id.slice(10);    
    parent.innerHTML = "<a class=\"fa fa-check-square-o\" onclick=\"disSelectSoftwares(this)\"></a>"
    if(mastersData.softwares.indexOf(theId) == -1) {
        mastersData.softwares.push(theId);
        console.log(mastersData.softwares);
    }
}

function disSelectSoftwares(theTag) {
    var parent = theTag.parentElement;
    var deleteData = parent.parentElement.id.slice(10);
    parent.innerHTML = "<a class=\"fa fa-square-o\" onclick=\"selectSoftwares(this)\"></a>"
    for (var key in mastersData.softwares) {
        if(deleteData == mastersData.softwares[key]) {
            mastersData.softwares.splice(key, 1);
            console.log(mastersData.softwares);            
        }
    }
}

function selectMaster(theTag) {
    var parent = theTag.parentElement;
    var theId = parent.parentElement.id.slice(14);
    parent.innerHTML = "<a class=\"fa fa-check-square-o\" onclick=\"disSelectMaster(this)\"></a>"
    if(mastersData.targets.indexOf(theId) == -1) {
        mastersData.targets.push(theId);
        console.log(mastersData.targets);
    }
}

function disSelectMaster(theTag) {
    var parent = theTag.parentElement;
    parent.innerHTML = "<a class=\"fa fa-square-o\" onclick=\"selectMaster(this)\"></a>"
    var theId = parent.parentElement.id;
    var deleteData = theId.slice(14);
    for (var key in mastersData.targets) {
        if(deleteData == mastersData.targets[key]) {
            mastersData.targets.splice(key, 1);
        }
    }
    console.log(mastersData.targets);
}

function activeTo1(theTag) {
    var grandfather = theTag.parentElement.parentElement;
    var topTitle = document.getElementsByClassName("index-main-top-nav")[0].lastChild;
    topTitle.innerText = "部署文件";
    console.log(topTitle);
    grandfather.innerHTML = "<li><a onclick=\"activeTo2(this)\">部署软件</a></li><li class=\"active\">部署文件</li>";
    console.log(grandfather);
    loadThePage();
}

function activeTo2(theTag) {
    var grandfather = theTag.parentElement.parentElement;
    var topTitle = document.getElementsByClassName("index-main-top-nav")[0].lastChild;
    topTitle.innerText = "部署软件";
    grandfather.innerHTML = "<li class=\"active\">部署软件</li><li><a onclick=\"activeTo1(this)\">部署文件</a></li>";
    console.log(grandfather);
    loadThePage();
}

function addMasters() {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if(xhr.readyState === 4) {
            if(xhr.status === 200) {
                console.log(xhr.responseText);
                var jsonData = xhr.responseText;
                var objData = JSON.parse(jsonData);
                modalPrintf(objData.targets);
            }
        }
    }
    var data = JSON.stringify({"option": "targets"});
    xhr.open("post","/deployment/");
    xhr.send(data);

    // test
    .ajax()
    modalPrintf(["new1", "new2"]);

    function modalPrintf(objArr) {
        var modalBody = document.getElementById("myModal").children[0].children[0].children[1];
        modalBody.innerHTML = "";
        for (var value of objArr) {
            // console.log(modalBody);
            if(mastersData.targets.indexOf(value) == -1) {
                modalBody.innerHTML += "<div id=\"master_select_" + value + "\"><div>&nbsp;" + value + "&nbsp;</div><div><a class=\"fa fa-square-o\" onclick=\"selectMaster(this)\"></a></div></div>";
            } else {
                modalBody.innerHTML += '<div id="master_select_' + value + '"><div>&nbsp;' + value + '&nbsp;</div><div><a class="fa fa-check-square-o" onclick="disSelectMaster(this)"></a></div></div>'
            }
        }
    }
}


function sendAjaxData() {
    var testData = {'minion-2': {'Redis': 'success', 'JDK': 'success', 'Zabbix': 'success'}, 
                    'minion-1': {'Redis': 'success', 'JDK': 'success', 'Zabbix': 'fail'}
                    }
    success(testData);

    var xhr = new XMLHttpRequest();
    var mastersDataJson = JSON.stringify(mastersData);
    xhr.onreadystatechange = function() {
	    if(xhr.readyState == 4 && xhr.status == 200) {
	        var  returnResult = JSON.parse(xhr.responseText);
	        success(returnResult);
	    }
    }
    xhr.open("post","");
    xhr.send(mastersDataJson);
    
    function success(data) {
        var resultDom = document.getElementsByClassName("return-result")[0];
        resultDom.innerHTML = "";
        for (var master in data) {
            resultDom.innerHTML += '<div class="result-masters"><div>&nbsp;' + master + '&nbsp;</div></div>';
            for (var software in data[master]) {
                if(data[master][software] == "success") {
                    resultDom.innerHTML += '<div class="result-softwares"><div>&nbsp;' + software + '&nbsp;</div><div><a class="fa fa-check-circle"></a></div></div>';
                } else {
                    resultDom.innerHTML += '<div class="result-softwares-error"><div>&nbsp;' + software + '&nbsp;</div><div><a class="fa fa-exclamation-circle"></a></div></div>';
                }
            }
        }
    }
}