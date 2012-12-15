var templateSearchResults, templateMain, inputTimer;
var RESULT_PER_PAGE = 10
  , currentPage = 1
  , maxPage = 1;

$(document).ready(function(){
  $('form#search').submit(function(){
    toggleWaiting(true);
    var query = $('#search-box').val();
    search(query, function(data){
      console.log("data=",data);
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

  $('#search-box').on("input", instantSearch);
  $('#search-box').on("change", instantSearch);
  $('#search-box').focus();
});

function toggleWaiting(forceShow) {
  $('#waiting').toggle(forceShow);
}

function instantSearch() {
  var query = $('#search-box').val();
  clearTimeout(inputTimer);

  if (query.length < 3)
    return;

  inputTimer = setTimeout(function(){
    $('form#search').submit();
  }, 800); // 800ms to fire the search function
}

function search(query, callback) {
  var q = {
    query: query,
    page: currentPage
  };

  $.ajax({
    url: "/search",
    data: q,
    type: "GET",
    success: function(data) {
      console.log(data);
      if (typeof(data) == 'string')
        data = JSON.parse(data);
      callback(data);
    },
    error: function(jqXHR, textStatus) {
    }
  });
}

function suggest(query, callback) {
  var q = {
    query: query
  };

  $.ajax({
    url: "/suggest",
    data: q,
    type: "GET",
    success: function(data) {
      if (typeof(data) == 'string')
        data = JSON.parse(data);
      callback(data.result);
    },
    error: function(jqXHR, textStatus) {
    }
  });
}

function searchNext(isNextPage) {
  if (isNextPage && currentPage < maxPage) {
    currentPage++;
    $('form#search').submit();
  } else if(!isNextPage && currentPage > 1) {
    currentPage--;
    $('form#search').submit();
  }
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
  maxPage = Math.ceil(count / RESULT_PER_PAGE);
  data.pager = count < RESULT_PER_PAGE ? false : true;
  data.page = currentPage;

  $('#results').html(templateSearchResults(data));
  $('.item').on({
    mouseenter: function() {
      $(this).addClass('well');
    },
    mouseleave: function() {
      $(this).removeClass('well');
    }
  });
  $('.next-page').on('click', searchNext(true));
  $('.next-page').on('click', searchNext(false));
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