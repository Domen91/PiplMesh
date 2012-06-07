function User(data) {
    var self = this;
    $.extend(self, data);
    self._key = self.username.toLowerCase();
}

function redrawUserList() {
    // TODO: Currently we just replace the whole list of users, it would be better to fade gone out, and fade new in

    var keys = [];
    $.each(onlineUsers, function (key, user) {
        keys.push(key);
    });
    keys.sort(function (key1, key2) {
        if (key1 < key2) return -1;
        if (key1 > key2) return 1;
        return 0;
    });
    $('#userlist').empty();

    var searchUsers = $('#search_users').val().toLowerCase();
    $.each(keys, function (i, key) {
        if (searchUsers === '' || key.indexOf(searchUsers) !== -1) {
            var user = onlineUsers[key];
            var li = $('<li/>');
            var image = $('<img/>').prop({
                'src': user.image_url,
                'alt': gettext("User image")
            });
            li.append(image);
            li.append(user.username);
            var div = $('<div/>').prop({
                'class': 'info'
            });
            div.append($('<a/>').prop('href', user.profile_url).text(gettext("User profile")));
            li.append(div);
            $('#userlist').append(li);
        }
    });
}

function updateUserList(data) {
    var user = new User(data.user);
    if (data.action === 'JOIN') {
        onlineUsers[user._key] = user;
        redrawUserList();
    }
    else if (data.action === 'PART') {
        if (onlineUsers[user._key]) {
            delete onlineUsers[user._key];
            redrawUserList();
        }
    }
}

$(document).ready(function () {
    $.updates.registerProcessor('home_channel', 'userlist', updateUserList);

    $('.panel .header').click(function (event) {
        $(this).next('ul').slideToggle('fast');
    });

    $('#search_users').change(redrawUserList).keyup(redrawUserList);

    redrawUserList();    
});

$(window).bind("load", function() {
    $('#id_password2').keyup(function() { checkPassword(); });
});

function checkPassword() {
    var pass1 = document.getElementById('id_password1');
    var pass2 = document.getElementById('id_password2');

    var goodColor = "#66cc66";
    var badColor = "#ff6666";

    if(pass1.value == pass2.value){
        pass2.style.backgroundColor = goodColor;
    } else {
        pass2.style.backgroundColor = badColor;
    }
}