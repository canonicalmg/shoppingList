function getCookie(c_name) {
        if(document.cookie.length > 0) {
            c_start = document.cookie.indexOf(c_name + "=");
            if(c_start != -1) {
                c_start = c_start + c_name.length + 1;
                c_end = document.cookie.indexOf(";", c_start);
                if(c_end == -1) c_end = document.cookie.length;
                return unescape(document.cookie.substring(c_start,c_end));
            }
        }
        return "";
    }
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function entryTemplate(item,shop,quantity,price, listName){
    var template = "<div class='panel panel-default'>"
        + "<div class='panel-heading clearfix'>"
    + "<h3 class='panel-title pull-left'>" + listName + "</h3>"
      + "<a class='btn btn-primary pull-right' href='#'>"
        + "<i class='fa fa-pencil'></i>"
        + "Edit"
      + "</a>"
    + "</div>"
    + "<div class='list-group'>"
      + "<div class='list-group-item'>"
        + "<h4 class='list-group-item-text'>Item</h4>"
        + "<h3 class='list-group-item-heading'>" + item + "</h3>"
      + "</div>"
      + "<div class='list-group-item'>"
        + "<h4 class='list-group-item-text'>Store</h4>"
        + "<h3 class='list-group-item-heading'>" + shop + "</h3>"
      + "</div>"
      + "<div class='list-group-item'>"
        + "<p class='list-group-item-text'>" + quantity + "</p>"
      + "</div>"
    + "</div>"
        +"</div>";
    return template;
}

$("#addItem").click(function(e){
   e.preventDefault();
    var itemName = $("#itemNameField").val() || null;
    var shopName = $("#shopNameField").val() || null;
    var quantity = $("#quantityField").val() || null;
    var price = $("#priceField").val() || null;
    $.ajax({
                 type:"POST",
                 url:"/addItemShoppingCart/",
                 headers : {
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                 data: {
                        'data': [itemName, shopName, quantity, price, currentSlug],
                        },
                 success: function(data){
                     console.log(entryTemplate(itemName, shopName, quantity, price));
                     $("#entryTable").append(entryTemplate(itemName, shopName, quantity, price, listName));
                 }
        });
});

$("#clearAll").click(function(e){
   e.preventDefault();
    $.ajax({
                 type:"POST",
                 url:"/clearAll/",
                 headers : {
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                 data: {
                        'data': currentSlug,
                        },
                 success: function(data){
                     $("#entryTable").empty();
                 }
        });
});