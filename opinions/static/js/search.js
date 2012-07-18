(function() {
  var results = [],
      selected = null,
      history = {},
      lastPartial = '',
      searchTimeout = null,
      searchDelay = 300,
      input = $('#search_term'),
      list = $('#search_results');

  // Hide the results list if anything but the input is clicked
  function hide(e) {
    if (e.target !== input[0]) {
      displayList([], '');
    }

    return true;
  }

  function autocomplete(e)
  {
    // esc
    if (e.which == 27) {
      input.val(lastPartial);
      displayList([], '');

      return true;
    }

    // up or down
    if ((e.which == 38 || e.which == 40) && selected) {
      return true;
    }

    var partial = lastPartial = input.val();

    clearTimeout(searchTimeout);

    if (history.hasOwnProperty(partial)) {
      // Display cached results
      displayList(history[partial], partial);
    } else if (partial.length) {
      searchTimeout = setTimeout(function() {
        $.getJSON('/autocomplete/'+partial, null, function(data) {
          history[partial] = data;
          displayList(data, partial);
        });
      }, searchDelay);
    } else {
      displayList([], partial);
    }

    return true;
  }

  function displayList(data, partial) {
    // Clear previous results
    list.html('');
    results = [];
    selected = null;

    if (list && partial.length && data.length) {
      $(data).each(function(i, item) {
        // TODO: Use anchor elements instead of binding to an LI's onclick
        var elem = $('<li><a href="'+item[1]+'">'+highlight(item[0], partial)+'</a></li>'),
            obj = {elem: elem, name: item[0], url: item[1]};

        $(elem).hover(function() {
          $(this).siblings().removeClass('selected');
          $(this).addClass('selected');
          selected = obj;
        });

        list.append(elem);
        results.push(obj);
      })
    }
  }

  function highlight(name, partial) {
    return name.replace(new RegExp('('+partial+')', 'ig'), '<strong>$1</strong>');
  }

  function select(e) {
    if (e.which == 13 && selected) {
      window.location = selected.url;
      return false;
    }

    if (!results.length || (e.which != 38 && e.which != 40)) return;

    var down = (e.which == 40) ? true : false,
        field = this,
        current = selected || results[0];

    if (current) {
      if (selected || !down) {
        var i = (down) ? results.indexOf(current) + 1 : results.indexOf(current) - 1;

        if (i >= results.length) {
          i = 0;
        } else if (i < 0) {
          i = results.length - 1;
        }

        next = results[i];
      } else {
        next = current;
      }

      selected = next;

      $(next.elem).siblings().removeClass('selected');
      $(next.elem).addClass('selected');

      $(field).val(next.name);
    }

    return false;
  }

  input.keyup(autocomplete).keydown(select);
  $(window).click(hide);
})();
