var csrftoken = Cookies.get('csrftoken');

$('[data-toggle="tooltip"]').tooltip({
    delay: {
        show: 100,
        hide: 100
    },
    trigger: 'hover',
});

function excluir_noticia(pk) {
    if (confirm('Deseja realmente apagar esta notícia?')) {
        $.ajax({
            type: 'post',
            url: '/excluir_noticia/' + pk,
            data: { csrfmiddlewaretoken: csrftoken, },
            dataType: 'json',
            success: function (response) {
                $('#noticia_' + pk).remove();
            },
        });
    }
}