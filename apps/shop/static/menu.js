
$(document).ready(function(){

  rebuild_cart_UI();

});


$('button.add-item').on('click', function(){

  var item_id = $(this).data('item_id');

  // if item already in cart, increase quantity
  var already_in_cart = false;
  $.each(SHOPPING_CART, function( index, cart_item ){
    if(cart_item['item_id'] == item_id && !already_in_cart){
      SHOPPING_CART[index]['quantity'] += 1;
      already_in_cart = true;
    }
  });
  // else, add to cart
  if (!already_in_cart) {
    SHOPPING_CART.push({
      'name': $(this).data('name'),
      'item_id': $(this).data('item_id'),
      'quantity': 1
    });
  }

  console.log(SHOPPING_CART);
  save_cart();
  rebuild_cart_UI();

});


function save_cart(){
  $.ajax({
    url: "",
    type: "POST",
    cache: false,
    data: {
      'shop_id': SHOP_ID,
      'line_channel_membership_id': LINE_CHANNEL_MEMBERSHIP_ID,
      // 'csrfmiddlewaretoken': CSRF_TOKEN,
      'cart': JSON.stringify(SHOPPING_CART)
    },
    headers: { "X-CSRFToken": CSRF_TOKEN }, // or use? getCookie("csrftoken")
    dataType: "json"
  })
  .done(function(data, textStatus, jqXHR){

  })
  .fail(function(jqXHR, textStatus, errorThrown){})
  .always(function(){});
}


function rebuild_cart_UI(){

  $("#order_items").empty();

  $.each(SHOPPING_CART, function( index, cart_item ){

    // set quantity on item btn
    $("#item_"+cart_item['item_id']+"_btn").data('quantity', cart_item['quantity'])

    // update UI
    new_order_item = $("#order_item_template").clone();
    new_order_item.attr("id", "order_item_"+cart_item['order_item_id']);

    new_order_item.data("order_item_id", cart_item['order_item_id']);
    new_order_item.data("item_id", cart_item['item_id']);
    new_order_item.data("quantity", cart_item['quantity']);

    console.log(cart_item);

    new_order_item.find(".item-quantity").text(cart_item['quantity']);
    new_order_item.find(".item-name").text(cart_item['name']);
    new_order_item.appendTo("#order_items");

    // console.log(new_order_item );

  });

  $('.item-remove').on('click', function(){
    SHOPPING_CART.splice($(this).closest('.order-item').index(), 1);
    rebuild_cart_UI();
    save_cart();
  });

}
