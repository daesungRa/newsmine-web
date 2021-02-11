/*
 * component.js (ver. 0.0.1)
 * => Made by Ra Daesung (daesungra@gmail.com)
 * => Created at '2021-02-11 KST'
 * => Updated at '2021-02-11 KST'
 * => This js component was created to activate functions
 *    of ..., etc.
 */

function drawModalComponent (modalForm, headerContents, footerContents, toggle) {
	const modal = $('.modal-component');
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

function activateModalComponentActions () {
};

function activateComponentActions () {
	/* Draw component form */
	$('.draw-modal-component').on('click', function () {
		let headerContents = 'Test';
		let footerContents = {'confirm': 'Confirm', 'cancel': 'Cancel'};
		let toggle = true;
		drawModalUsers('component response', headerContents, footerContents, toggle);
	});
	/* Submit modal form action */
	$('.modal-component #modal-footer-btn-confirm').on('click', function (event) {
		event.preventDefault();
		event.stopPropagation();
	});
};
