var selAll = document.querySelector("#selAll");
var infoLi = document.querySelectorAll(".panel tbody .li-checkbox");
var btnSubmit = document.querySelector("#btn-download-many");

//全选实现
selAll.addEventListener("click", function (e) {
    var c = e.target.checked;
    infoLi.forEach(function (item) {
        item.checked = c;
    })
});

//阻止空选提交
btnSubmit.addEventListener('click', function (e) {
    infoLi.forEach(function (item) {
        if (item.checked) {
            return true
        }
    });
    e.preventDefault();
    alert("你没有选择任何记录！");
    return false;
});
