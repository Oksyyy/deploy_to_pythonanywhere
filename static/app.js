const BASE_URL = "";

// Load everything
$(document).ready(function () {
    loadServices();
    loadProviders();

    $("#addService").click(createService);
    $("#saveProvider").click(saveProvider);
    $("#serviceFilter").change(filterProviders);
    $("#sortRate").change(filterProviders);

    $(document).on("click", ".service-item", function () {
        const serviceId = $(this).data("id");

        $(".service-item").removeClass("active");
        $(this).addClass("active");

        if (!serviceId) {
            $("#serviceFilter").val("");
            loadProviders(); // show all
        } else {
            $("#serviceFilter").val(serviceId);
            filterProviders();
        }
    });
});

// ---------- SERVICES ----------

function loadServices() {
    $.ajax({
        url: BASE_URL + "/services",
        method: "GET",
        success: function (services) {
            $("#serviceList").empty();
            $("#serviceSelect").empty();
            $("#serviceFilter").empty().append('<option value="">All Services</option>');

            // 👉 Add "All Services" button FIRST
            $("#serviceList").append(`
                <li class="service-item active" data-id="">
                    All Services
                </li>
            `);

            services.forEach(s => {
                $("#serviceList").append(`
                    <li class="service-item" data-id="${s.id}">
                        ${s.name}
                    </li>
                `);

                $("#serviceSelect").append(`<option value="${s.id}">${s.name}</option>`);
                $("#serviceFilter").append(`<option value="${s.id}">${s.name}</option>`);
            });
        }
    });
}

function createService() {
    const name = $("#serviceName").val();

    $.ajax({
        url: BASE_URL + "/services",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({ name }),
        success: function () {
            loadServices();
            $("#serviceName").val("");
        }
    });
}

// ---------- PROVIDERS ----------

function loadProviders() {
    $.ajax({
        url: BASE_URL + "/providers",
        method: "GET",
        success: renderProviders
    });
}

function filterProviders() {
    const serviceId = $("#serviceFilter").val();

    if (!serviceId) {
        loadProviders();
        return;
    }

    $.ajax({
        url: BASE_URL + "/providers/service/" + serviceId,
        method: "GET",
        success: renderProviders
    });
}

function renderProviders(providers) {
    const sortType = $("#sortRate").val();

    if (sortType === "asc") {
        providers.sort((a, b) => a.price_per_hour - b.price_per_hour);
    } else if (sortType === "desc") {
        providers.sort((a, b) => b.price_per_hour - a.price_per_hour);
    }

    const tbody = $("#providerTable tbody");
    tbody.empty();

    providers.forEach(p => {
        tbody.append(`
            <tr>
                <td>${p.name}</td>
                <td>${p.email}</td>
                <td>${p.phone}</td>
                <td>${p.price_per_hour}</td>
                <td>${p.service_name}</td>
                <td>
                    <span class="action edit" onclick="editProvider(${p.id})">Edit</span>
                    |
                    <span class="action delete" onclick="deleteProvider(${p.id})">Delete</span>
                </td>
            </tr>
        `);
    });
}

function saveProvider() {
    const id = $("#providerId").val();

    const provider = {
        name: $("#name").val(),
        email: $("#email").val(),
        phone: $("#phone").val(),
        price_per_hour: parseFloat($("#rate").val()),
        service_id: parseInt($("#serviceSelect").val())
    };

    if (id) {
        // UPDATE
        $.ajax({
            url: BASE_URL + "/providers/" + id,
            method: "PUT",
            contentType: "application/json",
            data: JSON.stringify(provider),
            success: function () {
                loadProviders();
                clearForm();
            }
        });
    } else {
        // CREATE
        $.ajax({
            url: BASE_URL + "/providers",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify(provider),
            success: function () {
                loadProviders();
                clearForm();
            }
        });
    }
}

function editProvider(id) {
    $.ajax({
        url: BASE_URL + "/providers/" + id,
        method: "GET",
        success: function (p) {
            $("#providerId").val(p.id);
            $("#name").val(p.name);
            $("#email").val(p.email);
            $("#phone").val(p.phone);
            $("#rate").val(p.price_per_hour);
            $("#serviceSelect").val(p.service_id);
        }
    });
}

function deleteProvider(id) {
    $.ajax({
        url: BASE_URL + "/providers/" + id,
        method: "DELETE",
        success: function () {
            loadProviders();
        }
    });
}

function clearForm() {
    $("#providerId").val("");
    $("#name").val("");
    $("#email").val("");
    $("#phone").val("");
    $("#rate").val("");
}