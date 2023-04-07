'use strict';
(function(w,d,$){
    $('#apps, #models, #fields, #dtable,label[for="models"],label[for="fields"]').hide()
    $.when(
      $.ajax({
            url: "/apps/",
            method: 'GET',
            datatype: 'json',

    })).then(function( data, textStatus, jqXHR ) {
        $.each(data.apps, function(index, value) {
            $('#apps').append('<option value="' + value + '">' + value + '</option>');
        });
        $('#apps').fadeIn('slow')
    }).fail(function(err){
      alert(err["responseJSON"] ["details"]);
    });


    $('#apps').on('change', function(e){
        e.preventDefault();
        $('#models,#fields').html('').fadeOut('slow');
        $('label[for="models"],label[for="fields"]').fadeOut('slow')
        let value = $(this).val();
        console.info(value)
        $.when(
            $.ajax({
                  url: "/models/",
                  method: 'GET',
                  datatype: 'json',
                  data: {"app":value}
            })).then(function( data, textStatus, jqXHR ) {
              $.each(data.models, function(index, value) {
                  $('#models').append('<option value="' + value + '">' + value + '</option>');
              });
              $('#models,label[for="models"]').fadeIn('slow')
          }).fail(function(err){
            alert(err["responseJSON"] ["details"]);
          });
    })


    $('#models').on('change', function(e){
        e.preventDefault();
        $('#fields').html('').fadeOut('slow');
        $('label[for="fields"]').fadeOut('slow')
        $('#dtable').fadeOut('slow');
        let value = $(this).val();
        let app = $("#apps").val();
        console.info(value)
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
              $('#fields').fadeIn('slow')
              $('label[for="fields"]').fadeIn('slow')
              $('#dtable').fadeIn('slow');
          }).fail(function(response) {
            
            alert(response ["responseJSON"] ["details"]);
            
          })
    })

    $('#dtable').on('click', function(e){
        let app = $('#apps').val();
        let fields_data = [];
        let columns_data = []
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