;(function () {
  'use strict';

  var URL = 'http://localhost:8080/';

  var onResponseReceived = function (data) {
    $('#result').text(JSON.stringify(data));
  };

  $('#get-member').on('click', function () {
    $.get(URL + 'members/100').then(onResponseReceived);
  });

  $('#get-members').on('click', function () {
    $.get(URL + 'members/').then(onResponseReceived);
  });

  $('#get-sounds').on('click', function () {
    $.get(URL + 'sounds/').then(onResponseReceived);
  });

  $('#post-member').on('click', function () {
    $.post(URL + 'members/', {name: 'New member'}).then(onResponseReceived);
  });

}());
