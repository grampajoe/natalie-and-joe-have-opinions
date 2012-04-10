var results = [];
var selected = null;

var history = {};
var lastPartial = '';
var searchTimeout = null;
var searchDelay = 300;
var input = null;

function hide(e)
{
	if (e.target != input)
		display_list(input, [], '');
	return true;
}

function autocomplete(e)
{
	// esc
	if (e.which == 27)
	{
		this.value = lastPartial;
		display_list(this, [], '');
		return true;
	}

	// up or down
	if ((e.which == 38 || e.which == 40) && selected) return true;

	var field = this;
	var partial = lastPartial = field.value;

	clearTimeout(searchTimeout);

	if (partial in history)
	{
		display_list(field, history[partial], partial);
	}
	else if (partial.length)
	{
		searchTimeout = setTimeout(function() {
			$.getJSON('/autocomplete/'+partial, null, function(data) {
				history[partial] = data;
				display_list(field, data, partial);
			});
		}, searchDelay);
	}
	else
	{
		display_list(field, [], partial);
	}

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
	input = $('#search input[name=term]')[0];
	$(input).keyup(autocomplete).keydown(select).parent().append('<ul class="results hidden"></ul>');
	$(window).click(hide);
});
