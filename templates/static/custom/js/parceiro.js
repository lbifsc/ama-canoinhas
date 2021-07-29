var csrftoken = Cookies.get('csrftoken');

function excluir_parceiro(pk) {
    if (confirm('Realmente deseja excluir este parceiro?')) {
        $.ajax({
            type: 'post',
            url: '/excluir_parceiro/' + pk,
            data: { csrfmiddlewaretoken: csrftoken, },
            dataType: 'json',
            success: function (response) {
                $('#parceiro_' + pk).remove();
            },
        });
    }
}