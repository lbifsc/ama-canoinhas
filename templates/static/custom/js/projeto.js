var csrftoken = Cookies.get('csrftoken');

function excluir_projeto(pk) {
    if (confirm('Deseja realmente excluir este projeto?')) {
        $.ajax({
            type: 'post',
            url: '/excluir_projeto/' + pk,
            data: { csrfmiddlewaretoken: csrftoken, },
            dataType: 'json',
            success: function (response) {
                $('#projeto_' + pk).remove();
            },
        });
    }
}