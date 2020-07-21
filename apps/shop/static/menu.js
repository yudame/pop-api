
$(document).ready(function(){

  //$.each(iterable_obj, function(key, value) { ... });  // reminder for old hands
  $.each(SHOPPING_CART, function( item_id, item_count ){

  });


  // $(".").onclick(function(){
  //
  // })





});


// <button class="autosave" data-clicks="0">Click Me</button>

//js
$('.add-menu-item').autosave({
  url: "/",
  method: "PUT",
  data: {
    'shop_id': SHOP_ID,
    'line_channel_membership_id': LINE_CHANNEL_MEMBERSHIP_ID,
    'csrf_token': CSRF_TOKEN
  },
  type: "json",
  event: "click",
  debug: DEBUG,
  before: function(){
    // increment item count
    $(this).data()['item_quantity'] += 1;


    // update cart on screen

    // get data snapshot of cart
    var cart_dict = {};
    $(".add_menu_item").each(function(item_elem){
      cart_dict[item_elem.data('item_id')] = item_elem.data('item_quantity')
    });

    $(this).data('cart_items', cart_dict);
  },
  done: function(){


    $(this).removeData('cart');
  }
});
