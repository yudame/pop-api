
$(document).ready(function(){

  rebuild_menu_UI();
  rebuild_cart_UI();

  $("#checkout").on('click', function(){
    // save_cart(checkout=true);
  });

  $("#cart_min").hide();
  $("#menu").removeClass("opacity-30");
  $("#cart_max").removeClass('d-flex');
  $("#cart_max").hide();
  if (SHOPPING_CART.ready_for_checkout[0]){
    $("#cart_min").show();
  }

});


// SHOPPING_CART[cart_index_string] = {
//   'name': $(this).data('name'),
//   'item_id': $(this).data('item_id'),
//   'quantity': 1,
//   'option_ids_array': $(this).data('option_ids_array'),
//   'addon_ids_array': $(this).data('addon_ids_array')
// };

$("#cart_min button").on("click", function(){
  $("#cart_min").hide();
  $("#cart_max").show();
  $("#menu").addClass("opacity-30");
  $("#cart_max").addClass('d-flex');
});
$("#menu").on("click", function(){
  $("#menu").removeClass("opacity-30");
  $("#cart_max").removeClass('d-flex');
  $("#cart_max").hide();
  if (SHOPPING_CART.ready_for_checkout[0]){
    $("#cart_min").show();
  }
});


$("button.btn-change-quantity").on('click', function() {
  if ($(this).data('operator') === "add"){
    document.getElementById($(this).data('element_id')).value++;
  } else if ($(this).data('operator') === "subtract"){
    if (document.getElementById($(this).data('element_id')).value >= 1){
      document.getElementById($(this).data('element_id')).value--;
    }
  }
  if (document.getElementById($(this).data('element_id')).value == 0){
    $(this).closest('.modal-content').find('button.btn-save-item').removeClass('btn-warning').addClass('btn-danger').html("REMOVE");
  }else{
    $(".modal-menu-item button.btn-save-item").removeClass('btn-danger').addClass('btn-warning').html("SAVE");
  }
  $("#"+$(this).data('element_id')).trigger('change');
});

$(".btn-save-item").on('click', function(){
  $(this).closest('.modal-menu-item').find("input.input-quantity").trigger('change').closest('.modal-menu-item').modal('toggle');
});

$("input.input-quantity").on('change', function() {
  var cart_index_string = $(this).data('cart_index_string');
  if (!(cart_index_string in SHOPPING_CART)) {
    SHOPPING_CART[cart_index_string] = {
      'item_id': $(this).data('item_id'),
      'item_name': $(this).data('item_name'),
    };
    alert('added new item to cart')
  }
  SHOPPING_CART[cart_index_string]['quantity'] = $(this).val();
});


$("textarea.textarea-notes").on('change', function() {
  var cart_index_string = $(this).data('cart_index_string');
  if (!(cart_index_string in SHOPPING_CART)) {
    SHOPPING_CART[cart_index_string] = {
      'item_id': $(this).data('item_id'),
      'name': $(this).data('item_name'),
      'quantity': 1,
    };
    alert('added new item to cart')
  }
  SHOPPING_CART[cart_index_string]['note'] = $(this).val();
});


