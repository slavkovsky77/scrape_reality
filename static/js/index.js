
$(window).on("load", () => {
    setup_buttons();
});

function setup_buttons() {
    const buttons_click_functions = {
        '#create_button': () => create_dialog(),
        '#update_button': () => update_dialog(),
        '#delete_button': () => delete_flats(),
    };

    for (const button_name in buttons_click_functions) {
        $(button_name).on("click", event => {
            buttons_click_functions[button_name]();
        });
    }
}

function get_selected_apartment_numbers() {
    const apartment_numbers = JSON.parse($("#apartment_numbers").val());
    const clean_apartment_numbers = JSON.parse($("#clean_apartment_numbers").val());

    var selected_apartment_numbers = [];
    for (let i = 0; i < clean_apartment_numbers.length; i++) {
        const clean_apartment_number = clean_apartment_numbers[i];
        const apartment_number = apartment_numbers[i];
        const select_checkbox = $("#flat_"+clean_apartment_number+"_checkbox");
        if (select_checkbox.is(":checked")) {
            selected_apartment_numbers.push(apartment_number);
        }
    }
    return selected_apartment_numbers;
}

function create_dialog_payload() {
    return {
        apartment_number: $("#apartment_number").val(),
        title: $("#title").val(),
        rooms: $("#rooms").val(),
        size: $("#size").val(),
        total_area_size: $("#total_area_size").val(),
        sales_price: $("#sales_price").val(),
        floor_number: $("#floor_number").val(),
        project_name: $("#project_name").val(),
        href: $("#href").val(),
        img_src: $("#img_src").val(),
        status: $("#status").val(),
    };
}

function create_dialog() {
    const dialog = bootbox.confirm({
        title: "Create flat",
        size: "large",
        message: $("#create_dialog").html(),
        callback: result => {
            api_request(
                create_dialog_payload(),
                '/api/flats/create_flat',
                "POST",
                () => location.reload());
        }
    });
}

function update_dialog() {
    const selected_apartment_numbers = get_selected_apartment_numbers();
    if (selected_apartment_numbers.length != 1) {
        bootbox.alert('To update you have to select exactly one flat!');
        return;
    }

    const apartment_number = selected_apartment_numbers[0];

    const dialog = bootbox.confirm({
        title: "Update flat",
        size: "medium",
        message: $("#create_dialog").html(),
        callback: result => {
            api_request(
                create_dialog_payload(),
                '/api/flats/'+apartment_number,
                "PUT",
                () => location.reload());
        }
    });

    dialog.init(() => {
        api_request({},
            '/api/flats/'+apartment_number,
            'GET',
            (data) => {
                for (const [key, value] of Object.entries(data)) {
                    $("#"+key).val(value);
                }
            });
    });
}

function delete_flats() {
    const selected_apartment_numbers = get_selected_apartment_numbers();
    for (const apartment_number of selected_apartment_numbers) {
        api_request({},
            "/api/flats/"+apartment_number,
            "DELETE",
            () => location.reload());
    }
}