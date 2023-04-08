'use strict';
(function(w,d,$){
    $('#models, #fields, #dtable,label[for="models"],label[for="fields"]').hide()
    $.when(
      $.ajax({
            url: "/apps/",
            method: 'GET',
            datatype: 'json',

    })).then(function( data, textStatus, jqXHR ) {
        $('#apps').append('<option value="' + '' + '" selected>' + 'Select an app' + '</option>');
        $.each(data.apps, function(index, value) {
            $('#apps').append('<option value="' + value.value + '">' + value.display_name + '</option>');
        });
    }).fail(function(err){
      alert(err["responseJSON"]);
    });

    $('#apps').on('change', function(e){
        e.preventDefault();
        $('#models').html('').fadeOut('slow');
        $('label[for="models"]').fadeOut('slow')
        $('#fields').html('').fadeOut('slow');
        $('label[for="fields"]').fadeOut('slow')
        $('#dtable').fadeOut('slow');
        let value = $(this).val();
        let app = $('#apps').val();
        console.info(value)

        $.when(
            $.ajax({
                  url: "/models/",
                  method: 'GET',
                  datatype: 'json',
                  data: {"app":app}
            })).then(function( data, textStatus, jqXHR ) {
                $('#models').append('<option value="' + '' + '" selected>' + 'Select a model' + '</option>');
              $.each(data.models, function(index, value) {
                  $('#models').append('<option value="' + value + '">' + value + '</option>');
              });
              $('#models').fadeIn('slow')
              $('label[for="models"]').fadeIn('slow')
          }).fail(function(response) {
            
            alert(response ["responseJSON"]);
        })
    })

    $('#models').on('change', function(e){
        e.preventDefault();
        $('#fields').html('').fadeOut('slow');
        $('label[for="fields"]').fadeOut('slow')
        $('#dtable').fadeOut('slow');
        let value = $(this).val();
        let app = $("#apps").val();
        $.when(
            $.ajax({
                  url: "/fields/",
                  method: 'GET',
                  datatype: 'json',
                  data: {"model":value, "app":app}
            })).then(function( data, textStatus, jqXHR ) {
              $.each(data.fields, function(index, value) {
                  $('#fields').append('<option value="' + value.field + '">' + value.field + '</option>');
              });
              $('#fields').attr("size", data.fields.length);
              $('#fields').fadeIn('slow')
              $('label[for="fields"]').fadeIn('slow')
              $('#dtable').fadeIn('slow');
          }).fail(function(response) {
            
            alert(response ["responseJSON"]);
            
          })
    })

    $('#dtable').on('click', function(e){
        let app = $('#apps').val();
        let fields_data = [];
        let columns_data = [];
        let model = $('#models').val();
        let fields = $('#fields').val();
        for(let i=0;i<fields.length;i++){
            fields_data.push({"data":fields[i]})
            columns_data.push({"searchable":true})
        }
        var template = Handlebars.compile($('#dtables-template').html());
        let res = template({ fields:fields_data });
        $('#result').html(res);

        if ($("#table").length > 0) {
            $('#table').DataTable({
                destroy: true,
                processing: true,
                ajax: {
                    url : '/dtables/',
                    data: {"format":"datatables","model":model,"app":app,"fields":fields_data},
                    type: 'GET'
                },
                columnDefs: [{
                    "defaultContent": "-",
                    "targets": "_all",
                }],
                columns: columns_data
            });
        }
    })
})(window,document,jQuery)