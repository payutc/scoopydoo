function change_count(id, increment) {
    var parent_article = $(".article#"+id);
    var current_count = parent_article.data("count");
    current_count = isNaN(current_count) ? 0 : current_count;
    parent_article.data("count", current_count + increment);
    update_articles();
}

function formatEuros(montant){
    return montant.toFixed(2).replace(".",",")+" €";
}

function update_articles() {
    $("#table tr").remove();
    $("#table").append('<tr><th>Désignation</th><th>Quantité</th><th>P.U.</th><th>Sous-total</th></tr>');
    var tot_price = 0;
    $('.article').each(function (index, element) {
        if ($(this).data("count") > 0) {
            var count = $(this).data("count");
            var price = $(this).data("price");
            tot_price += count*price;
            $('#table tr:last').after('<tr><td>'+$(this).text()+'</td><td>'
                +count+'</td><td>'+formatEuros(price)+'</td><td>'+formatEuros(price*count)+'</td></tr>');
        }
    });
    $('#table tr:last').after('<tr><td><b>TOTAL</b></td><td></td><td></td><td><b>'+formatEuros(tot_price)+'</b></td></tr>');
    $('#pay').removeAttr("disabled");
}

$(".article").click(function () {
    change_count($(this).data("article"), 1);
});

$(".x5").click(function () {
    change_count($(this).data("article"), 5);
});

$(".x10").click(function () {
    change_count($(this).data("article"), 10);
});

$("#cancel").click(function () {
    $("#pay").attr("disabled", "disabled");
    $("#table tr").remove();
    $("#table").append('<tr><th>Désignation</th><th>Quantité</th><th>P.U.</th><th>Sous-total</th></tr>');
    $('.article').each(function (index, element) {
        $(this).data("count", 0);
    });
});
