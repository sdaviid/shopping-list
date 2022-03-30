var total_value = 0.0;
var total_products = 0;
var list_product_row_edit = false;
var teste_ajax = false;



function reset_values_modal(){
    $('#tx_produto_add').val('');
    $('#tx_produto_edit').val('');
    $('#quantidade_add').val('0');
    $('#quantidade_edit').val('0');
    $('#valor_add').val('0');
    $('#valor_edit').val('0');
}


function update_totals(product_quantity, product_value){
    total_products += product_quantity;
    total_value += product_value;
    var total_value_str = total_value.toFixed(2);
    $('#total_itens').html(`<strong>Total Itens</strong>: ${total_products}`);
    $('#total_value').html(`<strong>Total Valor</strong>: ${total_value}`);
}


function add_product_to_list(product_name, product_quantity, product_value, id=0){
    var product_total = product_value * product_quantity;
    var product_total_str = product_total.toFixed(2);
    $('#tb_produtos tbody').append(`<tr>
        <td data-id=${id}>
            <input class="form-check-input padding-right-10" type="checkbox" value="" id="check_product">${product_name} <i id="btn_edit_product" class="padding-left-10 fa-solid fa-pen-to-square"></i><i id="btn_remove_product" class="padding-left-10 fa-solid fa-trash-can"></i>
        </td>
        <td>
            ${product_quantity}
        </td>
        <td>
            ${product_value}
        </td>
        <td>
            ${product_total}
        </td>
    </tr>`);
    $('#modal_products_add').modal('hide');
    reset_values_modal();
    update_totals(1, product_total);
}


$(document).on('click', '#btn_add', function(e){
    $('#modal_products_add').modal('show');
});


$(document).on('click', '#check_product', function(){
    if(this.checked)
        $(this).closest('tr').css('background', 'grey');
    else
        $(this).closest('tr').css('background', 'white');
});




$(document).on('click', '#btn_edit_product', function(){
    list_product_row_edit = $(this).closest('tr');
    $('#tx_produto_edit').val(list_product_row_edit.find("td").eq(0).text().trim());
    $('#quantidade_edit').val(list_product_row_edit.find("td").eq(1).text().trim());
    $('#valor_edit').val(list_product_row_edit.find("td").eq(2).text().trim());
    $('#modal_products_edit').modal('show');
});


$(document).on('click', '#btn_add_unit', function(e){
    var product_name = $('#tx_produto_add').val();
    var product_quantity = $('#quantidade_add').val();
    var product_value = $('#valor_add').val().replace(',', '.');
    add_product_to_list(product_name, product_quantity, product_value);
    if(id_load_list !== false){
        add_product(id_load_list, product_name, product_quantity, product_value)
    }
    
});


$(document).on('click', '#btn_save_unit', function(e){
    var product_old_quantity = list_product_row_edit.find("td").eq(1).text().trim();
    var product_old_value = list_product_row_edit.find("td").eq(2).text().trim();
    var product_old_total = product_old_value * product_old_quantity;
    var product_name = $('#tx_produto_edit').val();
    var product_quantity = $('#quantidade_edit').val();
    var product_value = $('#valor_edit').val().replace(',', '.');
    var product_total = product_value * product_quantity;
    update_totals(-1, (-1 * product_old_total));
    update_totals(1, product_total)
    list_product_row_edit.find('td').eq(0).html(`<input class="form-check-input padding-right-10" type="checkbox" value="" id="check_product">${product_name} <i id="btn_edit_product" class="padding-left-10 fa-solid fa-pen-to-square"></i><i id="btn_remove_product" class="padding-left-10 fa-solid fa-trash-can"></i>`);
    list_product_row_edit.find('td').eq(1).html(`${product_quantity}`);
    list_product_row_edit.find('td').eq(2).html(`${product_value}`);
    list_product_row_edit.find('td').eq(3).html(`${product_total}`);
    reset_values_modal();
    $('#modal_products_edit').modal('hide');
    if(list_product_row_edit.find("td").eq(0).attr('data-id') != '0'){
        update_product(id_load_list, list_product_row_edit.find("td").eq(0).attr('data-id'), product_name, product_quantity, product_value);
    }
});


function ajax_me(url, method='GET'){
    return $.ajax({
        url: url,
        type: method,
        async: false,
        cache: false,
        timeout: 10000,
        done: function(data){
            return data;
        }
    })
}

function update_product(id_list, id_product, title, quantity, value){
    var url = `/api/list/${id_list}/edit/${id_product}?tx_title=${title}&quantity=${quantity}&value=${value}`;
    var update_data = ajax_me(url);
    if(update_data.responseJSON.status === true)
        return true;
    return false;
}

function add_product(id_list, title, quantity, value){
    var url_list_add = `/api/list/${id_list}/add?tx_title=${title}&quantity=${quantity}&value=${value}`;
    var add_data = ajax_me(url_list_add);
    if(add_data.responseJSON.status === true)
        return true;
    return false;
}


function remove_product(id_list, id_product){
    var url = `/api/list/${id_list}/delete/${id_product}`;
    var update_data = ajax_me(url);
    if(update_data.responseJSON.status === true)
        return true;
    return false;
}


$(document).on('click', '#btn_save', function(e){
    var list_id = ajax_me('/api/list/create');
    if(list_id.responseJSON.status === true){
        var list_id_created = list_id.responseJSON.id;
        for(var product_index=0;product_index<$('#tb_produtos tbody').find('tr').length;product_index++){
            var product_row = $('#tb_produtos tbody').find('tr').eq(product_index);
            var product_name = product_row.find('td').eq(0).text().trim();
            var product_quantity = product_row.find('td').eq(1).text().trim();
            var product_value = product_row.find('td').eq(2).text().trim();
            var url_list_add = `/api/list/${list_id_created}/add?tx_title=${product_name}&quantity=${product_quantity}&value=${product_value}`;
            var add_product_response = ajax_me(url_list_add);
        }
        window.location.href = `/list/${list_id_created}`;
    }else{
        alert(list_id.responseJSON.message);
    }
});



$(document).on('click', '#btn_remove_product', function(e){
    list_product_row_edit = $(this).closest('tr');
    var product_row_name = list_product_row_edit.find('td').eq(0).text().trim();
    $('#message_remove_product').html(`Deseja mesmo remover ${product_row_name} de sua lista?`);
    $('#modal_products_remove').modal('show');
});


$(document).on('click', '#btn_new', function(e){
    window.location.href = '/';
});


$(document).on('click', '#btn_remove', function(e){
    if(list_product_row_edit.find("td").eq(0).attr('data-id') != '0'){
        remove_product(id_load_list, list_product_row_edit.find("td").eq(0).attr('data-id'));
    }
    $('#modal_products_remove').modal('hide');
    var product_quantity = list_product_row_edit.find("td").eq(1).text().trim();
    var product_value = list_product_row_edit.find("td").eq(2).text().trim();
    var product_total = product_value * product_quantity;
    update_totals(-1, (-1 * product_total));
    list_product_row_edit.remove();
    list_product_row_edit = false;
});