function drawModal (modalForm, headerContents, footerContents, toggle) {
	const modal = $('#modal');
	// Draw contents to modal
	modal.find('.modal-title').html(headerContents);
	modal.find('.modal-body').html(modalForm);
	modal.find('#modal-footer-btn-confirm').html(footerContents.confirm);
	modal.find('#modal-footer-btn-cancel').html(footerContents.cancel);
	// Toggle modal
	if (typeof toggle === 'boolean' && toggle) {
		modal.modal('toggle');
	};
	// activateModalActions();
};

function activateModalActions () {
	/* Try social login(github, kakao) */
	$('.a-social-login').on('click', function (event) {
		event.preventDefault();
		event.stopPropagation();
		let href = $(this).prop('href');
		let socialName = href.split('/login/')[1];
		$.ajax({
			type: 'get',
			url: href,
			success: function (response) {
				let toggle = false;
				if (response.includes('/users/login')) {
					let headerContents = `Login (${socialName}실패)`;
					let footerContents = {'confirm': 'Login', 'cancel': 'Cancel'};
					drawModal(response, headerContents, footerContents, toggle);
				} else if (response.includes('/users/signup')) {
					let headerContents = 'Sign Up';
					let footerContents = {'confirm': 'Confirm', 'cancel': 'Cancel'};
					drawModal(response, headerContents, footerContents, toggle);
				} else {
					$('#modal').modal('toggle');
					window.location.href = '';
				};
			},
			error: function (jqXHR) {
				console.log(jqXHR);
			},
		})
	});
};

function activateDefaultActions () {
	/* Draw login form */
	$('#nav-item-login').on('click', function () {
		$.ajax({
			type: 'get',
			url: '/users/login',
			success: function (response) {
				let headerContents = 'Log In';
				let footerContents = {'confirm': 'Login', 'cancel': 'Cancel'};
				let toggle = true;
				drawModal(response, headerContents, footerContents, toggle);
			},
			error: function (jqXHR) {
				console.log(jqXHR);
			},
		});
	});
	/* Draw signup form */
	$('#nav-item-signup').on('click', function () {
		$.ajax({
			type: 'get',
			url: '/users/signup',
			success: function (response) {
				let headerContents = 'Sign Up';
				let footerContents = {'confirm': 'Confirm', 'cancel': 'Cancel'};
				let toggle = true;
				drawModal(response, headerContents, footerContents, toggle);
			},
			error: function (jqXHR) {
				console.log(jqXHR);
			},
		});
	});
	/* Submit modal form action */
	$('#modal-footer-btn-confirm').on('click', function (event) {
		event.preventDefault();
		event.stopPropagation();

		let contentForm = $('#modal').find('form');
		$.ajax({
			type: contentForm.prop('method'),
			cache: false,
			url: contentForm.prop('action'),
			data: contentForm.serialize(),
			success: function (response) {
				let toggle = false;
				if (typeof response == 'string' && response.includes('/users/login"')) {
					let headerContents = 'Log In';
					let footerContents = {'confirm': 'Login', 'cancel': 'Cancel'};
					drawModal(response, headerContents, footerContents, toggle);
				} else if (typeof response == 'string' && response.includes('/users/signup')) {
					let headerContents = 'Sign Up';
					let footerContents = {'confirm': 'Confirm', 'cancel': 'Cancel'};
					drawModal(response, headerContents, footerContents, toggle);
				} else {
					window.location.href = response.hasOwnProperty('redirect_uri') ? `${response.redirect_uri}` : '';
				};
			},
			error: function (jqXHR) {
				console.log(jqXHR);
			},
		});
	});
};

$(document).ready(function () {
	activateDefaultActions();
});
