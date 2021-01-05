function drawModal (modalForm, headerContents, footerContents) {
	const modal = $('#modal');
	// Draw form to modal
	modal.find('.modal-body').html(modalForm);
	// Toggle modal
	modal.modal('toggle');
};

function activateDefaultFunctions () {
	/* Draw login form */
	$('#nav-item-login').on('click', function () {
		$.ajax({
			type: 'get',
			url: '/users/login',
			success: function (response) {
				drawModal(response/*, headerContents, footerContents */);
			},
			error: function (jqXHR) {
				console.log(jqXHR);
			},
		})
	});
}

$(document).ready(function () {
	activateDefaultFunctions();
});
