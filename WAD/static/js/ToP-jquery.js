// Once the page html fully loads, the jquery is executed in the {} function
$(document).ready(function() {
	$('a.trigger').hover(function() {
		$(this).next('.pop-up').show();
	},
	function() {
		$(this).next('.pop-up').hide();
	});
});