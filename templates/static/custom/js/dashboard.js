var csrftoken = Cookies.get('csrftoken');

$('[data-toggle="tooltip"]').tooltip({
    delay: {
        show: 100,
        hide: 100
    }
});

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

function excluir_mensagem(pk) {
    if (confirm('Deseja realmente apagar esta mensagem?')) {
        $.ajax({
            type: 'post',
            url: '/excluir_mensagem/' + pk,
            data: { csrfmiddlewaretoken: csrftoken, },
            dataType: 'json',
            success: function (response) {
                $('#mensagem_' + pk).remove();
            },
        });
    }
}

function marcar_lida(pk, element) {
    var lida = element.getAttribute('funvalue')

    $.ajax({
        type: 'post',
        url: '/marcar_lida/' + pk,
        data: {
            csrfmiddlewaretoken: csrftoken,
            lida: lida,
        },
        dataType: 'json',
        success: function (response) {
            icon = element.children;

            if ((response['lida']) == true) {
                element.setAttribute('funvalue', 'false')
                element.setAttribute('data-original-title', 'Marcar como não lida');
                icon[0]['className'] = 'icofont-envelope icofont-2x';
            } else {
                element.setAttribute('funvalue', 'true');
                element.setAttribute('data-original-title', 'Marcar como lida');
                icon[0]['className'] = 'icofont-envelope-open icofont-2x';
            }
            console.log(icon[0]['className'])
        }
    });
}