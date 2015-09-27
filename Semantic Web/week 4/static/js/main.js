$('#search').on('click', function(e){

	var query = $('#query').val();
	var endpoint = 'http://localhost:5820/weekfour/query';
	var format = 'JSON';
	var reasoning = document.getElementById('checkbox').checked

	$.get('/sparql',data={'endpoint': endpoint, 'query': query, 'format': format, 'reasoning': reasoning}, function(json){
		console.log(json);

		try {
			var vars = json.head.vars;

			var ul = $('<ul></ul>');
			ul.addClass('list-group');

			$.each(json.results.bindings, function(index,value){
				var li = $('<li></li>');
				li.addClass('list-group-item');

				$.each(vars, function(index, v){
					var v_type = value[v]['type'];
					var v_value = value[v]['value'];

					li.append('<strong>'+v+'</strong><br/>');

					// If the value is a URI, create a hyperlink
					if (v_type == 'uri') {
						var a = $('<a></a>');
						a.attr('href',v_value);
						a.text(v_value);
						li.append(a);
					// Else we're just showing the value.
					} else {
						li.append(v_value);
					}
					li.append('<br/>');

				});
				ul.append(li);

			});

			$('#resultbox').html(ul);
		} catch(err) {
			if (json.result == 'Error') {
				$('#resultbox').html('Something went wrong!');
			} else if (json.result == 'None') {
				$('#resultbox').html('No results found')
			} else {
				$('#resultbox').html('Something went very wrong!');
			}
		}
	});
});
