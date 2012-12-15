var templateSearchResults, templateMain, inputTimer;
var RESULT_PER_PAGE = 10
  , currentPage = 1;

$(document).ready(function(){
  $('form#search').submit(function(){
    toggleWaiting(true);
    var query = $('#search-box').val();
    search(query, function(data){
      showResults(data);
      toggleWaiting(false);
    });
    return false;
  });

  $('#search-box').typeahead({
    items: 6,
    minLength: 2,
    source: function(query, callback){
      toggleWaiting(true);
      suggest(query, function(array){
        toggleWaiting(false);
        callback(array);
      });
    }
  });

  $('#search-box').on("input", function(){
    var query = $(this).val();
    clearTimeout(inputTimer);

    if (query.length < 3)
      return;

    inputTimer = setTimeout(function(){
      console.log('do search');
      $('form#search').submit();
    }, 800); // 800ms to fire the search function
  });

  $('#search-box').focus();
});

function toggleWaiting(forceShow) {
  $('#waiting').toggle(forceShow);
}

function search(query, callback) {
  // $.ajax({
  //   url: "",
  //   type: "GET",
  //   dataType: "json",
  //   success: function(data) {
  //     callback(data);
  //   },
  //   error: function(jqXHR, textStatus) {
  //   }
  // });

  data = {
       "count" : 2293,
       "result" :
          [
             {
                "title" : "[必读]影响中石油股价变动重要信息汇总_股吧_东方财富网",
                "url" : "http://guba2.eastmoney.com/601857,4263125,guba.html",
                "text" : "... 同股同酬香港14元GB 作者： 58.39..."
             },             {
                "title" : "1[必读]影响中石油股价变动重要信息汇总_股吧_东方财富网",
                "url" : "http://guba2.eastmoney.com/601857,4263125,guba.html",
                "text" : "... 同股同酬香港14元GB 作者： 58.39..."
             }
          ]
    };
  callback(data);
}

function suggest(query, callback) {
  $.ajax({
    url: "",
    type: "GET",
    dataType: "json",
    success: function(data) {
      callback(data.result);
    },
    error: function(jqXHR, textStatus) {
    }
  });
  // var data = {
  //     "result" :
  //         [
  //             "程序员",
  //             "程序设计",
  //             "11111",
  //             "11221",
  //         ]
  // };
  // callback(data.result);
}

function showResults(data) {
  if ($('.jumbotron .welcome').is(":visible"))
    $('.jumbotron .welcome').fadeOut('slow', function() {
    // Animation complete.
    });

  if (!templateSearchResults) {
    var source = $('#template-search-results').html();
    templateSearchResults = Handlebars.compile(source);
  }

  var count = parseInt(data.count) || 0;
  data.pager = count < RESULT_PER_PAGE ? false : true;

  $('#results').html(templateSearchResults(data));
  $('.item').on({
    mouseenter: function() {
      $(this).addClass('well');
    },
    mouseleave: function() {
      $(this).removeClass('well');
    }
  });
}

function highlighter(keywords) {
  //split words
  //highlight each of them
  var src_str = $("#test").html();
  var term = "my text";
  term = term.replace(/(\s+)/,"(<[^>]+>)*$1(<[^>]+>)*");
  var pattern = new RegExp("("+term+")", "i");

  src_str = src_str.replace(pattern, "<mark>$1</mark>");
  src_str = src_str.replace(/(<mark>[^<>]*)((<[^>]+>)+)([^<>]*<\/mark>)/,"$1</mark>$2<mark>$4");

  $("#test").html(src_str);
}