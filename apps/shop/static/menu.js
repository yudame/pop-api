
$(document).ready(function(){

  rebuild_cart_UI();

  $("#checkout").on('click', function(){
    // save_cart(checkout=true);
  });

  $("#cart-max").removeClass('d-flex');
  $("#cart-max").hide();
  $("#cart-min").show();

});


// SHOPPING_CART[cart_index_string] = {
//   'name': $(this).data('name'),
//   'item_id': $(this).data('item_id'),
//   'quantity': 1,
//   'option_ids_array': $(this).data('option_ids_array'),
//   'addon_ids_array': $(this).data('addon_ids_array')
// };

$("#cart-min button").on("click", function(){
  $("#cart-min").hide();
  $("#cart-max").show();
  $("#cart-max").addClass('d-flex');
});
$("#menu").on("click", function(){
  $("#cart-max").removeClass('d-flex');
  $("#cart-max").hide();
  $("#cart-min").show();
});


$("button.btn-change-quantity").on('click', function() {
  if ($(this).data('operator') === "add"){
    document.getElementById($(this).data('element_id')).value++;
  } else if ($(this).data('operator') === "subtract"){
    if (document.getElementById($(this).data('element_id')).value >= 1){
      document.getElementById($(this).data('element_id')).value--;
    }
  }
  // if (document.getElementById($(this).data('element_id')).value == 0){
  //   $(this).closest('.modal-content').find('button.btn-save-item').removeClass('btn-warning');
  //   $(this).closest('.modal-content').find('button.btn-save-item').addClass('btn-danger');
  //   $(this).closest('.modal-content').find('button.btn-save-item').html("REMOVE");
  // }
  $("#"+$(this).data('element_id')).trigger('change');
});


$("input.input-quantity").on('change', function() {

  var cart_index_string = $(this).data('cart_index_string');

  if (!(cart_index_string in SHOPPING_CART)) {
    SHOPPING_CART[cart_index_string] = {
      'item_id': $(this).data('item_id'),
      'item_name': $(this).data('item_name'),
    }
  }
  SHOPPING_CART[cart_index_string]['quantity'] = $(this).val();
});


$("textarea.textarea-notes").on('change', function() {
  var cart_index_string = $(this).data('cart_index_string');

  if (!(cart_index_string in SHOPPING_CART)) {
    SHOPPING_CART[cart_index_string] = {
      'item_id': $(this).data('item_id'),
      'name': $(this).data('item_name'),  // update to include options in  (parenthesis)?
      'quantity': 1,
    }
  }
  SHOPPING_CART[cart_index_string]['note'] = $(this).val();
});


$('.modal-menu-item').on('hidden.bs.modal', function () {
  console.log(SHOPPING_CART);
  save_cart();
  rebuild_cart_UI();
});


function save_cart(checkout){
  checkout = checkout || false;

  $.ajax({
    url: "",
    type: "POST",
    cache: false,
    data: {
      'shop_id': SHOP_ID,
      'line_channel_membership_id': LINE_CHANNEL_MEMBERSHIP_ID,
      // 'csrfmiddlewaretoken': CSRF_TOKEN,
      'cart': JSON.stringify(SHOPPING_CART),
      'checkout': checkout
    },
    headers: { "X-CSRFToken": CSRF_TOKEN }, // or use? getCookie("csrftoken")
    dataType: "json"
  })
  .done(function(data, textStatus, jqXHR){
    if (checkout){
      window.location.href = LINE_CHANNEL_URL;
    }
  })
  .fail(function(jqXHR, textStatus, errorThrown){
    if (checkout) {
      if (confirm("hold on... error saving your order")){
        save_cart(checkout);
      }
    }
  })
  .always(function(){});
}


function rebuild_cart_UI(){

  $("#cart_item_list").empty();

  $.each(SHOPPING_CART, function( cart_index_string, cart_item ){
    console.log(cart_item);

    //update data on menu items
    $("#item_"+cart_item['item_id']+"_quantity").val(cart_item['quantity']);

    // update UI
    new_cart_item = $("#cart_item_template").clone();
    new_cart_item.attr("id", "cart_item_index_"+cart_index_string);

    // new_cart_item.data("cart_index_string", cart_index_string);
    // new_cart_item.data("order_item_id", cart_item['order_item_id']);
    // new_cart_item.data("item_id", cart_item['item_id']);
    // new_cart_item.data("quantity", cart_item['quantity']);

    new_cart_item.find(".item-quantity").text(cart_item['quantity']);
    new_cart_item.find(".item-name").text(cart_item['name']);
    if ('price' in cart_item){
      new_cart_item.find(".item-price").text(cart_item['price']);
    }else{
      new_cart_item.find(".item-price").text("...");
    }

    update_menu_item_UI(cart_item)

    new_cart_item.find(".btn-item-modal").on('click', function(){
      $("#item_"+cart_item['item_id']+"_modal").modal('toggle');
    });
    new_cart_item.appendTo("#cart_item_list");

    console.log(new_cart_item );

  });

  $('.item-remove').on('click', function(){
    SHOPPING_CART.splice($(this).closest('.order-item').index(), 1);
    rebuild_cart_UI();
    save_cart();
  });

}

function update_menu_item_UI(cart_item_data){
  if (cart_item_data['quantity'] > 0) {
    $("#item_" + cart_item_data['item_id']).find("button.btn-add-to-cart").hide();
    $("#item_" + cart_item_data['item_id']).find("button.btn-quantity span.item-quantity").html(cart_item_data['quantity']);
    $("#item_" + cart_item_data['item_id']).find("button.btn-quantity").show();
  } else {
    $("#item_" + cart_item_data['item_id']).find("button.btn-quantity").hide();
    $("#item_" + cart_item_data['item_id']).find("button.btn-add-to-cart").show();
  }

  $("#item_"+cart_item_data['item_id']+"_modal").find("textarea.textarea-notes").val(cart_item_data['note']);

  $("#item_"+cart_item_data['item_id']+"_modal").find("button.btn-save").html("SAVE");

}

