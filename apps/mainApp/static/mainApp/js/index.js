//
// start of map 
//
var delay = 100;
var infowindow = new google.maps.InfoWindow();
var latlng = new google.maps.LatLng(21.0000, 78.0000);
var mapOptions = {
	center: {lat: 37.773, lng: -122.431},
	zoom: 12, 
	mapTypeId: google.maps.MapTypeId.ROADMAP
}
var geocoder = new google.maps.Geocoder(); 
var map = new google.maps.Map(document.getElementById("map"), mapOptions);
var bounds = new google.maps.LatLngBounds();

function geocodeAddress(address, next) {
	geocoder.geocode({address:address}, function (results,status) { 
		if (status == google.maps.GeocoderStatus.OK) {
			var p = results[0].geometry.location;
			var lat=p.lat();
			var lng=p.lng();
			createMarker(address,lat,lng);
		}
		else {
			if (status == google.maps.GeocoderStatus.OVER_QUERY_LIMIT) {
				nextAddress--;
				delay++;
			} else {
            	}   
			}
    		next();
  		}
	);
}
function createMarker(add,lat,lng) {
	var contentString = add;
	var marker = new google.maps.Marker({
		position: new google.maps.LatLng(lat,lng),
		map: map,
	});

	google.maps.event.addListener(marker, 'click', function() {
		infowindow.setContent(contentString); 
		infowindow.open(map,marker);
	});

	bounds.extend(marker.position);
}	
var locations = [
	'Palace of Fine Arts',
	'City Hall', 
	'4400 20th St.',
	'Castro St.', 
	'835-865 Market Street at 5th Street'
];
var nextAddress = 0;

function theNext() {
	if (nextAddress < locations.length) {
		setTimeout('geocodeAddress("'+locations[nextAddress]+' San Francisco, CA",theNext)', delay);
		nextAddress++;
	} else {
		map.fitBounds(bounds);
		}
	}

theNext();
//
//	end of map
//

//
//	start of poster
//
function createTenPosterList(){
	var arr = {}
	for(var i = 1; i < 1586 ; i ++){
		$.get("https://data.sfgov.org/api/views/yitu-d5am/rows.json/" + i, function(data){
			// console.log(data)
			if (!arr[data.title]){
				if(Object.keys(arr).length < 10){
					arr[data.title] = data.title
					$("#movies").append(`<p>${arr[data.title]}</p>`)
				}
			}
		})
	}
	return arr
}

$(document).ready(function(){
	alert("Sss")
	var arr = {"24 Hours on Craigslist":"24 Hours on Craigslist","40 Days and 40 Nights":"40 Days and 40 Nights",'48 Hours':"48 Hours",'50 First Dates':"50 First Dates",'180':"180",'A Jitney Elopement':"A Jitney Elopement",'A Night Full of Rain':"A Night Full of Rain",'A Smile Like Yours':"A Smile Like Yours","A Smile Like Yours ":"A Smile Like Yours ",'A View to a Kill':"A View to a Kill"}
	function posters(){
		$.each(arr, function(key, value){
			console.log(key, "wwwwwwwww")
			$.get(`http://www.omdbapi.com/?t=${key}&y=&plot=short&r=json`, function(data){
				var poster = data.Poster
				$("#movies").append(`<img src="${poster}">`)
				
			})
		});
	}
	posters()
}) //document ready tag
//
//	end of posters
//