document.addEventListener('DOMContentLoaded', () => {
	const logo = document.getElementById('logo');
	const classic_button = document.getElementById('classic_button');

	logo.addEventListener('click', () => {
		window.location.href = 'index.html';
	});
	classic_button.addEventListener('click', () => {
		window.location.href = 'classic.html';
	});
});
