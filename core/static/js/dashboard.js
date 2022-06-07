function alerta_sucesso(mensagem, reload = false, url = null){
    return Swal.fire({
        title: "Sucesso",
        text: mensagem,
        icon: "success",
    }).then((result) => {
        if (result.isConfirmed) {
            if (reload){
                location.reload();
            }
            if (url) {
                window.location.href = url;
            }
        }
    })
}

function alerta_confirmar(mensagem, reload = false, url = null){
    return Swal.fire({
        title: "Confirmar?",
        html: mensagem,
        icon: "info",
        showCancelButton: true,
        cancelButtonText: 'Cancelar',
        confirmButtonText: 'Confirmar',
        cancelButtonColor: '#d33',
        confirmButtonColor: '#3085d6',
    }, (result) => {
        if (result) {
            return true
        }
        return false
    })
}

function alerta_deletar(mensagem){
    return Swal.fire({
        title: "Confirmar exclusão?",
        text: mensagem,
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: 'Sim',
        cancelButtonText: 'Não',
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
    }, (result) => {
        if (result) {
            return true
        }
        return false
    })
}

function alerta_deletar_html(mensagem){
    console.log(mensagem)
    return Swal.fire({
        title: "Confirmar exclusão?",
        html: mensagem,
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: 'Sim',
        cancelButtonText: 'Não',
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
    }, (result) => {
        if (result) {
            return true
        }
        return false
    })
}

function alerta_erro(mensagem, reload = false, url = null){
    return Swal.fire({
        title: "Erro!",
        text: mensagem,
        icon: "error",
    }).then((result) => {
        if (result.isConfirmed) {
            if (reload){
                location.reload();
            }
            if (url) {
                window.location.href = url;
            }
        }
    })
}

function alerta_erro_html(mensagem, html, reload = false, url = null){
    return Swal.fire({
        title: mensagem,
        html: html,
        icon: "error",
    }).then((result) => {
        if (result.isConfirmed) {
            if (reload){
                location.reload();
            }
            if (url) {
                window.location.href = url;
            }
        }
    })
}