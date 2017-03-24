// Once the page html fully loads, the jquery is executed in the {} function
// Hovering over a playlist name where an <a> tag's class is "trigger" 
// brings a popup showing that playlist's author
$(document).ready(function() {
	$('a.trigger').hover(function() {
		$(this).next('.pop-up').show();
	},
	function() {
		$(this).next('.pop-up').hide();
	});
});