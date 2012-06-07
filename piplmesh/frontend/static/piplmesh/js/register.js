$(document).ready(function () {
    $('#id_password2').keyup(checkPassword);
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