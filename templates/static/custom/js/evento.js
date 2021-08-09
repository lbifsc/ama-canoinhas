var csrftoken = Cookies.get('csrftoken');

function excluir_evento(pk) {
    if (confirm('Deseja realmente apagar este evento?')) {
        $.ajax({
            type: 'post',
            url: '/excluir_evento/' + pk,
            data: { csrfmiddlewaretoken: csrftoken, },
            dataType: 'json',
            success: function (response) {
                $('#evento_' + pk).remove();
            },
        });
    }
}