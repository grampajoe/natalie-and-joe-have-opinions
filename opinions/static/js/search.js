var results = [];
var selected = null;

function autocomplete(e)
{
	if (e.which == 38 || e.which == 40) return true;

	var field = this;
	var partial = field.value;

	$.getJSON('/autocomplete/'+partial, null, function(data) {
		display_list(field, data, partial);
	});

	return true;
}

function display_list(field, data, partial)
{
	var list = $('#search .results').html('').removeClass('hidden');
	results = [];
	selected = null;

	if (list && partial.length && data.length)
	{
		$(data).each(function(i, item) {
			var elem = $('<li>'+highlight(item[0], partial)+'</li>').click(function() {
				window.location = item[1];
			});

			var obj = {elem: elem, name: item[0], url: item[1]};

			$(elem).hover(function() {
				$(this).siblings().removeClass('selected');
				$(this).addClass('selected');
				selected = obj;
			});

			$(list).append(elem);
			results.push(obj);
		})
	}
	else
	{
		$('#search .results').addClass('hidden');
	}
}

function highlight(name, partial)
{
	return name.replace(new RegExp('('+partial+')', 'i'), '<strong>$1</strong>');
}

function select(e)
{
	if (e.which == 13 && selected)
	{
		window.location = selected.url;
		return false;
	}

	if (!results.length || (e.which != 38 && e.which != 40)) return;

	var down = (e.which == 40) ? true : false;

	var field = this;
	var current = selected || results[0];

	if (current)
	{
		if (selected || !down)
		{
			var i = (down) ? results.indexOf(current) + 1 : results.indexOf(current) - 1;
			if (i >= results.length) i = 0;
			else if (i < 0) i = results.length - 1;

			next = results[i];
		}
		else
		{
			next = current;
		}

		selected = next;

		$(next.elem).siblings().removeClass('selected');
		$(next.elem).addClass('selected');

		$(field).val(next.name);
	}

	return false;
}

$(document).ready(function() {
	$('#search input[name=term]').keyup(autocomplete).keydown(select).after('<ul class="results hidden"></ul>');
});
