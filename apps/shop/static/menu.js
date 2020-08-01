
$(document).ready(function(){

  // rebuild_cart_UI();

  $("#checkout").on('click', function(){
    save_cart(checkout=true);
  });

});


// SHOPPING_CART[item_index_string] = {
//   'name': $(this).data('name'),
//   'item_id': $(this).data('item_id'),
//   'quantity': 1,
//   'option_ids_array': $(this).data('option_ids_array'),
//   'addon_ids_array': $(this).data('addon_ids_array')
// };



$("button.btn-quantity").on('click', function() {
  if ($(this).data('operator') === "add"){
    document.getElementById($(this).data('element_id')).value++;
  } else if ($(this).data('operator') === "subtract"){
    if (document.getElementById($(this).data('element_id')).value >= 1){
      document.getElementById($(this).data('element_id')).value--;
    }
  }
  $("#"+$(this).data('element_id')).trigger('change');
});


$("input.input-quantity").on('change', function() {

  var item_index_string = $(this).data('item_index_string');

  if (!(item_index_string in SHOPPING_CART)) {
    SHOPPING_CART[item_index_string] = {
      'item_id': $(this).data('item_id'),
      'item_name': $(this).data('item_name'),
    }
  }
  SHOPPING_CART[item_index_string]['quantity'] = $(this).value;
});


$("textarea.textarea-notes").on('change', function() {
  var item_index_string = $(this).data('item_index_string');

  if (!(item_index_string in SHOPPING_CART)) {
    SHOPPING_CART[item_index_string] = {
      'item_id': $(this).data('item_id'),
      'item_name': $(this).data('item_name'),
      'quantity': 1,
    }
  }
  SHOPPING_CART[item_index_string]['notes'] = $(this).value;
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


// function rebuild_cart_UI(){
//
//   $("#order_items").empty();
//
//   $.each(SHOPPING_CART, function( index, cart_item ){
//
//     // set quantity on item btn
//     $("#item_"+cart_item['item_id']+"_btn").data('quantity', cart_item['quantity'])
//
//     // update UI
//     new_order_item = $("#order_item_template").clone();
//     new_order_item.attr("id", "order_item_"+cart_item['order_item_id']);
//
//     new_order_item.data("order_item_id", cart_item['order_item_id']);
//     new_order_item.data("item_id", cart_item['item_id']);
//     new_order_item.data("quantity", cart_item['quantity']);
//
//     console.log(cart_item);
//
//     new_order_item.find(".item-quantity").text(cart_item['quantity']);
//     new_order_item.find(".item-name").text(cart_item['name']);
//     new_order_item.appendTo("#order_items");
//
//     // console.log(new_order_item );
//
//   });
//
//   $('.item-remove').on('click', function(){
//     SHOPPING_CART.splice($(this).closest('.order-item').index(), 1);
//     rebuild_cart_UI();
//     save_cart();
//   });
//
// }

