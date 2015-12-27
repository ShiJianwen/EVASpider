window.onload = function() {
	$('.login-btn').on('click', function() {
		var data = {
			username: $('#InputStuid').val(),
			password: $('#InputPassword').val()
		};
		console.log(data);
		$.ajax({
			url: '/api/spider.py',
			method: 'POST',
			complete: function(data, status) {
				console.log(data);
			}
		});
	});
};