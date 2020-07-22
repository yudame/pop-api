
$(document).ready(function(){

  //$.each(iterable_obj, function(key, value) { ... });  // reminder for old hands


  $.each(SHOPPING_CART, function( cart_item ){

    // set quantity on item btn
    $("#item_"+cart_item['item_id']+"_btn").data('quantity', cart_item['item_quantity'])

    // update UI

  });


});


$('.add-menu-item').on('click', function(){

  SHOPPING_CART.push({
    'item_id': $(this).data('item_id'),
    'quantity': 1
  });

  console.log(SHOPPING_CART);

  save_cart();

});


$('.quantity-up').on('click', function(){
  $(this).data()['quantity'] += 1
});



function save_cart(){
  $.ajax({
    url: "",
    type: "POST",
    cache: false,
    data: {
      'shop_id': SHOP_ID,
      'line_channel_membership_id': LINE_CHANNEL_MEMBERSHIP_ID,
      'csrfmiddlewaretoken': CSRF_TOKEN,
      'cart': JSON.stringify(SHOPPING_CART)
    },
    headers: { "X-CSRFToken": CSRF_TOKEN },
    dataType: "json"
  })
  .done(function(data, textStatus, jqXHR){

  })
  .fail(function(jqXHR, textStatus, errorThrown){})
  .always(function(){});
}
