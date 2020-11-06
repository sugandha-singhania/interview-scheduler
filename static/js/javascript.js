$(function(){
$('button').click(function(){
	$.ajax({
		url: '/new_interview',
		data: $('form').serialize(),
		type: 'POST',
		success: function(response){
			console.log(response);
		},
		error: function(error){
			console.log(error);
		}
	});
});
});
