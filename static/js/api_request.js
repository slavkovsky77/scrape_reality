
const _saving_overlay_spinners = [];

function deactivate_saving_overlay() {
    while (_saving_overlay_spinners.length > 0) {
        _saving_overlay_spinners.pop().modal('hide');
    }
}

function activate_saving_overlay() {
    return new Promise(
        (resolve => {
            if (_saving_overlay_spinners.length === 0) {
                const saving_overlay_spinner = _create_overlay();
                _saving_overlay_spinners.push(saving_overlay_spinner);

                saving_overlay_spinner.on('shown.bs.modal', () => {
                    //Make sure _saving_overlay_spinners is not empty after a modal is shown
                    _saving_overlay_spinners.push(saving_overlay_spinner);
                    resolve();
                })
                saving_overlay_spinner.modal('show');
            } else {
                resolve();
            }
        })
    )
}

function _create_overlay() {
    const overlay = bootbox.dialog({
        message: /*html*/`
            <div class="d-flex">
                <div class="spinner-grow text-success d-flex" role="status"></div>
                <div class="text-success d-flex"> Processing the request...</div>
            </div>
            `,
        closeButton: false,
        show: false
    });
    overlay.on("keydown", event => {
        event.stopPropagation();
    })
    overlay.on("mousedown", event => {
        event.stopPropagation();
    })
    overlay.on("mouseup", event => {
        event.stopPropagation();
    })
    overlay.on("contextmenu", event => {
        event.preventDefault();
        event.stopPropagation();
    })

    return overlay;
}


function json_payload(request_data, type="POST") {
    return {
        data: JSON.stringify(request_data),
        processData: false,
        contentType: 'application/json',
        type: type
    };
}

function fail_dialog(text) {
    alert_dialog("Request failed", text);
}

function warning_dialog(text) {
    alert_dialog("Request produced warnings", text);
}

function alert_dialog(title, text) {
    bootbox.alert({
        title: title,
        message: text,
        onEscape: true,
        backdrop: true,
        size: 'xl'
    });
}

function api_request(payload, path, type, done_callback=null, overlay=true) {
    const request = new Promise((resolve, reject) => {
        $.ajax(path, json_payload(payload, type))
            .done(response => {
                if (done_callback !== null) {
                    done_callback(response);
                }

                if ('warning' in response) {
                    warning_dialog(response['warning']);
                }

                resolve();
            })
            .fail((jqXHR) => {
                fail_dialog(jqXHR.responseText);
                reject();
            });
    })

    if (overlay) {
        return Promise.allSettled([request, activate_saving_overlay()]).finally(deactivate_saving_overlay);
    } else {
        return Promise.allSettled([request]);
    }
}