ymaps.ready(init);
    
var myMap, myPlacemark;

var coordinates1 = 0;

function a() {
    return coordinates1;    
}

function init() {
    // Создание карты.
    var suggestView = new ymaps.SuggestView('suggest2');

    var myMap = new ymaps.Map("map", {
        // Координаты центра карты, Порядок по умолчанию: «широта, долгота».
        center: [55.76, 37.64],
        zoom: 10
    });
    
    function do_marker(s) {
        var searchArr = [s];
    
        searchArr.forEach(function(item) {
            ymaps.geocode(item, {
            results: 1
        }).then(function (res) {
                var firstGeoObject = res.geoObjects.get(0),
                    coords = firstGeoObject.geometry.getCoordinates();
                myMap.geoObjects.add(firstGeoObject);
    
                coordinates1 = coords;
            });
        }); 
    }

    $('#get').bind('click', function(e) {
        var obj = document.querySelector('#suggest2').value;
        do_marker(obj);
    });

    //do_marker();

    /*var myGeocoder = ymaps.geocode([55.7538337, 37.6211812]); // пытаюсь передать переменную 
            
    myGeocoder.then(
        function (res) {
            myMap.geoObjects.add(res.geoObjects);
                    
            var adres = result.geoObjects.get(0).properties.get('metaDataProperty').getAll(); // записываю координаты в переменную
                    

            console.log(adres);

            myPlacemark = new ymaps.Placemark([adres], { // пытаюсь передать координаты и поставить метку 
                hintContent: 'Москва!',
                balloonContent: 'Столица России'
            });

            myMap.geoObjects.add(myPlacemark);
            },
            function (err) {
                // обработка ошибки
            }
    );*/
}