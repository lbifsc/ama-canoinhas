var csrftoken = Cookies.get('csrftoken');

$(document).ready(function () {
    console.clear();
});

function confirma_exclusao(pk) {

}

function excluir_parceiro(pk) {
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