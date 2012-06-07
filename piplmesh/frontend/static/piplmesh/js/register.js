$(document).ready(function () {
    $('#id_password2').keyup(checkPassword);
    $('#id_email').keyup(checkEmail);
});

function checkPassword() {
    var pass1 = '#id_password1';
    var pass2 = '#id_password2';

    if($(pass1).val() == $(pass2).val()) {
        $(pass1).css('background-color','#66cc66');
        $(pass2).css('background-color','#66cc66');
    }
    else
    {
        $(pass1).css('background-color','#ff6666');
        $(pass2).css('background-color','#ff6666');
    }
}

function checkEmail() {
    var email = "#id_email";
    var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;

    var emailValue = $(email).val();
    if (!emailReg.test(emailValue)) {
        $(email).css('background-color','#ff6666');
    }
    else
    {
        $(email).css('background-color','#66cc66');
    }
}