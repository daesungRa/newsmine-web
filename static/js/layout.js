/*
 * layout.js (ver. 0.0.1)
 * => Made by Ra Daesung (daesungra@gmail.com)
 * => Created at '2021-02-11 KST'
 * => Updated at '2021-02-11 KST'
 * => This js component was created to activate default functions
 *    of drawing home page and user login, logout, signup, etc.
 */

function drawModalUsers (modalForm, headerContents, footerContents, toggle) {
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
	// activateModalUsersActions();
};

function activateModalUsersActions () {
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
					drawModalUsers(response, headerContents, footerContents, toggle);
				} else if (response.includes('/users/signup')) {
					let headerContents = 'Sign Up';
					let footerContents = {'confirm': 'Confirm', 'cancel': 'Cancel'};
					drawModalUsers(response, headerContents, footerContents, toggle);
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
				drawModalUsers(response, headerContents, footerContents, toggle);
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
				drawModalUsers(response, headerContents, footerContents, toggle);
			},
			error: function (jqXHR) {
				console.log(jqXHR);
			},
		});
	});
	/* Toggle dropdown menu active */
	$('.dropdown-menu .dropdown-item').on('mouseover', function () {
		$(this).parent().find('.dropdown-item').removeClass('active');
		$(this).addClass('active');
	});
	$('.dropdown-menu .dropdown-item').on('mouseout', function () {
		$(this).parent().find('.dropdown-item').removeClass('active');
	});
	/* Submit modal form action */
	$('#modal #modal-footer-btn-confirm').on('click', function (event) {
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
					drawModalUsers(response, headerContents, footerContents, toggle);
				} else if (typeof response == 'string' && response.includes('/users/signup')) {
					let headerContents = 'Sign Up';
					let footerContents = {'confirm': 'Confirm', 'cancel': 'Cancel'};
					drawModalUsers(response, headerContents, footerContents, toggle);
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
