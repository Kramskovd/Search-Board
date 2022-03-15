var fcategory = false;
var fthing= false;
var fsort = false;
var categoryValue = -1;
var priceValueFrom = 0;
var priceValueTo = '';
var sortValue = 'date';
var thingValue = -1;

function titleThingChange(){

    name_thing = $(event.target).html();
    thingValue = $(event.target).next().html();
    $('#choice-thing').html(name_thing);

    $("#thing-list").hide();
    fthing = false;
}
$(document).ready(function(){
    //выпадающие меню

    $('.title-category-button').on('click', function(event){
        const xhr = new XMLHttpRequest();
        id = $(event.target).next().html();
        name_category = $(event.target).html();
        categoryValue = id;

        //закрытие меню
        $('#category-list').hide();
        fcategory = false;

        //запись категории в кнопку
        $("#choice-category").html(name_category);
        $("#choice-thing").html("выберите вид");

        //удаляем список старых подкатегорий
        $("li").remove(".thing-button");

        //
        requestURL = '/category?id=' + id;
        xhr.open('GET', requestURL);
        xhr.onreadystatechange = function(){
            if(xhr.readyState !== 4 || xhr.status !== 200){
                return;
            }
            var res = JSON.parse(xhr.response);
            res = res["res"];

            for(var i=0; i < res.length; i++){
                res_id = res[i]["id"];
                res_name = res[i]["name_thing"];
                $("#thing-list-content").append('<li>' + res_name + "</li><span class='hide-block-id'>" + res_id + "</span>");
                $("#thing-list-content li").attr({
                    class: "thing-button title-thing-button",
                    onclick: "titleThingChange()"
                })
            }

        }
        xhr.send();
    });


    $('#fcategory').on('click', function(){
        if(fcategory === false){
            $('#category-list').show();
            fcategory = true;
        }else{
            fcategory = false;
            $('#category-list').hide();
        }
    });
    $('#fthing').on('click', function(){
        if(fthing === false){
            $('#thing-list').show();
            fthing = true;
        }else{
            fthing = false;
            $('#thing-list').hide();
        }
    });
    $('#fsort').on('click', function(){
        if(fsort === false){
            $('#sort-list').show();
            fsort = true;
        }else{
            fsort = false;
            $('#sort-list').hide();
        }
    });
    $('#price-sort').on('click', function(event){
        $("#fsort span").html($(event.target).html());
        $("#sort-list").hide();
        fsort = false;
        sortValue = 'price';
    });

    $("#date-sort").on('click', function(event){
        $("#fsort span").html($(event.target).html());
        $('#sort-list').hide();
        fsort = false;
        sortValue = 'date';
    });
    $("#input-from").change(function(event){
        priceValueFrom = $(event.target).val();
    });
    $("#input-to").change(function(event){
        priceValueTo = $(event.target).val();

    })

    $("#filter-button").on('click', function(){
        var filterURL = "/category_filter?category=" + categoryValue + "&thing="
                    + thingValue + "&sort=" + sortValue + "&price_to=" + priceValueTo + "&price_from="
                    + priceValueFrom + "&page=1";

        $(location).attr('href', filterURL);

    });

});