$('.modal-menu-item').on('hidden.bs.modal', function () {
  console.log(SHOPPING_CART);
  rebuild_menu_UI();
  save_cart();
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
      'shopping_cart': JSON.stringify(SHOPPING_CART),
      'checkout': checkout
    },
    headers: { "X-CSRFToken": CSRF_TOKEN }, // or use? getCookie("csrftoken")
    dataType: "json"
  })
  .done(function(data, textStatus, jqXHR){

    SHOPPING_CART = JSON.parse(data["shopping_cart_json"]);

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
  .always(function(){
    rebuild_cart_UI();
  });
}


function rebuild_menu_UI(){
  // clear UI fields then re-populate

  // Reset all Menu Items
  $("div.item-add-to-cart button.btn-quantity").hide();
  $("div.item-add-to-cart button.btn-quantity .item-quantity").html("0");
  $("div.item-add-to-cart button.btn-add").show();

  // Reset all Menu Item Modals
  $(".modal-menu-item input.input-quantity").val(1);
  $(".modal-menu-item textarea.textarea-notes").val("");
  $(".modal-menu-item button.btn-save-item").removeClass('btn-danger').addClass('btn-warning').html("ADD TO ORDER");

  // for item based on shopping cart contents
  $.each(SHOPPING_CART, function( cart_index_string, cart_item_data ) {
    if (!cart_index_string.startsWith('i')){
      return; //continue to next
    }

    // Update menu item UI
    let qty_span = $("#item_" + cart_item_data['item_id']).find("button.btn-quantity span.item-quantity");
    let new_qty = parseInt($(qty_span).html()) + parseInt(cart_item_data['quantity']);
    if (new_qty > 0){
      $(qty_span).html(new_qty);
      $("#item_" + cart_item_data['item_id']).find("button.btn-add").hide();
      $("#item_" + cart_item_data['item_id']).find("button.btn-quantity").show();
    }

    // Update menu item modal UI
    $("#item_"+cart_item_data['item_id']+"_modal textarea.textarea-notes").val(cart_item_data['note']);
    if (cart_item_data['quantity'] > 0){
      $("#item_"+cart_item_data['item_id']+"_modal input.input-quantity").val(cart_item_data['quantity']);
      $("#item_"+cart_item_data['item_id']+"_modal button.btn-save-item").html("SAVE");
    }else{
      // do nothing
    }

  });
}


function rebuild_cart_UI(){
  // clear UI fields then re-populate

  // Cart-Min Elements
  $("#cart_min_total_item_count").html("<i class='fas fa-spinner'></i>");  // temporary processing todo: use animated svg
  $("#cart_min_total_price_amount").html("<i class='fas fa-spinner'></i>");  // temporary processing todo: use animated svg
  // $("#cart_total_price_amount").html("...");  // temporary processing todo: use animated svg

  // Cart-Max Elements
  $("#cart_max_summary").empty();  // clear entire cart summary
  $("#cart_max_total_price_amount").html("<i class='fas fa-spinner'></i>");  // temporary processing todo: use animated svg


  $("#cart_min_total_item_count").html(SHOPPING_CART.total_item_count[0]);
  $("#cart_min_total_price_amount").html(SHOPPING_CART.total_price_amount[0]);
  $("#cart_max_total_price_amount").html(SHOPPING_CART.total_price_amount[0]);


  // for each item in shopping cart, update #cart_max_summary
  $.each(SHOPPING_CART, function( cart_index_string, cart_item_data ){
    if (!cart_index_string.startsWith('i')){
      return; //continue to next
    }

    if (parseInt(cart_item_data['quantity']) == 0){
      return; //continue to next
    }

    console.log(cart_item_data);

    // update UI
    new_cart_item = $("#cart_item_template").clone();
    new_cart_item.attr("id", "cart_item_index_"+cart_index_string);

    new_cart_item.data("cart_index_string", cart_index_string);
    new_cart_item.data("order_item_id", cart_item_data['order_item_id']);
    new_cart_item.data("item_id", cart_item_data['item_id']);
    new_cart_item.data("quantity", cart_item_data['quantity']);

    new_cart_item.find(".item-quantity").text(cart_item_data['quantity']);
    new_cart_item.find(".item-name").text(cart_item_data['name']);
    new_cart_item.find(".item-price").text(cart_item_data['price_amount']);
    if (cart_item_data['note'].length > 0) {
      new_cart_item.find(".item-note").text(cart_item_data['note']);
      new_cart_item.find(".item-note").parent().addClass("has-note");
    }

    new_cart_item.find(".btn-item-modal").on('click', function(){
      $("#menu").removeClass("opacity-30");
      $("#item_"+cart_item_data['item_id']+"_modal").modal('toggle');
    });
    new_cart_item.appendTo("#cart_max_summary");

    console.log(new_cart_item);

  });
}
