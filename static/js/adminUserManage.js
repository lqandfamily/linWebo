var btnNewUser = document.querySelector(".panel .btn-new-user");
var editNewUser = document.querySelector(".panel .edit-new-user");
var btnEditOk = document.querySelector(".edit-btn-group .btn-edit-ok");
var btnEditCancel = document.querySelector(".edit-btn-group .btn-edit-cancel");

//输入框
var userName = document.querySelector("#edit-name");
var userPwd = document.querySelector("#edit-pwd");

btnNewUser.addEventListener('click', function (e) {
    editNewUser.style.visibility = "visible";
});

btnEditCancel.addEventListener('click', function (e) {
    editNewUser.style.visibility = 'hidden';
});

btnEditOk.addEventListener('click', function (e) {
    if (userName.value === '' || userPwd.value === '') {
        alert("用户名或密码不能为空！");
        e.preventDefault();
        return false;
    }
    if (userName.value.length < 4 || userName.value.length < 4) {
        alert("用户名或密码长度至少为4！");
        e.preventDefault();
        return false;
    }
});
