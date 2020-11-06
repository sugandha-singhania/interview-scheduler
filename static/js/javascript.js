$(function(){
	$('button').click(function(){

    var start_time = $('#start_time').val();
		var ed_time = $('#end_time').val();
		$.ajax({
			url: 'http://localhost:5000/new_interview',
			// data: $('form').serialize(),
			data:  {"some_key": "some_valu"},
			type: 'POST',
      // json: {"some_key": "some_valu"},
			crossDomain : true,
			success: function(response){
				console.log({response});
			},
			error: function(error){
				console.log({error});
			}
		});
	});
});
