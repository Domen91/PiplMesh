$(document).ready(function() {
    $.getJSON("https://api.github.com/repos/wlanslovenija/PiplMesh/contributors",null,function(data){
		var contributors = '';
		$.each(data,function(i,element){
			contributors +='<span><img src="' + element.avatar_url +'"/><a href="https://github.com/' + element.login + '">' + element.login + '</a></span>';
		});
	    $('.contributors').html(contributors);
	}); 
});